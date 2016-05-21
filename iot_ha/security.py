print 'Importing packages...'
import threading
import RPi.GPIO as GPIO
import os
import time
import sys
import doorservo
import facedet
import facerec
import mailer
import motion_detector
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
data = {
            'led': led,
            'lock': lock,
            'ir': ir,
            'occ': occ
        }

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
            if lock == 0:
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
            if motion_detector.occ:
                print "OCCUPIED"
                occ = 1
                update_data()
                occ_flag = 1
                pubnub.publish(channel, data, callback=callback1, error=callback1)
        else:
            if motion_detector.occ == False :
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
    motion_detector.perform()
    
    

if __name__ == '__main__':
    Thread(target = func_recieve).start()
    Thread(target = func_publish).start()
    Thread(target = func_detector).start()

