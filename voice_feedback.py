import pyttsx3
import threading

# Create a lock to prevent overlapping speech
speech_lock = threading.Lock()

# Track last spoken message
last_message = None


def speak(message):
    global last_message

    # Prevent repeating same message
    if message == last_message:
        return

    last_message = message

    def _speak():
        with speech_lock:
            try:
                engine = pyttsx3.init()
                engine.setProperty('rate', 150)
                engine.say(message)
                engine.runAndWait()
                engine.stop()
            except Exception as e:
                print("Speech error:", e)

    thread = threading.Thread(target=_speak, daemon=True)
    thread.start()
