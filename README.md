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

- <img width="800" height="386" alt="image" src="https://github.com/user-attachments/assets/268ab235-f6d7-4c89-8e7f-a659256bc43c" />


### 2. 🎥 Real-Time Proctoring via Webcam
- **Head Pose Estimation**: Uses MediaPipe to track if the candidate is facing the screen.
- **Eye Movement Tracking**: Detects if the user is distracted or looking away.
- **Phone Detection**: Utilizes OpenCV to recognize if a mobile phone is visible in the frame.
- **Tab Switch Monitoring**: Tracks if the user changes browser tabs, marking it as a suspicious activity.

- <img width="219" height="350" alt="image" src="https://github.com/user-attachments/assets/72a4a2c5-479d-4a9b-9cb7-7576d6704905" />


### 3. 🧠 Chatbot – Inbuilt Proctoring Assistant
- A JavaScript chatbot embedded in the exam page that answers real-time queries related to exam rules, setup, and tech support.

- <img width="318" height="406" alt="image" src="https://github.com/user-attachments/assets/1a8e43d9-e397-4bd0-9b07-caf6b455327e" />


- 

### 4. 📝 Quiz System
- Fetches questions dynamically via API.
- Upon submission, the score is calculated and shown immediately.

- <img width="800" height="589" alt="image" src="https://github.com/user-attachments/assets/18b9efa9-95f7-483c-8b7f-7efaf7782b55" />

<img width="800" height="445" alt="image" src="https://github.com/user-attachments/assets/a2a0c39e-a91c-4730-b119-d892fc7423b7" />





### 5. 🚨 Cheating Alerts
- All cheating behaviors like looking away, tab switching, or phone detection are monitored live.
- Each suspicious action is logged with a timestamp for review.

- <img width="554" height="198" alt="image" src="https://github.com/user-attachments/assets/f10553f9-fde3-4873-bf0b-1a0c2baed674" />


## 💡 Highlights
- Runs entirely in-browser with webcam access
- Lightweight and responsive UI
- No need for manual invigilation
- Real-time decision-making through integrated AI modules

NeuroProctor provides a complete automated exam environment with transparency and security for both students and institutions.

