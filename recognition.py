import os

import cv2
import numpy as np
from PIL import Image


def get_images_and_labels(path):
    # Append all the absolute image paths in a list image_paths
    # We will not read the image with the .sad extension in the training set
    # Rather, we will use them to test our accuracy of the training
    image_paths = [os.path.join(path, f) for f in os.listdir(path) if not f.endswith('.sad')]
    # images will contains face images
    images = []
    # labels will contains the label that is assigned to the image
    labels = []
    for image_path in image_paths:
        # Read the image and convert to grayscale
        image_pil = Image.open(image_path).convert('L')
        # Convert the image format into numpy array
        image = np.array(image_pil, 'uint8')
        # Get the label of the image
        nbr = int(os.path.split(image_path)[1].split(".")[0])
        # Detect the face in the image
        images.append(image)
        labels.append(nbr)
    # return the images list and labels list
    return images, labels


cascPath = "Conf/haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascPath)
images, labels = get_images_and_labels("img/faces")
recognizer = cv2.face.createLBPHFaceRecognizer()
recognizer.train(images, np.array(labels))

video_capture = cv2.VideoCapture(0)
while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30),
                                         flags=cv2.CASCADE_SCALE_IMAGE)

    # Draw a rectangle around the faces

    for (x, y, w, h) in faces:
        if w * h > 50000:
            # cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            # cv2.imwrite( "test/" + str(i) + ".jpg", frame[y:y+h, x:x+w])
            # i+=1
            nbr_predicted, conf = recognizer.predict(gray[y: y + h, x: x + w])
            print(nbr_predicted, conf)
    # Display the resulting frame
    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()
