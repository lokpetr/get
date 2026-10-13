import time
from r2r_adc import R2R_ADC
from adc_plot import plot_voltage_vs_time, plot_sampling_period_hist
DYNAMIC_RANGE = 3.3  
DURATION = 3.0       
voltage_values = []
time_values = []
adc = None
try:
    adc = R2R_ADC(dynamic_range=DYNAMIC_RANGE, compare_time=0.0001)
    
    start_time = time.time()
    print(f"Запуск записи напряжений АЦП последовательного счёта на {DURATION} с...")
    
    while (time.time() - start_time) < DURATION:
        current_time = time.time() - start_time
        voltage = adc.get_sc_voltage()
        
        voltage_values.append(voltage)
        time_values.append(current_time)
    print(f"Сбор данных завершён. Вы отправляетесь в алабугуугабугу {len(voltage_values)}")

    plot_voltage_vs_time(time_values, voltage_values, DYNAMIC_RANGE)
    plot_sampling_period_hist(time_values)
except KeyboardInterrupt:
    print("\nСкрипт прерван пользователем.")
finally:
    if adc:
        adc.deinit()
        print("GPIO ресурсы деинициализированы.")