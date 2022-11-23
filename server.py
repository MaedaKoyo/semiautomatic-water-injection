import socket
import datetime
import threading
import RPi.GPIO as GPIO
import time
import subprocess
from gpiozero import MCP3008

#----------------setup-------------------
Motor1A = 16
Motor1B = 18
Motor1E = 22
GPIO.setmode(GPIO.BOARD)
GPIO.setup(Motor1A,GPIO.OUT)
GPIO.setup(Motor1B,GPIO.OUT)
GPIO.setup(Motor1E,GPIO.OUT)

#----------------method-------------------
def pomp_on():
    print("Turning motor on")
    GPIO.output(Motor1A,GPIO.HIGH)
    GPIO.output(Motor1B,GPIO.LOW)
    GPIO.output(Motor1E,GPIO.HIGH)
    
def pomp_off():
    print("Stopping motor")
    GPIO.output(Motor1E,GPIO.LOW)
    
    
def auto_water():

    def pomp_on():
        print("Turning motor on")
        GPIO.output(Motor1A,GPIO.HIGH)
        GPIO.output(Motor1B,GPIO.LOW)
        GPIO.output(Motor1E,GPIO.HIGH)
        
    def pomp_off():
        print("Stopping motor")
        GPIO.output(Motor1E,GPIO.LOW)

    Vref = 3.3
    dry = 270
    water = 119
    interval = (dry - water) / 3
    wet = water + interval
    lbdry = dry - interval

    try:
        while flg == "2":
            pot = MCP3008(channel=0)
            hum = round(pot.value * Vref * 100,1)
            if (hum > water and hum < wet):
                print("very Wet")
            elif (hum > wet and hum < lbdry):
                print("Wet")
            elif (hum < dry and hum > lbdry):
                print("Dry")
                pomp_on()
                time.sleep(3)
                pomp_off()
            
            msg = str(hum)
            time.sleep(10)
    except: KeyboardInterrupt
    subprocess.call('clear')

#----------------main-------------------
PORT =  55555
BUFSIZE = 4096

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("",PORT))
server.listen()

while True:
    client, adder = server.accept()
    msg = "none"
    flg = "0"
    
    flg = client.recv(BUFSIZE)
    print(flg.decode("UTF-8"))
    flg = flg.decode("UTF-8")
    
    if flg == "1":  #manual
        pomp_on()
        time.sleep(1)
        pomp_off()
        
        sen0193 = MCP3008(channel=0)
        hum = round(sen0193.value * 3.3 * 100,2)
        msg = str(hum)
        
    if flg == "2":  #auto
        thread1 = threading.Thread(target=auto_water)
        thread1.start()
        
    
    client.sendall(msg.encode("UTF-8"))
    client.close() 