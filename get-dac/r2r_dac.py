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