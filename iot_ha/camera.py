import sys
import subprocess
import facerec
import facedet

# Captures image using USB camera
def capture():
    
    print 'Starting camera capture...'
    subprocess.call("./capture.sh", shell=True)
    print 'Image Captured.'

# Detects and crops out face(s) in the captured image
def face_detect():

    print 'Detecting faces...'
    faces = facedet.perform_det()
    if faces > 0:
        print 'Face detection complete.'
        return False
    else:
        print 'No faces detected.'
        return True

# Identifies the person
def lookup(argument):

    switcher = {
        '1': "Tarek",
    }
    return switcher.get(argument, "Unknown")

# Performs face recognition on the cropped face
def face_rec():

    print 'Initiating face recognition...'
    result = facerec.perform_rec()
    print 'Face recognition complete.'
    return lookup(result['ident'])

# Performs the three steps (capture, detect face, and recognize face)
def identify():

    capture()
    face_detect()
    return face_rec()
    
if __name__ == '__main__':

    per = identify()
    print "===\nPerson identified: " + per                
