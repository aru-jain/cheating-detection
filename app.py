from flask import Flask, render_template, request, redirect, url_for, session, Response, jsonify
import mysql.connector
import cv2
import requests
import random
import html
from detection_modules.head_pose import process_head_pose
from detection_modules.eye_movement import process_eye_movement
from detection_modules.mobile_detection import process_mobile_detection

app = Flask(__name__)
app.secret_key = 'nirixa_secret'

# DB connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="A964696r.",
    database="nirixa_db"
)
cursor = db.cursor()

# Webcam setup
camera = cv2.VideoCapture(0)

# Face detection model
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# Cheating detection logic
def detect_cheating(frame):
    cheating_detected = False
    reasons = []

    # Head Pose
    _, head_direction = process_head_pose(frame, None)
    if head_direction != "Looking at Screen":
        cheating_detected = True
        reasons.append(f"Head direction: {head_direction}")

    # Eye Movement
    _, gaze_direction = process_eye_movement(frame)
    if gaze_direction != "Looking Center":
        cheating_detected = True
        reasons.append(f"Gaze direction: {gaze_direction}")

    # Mobile Detection
    _, mobile_detected = process_mobile_detection(frame)
    if mobile_detected:
        cheating_detected = True
        reasons.append("Mobile phone detected")

    return cheating_detected, head_direction, gaze_direction, ', '.join(reasons)

# Routes
@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        db.commit()
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
        user = cursor.fetchone()
        if user:
            session['username'] = username
            return redirect(url_for('exam'))
        else:
            return "Login failed. Try again."
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/exam')
def exam():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('exam.html', username=session['username'])

@app.route('/video_feed')
def video_feed():
    def generate():
        while True:
            success, frame = camera.read()
            if not success:
                break
            else:
                # Detect cheating
                cheating, head_direction, gaze_direction, reason = detect_cheating(frame)

                # Convert to grayscale for face detection
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray, 1.3, 5)

                for (x, y, w, h) in faces:
                    color = (0, 255, 0) if not cheating else (0, 0, 255)  # Green or Red
                    cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)

                # Add labels
                cv2.putText(frame, f"Head: {head_direction}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)
                cv2.putText(frame, f"Gaze: {gaze_direction}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)
                # if cheating:
                #     cv2.putText(frame, "⚠ Cheating Detected!", (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,255), 3)

                ret, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()

                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/detect')
def detect():
    success, frame = camera.read()
    if success:
        detected, head_direction, gaze_direction, reason = detect_cheating(frame)
        return jsonify({
            'cheating_detected': detected,
            'reason': reason
        })
    return jsonify({'error': 'No frame detected'})

@app.route('/quiz_questions')
def quiz_questions():
    try:
        # Configure OpenTDB parameters
        amount = 5  # Number of questions
        category = request.args.get('category', '')  # Optional: category ID
        difficulty = request.args.get('difficulty', '')  # Optional: easy, medium, hard
        
        # Build API URL
        api_url = "https://opentdb.com/api.php?amount=" + str(amount) + "&type=multiple"
        
        if category:
            api_url += f"&category={category}"
        
        if difficulty:
            api_url += f"&difficulty={difficulty}"
        
        # Make API request
        response = requests.get(api_url)
        data = response.json()
        
        if data['response_code'] != 0:
            # Handle API errors
            error_messages = {
                1: "Not enough questions available",
                2: "Invalid parameter",
                3: "Invalid session token",
                4: "Token exhausted"
            }
            return jsonify({"error": error_messages.get(data['response_code'], "Unknown API error")})
        
        # Process questions
        questions = []
        for idx, item in enumerate(data['results'], start=1):
            # Decode HTML entities
            question_text = html.unescape(item['question'])
            correct_answer = html.unescape(item['correct_answer'])
            incorrect_answers = [html.unescape(ans) for ans in item['incorrect_answers']]
            
            # Combine and shuffle options
            all_options = incorrect_answers + [correct_answer]
            random.shuffle(all_options)
            
            questions.append({
                "id": str(idx),
                "question": question_text,
                "options": all_options,
                "answer": correct_answer
            })
        
        # Store correct answers in session for scoring
        session['correct_answers'] = {str(idx): q['answer'] for idx, q in enumerate(questions, start=1)}
        
        # Remove answers before sending to frontend
        for q in questions:
            q.pop('answer', None)
            
        return jsonify(questions)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/submit_quiz', methods=['POST'])
def submit_quiz():
    try:
        submitted = request.json.get("answers", {})
        correct_answers = session.get('correct_answers', {})

        score = 0
        for qid, user_ans in submitted.items():
            if correct_answers.get(qid) == user_ans:
                score += 1
                
        return jsonify({"score": score, "total": len(correct_answers)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/log_cheating', methods=['POST'])
def log_cheating():
    data = request.get_json()
    reason = data.get('reason', 'Unknown reason')
    
    # Log the cheating attempt (you can store it in DB too)
    print(f"[Cheating Detected] User: {session.get('username', 'Unknown')} | Reason: {reason}")

    # Return confirmation
    return jsonify({'status': 'logged'})

@app.route('/categories')
def get_categories():
    try:
        response = requests.get("https://opentdb.com/api_category.php")
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)