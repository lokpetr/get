import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setmode(GPIO.BCM)
leds = [16, 12, 25, 17, 27, 23, 22, 24]
up_button = 9
down_button = 10
for pin in leds:
    GPIO.setup(pin, GPIO.OUT)
GPIO.output(leds, GPIO.LOW)
GPIO.setup(up_button, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(down_button, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
num = 0
sleep_time = 0.2
def dec2bin(value):
    return [int(element) for element in bin(value) [2:].zfill(8)]
sleep_time = 0.2
while True:
    up_pressed = GPIO.input(up_button) == GPIO.HIGH
    down_pressed = GPIO.input(down_button) == GPIO.HIGH
    if up_pressed and down_pressed:
        num= 255
        print("Обе кнопки нажаты. Максимум:", num, dec2bin(num))
        GPIO.output(leds, dec2bin(num))
        time.sleep(sleep_time)
        continue
    elif up_pressed:
        num += 1
        if num > 255:
            num = 0
        print("Вверх:", num, dec2bin(num))
        GPIO.output(leds, dec2bin(num))
        time.sleep(sleep_time)
    elif down_pressed:
        num -= 1
        if num <0:
            num = 255
        print("Вниз:", num, dec2bin(num))
        GPIO.output(leds, dec2bin(num))
        time.sleep(sleep_time)