import cv2

def recognize_face(image_path, model_path):
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read(model_path)

    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    faces = face_cascade.detectMultiScale(img, scaleFactor=1.1, minNeighbors=5)

    for (x, y, w, h) in faces:
        id, confidence = recognizer.predict(img[y:y+h, x:x+w])
        print(f"Predicted ID: {id}, Confidence: {confidence}")
        if confidence < 50:  # Adjust confidence threshold
            print("Face recognized!")
        else:
            print("Unknown face")
recognize_face()