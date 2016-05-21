print 'Importing packages...'
import threading
import RPi.GPIO as GPIO
import os
import time
import datetime
import sys
import doorservo
import facedet
import mailer
import cv2
import imutils
import argparse
from pubnub import Pubnub
from threading import Thread
print 'Packages imported.'

GPIO.setwarnings(False)
GPIO.setmode (GPIO.BCM)
LED_PIN = 4
GPIO.setup(LED_PIN,GPIO.OUT)
IR_PIN = 3
GPIO.setup(IR_PIN,GPIO.IN)

pubnub = Pubnub(publish_key='pub-c-df137065-b5ca-4b1d-841a-3f547ec9b6f0',
                    subscribe_key='sub-c-875a6a50-d26d-11e5-b684-02ee2ddab7fe')
channel = 'test'
led = 0
ir = 1
lock = 0
occ = 2
motion_occ = False
data = {
            'led': led,
            'lock': lock,
            'ir': ir,
            'occ': occ
        }

camera = cv2.VideoCapture(0)
    
def update_data():
    global data
    data = {
            'led': led,
            'lock': lock,
            'ir': ir,
            'occ': occ
        }
    
doorservo.unlock()

def led_on():
    global led
    GPIO.output(LED_PIN,True)
    led = 1

def led_off():
    global led
    GPIO.output(LED_PIN,False)
    led = 0

def func_recieve():
    
    print '(Thread 1) Listening...'

    def _callback(m, channel):
        if m['led'] == 1:
            if led == 0:
                led_on()
                print 'LED ON'
        if m['led'] == 0:
            if led == 1:
                led_off()
                print 'LED OFF'
        if m['lock'] == 1:
            if lock == 0
                lock = 1
                doorservo.lock()
                print 'DOOR LOCKED'
        if m['lock'] == 0:
            if lock == 1:    
                lock = 0
                doorservo.unlock()
                print 'DOOR UNLOCKED'    
          
    def _error(m):
            print(m)
     
    pubnub.subscribe(channels=channel, callback=_callback, error=_error)

def func_publish():

    counter = 0 
    ir_flag = 0;
    occ_flag = 0;
    global led
    global occ
    global lock
    global ir
    global motion_occ
    print '(Thread 2) Working...'

    while 1:
        if doorservo.locked:
            lock = 1
        else:
            lock = 0

        def callback1(m):
            print 'Object Detected. (IR)'

        def callback2(m):
            print 'No Object Detected. (IR)'
        if(occ_flag == 0):
            if motion_occ:
                print "OCCUPIED"
                occ = 1
                update_data()
                occ_flag = 1
                pubnub.publish(channel, data, callback=callback1, error=callback1)
        else:
            if motion_occ == False :
                print "NOT OCCUPIED"
                occ = 0
                update_data()
                occ_flag = 0
                pubnub.publish(channel, data, callback=callback1, error=callback1)
            
        if(ir_flag == 0):
            if(GPIO.input(IR_PIN) == 0):
                counter = 0
                ir = 0
                update_data()
                pubnub.publish(channel, data, callback=callback1, error=callback1)
                ir_flag = 1  
        else:
            if(GPIO.input(IR_PIN) == 1):
                if counter >= 60:
                    # notify_by_mail('tarek.elsherif9@gmail.com', 'The door is open.')
                    counter = 0
                ir = 1
                update_data()
                pubnub.publish(channel, data, callback=callback2, error=callback1)
                ir_flag = 0
                counter = 0
        time.sleep(0.2)
        if ir_flag:
            if counter < 100:
                counter = counter + 1
                if counter == 60:
                    print 'Mail mode activated'

def func_detector():

    print '(Thread 3) Detecting...'
    firstFrame = None
    first = True
    occ_flag = False
    motion_occ = False
    
    # loop over the frames of the video
    while True:
        # grab the current frame and initialize the occupied/unoccupied
        # text
        (grabbed, frame) = camera.read()
        text = "Unoccupied"
        occ_flag = False

        if first:
            (grabbed, frame) = camera.read()
            print grabbed
            frame = imutils.resize(frame, width=500)
            cv2.imshow("First", frame)
            first = False
         
        # if the frame could not be grabbed, then we have reached the end
        # of the video
        if not grabbed:
            break
         
        # resize the frame, convert it to grayscale, and blur it
        frame = imutils.resize(frame, width=500)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)
         
        # if the first frame is None, initialize it
        if firstFrame is None:
            firstFrame = gray
            continue
        
        # compute the absolute difference between the current frame and
        # first frame
        frameDelta = cv2.absdiff(firstFrame, gray)
        thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
         
        # dilate the thresholded image to fill in holes, then find contours
        # on thresholded image
        thresh = cv2.dilate(thresh, None, iterations=2)
        (cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
         
        # loop over the contours
        for c in cnts:
            # if the contour is too small, ignore it
            if cv2.contourArea(c) < args["min_area"]:
                continue
         
            # compute the bounding box for the contour, draw it on the frame,
            # and update the text
            (x, y, w, h) = cv2.boundingRect(c)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            text = "Occupied"
            occ_flag = True 
            break

        # draw the text and timestamp on the frame
        motion_occ = occ_flag
        cv2.putText(frame, "Room Status: {}".format(text), (10, 20),
        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
        (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
         
        # show the frame and record if the user presses a key
        cv2.imshow("Security Feed", frame)
        cv2.imshow("Thresh", thresh)
        cv2.imshow("Frame Delta", frameDelta)
        key = cv2.waitKey(1) & 0xFF
         
        # if the `q` key is pressed, break from the loop
        if key == ord("q"):
            break

        # cleanup the camera and close any open windows
    camera.release()
    cv2.destroyAllWindows()
    
    

if __name__ == '__main__':
    Thread(target = func_recieve).start()
    Thread(target = func_publish).start()
    Thread(target = func_detector).start()

