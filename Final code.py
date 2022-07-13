#import Adafruit_DHT
import RPi.GPIO as GPIO
import time

import dht11

import socket                   # Import socket module
import random

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)


Humidity = None
Temperature = None

GPIO_TRIGGER = 18
GPIO_ECHO = 24
 
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

GAS_PIN = 21
MOTION_PIN = 20
GPIO.setup(GAS_PIN, GPIO.IN)
GPIO.setup(MOTION_PIN, GPIO.IN)

instance = dht11.DHT11(pin=4)

  

port = 5000                     # Reserve a port for your service.
s = socket.socket()             # Create a socket object
host = "192.168.43.18"         #socket.gethostname()     # Get local machine name
#s.close()
s.bind((host, port))            # Bind to the port
s.listen(10)                     # Now wait for client connection.

print('Server listening....')

def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    StartTime = time.time()
    StopTime = time.time()
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
 
    return distance
 

try:
    while True:
        conn, addr = s.accept()     # Establish connection with client.
        print ('Got connection from', addr)
        dist = distance()
        dist2="%.1f cm" % dist
        dist1=str(dist2)
        print ("Measured Distance = %.1f cm" % dist)

        result = instance.read()
        if result.is_valid():
            temprature=result.temperature
            temprature1=str(temperature)
            humidity=result.humidity
            humidity1=str(humidity)+"%"
            print("Temp: %d C" % result.temperature +' '+"Humid: %d %%" % result.humidity)
        else:
            temperature1="0"
            humidity1="0%"
            print("Error reading")
        
        
        a=GPIO.input(GAS_PIN)
        b=GPIO.input(MOTION_PIN)
        if a==0:
            x="Gas_Detected"
            print("Gas Detected")
        else:
            x="No_Gas_Detected"
            print("No Gas Detected")
        if b==1:
            y="Motion_Detected"
            print("Motion Detected")
        else:
            y="No_Motion_Detected"
            print("No Motion Detected")
        #data = conn.recv(1024)
        #print('Server received', repr(data))
        if(y=="Motion_Detected"):
            human="Possibility_of_Human"
        else:
            human="No_Human_Possibility"

        
        
        tosend='Temperature={},Humidity={},Distance={},Radar={},Gas={},Human_Presence={}'.format(temperature1,humidity1,dist1,y,x,human)
        conn.send(tosend.encode('utf-8'))
        print('Done sending')
        conn.close()


        

except KeyboardInterrupt: # If there is a KeyboardInterrupt (when you press ctrl+c), exit the program and cleanup
    print("Cleaning up!")
    gpio.cleanup()

