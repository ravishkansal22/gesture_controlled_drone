import threading
import time

from gesture_control import run_gesture_system, get_current_state
from speech_controller import listen_for_command, map_voice_to_gesture
from voice_feedback import speak


def speech_loop():

    print("Speech thread started")

    while True:

        try:

            command = listen_for_command()

            if command is None:
                continue

            action = map_voice_to_gesture(command)

            if action:

                print("Voice command detected:", action)

                speak(f"Drone {action.lower()}")

        except Exception as e:

            print("Speech error:", e)



def gesture_monitor_loop():

    last_gesture = None

    while True:

        gesture, speed = get_current_state()

        if gesture != last_gesture:

            print("Gesture:", gesture, "Speed:", speed)

            last_gesture = gesture

        time.sleep(0.1)


speech_thread = threading.Thread(target=speech_loop)
speech_thread.daemon = True
speech_thread.start()

gesture_thread = threading.Thread(target=run_gesture_system)
gesture_thread.daemon = True
gesture_thread.start()


gesture_monitor_loop()
