import cv2
import socket
import pickle
import struct

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Set the IP address and port number of the Raspberry Pi
host_ip = 'RASPBERRY_PI_IP_ADDRESS'  # Replace with the actual IP address
port = 12345

# Connect to the server
client_socket.connect((host_ip, port))

# Receive and display the video frames
data = b""
payload_size = struct.calcsize("L")

while True:
    # Receive the message header containing the frame size
    while len(data) < payload_size:
        data += client_socket.recv(4096)

    # Unpack the frame size from the message header
    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack("L", packed_msg_size)[0]

    # Receive the serialized frame data
    while len(data) < msg_size:
        data += client_socket.recv(4096)

    # Deserialize the frame data using pickle
    frame_data = data[:msg_size]
    data = data[msg_size:]
    frame = pickle.loads(frame_data)

    # Display the received frame
    cv2.imshow('Received Frame', frame)
    cv2.waitKey(1)

# Close the client socket
client_socket.close()
