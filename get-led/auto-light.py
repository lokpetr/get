import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

led = 26
GPIO.setup(led,GPIO.OUT)

photo = 6
GPIO.setup(photo,GPIO.IN)

while True:
    GPIO.output(led, not GPIO.input(photo))   
https://github.com/gatin-kirill/education_rep/tree/main/get_adc
git add .
import RPi.GPIO as GPIO
import time
class R2R_ADC:
    def __init__(self, dynamic_range, compare_time=0.01, verbose=False):
        """
        Конструктор класса 8-битного R2R АЦП.
        
        :param dynamic_range: Динамический диапазон ЦАП в Вольтах (измеряется мультиметром)
        :param compare_time: Задержка для стабилизации компаратора (с)
        :param verbose: Вывод отладочной информации
        """
        self.dynamic_range = dynamic_range
        self.verbose = verbose
        self.compare_time = compare_time
        
        # Настройка пинов GPIO
        self.bits_gpio = [26, 20, 19, 16, 13, 12, 25, 11]  # D7..D0
        self.comp_gpio = 21                                 # Выход компаратора
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.bits_gpio, GPIO.OUT, initial=0)
        GPIO.setup(self.comp_gpio, GPIO.IN)
    def deinit(self):
        """
        'Деструктор': выставляет 0 на выход ЦАП и очищает настройки GPIO
        """
        try:
            GPIO.output(self.bits_gpio, 0)
            GPIO.cleanup()
        except Exception as e:
            if self.verbose:
                print(f"Ошибка при очистке GPIO: {e}")
    def __del__(self):
        self.deinit()
    def number_to_dac(self, number):
        """
        Подаёт 8-битное целое число на параллельный вход R2R ЦАП.
        Пины bits_gpio: [26, 20, 19, 16, 13, 12, 25, 11]
        26 — старший разряд (D7), 11 — младший разряд (D0)
        """
        number = max(0, min(255, int(number)))
        # Преобразование числа в список битов (D7 .. D0)
        bits = [(number >> i) & 1 for i in range(7, -1, -1)]
        
        # Запись логических уровней на соответствующе пины GPIO
        for pin, bit in zip(self.bits_gpio, bits):
            GPIO.output(pin, bit)
    def sequential_counting_adc(self):
        """
        Метод АЦП последовательного счёта (Sequential Counting ADC).
        1. Последовательно подаёт на вход ЦАП целые числа от 0 до 255.
        2. Делает паузу compare_time для работы компаратора.
        3. Считывает сигнал с выходя компаратора (comp_gpio).
        4. Если U_dac >= U_in, возвращает текущее число.
        """
        for number in range(256):
            self.number_to_dac(number)
            time.sleep(self.compare_time)
            comp_val = GPIO.input(self.comp_gpio)
            
            if self.verbose:
                print(f"[SC ADC] Код: {number:3d} (0b{number:08b}) | Компаратор: {comp_val}")
                
            # Если компаратор сработал (U_dac > U_in)
            if comp_val == 1:
                return number
                
        return 255
    def get_sc_voltage(self):
        """
        Возвращает измеренное напряжение в Вольтах методом последовательного счёта
        """
        code = self.sequential_counting_adc()
        return (code / 255.0) * self.dynamic_range
    def successive_approximation_adc(self):
        """
        Метод АЦП последовательного приближения (SAR ADC / Бинарный поиск).
        1. Проверяет каждый бит от старшего (D7) к младшему (D0).
        2. Устанавливает бит в 1 и проверяет компаратор.
        3. Если U_dac > U_in, сбрасывает бит в 0, иначе оставляет 1.
        """
        code = 0
        for bit in range(7, -1, -1):
            test_code = code | (1 << bit)
            self.number_to_dac(test_code)
            time.sleep(self.compare_time)
            comp_val = GPIO.input(self.comp_gpio)
            
            if self.verbose:
                print(f"[SAR ADC] Бит {bit} | Пробуем код: {test_code:3d} (0b{test_code:08b}) | Comp: {comp_val}")
                
            # Если U_dac <= U_in, то comp_val == 0 — оставляем 1 в бите
            if comp_val == 0:
                code = test_code
            # Если comp_val == 1 (U_dac > U_in), бит не фиксируем (остается 0)
            
        return code
    def get_sar_voltage(self):
        """
        Возвращает измеренное напряжение в Вольтах методом бинарного поиска (SAR)
        """
        code = self.successive_approximation_adc()
        return (code / 255.0) * self.dynamic_range
# Основной охранник (Main Guard)
if __name__ == "__main__":
    DYNAMIC_RANGE = 3.3  # Измеренный мультиметром динамический диапазон ЦАП (В)
    adc = None
    try:
        # Создание объекта класса R2R_ADC
        adc = R2R_ADC(dynamic_range=DYNAMIC_RANGE, compare_time=0.01, verbose=True)
        print("=== Запуск измерения напряжения в бесконечном цикле (Ctrl+C для остановки) ===")
        
        while True:
            # Чтение напряжения методом последовательного счёта или бинарного поиска
            voltage = adc.get_sar_voltage()
            print(f"Измеренное напряжение: {voltage:.3f} В")
            time.sleep(0.5)
            
    except KeyboardInterrupt:
        print("\nИзмерение остановлено пользователем.")
    finally:
        if adc:
            adc.deinit()
            print("Ресурсы GPIO успешно освобождены.")
import time
from r2r_adc import R2R_ADC
from adc_plot import plot_voltage_vs_time, plot_sampling_period_hist
# Константы эксперимента
DYNAMIC_RANGE = 3.3  # Измеренный динамический диапазон ЦАП (В)
DURATION = 3.0       # Продолжительность измерений (секунды)
voltage_values = []
time_values = []
adc = None
try:
    # Создаём объект класса R2R_ADC с малым временем стабилизации компаратора
    adc = R2R_ADC(dynamic_range=DYNAMIC_RANGE, compare_time=0.0001)
    
    start_time = time.time()
    print(f"Запуск записи напряжений АЦП последовательного счёта на {DURATION} с...")
    
    while (time.time() - start_time) < DURATION:
        current_time = time.time() - start_time
        voltage = adc.get_sc_voltage()
        
        voltage_values.append(voltage)
        time_values.append(current_time)
    print(f"Сбор данных завершён. Выполнено измерений: {len(voltage_values)}")
    
    # Визуализация 1: Зависимость напряжения от времени
    plot_voltage_vs_time(time_values, voltage_values, DYNAMIC_RANGE)
    
    # Визуализация 2: Гистограмма периодов дискретизации
    plot_sampling_period_hist(time_values)
except KeyboardInterrupt:
    print("\nСкрипт прерван пользователем.")
finally:
    if adc:
        adc.deinit()
        print("GPIO ресурсы деинициализированы.")
import time
from r2r_adc import R2R_ADC
from adc_plot import plot_voltage_vs_time
# Константы эксперимента
DYNAMIC_RANGE = 3.3  # Измеренный динамический диапазон ЦАП (В)
DURATION = 3.0       # Продолжительность измерений (секунды)
voltage_values = []
time_values = []
adc = None
try:
    # Создаём объект класса R2R_ADC
    adc = R2R_ADC(dynamic_range=DYNAMIC_RANGE, compare_time=0.0001)
    
    start_time = time.time()
    print(f"Запуск записи АЦП последовательного приближения (SAR) на {DURATION} с...")
    
    while (time.time() - start_time) < DURATION:
        current_time = time.time() - start_time
        voltage = adc.get_sar_voltage()
        
        voltage_values.append(voltage)
        time_values.append(current_time)
    print(f"Сбор данных завершён. Выполнено измерений: {len(voltage_values)}")
    
    # Визуализация графика зависимости напряжения от времени
    plot_voltage_vs_time(time_values, voltage_values, DYNAMIC_RANGE)
except KeyboardInterrupt:
    print("\nСкрипт прерван пользователем.")
finally:
    if adc:
        adc.deinit()
        print("GPIO ресурсы деинициализированы.")
import smbus
import time
class MCP3021:
    def __init__(self, dynamic_range, verbose=False):
        """
        Конструктор класса драйвера I2C АЦП MCP3021.
        
        :param dynamic_range: Измеренное напряжение питания АЦП на контакте PWR (В)
        :param verbose: Вывод отладочных сообщений по шине I2C
        """
        self.bus = smbus.SMBus(1)
        self.dynamic_range = dynamic_range
        self.address = 0x4D
        self.verbose = verbose
    def deinit(self):
        """
        'Деструктор': освобождает шину I2C
        """
        try:
            self.bus.close()
        except Exception:
            pass
    def __del__(self):
        self.deinit()
    def get_number(self):
        """
        Считывает 10-битное целое число из микросхемы MCP3021.
        
        Байты по I2C приходят в формате:
        - Старший байт содержит первые старшие биты
        - Младший байт содержит младшие биты
        Число собирается: (upper_data_byte << 6) | (lower_data_byte >> 2)
        """
        data = self.bus.read_word_data(self.address, 0)
        lower_data_byte = data >> 8
        upper_data_byte = data & 0xFF
        
        number = (upper_data_byte << 6) | (lower_data_byte >> 2)
        
        if self.verbose:
            print(f"Принятые данные: {data}, Старший байт: 0x{upper_data_byte:02X}, "
                  f"Младший байт: 0x{lower_data_byte:02X}, Число (10-bit): {number}")
            
        return number
    def get_voltage(self):
        """
        Возвращает измеренное микросхемой MCP3021 напряжение в Вольтах
        на основе 10-битного разрешения (0..1023) и динамического диапазона.
        """
        number = self.get_number()
        return (number / 1023.0) * self.dynamic_range
# Основной охранник (Main Guard)
if __name__ == "__main__":
    # Динамический диапазон измеряется мультиметром на контакте PWR блока AUX (~3.3В или ~5.0В)
    DYNAMIC_RANGE = 3.3
    mcp = None
    try:
        mcp = MCP3021(dynamic_range=DYNAMIC_RANGE, verbose=True)
        print("=== Чтение микросхемы MCP3021 по шине I2C (Ctrl+C для выхода) ===")
        
        while True:
            voltage = mcp.get_voltage()
            print(f"Напряжение на MCP3021: {voltage:.3f} В")
            time.sleep(1.0)
            
    except KeyboardInterrupt:
        print("\nОстановлено пользователем.")
    finally:
        if mcp:
            mcp.deinit()
            print("Шина I2C закрыта.")
import time
from mcp3021_driver import MCP3021
from adc_plot import plot_voltage_vs_time
# Параметры эксперимента
DYNAMIC_RANGE = 3.3  # Измеренное напряжение на контакте PWR блока AUX
DURATION = 10.0      # Продолжительность эксперимента (секунды)
voltage_values = []
time_values = []
mcp = None
try:
    mcp = MCP3021(dynamic_range=DYNAMIC_RANGE)
    start_time = time.time()
    
    print(f"Запуск записи показаний MCP3021 на {DURATION} с...")
    print("Инструкция:")
    print(" - Терморезистор: прижмите палец в середине эксперимента")
    print(" - Фоторезистор: подносите/относите фонарик телефона")
    
    while (time.time() - start_time) < DURATION:
        current_time = time.time() - start_time
        voltage = mcp.get_voltage()
        
        voltage_values.append(voltage)
        time_values.append(current_time)
        time.sleep(0.05)  # Небольшая пауза между опросами I2C
    print(f"Измерение завершено! Все опросные данные собраны: {len(voltage_values)} точек.")
    
    # Визуализация графика зависимости напряжения от времени
    plot_voltage_vs_time(time_values, voltage_values, DYNAMIC_RANGE)
except KeyboardInterrupt:
    print("\nИзмерение прервано пользователем.")
finally:
    if mcp:
        mcp.deinit()
        print("Драйвер MCP3021 успешно закрыт.")
