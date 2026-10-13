import RPi.GPIO as GPIO
import time
class R2R_ADC:
    def __init__(self, dynamic_range, compare_time=0.01, verbose=False):
        self.dynamic_range = dynamic_range
        self.verbose = verbose
        self.compare_time = compare_time

        self.bits_gpio = [26, 20, 19, 16, 13, 12, 25, 11]  
        self.comp_gpio = 21                                 
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.bits_gpio, GPIO.OUT, initial=0)
        GPIO.setup(self.comp_gpio, GPIO.IN)
    def deinit(self):
        try:
            GPIO.output(self.bits_gpio, 0)
            GPIO.cleanup()
        except Exception as e:
            if self.verbose:
                print(f"Ошибка при очистке GPIO: {e}")
    def __del__(self):
        self.deinit()
    def number_to_dac(self, number):

        number = max(0, min(255, int(number)))
        bits = [(number >> i) & 1 for i in range(7, -1, -1)]
        for pin, bit in zip(self.bits_gpio, bits):
            GPIO.output(pin, bit)
    def sequential_counting_adc(self):

        for number in range(256):
            self.number_to_dac(number)
            time.sleep(self.compare_time)
            comp_val = GPIO.input(self.comp_gpio)
            
            if self.verbose:
                print(f"[SC ADC] Код: {number:3d} (0b{number:08b}) | Компаратор: {comp_val}")

            if comp_val == 1:
                return number
                
        return 255
    def get_sc_voltage(self):
        code = self.sequential_counting_adc()
        return (code / 255.0) * self.dynamic_range
    def successive_approximation_adc(self):
        code = 0
        for bit in range(7, -1, -1):
            test_code = code | (1 << bit)
            self.number_to_dac(test_code)
            time.sleep(self.compare_time)
            comp_val = GPIO.input(self.comp_gpio)
            
            if self.verbose:
                print(f"[SAR ADC] Бит {bit} | Пробуем код: {test_code:3d} (0b{test_code:08b}) | Comp: {comp_val}")
            if comp_val == 0:
                code = test_code
        return code
    def get_sar_voltage(self):
        code = self.successive_approximation_adc()
        return (code / 255.0) * self.dynamic_range
if __name__ == "__main__":
    DYNAMIC_RANGE = 3.3  
    adc = None
    try:
        adc = R2R_ADC(dynamic_range=DYNAMIC_RANGE, compare_time=0.01, verbose=True)
        print("=== Запуск измерения напряжения в бесконечном цикле (Ctrl+C для остановки) ===")
        
        while True:
            voltage = adc.get_sar_voltage()
            print(f"Измеренное напряжение: {voltage:.3f} В")
            time.sleep(0.5)
            
    except KeyboardInterrupt:
        print("\nИзмерение остановлено пользователем.")
    finally:
        if adc:
            adc.deinit()
            print("Ресурсы GPIO успешно освобождены.")