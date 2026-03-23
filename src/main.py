import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0, cv2.CAP_AVFOUNDATION)

while True:
    ret, frame = cap.read()

    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:

            # Draw hand
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Get landmarks
            lm = hand_landmarks.landmark

            fingers = []

            # Index
            fingers.append(1 if lm[8].y < lm[6].y else 0)

            # Middle
            fingers.append(1 if lm[12].y < lm[10].y else 0)

            # Ring
            fingers.append(1 if lm[16].y < lm[14].y else 0)

            # Pinky
            fingers.append(1 if lm[20].y < lm[18].y else 0)

            total = sum(fingers)

            if total >= 3:
                text = "OPEN"
            else:
                text = "FIST"

            # Display result
            cv2.putText(frame, text, (50, 100),
                        cv2.FONT_HERSHEY_SIMPLEX, 2,
                        (0, 255, 0), 3)

    cv2.imshow("Hand Tracking", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()