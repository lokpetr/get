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