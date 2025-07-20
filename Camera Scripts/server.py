import socket

# Define server host and port
HOST = '127.0.0.1'  # Localhost (for testing)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

# Create a TCP/IP socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

print(f"Server listening on {HOST}:{PORT}")

# Wait for a client to connect
conn, addr = server.accept()
print(f"Connected by {addr}")

# Create a buffer to receive data
buffer_size = 4096

while True:
    data = conn.recv(buffer_size)
    if not data:
        break
    

# Close the connection
conn.close()
server.close()
