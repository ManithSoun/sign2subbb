from fastapi import FastAPI, UploadFile, File
import numpy as np
import cv2
import joblib
import mediapipe as mp
from pydantic import BaseModel
from typing import List

app = FastAPI(title="Sign2Sub API")

# Load your trained RandomForest model
model = joblib.load("model/sign_rf_model.pkl")

# Setup Mediapipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1,
                       min_detection_confidence=0.5, min_tracking_confidence=0.5)

translations = {
    "Again": "ម្តងទៀត",
    "Bathroom": "បន្ទប់ទឹក",
    "Eat": "ញ៉ាំ",
    "Find": "ស្វែងរក",
    "Fine": "មិនអីទេ",
    "Good": "ល្អ",
    "Hello": "សួស្តី",
    "I_Love_You": "ខ្ញុំស្រឡាញ់អ្នក",
    "Like": "ចូលចិត្ត",
    "Me": "ខ្ញុំ",
    "Milk": "ទឹកដោះគោ",
    "No": "ទេ",
    "Please": "សូម",
    "See_You_Later": "ជួបគ្នាលើកក្រោយ",
    "Sleep": "គេង",
    "Talk": "និយាយ",
    "Thank_You": "អរគុណ",
    "Understand": "យល់",
    "Want": "ចង់",
    "What's_Up": "មានអ្វីដែរ",
    "Who": "នរណា",
    "Why": "ហេតុអ្វី",
    "Yes": "បាទ/ចាស",
    "You": "អ្នក"
}

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    # Read image from client
    image_bytes = await file.read()
    np_arr = np.frombuffer(image_bytes, np.uint8)
    frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    # Process with mediapipe
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    if not results.multi_hand_landmarks:
        return {"gesture": None, "confidence": 0.0}

    row = []
    for lm in results.multi_hand_landmarks[0].landmark:
        row += [lm.x, lm.y, lm.z]
    row = np.array(row).reshape(1, -1)

    pred = model.predict(row)[0]
    proba = model.predict_proba(row).max()

    return {
        "gesture": pred,
        "translation": translations.get(pred, pred),
        "confidence": float(proba)
    }
