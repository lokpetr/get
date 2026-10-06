import r2r_dac as r2r
import signal_generator_triangle as sg
import time

amplitude = 3.2
signal_frequency = 10
sampling_frequency = 10000
pins = [16, 20, 21, 25, 26, 17, 27, 22]
dynamic_range = 3.3

try:
    dac = r2r.R2R_DAC(pins, dynamic_range)

    while True:
            try:
                voltage = sg.get_triangle_amplitude(signal_frequency, time.time())*amplitude
                sg.wait_for_sampling_period(sampling_frequency)
                dac.set_voltage(voltage)

            except ValueError:
                print("Выход за границы диапозона")

finally:
    dac.deinit()