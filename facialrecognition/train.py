import os
import cv2
import numpy as np

def train_model(data_path):
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    face_samples = []
    ids = []
    
    person_names = sorted(os.listdir(data_path))
    
    for person_id, person_name in enumerate(person_names):
        person_path = os.path.join(data_path, person_name)
        
        if not os.path.isdir(person_path):
            continue
        
        for image_name in os.listdir(person_path):
            img_path = os.path.join(person_path, image_name)
            gray_img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
            
            if gray_img is None:
                print(f"Warning: Could not read image {img_path}")
                continue
            
            faces = face_cascade.detectMultiScale(gray_img, scaleFactor=1.1, minNeighbors=5)
            for (x, y, w, h) in faces:
                face_samples.append(gray_img[y:y+h, x:x+w])
                ids.append(person_id)
    
    recognizer.train(face_samples, np.array(ids))
    recognizer.save('face_recognizer.yml') 
    print(f"Labels (IDs): {ids}")
    print("Training complete.")

train_model('/Users/cindyli/Documents/GitHub/pi-pal/facialrecognition/people')
