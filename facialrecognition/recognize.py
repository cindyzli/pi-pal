import cv2
# from simple_facerec import SimpleFacerec

# sfr.load_encoding_images

# cap = cv2.VideoCapture(0)


# while True:
#      ret, frame = cap.read()
#      cv2.imshow("Frame", frame)
#      key = cv2.waitKey(1)
#      if key == 27:
#           break

# cap.release()
# cv2.destroyAllWindows()


# Load the recognizer and Haar Cascade
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('face_recognizer.yml')
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Open webcam
cap = cv2.VideoCapture(0)

id_to_names = {}
id_to_names[0] = "cindyli"
id_to_names[1] = "elise"

while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    
    for (x, y, w, h) in faces:
        face = gray[y:y+h, x:x+w]
        label, confidence = recognizer.predict(face)
        if confidence < 36:  # Threshold for recognition
            cv2.putText(frame, f"ID: {id_to_names[label]}, Conf: {int(confidence)}", (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        else:
            cv2.putText(frame, "Unknown", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
    
    cv2.imshow('Face Recognition', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
