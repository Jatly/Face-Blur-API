# 🎭 Face Blur API – FastAPI App to Automatically Blur a Person’s Face

This project allows you to **blur the face of a specific person** in any **image or video** by using a **reference photo** of that person.

It's built using **FastAPI**, **OpenCV**, and **face_recognition**.

---

## 🖼️ Example Demo

| Reference Image (Input) | Target Image (Input) | Output (Blurred) |
|-------------------------|----------------------|------------------|
| ![ref](./rd.jpg)        | ![input](./sddefault.jpg) | ![output](./blurred_output.jpeg) |

> The API finds the person from the reference image and blurs only their face in the target image/video.

---

## 🚀 How It Works

1. Upload a **reference image** (of the person to blur)
2. Upload a **target image or video**
3. The app compares faces using deep encoding
4. If the face matches → it applies a **Gaussian blur**
5. Returns a downloadable blurred result

---

## 🛠️ Tech Stack

- [FastAPI](https://fastapi.tiangolo.com/)
- [face_recognition](https://github.com/ageitgey/face_recognition)
- OpenCV
- Python

---

## 📦 Installation

### 1. Clone the repo

```bash
git clone https://github.com/your-username/Face-Blur-API.git
cd Face-Blur-API
