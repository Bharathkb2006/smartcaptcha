import cv2
import mediapipe as mp
import time
from captcha import generate_challenges
from voice import speak
hands_module = mp.solutions.hands
drawing_module = mp.solutions.drawing_utils
def countfingers(hand):
    tips = [8, 12, 16, 20]
    total = 0
    for tip in tips:
        if hand.landmark[tip].y < hand.landmark[tip - 2].y:
            total += 1
    if hand.landmark[4].x < hand.landmark[3].x:
        total += 1
    return total
camera = cv2.VideoCapture(0)
questions = generate_challenges()
index = 0
speak("Camera is on.")
last_index = -1
wrong_time = 0
last_spoken_time = 0
with hands_module.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7) as hands:
    while camera.isOpened():
        ok, image = camera.read()
        if not ok:
            break
        image = cv2.flip(image, 1)
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        output = hands.process(rgb)
        if index < len(questions):
            expected = questions[index]
            if last_index != index:
                speak(f"show {expected} ")
                last_index = index
                last_spoken_time = time.time()
                continue  
            if time.time() - last_spoken_time < 2:
                continue
            cv2.putText(image, f"Show: {expected}", (10, 40), cv2.FONT_HERSHEY_COMPLEX, 1.2, (255, 255, 255), 2)
            if output.multi_hand_landmarks:
                for hand in output.multi_hand_landmarks:
                    fingers = countfingers(hand)
                    drawing_module.draw_landmarks(image, hand, hands_module.HAND_CONNECTIONS)
                    cv2.putText(image, f"Detected: {fingers}", (10, 80), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

                    if fingers == expected:
                        if index == len(questions) - 1:
                            speak("CAPTCHA completed. You may proceed.")
                            cv2.putText(image, "Access Granted!", (100, 200), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 255, 255), 4)
                            cv2.imshow("Gesture CAPTCHA", image)
                            cv2.waitKey(2000)
                            camera.release()
                            cv2.destroyAllWindows()
                            exit()
                        else:
                            index += 1
                            last_index = -1
                            time.sleep(0.5)
                    else:
                        now = time.time()
                        if now - wrong_time > 2:
                            speak("Try again")
                            time.sleep(1)
                            speak(f"show {expected} ")
                            wrong_time = now

        cv2.imshow("Gesture CAPTCHA", image)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
camera.release()
cv2.destroyAllWindows()
