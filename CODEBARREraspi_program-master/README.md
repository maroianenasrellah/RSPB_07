# CODEBARREraspi_program
# coding:utf-8
#!/usr/bin/python
# System modules
#from requests import get
from queue import Queue
from threading import  Thread
import time,sys,socket,requests
import RPi.GPIO as GPIO
import threading
import queue
import logging

redPin=22
greenPin=23
bluegreenPin=17
blueredPin=18
relais = 25

time_sleep_led=2

def turnOff(pin):
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, False)
    
def blink(pin):
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin,True)
    
def redOn():
	blink(redPin)
	
def greenOn():
	blink(greenPin)   

def blueOn():
	blink(bluePin)
    
def bluegreenOn():
	blink(bluegreenPin)
	
def blueredOn():
	blink(blueredPin)	
	
def blueredOn():
	blink(blueredPin)	
	
	
def redOff():
	turnOff(redPin)
	
def greenOff():
	turnOff(greenPin)
	
def blueOff():
	turnOff(bluePin)

	
def bluegreenOff():
	turnOff(bluegreenPin)
	
def blueredOff():
	turnOff(blueredPin)
    
	
def LED_Blink(Kel_led):
    iLed = threading.local()
    iLed.i = 0
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(Kel_led, GPIO.OUT)
    while (iLed.i <= 15):
        GPIO.output(Kel_led, True)
        time.sleep(0.1)   
        GPIO.output(Kel_led, False)
        time.sleep(0.1)
        iLed.i = iLed.i + 1
        
#t4 = threading.Thread(name='t4',target=LED_Blink, args=(bluePin,))

#t5 = threading.Thread(name='t5',target=LED_Blink, args=(bluered,))

#t4.start()

#t5.start(
##
##time.sleep(time_sleep_led)
##
##blueOff()
##    
##time.sleep(time_sleep_led)

##blueredOn()
##print("red on")
##
##time.sleep(time_sleep_led)
####
##blueredOff()
bluegreenOff()
##time.sleep(time_sleep_led)
##
##bluegreenOn()
##print("green on")
##
##time.sleep(time_sleep_led)
####
##bluegreenOff()
##print("green off")
##greenOff()
##time.sleep(time_sleep_led)
##greenOn()
##time.sleep(time_sleep_led)
##greenOff()

##redOff()
##time.sleep(time_sleep_led)
##redOn()
##time.sleep(time_sleep_led)
##redOff()

#GPIO.cleanup()
