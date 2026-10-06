import mcp4725_driver as mcp4725
import signal_generator_triangle as sg
import time

amplitude = 2
signal_frequency = 10
sampling_frequency = 1000
pins = [16, 20, 21, 25, 26, 17, 27, 22]
dynamic_range = 3.3

try:
    dac = mcp4725.MCP4725(dynamic_range)

    while True:
            try:
                voltage = sg.get_triangle_amplitude(signal_frequency, time.time())*amplitude
                sg.wait_for_sampling_period(sampling_frequency)
                dac.set_voltage(voltage)

            except ValueError:
                print("Выход за границы диапозона")

finally:
    dac.deinit()