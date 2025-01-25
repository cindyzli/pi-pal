import cv2
import socket
import json
import time
import random

# Function to process the frame and generate JSON commands
def process_frame_and_generate_command(frame):
    return {
        "action": "adjust_led",
        "brightness": random.choice([0, 20, 40, 60, 80, 100]),
    }

# Function to send command to Raspberry Pi
def send_command_to_pi(command, host, port):
    # Serialize the command to JSON
    command_json = json.dumps(command)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((host, port))  # Connect to Raspberry Pi
        client_socket.sendall(command_json.encode('utf-8'))  # Send the JSON data
        print(f"Sent command: {command_json}")

# Set up the socket connection
raspberry_pi_ip = "10.150.242.209"  # Replace with your Pi's IP address
raspberry_pi_port = 12345  # Port for communication

# Open the local camera (you can replace 0 with a different camera ID if needed)
cap = cv2.VideoCapture(0)

while True:
    time.sleep(1)
    ret, frame = cap.read()  # Capture a frame
    if not ret:
        break

    # Process the frame and generate a command
    command = process_frame_and_generate_command(frame)

    # Send the command to the Raspberry Pi
    send_command_to_pi(command, raspberry_pi_ip, raspberry_pi_port)

    # Display the frame (optional for debugging)
    cv2.imshow("Camera Feed", frame)

    # Exit the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # Add a small delay to control frame rate (optional)
    time.sleep(0.1)

cap.release()  # Release the camera
cv2.destroyAllWindows()  # Close the window