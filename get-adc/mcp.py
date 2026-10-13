import time
from mcp3021_driver import MCP3021
from adc_plot import plot_voltage_vs_time

DYNAMIC_RANGE = 3.3  
DURATION = 10.0     
voltage_values = []
time_values = []
mcp = None
try:
    mcp = MCP3021(dynamic_range=DYNAMIC_RANGE)
    start_time = time.time()
    
    print(f"Запуск гейства на {DURATION} с...")
    
    while (time.time() - start_time) < DURATION:
        current_time = time.time() - start_time
        voltage = mcp.get_voltage()
        
        voltage_values.append(voltage)
        time_values.append(current_time)
        time.sleep(0.05)  
    print(f"Измерение завершено! Все опросные данные собраны: {len(voltage_values)} точек.")

    plot_voltage_vs_time(time_values, voltage_values, DYNAMIC_RANGE)
except KeyboardInterrupt:
    print("\nИзмерение прервано пользователем.")
finally:
    if mcp:
        mcp.deinit()
        print("Драйвер MCP3021 успешно закрыт.")
