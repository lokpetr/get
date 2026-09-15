import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
leds = [16,12,25,17,27,23,22,24]
GPIO.setup(leds,GPIO.OUT)
GPIO.output(leds,0)
num = 0
up = 10
down = 9
def dec2bin(value):
    return[int(element) for element in bin(value)[2:].zfill(8)]
sleeptime = 0.2
while True:
    if GPIO.input(up):
        if num >255:
            num = num +1
            print(num,dec2bin(num))
            time.sleep(sleeptime)
    elif GPIO.input(down):
        if num >0:
            num = num-1
            print(num,dec2bin(num))
            time.sleep(sleeptime)
    GPIO.output(leds,dec2bin(num))