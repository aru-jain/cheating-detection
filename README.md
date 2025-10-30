# 🧠 NeuroProctor – AI-Based Exam Proctoring System

## ⚙️ Tech Stack
- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Python (Flask)
- **AI/ML Libraries**: OpenCV, MediaPipe
- **Database**: MySQL
- **Chatbot Assistant**: Vanilla JavaScript
- **Quiz API**: Open Trivia DB

## 🚀 How It Works

### 1. 🔐 User Authentication
- Users sign up or log in securely through a Flask-based backend connected to a MySQL database.

### 2. 🎥 Real-Time Proctoring via Webcam
- **Head Pose Estimation**: Uses MediaPipe to track if the candidate is facing the screen.
- **Eye Movement Tracking**: Detects if the user is distracted or looking away.
- **Phone Detection**: Utilizes OpenCV to recognize if a mobile phone is visible in the frame.
- **Tab Switch Monitoring**: Tracks if the user changes browser tabs, marking it as a suspicious activity.

### 3. 🧠 Erica – Inbuilt Proctoring Assistant
- A JavaScript chatbot embedded in the exam page that answers real-time queries related to exam rules, setup, and tech support.

### 4. 📝 Quiz System
- Fetches questions dynamically via API.
- Displays one question at a time with multiple options.
- Upon submission, the score is calculated and shown immediately.

### 5. 🚨 Cheating Alerts
- All cheating behaviors like looking away, tab switching, or phone detection are monitored live.
- Each suspicious action is logged with a timestamp for review.

## 💡 Highlights
- Runs entirely in-browser with webcam access
- Lightweight and responsive UI
- No need for manual invigilation
- Real-time decision-making through integrated AI modules

NeuroProctor provides a complete automated exam environment with transparency and security for both students and institutions.

