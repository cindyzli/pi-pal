import cv2 
from cvzone.HandTrackingModule import HandDetector
import numpy as np
import math

# Initialize hand detector to recognize one hand at a time at max
detector = HandDetector(staticMode=False, maxHands=2, modelComplexity=1, detectionCon=0.5, minTrackCon=0.5)

# Default laptop webcam index
video = cv2.VideoCapture(0) 

# Number of rfingersup
rfingers= 0

# Right hand
def countFingers(hand):
    global rfingers
    global detector
    # Getting number of rfingers up
    fingerup = detector.fingersUp(hand)   
    if fingerup == [0, 0, 0, 0, 0] and rfingers!= 0:
        rfingers= 0
        print(rfingers)
    if fingerup == [0, 1, 0, 0, 0] and rfingers!= 1: 
        rfingers= 1
        print(rfingers)
    if fingerup == [0, 1, 1, 0, 0] and rfingers!= 2: 
        rfingers= 2
        print(rfingers)
    if fingerup == [0, 1, 1, 1, 0] and rfingers!= 3: 
        rfingers= 3
        print(rfingers)
    if fingerup == [0, 1, 1, 1, 1] and rfingers!= 4: 
        rfingers= 4
        print(rfingers)
    if fingerup == [1, 1, 1, 1, 1] and rfingers!= 5: 
        rfingers= 5
        print(rfingers)
    
    return rfingers

# Left hand
def isBuzzer(hand):
    landmarks = hand['lmList']
    
    # Get landmarks for fingers
    thumb_tip = landmarks[4]   # Thumb tip (x, y)
    index_tip = landmarks[8]   # Index tip (x, y)
    middle_tip = landmarks[12] # Middle tip (x, y)
    ring_tip = landmarks[16]   # Ring tip (x, y)
    pinky_tip = landmarks[20]  # Pinky tip (x, y)
    
    # Check if thumb and pinky are extended
    thumb_extended = thumb_tip[1] < landmarks[3][1]
    pinky_extended = pinky_tip[1] < landmarks[17][1]

    # Check if other fingers are down (tip is below base)
    index_curl = index_tip[1] > landmarks[6][1]
    middle_curl = middle_tip[1] > landmarks[10][1]
    ring_curl = ring_tip[1] > landmarks[14][1]

    if thumb_extended and pinky_extended and index_curl and middle_curl and ring_curl:
        print("BUZZER")
        return True
    return False

while True: 
    _, img = video.read() # Capture image frame
    
    hands, img = detector.findHands(img, draw=True, flipType=True)

    if hands:   
        # Process first hand
        hand1 = hands[0]
        
        if hand1["type"] == "Right":
            countFingers(hand1)
        if hand1["type"] == "Left":
            isBuzzer(hand1)

        # Process second hand, if it exists
        if len(hands) == 2:
            hand2 = hands[1]
            if hand2["type"] == "Right":
                countFingers(hand2)
            elif hand2["type"] == "Left":
                isBuzzer(hand2)

    cv2.imshow("Video", img) 
    cv2.waitKey(1)

    # Quit program
    if cv2.waitKey(1) & 0xFF == ord('q'): 
        break

video.release() 
cv2.destroyAllWindows()