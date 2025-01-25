import cv2
import socket
import struct
import pickle

HOST = "0.0.0.0"  # Listen on all network interfaces
PORT = 12345      # Port to stream video

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)
print(f"Waiting for connection on {HOST}:{PORT}...")

conn, addr = server_socket.accept()
print(f"Connection established with {addr}")

cap = cv2.VideoCapture(0)  # Open the local camera

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    data = pickle.dumps(frame)
    conn.sendall(struct.pack("Q", len(data)) + data)

cap.release()
conn.close()
server_socket.close()