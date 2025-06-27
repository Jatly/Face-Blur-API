from fastapi import FastAPI, File, UploadFile, BackgroundTasks
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os
import cv2
import face_recognition
import uuid
import mimetypes

app = FastAPI()

# ✅ Enable CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for local testing
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Create uploads folder if it doesn't exist
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# ✅ Utility: blur the matched face
def blur_face(img, top, right, bottom, left):
    face = img[top:bottom, left:right]
    face = cv2.GaussianBlur(face, (99, 99), 30)
    img[top:bottom, left:right] = face
    return img

# ✅ Utility: save uploaded file with unique name
def save_upload_file_tmp(upload_file: UploadFile) -> str:
    file_id = str(uuid.uuid4())
    filename = f"{file_id}_{upload_file.filename}"
    file_path = os.path.join(UPLOAD_DIR, filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(upload_file.file, buffer)
    return file_path

@app.post("/blur-face/")
async def blur_face_api(
    background_tasks: BackgroundTasks,
    reference_face: UploadFile = File(...),
    target_file: UploadFile = File(...)
):
    ref_path = save_upload_file_tmp(reference_face)
    target_path = save_upload_file_tmp(target_file)
    output_path = ""  # define here for cleanup

    try:
        # ✅ Load and encode reference face
        reference_img = face_recognition.load_image_file(ref_path)
        face_locations = face_recognition.face_locations(reference_img)
        ref_encodings = face_recognition.face_encodings(reference_img, face_locations)

        if not face_locations or not ref_encodings:
            return JSONResponse(content={"error": "No face found in reference image"}, status_code=400)

        reference_encoding = ref_encodings[0]

        # ✅ Process Image
        if target_file.content_type.startswith("image"):
            image = face_recognition.load_image_file(target_path)
            locations = face_recognition.face_locations(image)
            encodings = face_recognition.face_encodings(image, locations)

            for (top, right, bottom, left), face_encoding in zip(locations, encodings):
                if face_recognition.compare_faces([reference_encoding], face_encoding)[0]:
                    image = blur_face(image, top, right, bottom, left)

            output_path = os.path.join(UPLOAD_DIR, "blurred_" + target_file.filename)
            cv2.imwrite(output_path, cv2.cvtColor(image, cv2.COLOR_RGB2BGR))

        # ✅ Process Video
        elif target_file.content_type.startswith("video"):
            cap = cv2.VideoCapture(target_path)
            fourcc = cv2.VideoWriter_fourcc(*"mp4v")
            fps = cap.get(cv2.CAP_PROP_FPS)
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

            output_path = os.path.join(UPLOAD_DIR, "blurred_" + target_file.filename)
            out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

            while True:
                ret, frame = cap.read()
                if not ret:
                    break

                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                locations = face_recognition.face_locations(rgb_frame)
                encodings = face_recognition.face_encodings(rgb_frame, locations)

                for (top, right, bottom, left), face_encoding in zip(locations, encodings):
                    if face_recognition.compare_faces([reference_encoding], face_encoding)[0]:
                        frame = blur_face(frame, top, right, bottom, left)

                out.write(frame)

            cap.release()
            out.release()

        else:
            return JSONResponse(content={"error": "Unsupported file type"}, status_code=400)

        # ✅ Clean up temp files after response
        background_tasks.add_task(os.remove, ref_path)
        background_tasks.add_task(os.remove, target_path)
        background_tasks.add_task(os.remove, output_path)

        # ✅ Detect content type for correct download
        media_type, _ = mimetypes.guess_type(output_path)
        media_type = media_type or "application/octet-stream"

        return FileResponse(
            output_path,
            background=background_tasks,
            media_type=media_type,
            filename=os.path.basename(output_path)
        )

    except Exception as e:
        print("❌ Error:", e)
        background_tasks.add_task(os.remove, ref_path)
        background_tasks.add_task(os.remove, target_path)
        if output_path and os.path.exists(output_path):
            background_tasks.add_task(os.remove, output_path)

        return JSONResponse(content={"error": str(e)}, status_code=500)
