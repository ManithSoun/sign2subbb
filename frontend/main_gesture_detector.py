import cv2
import numpy as np
import mediapipe as mp
import joblib

class GestureDetector:
    def __init__(self):
        self.confidence_threshold = 0.7
        self.space = 20
        self.imgSize = 300

        # Load RandomForest model (trained from CSV)
        try:
            self.model = joblib.load("model/sign_rf_model.pkl")  # 👈 trained model path
            self.model_loaded = True
            print("✅ RandomForest model loaded")
        except Exception as e:
            print(f"Error loading RandomForest model: {e}")
            self.model_loaded = False

        # Mediapipe Hands
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.mp_draw = mp.solutions.drawing_utils

    def set_confidence_threshold(self, threshold):
        self.confidence_threshold = threshold

    def get_gesture_text(self, label, language="english"):
        """Return gesture text in specified language"""
        # For now, labels are already strings (e.g., "Hello", "ThankYou")
        return label

    def process_frame(self, frame):
        if not self.model_loaded:
            return frame, None, 0.0

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb)

        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks:
                row = []
                for lm in handLms.landmark:
                    row += [lm.x, lm.y, lm.z]
                row = np.array(row).reshape(1, -1)

                # Predict gesture
                pred = self.model.predict(row)[0]
                # NOTE: scikit-learn RandomForest doesn't give probabilities by default
                # If you need confidence, use predict_proba
                proba = self.model.predict_proba(row).max()

                # Draw landmarks
                self.mp_draw.draw_landmarks(frame, handLms, self.mp_hands.HAND_CONNECTIONS)

                return frame, pred, proba

        return frame, None, 0.0
