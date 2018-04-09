# coding:utf-8
#!/usr/bin/python
# System module
import socket
import time
import sys
import requests
import RPi.GPIO as GPIO
import threading
import queue
import os
rbnom=str(socket.gethostname())
cb=""
cmpt=0
    
# Set up some global variables
encore = True
time_sleep_led=5
time_sleep_relay=1
time_boucle=1
time_bad=0.5
redPin=23
greenPin=18
relaisPin = 21
q = queue.Queue()

srv_adress_ip="192.168.1.219"

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(redPin, GPIO.OUT)
GPIO.setup(greenPin, GPIO.OUT)
GPIO.setup(relaisPin, GPIO.OUT)
##
##def turnOff(pin):
##    GPIO.setmode(GPIO.BCM)
##    GPIO.setwarnings(False)
##    GPIO.setup(pin, GPIO.OUT)
##    GPIO.output(pin, False)
    
##def turnOn(pin):
##    GPIO.setmode(GPIO.BCM)
##    GPIO.setwarnings(False)
##    GPIO.setup(pin, GPIO.OUT)
##    GPIO.output(pin,True)
##
def turnOn(pin):
    GPIO.output(pin,True)
    time.sleep(time_sleep_led)
    GPIO.output(pin,False)
    
##def redOn():
##	blink(redPin)
##	
##def greenOn():
##	blink(greenPin)   
##
##def bluegreenOn():
##	blink(bluegreenPin)
##	
##def blueredOn():
##	blink(blueredPin)	
##	
##def redOff():
##	turnOff(redPin)
##	
##def greenOff():
##	turnOff(greenPin)
##	
##def bluegreenOff():
##	turnOff(bluegreenPin)
##	
##def blueredOff():
##	turnOff(blueredPin)

def LED_Blink(Kel_led):
    iLed = threading.local()
    iLed.i = 0
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(Kel_led, GPIO.OUT)
    while (iLed.i <= 25):
        GPIO.output(Kel_led, True)
        time.sleep(0.1)   
        GPIO.output(Kel_led, False)
        time.sleep(0.1)
        iLed.i = iLed.i + 1
        
def LED_Blink_Fast(Kel_led):
    iLed = threading.local()
    iLed.i = 0
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(Kel_led, GPIO.OUT)
    while (iLed.i <= 50):
        GPIO.output(Kel_led, True)
        time.sleep(0.05)   
        GPIO.output(Kel_led, False)
        time.sleep(0.05)
        iLed.i = iLed.i + 1

def LED_Blink_VeryFast(Kel_led):
    iLed = threading.local()
    iLed.i = 0
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(Kel_led, GPIO.OUT)
    while (iLed.i <= 80):
        GPIO.output(Kel_led, True)
        time.sleep(0.025)   
        GPIO.output(Kel_led, False)
        time.sleep(0.025)
        iLed.i = iLed.i + 1
                

def declencherelay():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(relaisPin, GPIO.OUT)
    GPIO.output(relaisPin, False)
    time.sleep(time_sleep_relay)#attend 1 secondes sans rien faire
    GPIO.output(relaisPin, True)
def IMALIVE():
    try:
        url="http://"+srv_adress_ip+"/CHECK/"+rbnom+":IAMALIVE"
        r=requests.get(url)
        print("I AM ALIVE")
        print(r.text)
       
    except requests.exceptions.RequestException as erc:
        print("Error Connecting")
        LED_Blink_VeryFast(redPin)
        cmd = 'sudo reboot'
        os.system(cmd)
##
def worker():
    oldcb =""
    while 1:
       
        #Lecteur code barre python
        codebarre=sys.stdin.readline().rstrip('\n')
        cmpt=0
        #print(codebarre)
        if(codebarre != oldcb):
             oldcb=codebarre
            #Put codebarre into the queue
             q.put(oldcb)
        #else:
            #logging.debug('No value yet')
            #print(codebarre, " : previous read")
                
#queues = []
            

# crée le thread  
w = threading.Thread(name='worker', target=worker)
# démarre le thread 2018AEXD820801

w.start()
IMALIVE()
declencherelay()


while 1:
    
    if not q.empty():
        cmpt=0    
        if(cb == "") and (q.qsize()>0):
            cb=q.get()
            #print('scan code:')
            #Lecteur code barre python
            #codebarre=sys.stdin.readline().rstrip('\n')
        if(cb != ""):
            try:
                url="http://"+srv_adress_ip+"/CHECK/"+rbnom+":"+cb
                content=requests.get(url)
                codebarre=cb
                if(content.text.find('OK')!=(-1)):
                    #print(cb,' : OK ')
                    print(time.asctime(time.localtime(time.time())), ' > CB:', cb,' : ',content.text)
                   # greenOn()
                    #DECLENCHER RELAIS
                    t = threading.Thread(name='declencherelay', target=declencherelay).start()
                    #time.sleep(time_sleep_led)
                    turnOn(greenPin)
                    #greenOff()
                    cb=""
                elif (content.text.find('NEAR')!=(-1)):
                    #print(cb,' : NEAR')
                    print(time.asctime(time.localtime(time.time())), ' > CB:', cb, ' : ',content.text)
                    LED_Blink(greenPin)
                    cb=""
                elif (content.text.find('BAD')!=(-1)):    
                     #pwhile 1:rint(cb,' : BAD')
                     print(time.asctime(time.localtime(time.time())), ' > CB:', cb,' : ',content.text)            
                     LED_Blink(redPin)               
                     #turnOn(redPin)
                     cb=""    
                else:
                    print(time.asctime(time.localtime(time.time())), ' > CB:', cb, ' : ', content.text, ' : ERROR: ')
                    LED_Blink_Fast(redPin)
                time.sleep(time_bad)
            except requests.exceptions.RequestException as erc:
                
                print("Error Connecting")
                LED_Blink_VeryFast(redPin)
                cmd = 'sudo reboot'
                os.system(cmd)
                
    else:
        print(time.asctime(time.localtime(time.time())), ' > None')
        cmpt=cmpt+1
        if(cmpt>=60):
            IMALIVE()
            cmpt=0
        time.sleep(time_boucle)
  
  
            