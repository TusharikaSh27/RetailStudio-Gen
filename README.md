## 🛍️ RetailStudio-Gen

**RetailStudio-Gen** is an AI-assisted creative generation tool for retail brands.
It helps generate marketing creatives by uploading a product image, extracting colors, removing backgrounds, and applying ready-made design templates.

This version is a **hackathon submission MVP**. Some features are partially implemented and will be improved later.

---
## 🚀 Features

* 📤 Upload product images
* 🎨 Automatic color palette extraction
* 🧼 Background removal (AI-based)
* 🖼️ Predefined creative templates (square, portrait, landscape)
* ✍️ AI-generated marketing text (via Groq)
* 🧩 Frontend editor to preview creatives
* 🌐 REST API using Flask
---
## 🛠️ Tech Stack
### Frontend

* React.js
* Konva.js (canvas editor)
* CSS

### Backend
* Python
* Flask
* Pillow
* rembg
* ColorThief
* Flask-CORS
* Groq API (for text generation)
---

## 📂 Project Structure

```
retail_project/
│
├── backend/
│   ├── app.py
│   ├── utils/
│   ├── uploads/
│   ├── processed/
│   └── creatives/
│
├── frontend/
│   ├── src/
│   ├── public/
│   └── package.json
│
├── requirements.txt
└── README.md
```
---

## ⚙️ Setup Instructions

### 1️⃣ Backend Setup

```bash
cd backend
python -m venv venv
venv\Scripts\activate   # Windows
pip install -r requirements.txt
python app.py
```

Backend runs on:

```
http://localhost:5000
```

---

### 2️⃣ Frontend Setup

```bash
cd frontend
npm install
npm start
```

Frontend runs on:

```
http://localhost:3000
```

---

## Hackathon Notes

* This is an **MVP version**
* Some image editing options may be limited
* Error handling and UI polish are in progress
* Performance optimizations are planned post-hackathon
---

## 🔐 Environment Variables

Create a `.env` file (not committed):

```
GROQ_API_KEY=your_api_key_here
```

---

## 📌 Future Improvements

* Better image editor tools
* More creative templates
* Improved background removal accuracy
* User authentication
* Cloud deployment

---

## 👩‍💻 Author
**Tusharika Sharma**
https://github.com/TusharikaSh27

Hackathon Project 🚀
---
