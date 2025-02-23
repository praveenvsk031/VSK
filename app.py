from flask import Flask, request, jsonify, render_template, redirect, url_for, session
import os
import cv2
import numpy as np
from werkzeug.utils import secure_filename
from deepfake_detector import DeepFakeDetector

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Change this to a secure secret key in production

# Load the trained deepfake detection model
detector = DeepFakeDetector("deepfake_detector_85.h5")

# Allowed file extensions
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'mkv'}
UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Dummy users database (replace with a proper database in production)
users = {}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    if 'user' in session:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if username in users:
        return jsonify({"error": "Username already exists"}), 400
    
    users[username] = password
    return jsonify({"message": "Signup successful"}), 200

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if users.get(username) == password:
        session['user'] = username
        return jsonify({"message": "Login successful"}), 200
    
    return jsonify({"error": "Invalid credentials"}), 401

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('index'))
    return render_template('dashboard.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'user' not in session:
        return jsonify({"error": "Unauthorized"}), 401
    
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        # Extract frame and predict
        frame = detector.extract_first_frame(filepath)
        if frame is None:
            return jsonify({"error": "Failed to process video"}), 400
        
        # Save frame for visualization
        frame_path = os.path.join(UPLOAD_FOLDER, f"frame_{filename}.jpg")
        cv2.imwrite(frame_path, frame)
        
        # Get prediction
        prediction = detector.predict_frame(frame)
        
        result = "Real" if prediction > 0.5 else "Fake"
        confidence = float(prediction) if prediction > 0.5 else float(1 - prediction)
        
        return jsonify({
            "prediction": result,
            "confidence": f"{confidence * 100:.2f}%",
            "color": "green" if result == "Real" else "red",
            "frame_url": f"/static/uploads/frame_{filename}.jpg"
        })
    
    return jsonify({'error': 'Invalid file type'}), 400

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)