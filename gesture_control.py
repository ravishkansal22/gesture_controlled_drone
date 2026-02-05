import cv2
import mediapipe as mp
from voice_feedback import speak
from speech_controller import start_voice_listener, get_voice_command, map_voice_to_gesture

current_gesture = "NONE"
current_speed = 0

def get_current_state():
    return current_gesture, current_speed

last_gesture = None
last_voice_command = None

TIP_IDS = [4, 8, 12, 16, 20]
speed = None

gesture_voice_map = {
    "DRONE WILL GO UP": "Drone moving up",
    "DRONE WILL MOVE FORWARD": "Drone moving forward",
    "DRONE WILL GO BACKWARD": "Drone moving backward",
    "DRONE WILL GO LEFT": "Drone moving left",
    "DRONE WILL GO RIGHT": "Drone moving right",
    "DRONE WILL LAND": "Drone landing",
    "DRONE WILL FLIP": "Drone flipping",
    "DRONE WILL STOP": "Drone stopped"
}

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

FONT = cv2.FONT_HERSHEY_SIMPLEX
FONT_SCALE = 0.7
COLOR_TEXT = (0, 255, 255)
COLOR_FINGER = (0, 255, 0)

start_voice_listener()

import math

def calculate_distance(p1, p2, frame):

    h, w, _ = frame.shape

    x1, y1 = int(p1.x * w), int(p1.y * h)
    x2, y2 = int(p2.x * w), int(p2.y * h)

    distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

    return distance, x1, y1, x2, y2

def distance_to_speed(distance):

    min_dist = 20
    max_dist = 200

    min_speed = 20
    max_speed = 100

    if distance < min_dist:
        distance = min_dist
    if distance > max_dist:
        distance = max_dist

    speed = ((distance - min_dist) / (max_dist - min_dist)) * (max_speed - min_speed) + min_speed

    return int(speed)


def detect_fingers(landmarks):
    """
    Returns finger state array:
    [thumb, index, middle, ring, little]
    """
    fingers = []

    if landmarks[4].x > landmarks[3].x:
        fingers.append(1)
    else:
        fingers.append(0)

    for tip in TIP_IDS[1:]:
        if landmarks[tip].y < landmarks[tip - 2].y:
            fingers.append(1)
        else:
            fingers.append(0)

    return fingers

def detect_gesture(fingers):
    """
    Map finger pattern to gesture
    """

    if fingers == [0, 1, 0, 0, 0]:
        return "DRONE WILL GO UP"

    elif fingers == [1, 0, 0, 0, 0]:
        return "DRONE WILL GO RIGHT"

    elif fingers == [0, 0, 0, 0, 1]:
        return "DRONE WILL GO LEFT"

    elif fingers == [0, 0, 0, 0, 0]:
        return "DRONE WILL LAND"

    elif fingers == [1, 1, 0, 0, 0]:
        return "DRONE WILL MOVE FORWARD"

    elif fingers == [0, 1, 0, 0, 1]:
        return "DRONE WILL FLIP"
    
    elif fingers == [1, 1, 1, 0, 0]:
        return "DRONE WILL GO BACKWARD"
    
    elif fingers == [1, 1, 1, 1, 1]:
        return "DRONE WILL STOP"

    else:
        return "NONE"

while True:

    ret, frame = cap.read()
    gesture = "NONE"
    if not ret:
        print("Failed to read camera")
        break

    frame = cv2.flip(frame, 1)

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    result = hands.process(frame_rgb)

    gesture = "NONE"

    command = get_voice_command()
    voice_action = map_voice_to_gesture(command)
    if voice_action:
        last_voice_command = voice_action
        speak(voice_action)
    
    if result.multi_hand_landmarks:

        for hand_landmarks in result.multi_hand_landmarks:

            landmarks = hand_landmarks.landmark
            thumb_tip = landmarks[4]
            index_tip = landmarks[8]

            distance, x1, y1, x2, y2 = calculate_distance(thumb_tip, index_tip, frame)

            cv2.line(frame, (x1, y1), (x2, y2), (255, 0, 255), 3)

            fingers = detect_fingers(landmarks)

            gesture = detect_gesture(fingers)

            if gesture != last_gesture:
            
                if gesture in gesture_voice_map:
                    speak(gesture_voice_map[gesture])
            
                last_gesture = gesture

            if gesture == "UP":
                speak("Drone moving up")
            
            elif gesture == "DRONE WILL MOVE FORWARD":
                speak("Drone moving forward")
            
            elif gesture == "DRONE WILL GO BACKWARD":
                speak("Drone moving backward")
            
            elif gesture == "DRONE WILL GO LEFT":
                speak("Drone moving left")
            
            elif gesture == "DRONE WILL GO RIGHT":
                speak("Drone moving right")
            
            elif gesture == "DRONE WILL LAND":
                speak("Drone landing")
            
            elif gesture == "DRONE WILL FLIP":
                speak("Drone flipping")
            
            elif gesture == "DRONE WILL STOP":
                speak("Drone stopped")

            if gesture in ["DRONE WILL GO UP", "DRONE WILL MOVE FORWARD", "DRONE WILL GO BACKWARD"]:
                speed = distance_to_speed(distance)
            mp_draw.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )
    cv2.putText(
        frame,
        f"Gesture: {gesture}",
        (10, 50),
        FONT,
        FONT_SCALE,
        COLOR_TEXT,
        2
    )
    
    if speed is not None:
        cv2.putText(
        frame,
        f"Speed: {speed}",
        (10, 90),
        FONT,
        0.7,
        (255, 255, 0),
        2
  )
        
    cv2.putText(
        frame,
        f"Voice: {last_voice_command}",
        (10, 130),
        FONT,
        FONT_SCALE,
        (0, 200, 255),
        2
    )


    cv2.imshow("Gesture Controlled Drone", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
