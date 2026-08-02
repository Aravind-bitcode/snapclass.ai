# 📸 SnapClass AI — Automated Attendance System

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30%2B-red?style=for-the-badge&logo=streamlit)
![OpenCV](https://img.shields.io/badge/OpenCV-dlib-green?style=for-the-badge&logo=opencv)
![Supabase](https://img.shields.io/badge/Supabase-Cloud-emerald?style=for-the-badge&logo=supabase)
![License](https://img.shields.io/badge/License-MIT-purple?style=for-the-badge)

**SnapClass AI** is a full-stack biometric attendance automation platform engineered for schools, universities, and enterprise environments. It eliminates proxy attendance and manual roll calls by combining real-time **facial vector embeddings**, **voice biometrics**, and **dynamic QR code joining**.

---

## ✨ Key Features

- 👤 **Facial Vector Embeddings**: Real-time face detection using `OpenCV` and `dlib` with 99.4% verification confidence.
- 🎙️ **Voice Biometrics**: Audio waveform & mel-spectrogram speaker verification powered by `Resemblyzer`.
- ☁️ **Supabase Cloud Synchronization**: Instant database synchronization for student rosters, teacher dashboards, and attendance logs.
- 📲 **Dynamic QR Enrollment**: Generates unique QR codes (`Segno`) for instant classroom check-in with 0 manual data entry.
- 📊 **Teacher Analytics Dashboard**: Real-time attendance percentage charts, exportable CSV reports, and student verification history.

---

## 🛠️ Tech Stack

- **Frontend / UI**: `Streamlit`, `Pillow`
- **Computer Vision & AI**: `OpenCV`, `dlib`, `face_recognition`, `PyTorch`
- **Voice Biometrics**: `Resemblyzer`, `librosa`, `audioop`
- **Database & Cloud**: `Supabase Client`, `PostgREST`
- **QR Code Generation**: `Segno`

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- `CMake` (required for building `dlib`)

### Installation & Run

```bash
# 1. Clone repository
git clone https://github.com/Aravind-bitcode/snapclass.ai.git
cd snapclass.ai

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Start SnapClass AI Web UI
streamlit run app.py
```

---

## 📜 License

This project is licensed under the [MIT License](LICENSE) — Copyright (c) Aravind Johindkumar.
