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
    
