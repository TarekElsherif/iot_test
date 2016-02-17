import threading
import RPi.GPIO as GPIO
import time
import sys
from pubnub import Pubnub
from threading import Thread

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

def led_on():
    global led
    led = 1

def led_off():
    global led
    led = 0

def func_recieve():
    
    print '(Thread 1) Listening...'
    
    def _callback(m, channel):
      if m['led'] == 1:
          GPIO.output(LED_PIN,True)
          led_on()
          print 'LED ON'
      if m['led'] == 0:  
          GPIO.output(LED_PIN,False)
          led_off()
          print 'LED OFF'
          
    def _error(m):
            print(m)
     
    pubnub.subscribe(channels=channel, callback=_callback, error=_error)

def func_publish():

    flag = 0;
    print '(Thread 2) Working...'

    while 1:
        global led
        data0 = {
            'ir': 0,
            'led': led
        }
        data1 = {
            'ir': 1,
            'led': led
        }
        
        def callback1(m):
            print 'Object Detected. (IR)'

        def callback2(m):
            print 'No Object Detected. (IR)'
            
        if(flag == 0):
            if(GPIO.input(IR_PIN) == 0):
                pubnub.publish(channel, data0, callback=callback1, error=callback1)
                flag = 1  
        else:
            if(GPIO.input(IR_PIN) == 1):
                pubnub.publish(channel, data1, callback=callback2, error=callback1)
                flag = 0
        time.sleep(0.2) 

if __name__ == '__main__':
    Thread(target = func_recieve).start()
    Thread(target = func_publish).start()
