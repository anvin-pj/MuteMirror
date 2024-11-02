import cv2
import mediapipe as mp
import pyautogui
import numpy as np
import time

# Initialize MediaPipe Hands with increased confidence
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.8)
mp_drawing = mp.solutions.drawing_utils

# Initialize webcam
cap = cv2.VideoCapture(0)

# Variables for volume control and toggling mode
volume_level = 50
is_muted = True  # Initially set to muted
toggle_real_volume = False  # Start in simulated mode

# Fake equalizer settings
equalizer_bars = [np.random.randint(10, 50) for _ in range(5)]

# Function to adjust system volume (real functionality)
def adjust_system_volume(volume):
    pyautogui.press("volumeup") if volume > volume_level else pyautogui.press("volumedown")

# Main loop
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Flip frame and convert color
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Detect hand and get landmarks
    result = hands.process(rgb_frame)
    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            # Draw landmarks on the hand
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Get coordinates of the index and thumb tips
            index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]

            # Convert to pixel coordinates
            h, w, _ = frame.shape
            ix, iy = int(index_finger_tip.x * w), int(index_finger_tip.y * h)
            tx, ty = int(thumb_tip.x * w), int(thumb_tip.y * h)

            # Calculate distance between index and thumb
            distance = np.sqrt((ix - tx) ** 2 + (iy - ty) ** 2)

            # Increase or decrease volume based on gesture
            if distance > 100:
                volume_level = min(volume_level + 1, 100)
            else:
                volume_level = max(volume_level - 1, 0)

            # Control actual system volume if real volume toggle is active
            if toggle_real_volume:
                adjust_system_volume(volume_level)

    # Display volume level and mute status
    cv2.rectangle(frame, (50, 50), (300, 150), (50, 50, 50), -1)
    volume_text = f"Volume Level: {volume_level}% {'(Muted)' if is_muted else '(Live)'}"
    cv2.putText(frame, volume_text, (60, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    # Toggle button display
    cv2.rectangle(frame, (50, 200), (300, 250), (0, 255, 0) if toggle_real_volume else (0, 0, 255), -1)
    toggle_text = "Real Volume" if toggle_real_volume else "Simulated Volume"
    cv2.putText(frame, toggle_text, (90, 235), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    # "Unmute" button that does nothing in simulated mode
    cv2.rectangle(frame, (50, 300), (300, 350), (0, 0, 255), -1)
    cv2.putText(frame, "Unmute", (130, 335), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    if is_muted:
        cv2.putText(frame, "Oops, still muted!", (60, 400), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

    # Fake equalizer display
    for i in range(5):
        bar_height = equalizer_bars[i]
        cv2.rectangle(frame, (400 + i * 30, 150 - bar_height), (420 + i * 30, 150), (255, 0, 0), -1)
        # Randomly change the height for the fake equalizer effect
        equalizer_bars[i] = max(10, np.random.randint(10, 50))

    # Show the result frame
    cv2.imshow("Gesture-Controlled Volume (Muted or Live)", frame)

    # Check for key presses
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break  # Quit on 'q'
    elif key == ord('t'):
        toggle_real_volume = not toggle_real_volume  # Toggle between simulated and real volume
        is_muted = not toggle_real_volume  # Update mute status based on mode

# Release resources
cap.release()
cv2.destroyAllWindows()