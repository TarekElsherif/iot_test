from Tkinter import *
import RPi.GPIO as GPIO
import time
import sys
from pubnub import Pubnub

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)
pwm = GPIO.PWM(18, 100)
pwm.start(5)

##pubnub = Pubnub(publish_key='pub-c-df137065-b5ca-4b1d-841a-3f547ec9b6f0',
##                    subscribe_key='sub-c-875a6a50-d26d-11e5-b684-02ee2ddab7fe')
##channel = 'test'

def servo(angle):
    GPIO.setup(18, GPIO.OUT)
    duty = float(angle) / 10.0 + 2.5
    pwm.ChangeDutyCycle(duty)
    time.sleep(1)
    GPIO.setup(18, GPIO.IN)

def _callback(m, channel):
    if m['lock'] == 1:
        servo(90)
    if m['lock'] == 0:  
        servo(0)

def lock:
    servo(90)

def unlock:
    servo(0)

def _error(m):
    print(m)
    
##pubnub.subscribe(channels=channel, callback=_callback, error=_error)
