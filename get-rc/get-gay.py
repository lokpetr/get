import time
from mcp3021_driver import MCP3021

DYNAMIC_RANGE = 3.3   # измерьте мультиметром на контакте PWR и впишите точное значение
DURATION = 10.0       # длительность измерения, с (примерно 5·RC)
PERIOD = 0.05         # пауза между измерениями, с

voltage_values = []
time_values = []
mcp = None

try:
    mcp = MCP3021(dynamic_range=DYNAMIC_RANGE)
    start_time = time.time()
    print(f"Запуск измерения на {DURATION} с...")

    while (time.time() - start_time) < DURATION:
        current_time = time.time() - start_time
        voltage = mcp.get_voltage()

        time_values.append(current_time)
        voltage_values.append(voltage)
        time.sleep(PERIOD)

    print(f"Измерение завершено! Собрано {len(voltage_values)} точек.")

except KeyboardInterrupt:
    print("\nИзмерение прервано пользователем.")

finally:
    if mcp:
        mcp.deinit()
        print("Драйвер MCP3021 закрыт.")

# Сохранение данных (выполняется и при досрочной остановке)
if time_values:
    with open('data.csv', 'w', encoding='utf-8') as f:
        f.write('Время[с],Напряжение[В]\n')
        for t, u in zip(time_values, voltage_values):
            f.write(f'{t:.4f},{u:.4f}\n')
    print("Данные сохранены в data.csv")