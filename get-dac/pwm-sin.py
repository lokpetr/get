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