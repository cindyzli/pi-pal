import cv2
import socket
import json
import time
import random
from cvzone.HandTrackingModule import HandDetector
from pymongo.mongo_client import MongoClient

uri = "mongodb+srv://cyang2023:Bthgt0SuRB39sFB1@cluster0.ka5bm.mongodb.net/pi-pal?retryWrites=true&w=majority&appName=Cluster0"

client = MongoClient(uri)
collection = client["stats"]
fingers = 0

# Function to process the frame and generate JSON commands
def process_frame_and_generate_command(img):

    hand, img = detector.findHands(img, draw=True, flipType=True)
    send = False
    global fingers

    if hand:   
        # Find landmarks of the hand
        lmlist = hand[0]  
        if lmlist: 
            
            # Getting number of fingers up
            fingerup = detector.fingersUp(lmlist)   
            
            if fingerup == [0, 0, 0, 0, 0] and fingers != 0:
                fingers = 0
                send = True
            if fingerup == [0, 1, 0, 0, 0] and fingers != 1: 
                fingers = 1
                send = True
            if fingerup == [0, 1, 1, 0, 0] and fingers != 2: 
                fingers = 2
                send = True
            if fingerup == [0, 1, 1, 1, 0] and fingers != 3: 
                fingers = 3
                send = True
            if fingerup == [0, 1, 1, 1, 1] and fingers != 4: 
                fingers = 4
                send = True
            if fingerup == [1, 1, 1, 1, 1] and fingers != 5: 
                fingers = 5
                send = True

    if send:
        # add number to history array
        collection.update_one({"id": "light"}, {"$push": {"history": fingers}})

        return {
            "action": "adjust_led",
            "brightness": fingers*20,
        }, img
    

    return {
        "action": "none",
    }, img

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

detector = HandDetector(staticMode=False, maxHands=1, modelComplexity=1, detectionCon=0.5, minTrackCon=0.5)

while True:
    ret, frame = cap.read()  # Capture a frame
    if not ret:
        break

    # Process the frame and generate a command
    command, img = process_frame_and_generate_command(frame)

    # Send the command to the Raspberry Pi
    if command["action"] != "none": send_command_to_pi(command, raspberry_pi_ip, raspberry_pi_port)

    # Display the frame (optional for debugging)
    cv2.imshow("Camera Feed", img)

    # Exit the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # Add a small delay to control frame rate (optional)
    time.sleep(0.1)

cap.release()  # Release the camera
cv2.destroyAllWindows()  # Close the window