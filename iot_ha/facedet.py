import cv2
import sys


def perform_det():
    # Get user supplied values
    imagePath = 'captured/test.jpg'
    cascPath = 'haarcascade_frontalface_default.xml'

    # Create the haar cascade
    faceCascade = cv2.CascadeClassifier(cascPath)

    # Read the image
    image = cv2.imread(imagePath)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Detect faces in the image
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags = cv2.cv.CV_HAAR_SCALE_IMAGE
    )

    print "Found {0} faces!".format(len(faces))

    for (x, y, w, h) in faces:
        # Crops face
        w_mod = (h * 92)/112
        crop_img = image[y:y+h, x:x+w_mod]
        crop_img = cv2.resize(crop_img, (92, 112))
        cv2.imwrite("test_faces/face.jpg", crop_img)
        # cv2.imshow("Cropped face", crop_img)
        # Draws rectangle
        cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 1)
        cv2.imwrite("captured/test.jpg", image)

    return len(faces)

if __name__ == '__main__':
    perform_det()
    # cv2.imshow("Faces found", image)
    # cv2.waitKey(0)
