import cv2
import sys
import time
import subprocess
import socket

# Function to install missing packages
def install(package):
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])

# List of required packages
required_packages = ['opencv-python']

# Install required packages if they are not already installed
for package in required_packages:
    try:
        __import__(package.split('-')[0])  # 'opencv-python' should be imported as 'cv2'
    except ImportError:
        install(package)

# Define server details (should match with the server)
HOST = '127.0.0.1'  # Localhost (for testing)
PORT = 65432        # Port number to connect to

# Create a TCP/IP socket for connecting to the server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    client.connect((HOST, PORT))
    print(f"Connected to server at {HOST}:{PORT}")
except ConnectionRefusedError:
    print("Connection failed. Please ensure the server is running.")
    sys.exit()

# Start capturing images from the webcam
cap = cv2.VideoCapture(0)

# Capture 10 images with a 1-second delay between each
for i in range(10):
    success, image = cap.read()
    if success:
        # Save the image locally (optional)
        image_filename = f'image_{i+1}.jpg'
        cv2.imwrite(image_filename, image)
        print(f"Captured and saved {image_filename}")
        
        # Encode the image as JPEG to send it
        _, img_encoded = cv2.imencode('.jpg', image)
        img_data = img_encoded.tobytes()
        
        # Send the image data to the server
        client.sendall(img_data)
        print(f"Image {i+1} sent to the server")
        
        # Wait for 1 second before capturing the next image
        time.sleep(1)
    else:
        print("Failed to capture image")

# Release the webcam and close the client connection
cap.release()
cv2.destroyAllWindows()
client.close()
print("Client connection closed")
