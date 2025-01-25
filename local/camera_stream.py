import cv2
import socket
import json
import time
import random
from cvzone.HandTrackingModule import HandDetector
from playsound import playsound

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('face_recognizer.yml')
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
id_to_names = {}
id_to_names[0] = "cindyli"
id_to_names[1] = "elise"

# Function to process the frame and generate JSON commands
def process_frame_and_generate_command(img):

    hand, img = detector.findHands(img, draw=True, flipType=True)
    fingers = 0

    if hand:   
        # Find landmarks of the hand
        lmlist = hand[0]  
        if lmlist: 
            
            # Getting number of fingers up
            fingerup = detector.fingersUp(lmlist)   
            
            if fingerup == [0, 0, 0, 0, 0] and fingers != 0:
                fingers = 0
                print(fingers)
            if fingerup == [0, 1, 0, 0, 0] and fingers != 1: 
                fingers = 1
                print(fingers)
            if fingerup == [0, 1, 1, 0, 0] and fingers != 2: 
                fingers = 2
                print(fingers)
            if fingerup == [0, 1, 1, 1, 0] and fingers != 3: 
                fingers = 3
                print(fingers)
            if fingerup == [0, 1, 1, 1, 1] and fingers != 4: 
                fingers = 4
                print(fingers)
            if fingerup == [1, 1, 1, 1, 1] and fingers != 5: 
                fingers = 5
                print(fingers)

    return {
        "action": "adjust_led",
        "brightness": fingers*20,
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

face_recognized = False

while True:
    ret, frame = cap.read()  # Capture a frame
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    for (x, y, w, h) in faces:
        face = gray[y:y+h, x:x+w]
        label, confidence = recognizer.predict(face)
        if confidence < 50:  # Threshold for recognition
            cv2.putText(frame, f"ID: {id_to_names[label]}, Conf: {int(confidence)}", (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            if not face_recognized:
                face_recognized = True
                # playsound('audio/accessgranted.mp3')

        else:
            cv2.putText(frame, "Unknown", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
    
    cv2.imshow('Face Recognition', frame)

    # Process the frame and generate a command
    command, img = process_frame_and_generate_command(frame)

    # Send the command to the Raspberry Pi
    send_command_to_pi(command, raspberry_pi_ip, raspberry_pi_port)

    # Display the frame (optional for debugging)
    cv2.imshow("Camera Feed", img)

    # Exit the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # Add a small delay to control frame rate (optional)
    time.sleep(0.1)

cap.release()  # Release the camera
cv2.destroyAllWindows()  # Close the window