import tensorflow as tf
import cv2
import numpy as np

class DeepFakeDetector:
    def __init__(self, model_path):
        """Initialize the DeepFake detector with a trained model."""
        self.model = tf.keras.models.load_model(model_path)

    def preprocess_frame(self, frame):
        """Preprocess a video frame for model input."""
        # Resize frame to match model's expected input size
        frame = cv2.resize(frame, (224, 224))
        
        # Convert to RGB if needed
        if len(frame.shape) == 2:
            frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2RGB)
        elif frame.shape[2] == 4:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2RGB)
        elif frame.shape[2] == 3:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
        # Normalize pixel values
        frame = frame.astype(np.float32) / 255.0
        
        # Add batch dimension
        frame = np.expand_dims(frame, axis=0)
        
        return frame

    def predict_frame(self, frame):
        """Predict whether a single frame is real or fake."""
        processed_frame = self.preprocess_frame(frame)
        prediction = self.model.predict(processed_frame)[0][0]
        return prediction

    def predict_video(self, video_path, num_frames=10):
        """Analyze video and return deepfake probability."""
        cap = cv2.VideoCapture(video_path)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        frame_indices = np.linspace(0, total_frames - 1, num_frames, dtype=int)
        
        predictions = []
        
        for frame_idx in frame_indices:
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
            ret, frame = cap.read()
            if ret:
                prediction = self.predict_frame(frame)
                predictions.append(prediction)
        
        cap.release()
        
        if predictions:
            avg_prediction = np.mean(predictions)
            return avg_prediction
        return 0.5  # Return neutral prediction if no frames were processed

    def extract_first_frame(self, video_path):
        """Extract and return the first frame of the video."""
        cap = cv2.VideoCapture(video_path)
        ret, frame = cap.read()
        cap.release()
        
        if ret:
            return frame
        return None