print 'Importing...'
import sys
import time
import subprocess
import picamera
import facerec
import facedet

# Configuring PiCamera
camera = picamera.PiCamera()
camera.sharpness = 0
camera.contrast = 0
camera.brightness = 60
camera.saturation = 0
camera.ISO = 0
camera.video_stabilization = False
camera.exposure_compensation = 0
camera.exposure_mode = 'auto'
camera.meter_mode = 'average'
camera.awb_mode = 'auto'
camera.image_effect = 'none'
camera.color_effects = None
camera.rotation = 0
camera.hflip = False
camera.vflip = False
camera.crop = (0.0, 0.0, 1.0, 1.0)

# Captures image using USB camera
def capture(pi_module):

    print 'Starting camera capture...'
    if pi_module:
        camera.capture('captured/test.jpg')
    else:
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
        '2': "Mohammed",
    }
    return switcher.get(argument, "Unknown")

# Performs face recognition on the cropped face
def face_rec():

    print 'Initiating face recognition...'
    result = facerec.perform_rec()
    print 'Face recognition complete.'
    if result['dist'] > 2:
        return "Unknown"
    return lookup(result['ident'])

# Performs the three steps (capture, detect face, and recognize face)
def identify():

    capture(True)
    if not face_detect():
        return face_rec()
    else:
        return "No person detected."

def preview():

    print 'Starting camera preview...'
    camera.start_preview()
    time.sleep(10)
    print 'Camera stopped previewing.'
    
if __name__ == '__main__':

    preview()           
