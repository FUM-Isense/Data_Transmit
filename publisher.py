import cv2
import socket
import pickle
import struct

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Get the IP address of the Raspberry Pi
host_name = socket.gethostname()
host_ip = socket.gethostbyname(host_name)
print("Host IP:", host_ip)

# Set the port number and bind the socket to it
port = 12345
socket_address = (host_ip, port)
server_socket.bind(socket_address)

# Listen for incoming connections
server_socket.listen(5)
print("Listening for incoming connections...")

while True:
    # Accept a client connection
    client_socket, addr = server_socket.accept()
    print('Got connection from', addr)

    # Open the video capture device (webcam)
    cap = cv2.VideoCapture(0)

    while True:
        # Read a frame from the video capture device
        ret, frame = cap.read()

        # Serialize the frame using pickle
        data = pickle.dumps(frame)

        # Pack the serialized frame and send it over the network
        message_size = struct.pack("L", len(data))
        client_socket.sendall(message_size + data)

    # Release the video capture device and close the client socket
    cap.release()
    client_socket.close()
