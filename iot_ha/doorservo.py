import RPi.GPIO as GPIO
import time
import sys

GPIO.setmode (GPIO.BCM)
SERVO_PIN = 18
GPIO.setup(SERVO_PIN,GPIO.OUT)


while 1:
    GPIO.output(SERVO_PIN,True)
    print 'out'
    time.sleep(0.1); 
    GPIO.output(SERVO_PIN,False)
    time.sleep(0.1); 
