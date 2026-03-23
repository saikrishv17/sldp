import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0, cv2.CAP_AVFOUNDATION)

prev_x = None
threshold = 0.07

gesture_text = ""
direction = ""

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(rgb)

    direction = ""
    gesture_text = ""

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:

            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            lm = hand_landmarks.landmark

            fingers = []

            fingers.append(1 if lm[8].y < lm[6].y else 0)
            fingers.append(1 if lm[12].y < lm[10].y else 0)
            fingers.append(1 if lm[16].y < lm[14].y else 0)
            fingers.append(1 if lm[20].y < lm[18].y else 0)

            total = sum(fingers)

            if total >= 3:
                gesture_text = "OPEN"
            else:
                gesture_text = "FIST"

            current_x = lm[8].x

            if gesture_text == "OPEN" and prev_x is not None:
                diff = current_x - prev_x

                if diff > threshold:
                    direction = "RIGHT"
                elif diff < -threshold:
                    direction = "LEFT"

            prev_x = current_x

    display_text = gesture_text

    if direction:
        display_text = direction

    if display_text:
        cv2.putText(frame, display_text, (50, 100),
                    cv2.FONT_HERSHEY_SIMPLEX, 2,
                    (0, 255, 0), 3)

    cv2.imshow("Gesture System", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()