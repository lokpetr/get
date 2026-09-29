import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

led = 26
GPIO.setup(led,GPIO.OUT)

photo = 6
GPIO.setup(photo,GPIO.IN)

while True:
    GPIO.output(led, not GPIO.input(photo))   
import numpy as np
import time


def get_sin_wave_amplitude(freq, time):
    return (np.sin(2 * np.pi * freq * time) + 1) / 2


def wait_for_sampling_period(sampling_frequency):
    time.sleep(1 / sampling_frequency)
import r2r_dac as r2r
import signal_generator as sg
import time


amplitude = 3.2
signal_frequency = 10
sampling_frequency = 1000


try:
    dac = r2r.R2R_DAC(
        [16, 20, 21, 25, 26, 17, 27, 22],
        3.183,
        True
    )

    start_time = time.time()

    while True:
        current_time = time.time() - start_time

        signal = sg.get_sin_wave_amplitude(
            signal_frequency,
            current_time
        )

        voltage = signal * amplitude

        dac.set_voltage(voltage)

        sg.wait_for_sampling_period(sampling_frequency)

finally:
    dac.deinit()
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
import pwm_dac as pwm
import signal_generator as sg
import time


amplitude = 3.2
signal_frequency = 10
sampling_frequency = 1000


try:
    dac = pwm.PWM_DAC(
        12,
        500,
        3.290,
        True
    )

    start_time = time.time()

    while True:
        current_time = time.time() - start_time

        signal = sg.get_sin_wave_amplitude(
            signal_frequency,
            current_time
        )

        voltage = signal * amplitude

        dac.set_voltage(voltage)

        sg.wait_for_sampling_period(sampling_frequency)

finally:
    dac.deinit()
    
            except ValueError:
                print("Вы ввели не число. Попробуйте ещё раз\n")

    finally:
        dac.deinit()
import RPi.GPIO as GPIO
import signal_generator as sg
import time


class R2R_DAC:
    def __init__(self, gpio_bits, dynamic_range):
        self.gpio_bits = gpio_bits
        self.dynamic_range = dynamic_range

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.gpio_bits, GPIO.OUT, initial=0)

    def set_voltage(self, voltage):
        number = int(voltage / self.dynamic_range * 255)

        for i in range(8):
            bit = (number >> i) & 1
            GPIO.output(self.gpio_bits[i], bit)

    def deinit(self):
        GPIO.output(self.gpio_bits, 0)
        GPIO.cleanup()


amplitude = 3.2
signal_frequency = 10
sampling_frequency = 1000


try:
    dac = R2R_DAC(
        [16, 20, 21, 25, 26, 17, 27, 22],
        3.183
    )

    start_time = time.time()

    while True:
        current_time = time.time() - start_time

        signal = sg.get_sin_wave_amplitude(
            signal_frequency,
            current_time
        )

        voltage = signal * amplitude

        dac.set_voltage(voltage)
        

        sg.wait_for_sampling_period(sampling_frequency)



finally:
    dac.deinit()
import RPi.GPIO as GPIO
import signal_generator as sg
import time


class PWM_DAC:
    def __init__(self, gpio_pin, pwm_frequency, dynamic_range):
        self.gpio_pin = gpio_pin
        self.pwm_frequency = pwm_frequency
        self.dynamic_range = dynamic_range

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.gpio_pin, GPIO.OUT)

        self.pwm = GPIO.PWM(self.gpio_pin, self.pwm_frequency)
        self.pwm.start(0)

    def set_voltage(self, voltage):
        duty_cycle = voltage / self.dynamic_range * 100

        if duty_cycle < 0:
            duty_cycle = 0

        if duty_cycle > 100:
            duty_cycle = 100

        self.pwm.ChangeDutyCycle(duty_cycle)

    def deinit(self):
        self.pwm.stop()
        GPIO.cleanup()


amplitude = 3.2
signal_frequency = 10
sampling_frequency = 1000


try:
    dac = PWM_DAC(
        12,
        500,
        3.290
    )

    start_time = time.time()

    while True:
        current_time = time.time() - start_time

        signal = sg.get_sin_wave_amplitude(
            signal_frequency,
            current_time
        )

        voltage = signal * amplitude

        dac.set_voltage(voltage)

        sg.wait_for_sampling_period(sampling_frequency)

finally:
    dac.deinit()
