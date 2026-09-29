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


class R2R_DAC:
    def __init__(self, gpio_bits, dynamic_range, verbose=False):
        self.gpio_bits = gpio_bits
        self.dynamic_range = dynamic_range
        self.verbose = verbose

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.gpio_bits, GPIO.OUT, initial=0)

    def deinit(self):
        GPIO.output(self.gpio_bits, 0)
        GPIO.cleanup()

    def set_number(self, number):
        if not (0 <= number <= 255):
            print("Число должно быть от 0 до 255")
            return

        for i in range(8):
            bit = (number >> i) & 1
            GPIO.output(self.gpio_bits[i], bit)

        if self.verbose:
            print(f"Установлено число: {number}")

    def set_voltage(self, voltage):
        if not (0.0 <= voltage <= self.dynamic_range):
            print(
                f"Напряжение выходит за динамический диапазон "
                f"ЦАП (0.00 - {self.dynamic_range:.2f} В)"
            )
            print("Устанавливаем 0.0 В")
            self.set_number(0)
            return

        number = int(voltage / self.dynamic_range * 255)

        if self.verbose:
            print(f"Напряжение: {voltage:.2f} В")
            print(f"Число: {number}")

        self.set_number(number)


if __name__ == "__main__":
    try:
        dac = R2R_DAC(
            [16, 20, 21, 25, 26, 17, 27, 22],
            3.183,
            True
        )

        while True:
            try:
                voltage = float(input("Введите напряжение в Вольтах: "))
                dac.set_voltage(voltage)

            except ValueError:
                print("Вы ввели не число. Попробуйте ещё раз\n")

    finally:
        dac.deinit()
