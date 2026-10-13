import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

led = 26
GPIO.setup(led,GPIO.OUT)

photo = 6
GPIO.setup(photo,GPIO.IN)

while True:
    GPIO.output(led, not GPIO.input(photo))   
https://github.com/gatin-kirill/education_rep/tree/main/get_adc
git add .
git commit -m "Add project"
git pull origin main --allow-unrelated-histories
git push -u origin main
