import cv2
import mediapipe as mp
import numpy as np


mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils


cap = cv2.VideoCapture(0)


volume_level = 0

while True:
   
    success, frame = cap.read()
    if not success:
        break

    frame = cv2.flip(frame, 1)
    
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
            index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]

            thumb_pos = np.array([thumb_tip.x, thumb_tip.y])
            index_pos = np.array([index_tip.x, index_tip.y])
            distance = np.linalg.norm(thumb_pos - index_pos)

            volume_level = int(np.interp(distance, [0.02, 0.2], [0, 100]))
    
    
    cv2.rectangle(frame, (50, 150), (85, 400), (255, 0, 0), 3)  # Volume bar outline
    cv2.rectangle(frame, (50, 400 - int(volume_level * 2.5)), (85, 400), (255, 0, 0), -1)  # Volume bar fill
    cv2.putText(frame, f'Volume: {volume_level}%', (40, 430), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)

    
    cv2.imshow("Gesture Controlled Volume", frame)

    # Break loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()
