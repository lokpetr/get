import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

led = 26
GPIO.setup(led,GPIO.OUT)

photo = 6
GPIO.setup(photo,GPIO.IN)

while True:
    GPIO.output(led, not GPIO.input(photo))   
import RPi.GPIO as GPIO

# GPIO-пины, подключённые к 8-битному R2R-ЦАП
# Замени номера на свои из схемы!
dac_bits = [5, 6, 13, 19, 26, 16, 20, 21]

# Настройка GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(dac_bits, GPIO.OUT, initial=GPIO.LOW)

# Динамический диапазон ЦАП
dynamic_range = 3.3


def voltage_to_number(voltage):
    if not (0.0 <= voltage <= dynamic_range):
        print(
            f"Напряжение выходит за динамический диапазон "
            f"ЦАП (0.00 - {dynamic_range:.2f} В)"
        )
        print("Устанавливаем 0.0 В")
        return 0

    return int(voltage / dynamic_range * 255)


def number_to_dac(number):
    # Переводим число в двоичный вид и
    # подаём каждый бит на соответствующий GPIO
    for i in range(8):
        bit = (number >> i) & 1
        GPIO.output(dac_bits[i], bit)


try:
    while True:
        try:
            voltage = float(input("Введите напряжение в Вольтах: "))

            number = voltage_to_number(voltage)
            number_to_dac(number)

        except ValueError:
            print("Вы ввели не число. Попробуйте ещё раз\n")

finally:
    GPIO.output(dac_bits, 0)
    GPIO.cleanup()
