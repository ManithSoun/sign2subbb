import cv2
import mediapipe as mp
import joblib
import numpy as np

# ==== LOAD MODEL ====
clf = joblib.load("sign_rf_model.pkl")

# ==== SETUP MEDIAPIPE ====
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)
mp_draw = mp.solutions.drawing_utils

# ==== START CAMERA ====
cap = cv2.VideoCapture(0)

print("🎥 Starting real-time sign prediction... Press 'q' to quit.")
while True:
    ret, frame = cap.read()
    if not ret:
        continue

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    label = "No hand"
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            row = []
            for lm in handLms.landmark:
                row += [lm.x, lm.y, lm.z]
            row = np.array(row).reshape(1, -1)

            # Predict gesture
            pred = clf.predict(row)[0]
            label = pred

            # Draw hand landmarks
            mp_draw.draw_landmarks(frame, handLms, mp_hands.HAND_CONNECTIONS)

    # Show prediction on screen
    cv2.putText(frame, f"Prediction: {label}", (10, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("Sign Prediction", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
