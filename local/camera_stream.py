import cv2
import socket
import json
import time
from cvzone.HandTrackingModule import HandDetector
from playsound import playsound
from pymongo.mongo_client import MongoClient

# Initialize HandDetector for hand tracking
detector = HandDetector(staticMode=False, maxHands=2, modelComplexity=1, detectionCon=0.5, minTrackCon=0.5)

# Initialize face recognizer
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('face_recognizer.yml')
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
id_to_names = {0: "cindyli", 1: "elise"}

# MongoDB connection for storing stats
uri = "mongodb+srv://cyang2023:Bthgt0SuRB39sFB1@cluster0.ka5bm.mongodb.net/pi-pal?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri)
database = client["pi-pal"]
collection = database["stats"]
fingers = 0

# Raspberry Pi setup for sending commands
raspberry_pi_ip = "10.150.242.209"  # Replace with your Pi's IP address
raspberry_pi_port = 12345  # Port for communication

# Initialize video capture
cap = cv2.VideoCapture(0)

# Function to process frame and count fingers raised
def countFingers(hand):
    global fingers
    fingerup = detector.fingersUp(hand)   
    if fingerup == [0, 0, 0, 0, 0] and fingers != 0:
        fingers = 0
    elif fingerup == [0, 1, 0, 0, 0] and fingers != 1: 
        fingers = 1
    elif fingerup == [0, 1, 1, 0, 0] and fingers != 2: 
        fingers = 2
    elif fingerup == [0, 1, 1, 1, 0] and fingers != 3: 
        fingers = 3
    elif fingerup == [0, 1, 1, 1, 1] and fingers != 4: 
        fingers = 4
    elif fingerup == [1, 1, 1, 1, 1] and fingers != 5: 
        fingers = 5
    return fingers

# Function to check if left hand is making buzzer sign
def isBuzzer(hand, img):
    landmarks = hand['lmList']

    thumb_tip = landmarks[4]   # Thumb tip (x, y)
    pinky_tip = landmarks[20]  # Pinky tip (x, y)
    index_tip = landmarks[8]   # Index tip (x, y)
    middle_tip = landmarks[12] # Middle tip (x, y)
    ring_tip = landmarks[16]   # Ring tip (x, y)
    
    # Check if thumb and pinky are extended
    thumb_extended = thumb_tip[1] < landmarks[3][1]
    pinky_extended = pinky_tip[1] < landmarks[17][1]

    # Check if other fingers are curled
    index_curl = index_tip[1] > landmarks[6][1]
    middle_curl = middle_tip[1] > landmarks[10][1]
    ring_curl = ring_tip[1] > landmarks[14][1]

    if thumb_extended and pinky_extended and index_curl and middle_curl and ring_curl:
        return {
            "action": "sound_buzzer",
        }, img
    
    return {
        "action": "none",
    }, img

# Function to process the frame and generate JSON commands based on finger count
def process_frame_and_generate_command(img):
    hand, img = detector.findHands(img, draw=True, flipType=True)
    send = False
    global fingers

    if hand:   
        # Process both hands if detected
        for h in hand:
            if h["type"] == "Right":
                # Count fingers for the right hand
                fingerup = detector.fingersUp(h)   
                send = countFingers(h) != fingers
            elif h["type"] == "Left":
                # Check for buzzer gesture with the left hand
                action, img = isBuzzer(h, img)
                if action["action"] == "sound_buzzer":
                    playsound('audio/buzzer.mp3')  # Play buzzer sound

    if send:
        # add number to history array
        # collection.update_one({"id": "light"}, {"$push": {"history": fingers}})

        return {
            "action": "adjust_led",
            "brightness": fingers * 20,
        }, img
    
    return {
        "action": "none",
    }, img

# Function to send command to Raspberry Pi
def send_command_to_pi(command, host, port):
    command_json = json.dumps(command)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((host, port))  # Connect to Raspberry Pi
        client_socket.sendall(command_json.encode('utf-8'))  # Send the JSON data
        print(f"Sent command: {command_json}")

# Main loop for video capture and processing
face_recognized = False
while True:
    ret, frame = cap.read()  # Capture a frame
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Face detection
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
    
    # Process the frame for hand gesture and send commands
    command, img = process_frame_and_generate_command(frame)
    if command["action"] != "none": 
        send_command_to_pi(command, raspberry_pi_ip, raspberry_pi_port)

    # Display the frame (optional for debugging)
    cv2.imshow("Camera Feed", img)

    # Exit the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    time.sleep(0.1)  # Delay to control frame rate

cap.release()  # Release the camera
cv2.destroyAllWindows()  # Close the window