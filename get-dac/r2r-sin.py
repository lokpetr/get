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
            GPIO.output(self.gpio_bits[7-i], bit)

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