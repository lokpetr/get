import pwm_dac as pwm
import signal_generator_triangle as sg
import time

amplitude = 3.2
pwm_frequency = 500
signal_frequency = 10
sampling_frequency = 1000
pin = 12
dynamic_range = 3.3

try:
    dac = pwm.PWM_DAC(pin, pwm_frequency, dynamic_range)

    while True:
            try:
                voltage = sg.get_triangle_amplitude(signal_frequency, time.time())*amplitude
                sg.wait_for_sampling_period(sampling_frequency)
                dac.set_voltage(voltage)

            except ValueError:
                print("Выход за границы диапозона")

finally:
    dac.deinit()