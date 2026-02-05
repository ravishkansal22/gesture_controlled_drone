# Gesture Controlled Drone using Hand Gestures and Voice Commands

A real-time Human–Drone Interaction System that allows controlling a drone using hand gestures and voice commands through computer vision and speech recognition.

Built using Python, OpenCV, MediaPipe, and SpeechRecognition.

---

## Project Overview

This project uses a webcam to detect hand gestures and a microphone to detect voice commands. Based on the input, the system generates drone control actions such as move up, forward, backward, land, stop, and more.

The system also provides voice feedback and displays gesture, speed, and voice command on the camera screen.

---

## Features

- Real-time hand gesture detection
- Voice command recognition
- Speed control using finger distance
- Voice feedback system
- Live visual command display
- Modular and scalable code structure
- Ready for drone integration

---

## Gesture Controls

| Gesture | Action |
|--------|--------|
| Index finger up | Move UP |
| Thumb up | Move RIGHT |
| Little finger up | Move LEFT |
| Peace sign | Move FORWARD |
| First three fingers up | Move BACKWARD |
| Closed fist | LAND |
| Index + Little finger | FLIP |
| All fingers open | STOP |
| Thumb–Index gap | Speed Control |

---

## Voice Commands Supported

Say the following commands:
up
forward
backward
left
right
land
flip
stop

## How It Works

1. Camera captures hand input
2. MediaPipe detects hand landmarks
3. Gesture is identified from finger positions
4. Microphone captures voice commands
5. System converts input into drone action
6. Voice feedback confirms the command

## Future Improvements

- Real drone integration (DJI Tello)
- Gesture stability filtering
- Drone simulator support
- Graphical user interface
- Autonomous tracking

