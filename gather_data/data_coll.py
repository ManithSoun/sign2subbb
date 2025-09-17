import cv2
import mediapipe as mp
import csv
import os

# ==== SETTINGS ====
gesture_label = "Fine"     # 👈 change this for each gesture
num_samples = 200           # how many frames to capture
output_file = "sign_data.csv"

# ==== SETUP ====
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

# create CSV if not exists
file_exists = os.path.isfile(output_file)
csvfile = open(output_file, mode="a", newline="")
csvwriter = csv.writer(csvfile)

# write header if new file
if not file_exists:
    header = ["label"]
    for i in range(21):   # 21 landmarks
        header += [f"x{i}", f"y{i}", f"z{i}"]
    csvwriter.writerow(header)

count = 0
print(f"Collecting {num_samples} samples for gesture: {gesture_label}")

while count < num_samples:
    ret, frame = cap.read()
    if not ret:
        continue

    frame = cv2.flip(frame, 1)  # mirror
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            row = [gesture_label]
            for lm in handLms.landmark:
                row += [lm.x, lm.y, lm.z]
            csvwriter.writerow(row)
            count += 1
            print(f"Captured {count}/{num_samples}")
            mp_draw.draw_landmarks(frame, handLms, mp_hands.HAND_CONNECTIONS)

    cv2.imshow("Capture - Press q to quit", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

print("✅ Data collection complete")
csvfile.close()
cap.release()
cv2.destroyAllWindows()