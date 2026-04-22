<div align="center">

# 👷 AI PPE Safety Monitor
### *Real-Time Personal Protective Equipment Detection & Compliance System*

[![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![YOLOv8](https://img.shields.io/badge/YOLOv8-Ultralytics-FF6B35?style=for-the-badge&logo=pytorch&logoColor=white)](https://ultralytics.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![OpenCV](https://img.shields.io/badge/OpenCV-Computer%20Vision-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white)](https://opencv.org)
[![License](https://img.shields.io/badge/License-MIT-22C55E?style=for-the-badge)](LICENSE)

> **An end-to-end Computer Vision solution that monitors PPE compliance in real-time — protecting workers before accidents happen.**

---

</div>

## 🎯 Overview

The **AI PPE Safety Monitor** leverages a custom-trained **YOLOv8** deep learning model to automatically detect Personal Protective Equipment (PPE) violations in workplace environments. Whether monitoring a live camera feed, processing uploaded footage, or analyzing images — this system instantly identifies safety hazards and alerts administrators, enabling proactive risk management.

---

## ✨ Key Features

| Feature | Description |
|---|---|
| 🎥 **Live Webcam Monitoring** | Real-time detection from any connected camera with instant on-screen feedback |
| 📹 **Video Analysis** | Upload and process MP4/AVI footage with frame-by-frame violation tracking |
| 🖼️ **Image Detection** | Instant PPE compliance analysis on uploaded images (JPG/PNG) |
| 📊 **Enterprise Safety Logs** | All detections automatically logged to timestamped CSV for audit trails |
| 📧 **Email Alerts** | Automatic email notifications with violation snapshots sent to administrators |
| 💾 **Organized Data Storage** | Detections saved in labeled, structured folders (images / videos / webcam) |
| ⚙️ **Configurable Dashboard** | Adjustable alert cooldowns, email settings, and kill-switch controls |

---

## 🛡️ Detected PPE Classes

The model is trained to identify the following items and their **violation states**:

- ✅ Helmet / ❌ NO-Helmet
- ✅ Safety Vest / ❌ NO-Safety Vest
- ✅ Mask / ❌ NO-Mask
- ✅ Vehicles / ❌ NO-Vehicles

---

## 🏗️ Tech Stack

| Technology | Role |
|---|---|
| **YOLOv8** (Ultralytics) | Object detection model (custom-trained on PPE dataset) |
| **Python 3.8+** | Core programming language |
| **Streamlit** | Interactive web dashboard |
| **OpenCV** | Video/frame capture & processing |
| **Pandas** | Data logging and CSV management |
| **Pillow (PIL)** | Image handling |
| **Google Colab (T4 GPU)** | Model training environment |

---

## 📂 Project Structure

```
📦 PPE-Safety-Monitor/
├── 🐍 app.py                   # Main Streamlit web application
├── 🤖 best.pt                  # Custom-trained YOLOv8 model weights
├── 📋 requirements.txt         # Python dependencies
├── 📁 detections_history/
│   ├── 📸 images/              # Saved image detections
│   ├── 🎬 videos/              # Processed video files
│   ├── 📷 webcam/              # Webcam recording captures
│   └── 📊 detections_log.csv   # Master detection & violation log
└── 📖 README.md
```

---

## ⚙️ Getting Started

### Prerequisites
- Python 3.8 or higher
- A webcam (for live monitoring mode)
- Gmail account with **App Password** enabled (for email alerts)

### 1. Clone the Repository

```bash
git clone https://github.com/uk7by007-ai/ppe-detection-system.git
cd ppe-detection-system
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Launch the Application

```bash
streamlit run app.py
```

The app will open automatically in your browser at `http://localhost:8501`.

---

## 📧 Email Alert Setup (Optional)

To enable automatic violation alerts:

1. Enable **2-Step Verification** on your Gmail account.
2. Generate a **Google App Password** from your Google Account settings.
3. In the app sidebar, click **📧 Email Settings** and enter:
   - Sender Gmail address
   - Google App Password
   - Administrator recipient email
   - Alert cooldown period (seconds)

> **Note:** The system respects a configurable cooldown period between alerts to prevent notification spam.

---

## 📊 How It Works

```
Input Source  ──►  YOLOv8 Model  ──►  Violation Detection
   (Image /              │                      │
   Video /               ▼                      ▼
   Webcam)        Annotated Frame        CSV Log + Email Alert
                         │
                         ▼
                  Streamlit Dashboard
```

1. **Input** — Select a source: live webcam, video upload, or image upload.
2. **Detection** — YOLOv8 runs inference and identifies all PPE items in frame.
3. **Classification** — Detected objects are classified as compliant ✅ or violation ❌.
4. **Logging** — Results are appended to `detections_log.csv` with timestamps.
5. **Alerting** — Email alerts with violation snapshots are dispatched to the admin.

---

## 🖥️ Dashboard Preview

| Mode | Description |
|---|---|
| **Live Webcam** | Checkbox to start/stop real-time monitoring |
| **Upload Video** | Progress bar, frame-by-frame analysis, auto-saved output |
| **Upload Image** | Instant analysis with a one-click save button |
| **Safety Logs** | Scrollable table showing the 15 most recent detections |

---

## 🤝 Contributing

Contributions are welcome! If you have ideas for new features or improvements:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

<div align="center">

**Built with ❤️ to make workplaces safer.**

*If this project helped you, please ⭐ star the repository!*

</div>