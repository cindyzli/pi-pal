import cv2
import socket
import struct
import pickle

HOST = "<your_windows_ip>"  # Replace with your Windows machine's IP
PORT = 12345               # Same port as in the streaming script

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))
data = b""
payload_size = struct.calcsize("Q")

while True:
    while len(data) < payload_size:
        packet = client_socket.recv(4 * 1024)  # Receive data in chunks
        if not packet:
            break
        data += packet

    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack("Q", packed_msg_size)[0]

    while len(data) < msg_size:
        data += client_socket.recv(4 * 1024)

    frame_data = data[:msg_size]
    data = data[msg_size:]
    frame = pickle.loads(frame_data)

    cv2.imshow("Remote Camera Feed", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

client_socket.close()