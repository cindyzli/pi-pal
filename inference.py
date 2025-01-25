import cv2 
from cvzone.HandTrackingModule import HandDetector

# Initialize hand detector to recognize one hand at a time at max
detector = HandDetector(staticMode=False, maxHands=1, modelComplexity=1, detectionCon=0.5, minTrackCon=0.5)

# Default laptop webcam index
video = cv2.VideoCapture(0) 

# Number of fingers up
fingers = 0

while True: 
    _, img = video.read() # Capture image frame
    
    hand, img = detector.findHands(img, draw=True, flipType=True)

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

    cv2.imshow("Video", img) 
    
    # Quit program
    if cv2.waitKey(1) & 0xFF == ord('q'): 
        break

video.release() 
cv2.destroyAllWindows()