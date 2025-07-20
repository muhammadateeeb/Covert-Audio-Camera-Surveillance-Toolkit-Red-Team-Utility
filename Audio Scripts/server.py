import socket

# Server details
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 12345

def start_server():
    # Create server socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_HOST, SERVER_PORT))
    server_socket.listen(5)

    print(f"Server listening on {SERVER_HOST}:{SERVER_PORT}...")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Connection from {client_address}")

        audio_data = b''
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            audio_data += data

        with open('received_audio.wav', 'wb') as f:
            f.write(audio_data)
        print("Audio received and saved as received_audio.wav")

        client_socket.close()

if __name__ == '__main__':
    start_server()
