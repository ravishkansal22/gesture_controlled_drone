import speech_recognition as sr
import threading

# Initialize recognizer and microphone
recognizer = sr.Recognizer()
microphone = sr.Microphone()

# Shared variables
_current_command = None
_listening = False
_lock = threading.Lock()


def _voice_callback(recognizer, audio):
    """
    This function runs automatically when voice is detected.
    It processes speech in background.
    """
    global _current_command

    try:
        command = recognizer.recognize_google(audio)
        command = command.lower()

        with _lock:
            _current_command = command

    except sr.UnknownValueError:
        pass

    except sr.RequestError:
        pass


def start_voice_listener():
    """
    Starts background speech recognition.
    Call this ONCE when starting your system.
    """
    global _listening

    if _listening:
        return

    with microphone as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.5)

    recognizer.listen_in_background(
        microphone,
        _voice_callback,
        phrase_time_limit=3
    )

    _listening = True


def get_voice_command():
    """
    Returns latest voice command and clears it.
    Use this inside your camera loop.
    """
    global _current_command

    with _lock:
        command = _current_command
        _current_command = None

    return command


def map_voice_to_gesture(command):
    """
    Converts voice text to drone action.
    """

    if command is None:
        return None

    if "up" in command:
        return "UP"

    elif "forward" in command:
        return "FORWARD"

    elif "backward" in command:
        return "BACKWARD"

    elif "left" in command:
        return "LEFT"

    elif "right" in command:
        return "RIGHT"

    elif "land" in command:
        return "LAND"

    elif "flip" in command:
        return "FLIP"

    elif "stop" in command:
        return "STOP"

    elif "take off" in command or "takeoff" in command:
        return "TAKEOFF"

    return None


def is_listening():
    """
    Optional: returns True if voice system is active.
    """
    return _listening
