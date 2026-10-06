import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

led = 26
GPIO.setup(led,GPIO.OUT)

photo = 6
GPIO.setup(photo,GPIO.IN)

while True:
    GPIO.output(led, not GPIO.input(photo))   
import RPi.GPIO as GPIO

class R2R_DAC:
    def __init__(self, pins, dynamic_range, verbose = False):
        self.pins = pins
        self.dynamic_range = dynamic_range
        self.verbose = verbose
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pins, GPIO.OUT, initial = 0)

    def deinit(self):
        GPIO.output(self.pins, 0)
        GPIO.cleanup()

    def set_number(self, number):
        if number>2**len(self.pins)-1:
            print("Число вышло за допустимый диапозон")
            return 0

        for pin in self.pins:
            GPIO.output(pin, 0)
        
        bin_num = ''
        while number != 0:
            bin_num=str(number%2)+bin_num
            number = number//2

        for i in range(len(bin_num)):
            GPIO.output(self.pins[8-len(bin_num)+i], int(bin_num[i]))
        
        return 0

    def set_voltage(self, voltage):
        if not (0.0 <= voltage <= self.dynamic_range):
            print(f"Напряжение выходит за динамический диапозон ЦАП (0.00 - {dynamic_range:.2f} В")
            print("Устанавливаем 0.0 В")
            return 0
    
        number = int(voltage/self.dynamic_range * 255)

        if number>2**len(self.pins)-1:
            print("Число вышло за допустимый диапозон")
            return 0

        '''
        for pin in self.pins:
            GPIO.output(pin, 0)
        
        '''
        bin_num = ''
        while number != 0:
            bin_num=str(number%2)+bin_num
            number = number//2

        if len(bin_num)<8:
            bin_num = '0'*(8-len(bin_num))+bin_num

        for i in range(len(bin_num)):
            GPIO.output(self.pins[8-len(bin_num)+i], int(bin_num[i]))
        
        return 0
        

if __name__ == "__main__":
    try:
        dac = R2R_DAC([16, 20, 21, 25, 26, 17, 27, 22], 3.183, True)

        while True:
            try:
                voltage = float(input("Введите напряжение в Вольтах: "))
                dac.set_voltage(voltage)

            except ValueError:
                print("Вы ввели не число. Попробуйте ещё раз\n")

    finally:
        dac.deinit()
import time

def get_triangle_amplitude(freq, tm):
    return freq*abs(1/freq-2*(tm%(1/freq)))

def wait_for_sampling_period(sampling_frequency):
    time.sleep(1/sampling_frequency)
    return None
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
import pwm_dac as pwm
import signal_generator as sg
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
                voltage = sg.get_sin_wave_amplitude(signal_frequency, time.time())*amplitude
                sg.wait_for_sampling_period(sampling_frequency)
                dac.set_voltage(voltage)

            except ValueError:
                print("Выход за границы диапозона")

finally:
    dac.deinit()
import smbus

class MCP4725:
    def __init__(self, dynamic_range, address=0x61, verbose = True):
        self.bus = smbus.SMBus(1)

        self.address = address
        self.wm = 0x00
        self.pds = 0x00

        self.verbose = verbose
        self.dynamic_range = dynamic_range

    def deinit(self):
        self.bus.close()


    def set_number(self, number):
        if not isinstance(number, int):
            print("На вход ЦАП можно подавать только целые числа")

        if not (0 <= number <= 4095):
            print("Число выходит за разрядность MCP4752 (12 бит)")

        first_byte = self.wm | self.pds | number >> 8
        second_byte = number & 0xFF
        self.bus.write_byte_data(0x61, first_byte, second_byte)

        if self.verbose:
            print(f"Число: {number}, отправленное по I2C данные: [0x{(self.address << 1):02X}, 0x{first_byte:02X}, 0x{second_byte:02X}]\n")

    def set_voltage(self, voltage):
        number = int(voltage/self.dynamic_range*4095)
        self.set_number(number)

if __name__ == "__main__":
        try:
            mcp = MCP4725(5.00)

            while True:
                try:
                    voltage = float(input("Введите напряжение в Вольтах: "))
                    mcp.set_voltage(voltage)

                except ValueError:
                    print("Вы ввели не число. Попробуйте ещё раз\n")

        finally:
            mcp.deinit()
import mcp4725_driver as mcp4725
import signal_generator as sg
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
                voltage = sg.get_sin_wave_amplitude(signal_frequency, time.time())*amplitude
                sg.wait_for_sampling_period(sampling_frequency)
                dac.set_voltage(voltage)

            except ValueError:
                print("Выход за границы диапозона")

finally:
    dac.deinit()
import RPi.GPIO as GPIO

class PWM_DAC:
    def __init__(self, pin, pwn_frequency, dynamic_range, verbose = False):
        self.pin = pin
        self.pwn_frequency = pwn_frequency
        self.dynamic_range = dynamic_range
        self.verbose = verbose
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)

        global pwm
        pwm = GPIO.PWM(self.pin, self.pwn_frequency)

    def deinit(self):
        GPIO.output(self.pin, 0)
        GPIO.cleanup()
        pwm.stop()

    def set_voltage(self, voltage):
        if not (0.0 <= voltage <= self.dynamic_range):
            print(f"Напряжение выходит за динамический диапозон ЦАП (0.00 - {self.dynamic_range:.2f} В)")
        else:
            k = voltage/self.dynamic_range * 100
            pwm.start(k)
            #print(f"Стартовал ШИМ со скважностью {k} на пине {self.pin}  с частотой {self.pwn_frequency}")

        return None

if __name__ == "__main__":
    try:
        dac = PWM_DAC(12, 500, 3.290, True)

        while True:
            try:
                voltage = float(input("Введите напряжение в Вольтах: "))
                dac.set_voltage(voltage)

            except ValueError:
                print("Вы ввели не число. Попробуйте ещё раз\n")

    finally:
        dac.deinit()
