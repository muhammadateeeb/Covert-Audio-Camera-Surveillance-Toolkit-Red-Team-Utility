import pyaudio
import socket
import wave
import os
import sys

# Server details
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 12345

# Audio parameters
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
AUDIO_FILE = 'audio.wav'

def list_microphones():
    p = pyaudio.PyAudio()

    # List available input devices
    device_count = p.get_device_count()
    mic_devices = []

    print("Available microphones:")
    for i in range(device_count):
        device_info = p.get_device_info_by_index(i)
        if device_info['maxInputChannels'] > 0:  # This device has an input channel
            mic_devices.append((i, device_info['name']))
            print(f"{i}: {device_info['name']}")

    if len(mic_devices) == 0:
        print("No microphone found. Please check your microphone settings.")
        sys.exit(1)

    p.terminate()

    return mic_devices

def select_microphone(mic_devices):
    try:
        choice = int(input("Select the microphone by number: "))
        if choice < 0 or choice >= len(mic_devices):
            raise ValueError
        return mic_devices[choice][0]
    except (ValueError, IndexError):
        print("Invalid choice, defaulting to first microphone.")
        return mic_devices[0][0]

def record_audio(device_index):
    p = pyaudio.PyAudio()

    # Open stream with the selected device
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    input_device_index=device_index,  # Specify device index
                    frames_per_buffer=CHUNK)

    print("Recording audio...")

    frames = []

    try:
        while True:
            data = stream.read(CHUNK)
            frames.append(data)
    except KeyboardInterrupt:
        print("Recording stopped.")
        pass

    # Stop recording
    stream.stop_stream()
    stream.close()
    p.terminate()

    # Save audio to file
    save_audio(frames)

def save_audio(frames):
    with wave.open(AUDIO_FILE, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(pyaudio.PyAudio().get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))

    print(f"Audio saved as {AUDIO_FILE}")
    send_audio_to_server()

def send_audio_to_server():
    # Create socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_HOST, SERVER_PORT))

    with open(AUDIO_FILE, 'rb') as f:
        audio_data = f.read()
        client_socket.sendall(audio_data)

    print("Audio sent to server.")
    client_socket.close()

    # Cleanup
    os.remove(AUDIO_FILE)
    print("Audio file removed.")

if __name__ == '__main__':
    mic_devices = list_microphones()  # List available devices
    selected_device_index = select_microphone(mic_devices)  # Select device
    record_audio(selected_device_index)  # Proceed with audio recording
