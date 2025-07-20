# Covert Audio & Camera Surveillance Toolkit

## Overview
This Python-based surveillance toolkit is designed for **red team operations**, **penetration testing**, and **cybersecurity research**. It enables covert audio recording and webcam image capture from target machines, with real-time data exfiltration over TCP to a controlled command-and-control (C2) server.

---

## Features

- 🎙 **Audio Recording Module**
  - Captures real-time microphone input.
  - Streams recorded audio to the C2 server.
  - Auto-clears local traces post-transmission.

-  **Camera Image Capture Module**
  - Captures sequential webcam images (10 by default).
  - Sends images as encoded JPEGs to the server.

-  **C2 Server Module**
  - Receives and stores audio/image files.
  - Supports continuous listening for incoming connections.

---

## Technologies Used

- Python 3.x
- PyAudio
- OpenCV
- Standard Libraries: `socket`, `wave`, `os`, `sys`, `time`, `subprocess`

---

## Usage Instructions

### 1️⃣ Start the Server:
```bash
     python3 server.py
```
### Run Audio Surveillance:
```bash
python3 audio.py
```
3️### Run Camera Surveillance:
```bash
python3 camera_client.py
