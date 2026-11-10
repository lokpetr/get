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

    plt.xlim(0, 0.06)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()
git config --global credential.helper store
git clone https://github.com/lokpetr/get.git
