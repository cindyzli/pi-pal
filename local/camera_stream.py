import cv2
import socket
import json
import time
from cvzone.HandTrackingModule import HandDetector
from pymongo.mongo_client import MongoClient
import datetime

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

# Global counter variables
fingers = 0
buzzerFrames = 0
pillFrames = 0

# Raspberry Pi setup for sending commands
raspberry_pi_ip = "10.150.237.86"  # Replace with your Pi's IP address
raspberry_pi_port = 12345  # Port for communication

# Initialize video capture
cap = cv2.VideoCapture(0)

# Function to process frame and count fingers raised
def countFingers(hand):
    global fingers
    landmarks = hand['lmList']

    fingerup = detector.fingersUp(hand)   
    
    thumb_tip = landmarks[4]   # Thumb tip (x, y)
    index_tip = landmarks[8]   # Index tip (x, y)
    middle_tip = landmarks[12] # Middle tip (x, y)
    ring_tip = landmarks[16]   # Ring tip (x, y)
    pinky_tip = landmarks[20]  # Pinky tip (x, y)

    thumb_curl = thumb_tip[1] > landmarks[2][1]
    index_curl = index_tip[1] > landmarks[6][1]
    middle_curl = middle_tip[1] > landmarks[10][1]
    ring_curl = ring_tip[1] > landmarks[14][1]
    pinky_curl = pinky_tip[1] > landmarks[18][1]

    if thumb_curl and index_curl and middle_curl and ring_curl and pinky_curl:
        fingers = 0
        return True
    elif fingerup == [0, 1, 0, 0, 0] and fingers != 1: 
        fingers = 1
        return True
    elif fingerup == [0, 1, 1, 0, 0] and fingers != 2: 
        fingers = 2
        return True
    elif fingerup == [0, 1, 1, 1, 0] and fingers != 3: 
        fingers = 3
        return True
    elif fingerup == [0, 1, 1, 1, 1] and fingers != 4: 
        fingers = 4
        return True
    elif fingerup == [1, 1, 1, 1, 1] and fingers != 5: 
        fingers = 5
        return True
    return False

# Function to check if left hand is making buzzer sign
def isBuzzer(hand):
    landmarks = hand['lmList']

    thumb_tip = landmarks[4]   # Thumb tip (x, y)
    index_tip = landmarks[8]   # Index tip (x, y)
    middle_tip = landmarks[12] # Middle tip (x, y)
    ring_tip = landmarks[16]   # Ring tip (x, y)
    pinky_tip = landmarks[20]  # Pinky tip (x, y)
    
    # Check if thumb and pinky are extended
    thumb_extended = thumb_tip[1] < landmarks[3][1]
    pinky_extended = pinky_tip[1] < landmarks[17][1]

    # Check if other fingers are curled
    index_curl = index_tip[1] > landmarks[6][1]
    middle_curl = middle_tip[1] > landmarks[10][1]
    ring_curl = ring_tip[1] > landmarks[14][1]

    if thumb_extended and pinky_extended and index_curl and middle_curl and ring_curl:
        return True
    return False

def isDispensePill(hand):
    landmarks = hand['lmList']

    thumb_tip = landmarks[4]   # Thumb tip (x, y)
    index_tip = landmarks[8]   # Index tip (x, y)
    middle_tip = landmarks[12] # Middle tip (x, y)
    ring_tip = landmarks[16]   # Ring tip (x, y)
    pinky_tip = landmarks[20]  # Pinky tip (x, y)
    
    # Check if middle, ring, and pinky fingers are extended
    middle_extended = middle_tip[1] < landmarks[9][1]
    ring_extended = ring_tip[1] < landmarks[13][1]    
    pinky_extended = pinky_tip[1] < landmarks[17][1]

    # Check if thumb and index tip are touching
    thumb_index_touching = False
    if abs(thumb_tip[0] - pinky_tip[0]) < 20 and abs(thumb_tip[1] - pinky_tip[1] < 20):
        thumb_index_touching = True

    if middle_extended and ring_extended and pinky_extended and thumb_index_touching:
        return True
    return False

# Function to process the frame and generate JSON commands based on finger count
def process_frame_and_generate_command(img):
    hand, new_img = detector.findHands(img, draw=True, flipType=True)
    changeLed = False
    soundBuzzer = False
    dispensePill = False
    global fingers
    global buzzerFrames
    global pillFrames

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Face detection
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    for (x, y, w, h) in faces:
        face = gray[y:y+h, x:x+w]
        label, confidence = recognizer.predict(face)
        if confidence < 50:  # Threshold for recognition
            cv2.putText(new_img, f"ID: {id_to_names[label]}, Conf: {int(confidence)}", (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            cv2.rectangle(new_img, (x, y), (x+w, y+h), (0, 255, 0), 2)
            if not face_recognized:
                face_recognized = True
                # playsound('audio/accessgranted.mp3')

        else:
            cv2.putText(new_img, "Unknown", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
            cv2.rectangle(new_img, (x, y), (x+w, y+h), (0, 0, 255), 2)

    if hand:   
        # Process both hands if detected
        for h in hand:
            if h["type"] == "Right":
                # Count fingers for the right hand
                changeLed = countFingers(h)
            elif h["type"] == "Left":
                # Check for buzzer gesture with the left hand
                soundBuzzer = isBuzzer(h)
                # Check for pill dispensing gesture with the left hand
                dispensePill = isDispensePill(h)

    if changeLed:
        collection.insert_one({
            "timestamp": datetime.now(),
            "action": "dimming_lights",
            "value": str(fingers * 20) + "%"
        })
        return {
            "action": "adjust_led",
            "brightness": fingers * 20,
        }, img

    if soundBuzzer:
        collection.insert_one({
            "timestamp": datetime.now(),
            "action": "call_sign",
            "value": "emergency",
        })
        buzzerFrames += 1
        if buzzerFrames == 5:
            buzzerFrames = 0
            return {
                "action": "sound_buzzer",
            }, img
    
    if dispensePill:
        collection.insert_one({
            "timestamp": datetime.now(),
            "action": "nurse_request",
            "value": "painkillers"
        })
        pillFrames += 1
        if pillFrames == 5:
            pillFrames = 0
            return {
                "action": "dispense_pill",
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