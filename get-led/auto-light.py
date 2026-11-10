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

    plt.xlim(0, 0.06)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()
git config --global credential.helper store
git clone https://github.com/lokpetr/get.git
import time
import RPi.GPIO as GPIO
from r2r_adc import R2R_ADC   # ваш класс АЦП, сохранённый в файле r2r_adc.py рядом
 
# ===== Настройки =====
DYNAMIC_RANGE = 3.3   # диапазон АЦП, В
COMPARE_TIME = 0.0005 # пауза на сравнение; 0.01 слишком медленно (8 бит × 0.01 = 80 мс на точку)
CHARGE_PIN = 17       # пин, через который заряжается RC-цепочка; None — если заряжаете вручную
DURATION = 10.0       # длительность измерения, с (должна быть в несколько раз больше RC)
 
adc = R2R_ADC(dynamic_range=DYNAMIC_RANGE, compare_time=COMPARE_TIME)
 
if CHARGE_PIN is not None:
    GPIO.setup(CHARGE_PIN, GPIO.OUT, initial=GPIO.LOW)
 
times, voltages = [], []
 
try:
    if CHARGE_PIN is not None:
        print('Разряжаю конденсатор...')
        GPIO.output(CHARGE_PIN, GPIO.LOW)
        time.sleep(3)
        GPIO.output(CHARGE_PIN, GPIO.HIGH)   # начинаем заряд
    else:
        input('Подайте напряжение на RC-цепочку и сразу нажмите Enter...')
 
    print('Идёт измерение...')
    start = time.time()
    while time.time() - start < DURATION:
        u = adc.get_sar_voltage()
        times.append(time.time() - start)
        voltages.append(u)
 
except KeyboardInterrupt:
    print('Измерение остановлено досрочно.')
 
finally:
    if CHARGE_PIN is not None:
        GPIO.output(CHARGE_PIN, GPIO.LOW)
    adc.deinit()
 
# ===== Сохранение в файл =====
with open('data.csv', 'w', encoding='utf-8') as f:
    f.write('Время[с],Напряжение[В]\n')
    for t, u in zip(times, voltages):
        f.write(f'{t:.4f},{u:.4f}\n')
 
print(f'Сохранено {len(times)} точек в data.csv')
