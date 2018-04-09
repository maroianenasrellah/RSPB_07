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
import os

rbnom=str(socket.gethostname())
q = queue.Queue()

# Set up some global variables
encore = True
time_sleep_led=3
time_sleep_relay=1
time_boucle=1
redPin=23
greenPin=18
bluegreenPin=24
blueredPin=25
relais = 21

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

def bluegreenOn():
	blink(bluegreenPin)
	
def blueredOn():
	blink(blueredPin)	
	
def redOff():
	turnOff(redPin)
	
def greenOff():
	turnOff(greenPin)
	
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

def declencherelay():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(relais, GPIO.OUT)
    GPIO.output(relais, True)
    time.sleep(time_sleep_relay)#attend 1 secondes sans rien faire
    GPIO.output(relais, False)

def worker():
    oldcb =""
    while 1:
       
        #Lecteur code barre python
        codebarre=sys.stdin.readline().rstrip('\n')
        #print(codebarre)
        if(codebarre != oldcb):
            oldcb=codebarre
            #Put codebarre into the queue
            q.put(codebarre)
        #else:
            #logging.debug('No value yet')
            #print(codebarre, " : previous read")
                
#queues = []
            

# crée le thread  
w = threading.Thread(name='worker', target=worker)
# démarre le thread 
w.start()

threads = []
t1 = threading.Thread(name='t1',target=declencherelay)
t2 = threading.Thread(name='t2',target=LED_Blink, args=(redPin,))
t3 = threading.Thread(name='t3',target=LED_Blink, args=(greenPin,))
t4 = threading.Thread(name='t4',target=LED_Blink, args=(bluegreenPin,))
t1.start()
t2.start()
t3.start()
t4.start()

#LED_Blink(redPin)
#LED_Blink(greenPin)
#LED_Blink(bluePin)
#declencherelay()

##logging.basicConfig(
##    level=logging.DEBUG,
##    format='(%(message)s',
##)
##
cb=""
print('Début')


while encore:
    
   #bluegreenOff()
    
     
    
    # print('.')
    if not q.empty():
        
        
        bluegreenOff()
        
        blueredOn()

        if(cb == "") and (q.qsize()>0):
            
            cb=q.get()
            
        
        else:
            print("bluegreenOff()")

        
        if(cb != ""):    
            
            url="http://aex.e-maroc.info/CHECK/"+rbnom+":"+cb
            
            try:
                
                content=requests.get(url)
                
                
                if(content.text.find('OK')!=(-1)):
                    
                    print(time.asctime(time.localtime(time.time())), ' > CB:', cb, ' : OK - Queued remains : ' , q.qsize())
                    
                    
                    greenOn()
                    
                    #DECLENCHER RELAIS
                    t = threading.Thread(name='declencherelay', target=declencherelay).start()
                    
                    time.sleep(time_sleep_led)
                    
                    greenOff()
                    
                    cb=""
                    
                   
                #NEAR ALLUMER LED bleu
                elif (content.text.find('NEAR')!=(-1)):
                     print(cb,' : NEAR')
                     print(time.asctime(time.localtime(time.time())), ' > CB:', cb, ' : NEAR - Queued remains : ' , q.qsize())
                     LED_Blink(greenPin)
                     #greenOn()
                     #redOn()
                     #time.sleep(time_sleep_led)
                     #greenOff()
                     #redOff()
                     
                     cb=""
                   
                #BAD ALLUMER LED ROUGE
                elif (content.text.find('BAD')!=(-1)):
                        #print(cb,' : BAD')
                        print(time.asctime(time.localtime(time.time())), ' > CB:', cb, ' : BAD - Queued remains : ' , q.qsize())
                        LED_Blink(redPin)
                        #redOn()
                        #time.sleep(time_sleep_led)
                        #redOff()
                        cb=""
                
                
 
                else:
                        blueredOn()
                        
                        print(time.asctime(time.localtime(time.time())), ' > CB:', cb, ' : ', content.text, ' : unknown - Queued remains : ' , q.qsize())    

            except requests.exceptions.RequestException as erc:
                
                blueredOn()
                
                
                print("Error Connecting")
                
                
                cmd = 'sudo route -n add default gw 192.168.1.1'
                
                os.system(cmd)
                
                time.sleep(time_boucle)

    else:
        blueredOff()
        bluegreenOn()
        print(time.asctime(time.localtime(time.time())), ' > None')
        time.sleep(time_boucle)
           
