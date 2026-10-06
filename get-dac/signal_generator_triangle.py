import time

def get_triangle_amplitude(freq, tm):
    return freq*abs(1/freq-2*(tm%(1/freq)))

def wait_for_sampling_period(sampling_frequency):
    time.sleep(1/sampling_frequency)
    return None