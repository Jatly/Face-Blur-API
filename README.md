# 🎭 Face Blur API

A FastAPI-powered application that automatically blurs a specific person’s face from an image or video using a reference image.

Whether you're editing content for privacy, anonymity, or style — this API makes it as simple as upload → blur → download.

---

## 🔍 How It Works

1. Upload a **reference image** of the person you want to blur.
2. Upload a **target image or video** containing that person.
3. The API detects all faces in the target.
4. It compares each face with the reference face using deep face encodings.
5. Matching faces are blurred using Gaussian blur.
6. A blurred version of the original image or video is returned.

---

## 🖼️ Demo Example

| Reference Image | Target Image | Blurred Output |
|------------------|----------------------|------------------|
| ![Reference](./rd.jpg) | ![Target](./sddefault.jpg) | ![Blurred](./blurred_output.jpeg) |

---

## 🚀 Features

- ✅ Blur by face recognition (not position)
- ✅ Works with both **images** and **videos**
- ✅ Cleans up temporary files automatically
- ✅ MIME type aware responses (proper file types)
- ✅ CORS enabled (frontend ready)

---

## 🧰 Tech Stack

- 🐍 Python 3.8+
- ⚡ FastAPI
- 🎥 OpenCV
- 👤 face_recognition
- 🧠 dlib (via face_recognition)
- 📄 Uvicorn
- 📦 Python-multipart

---

## 📦 Installation

### 1. Clone this repo

```bash
git clone https://github.com/your-username/Face-Blur-API.git
cd Face-Blur-API
