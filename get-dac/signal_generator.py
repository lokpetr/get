import numpy as np
import time
def get_sin_wave_amplitude(freq, time):
    return (np.sin(2 * np.pi * freq * time) + 1)
def wait_for_sampling_period(sampling_frequency):
    time.sleep(1 / sampling_frequency)