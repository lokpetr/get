import csv
import matplotlib.pyplot as plt
 
# 1. Загрузка данных из data.csv (без pandas)
t, u = [], []
with open('data.csv', encoding='utf-8') as f:
    reader = csv.reader(f)
    header = next(reader)            # строка с названиями столбцов
    for row in reader:
        if not row:
            continue                 # пропускаем пустые строки
        t.append(float(row[0]))
        u.append(float(row[1]))
 
print(f'Столбцы: {header}, точек: {len(t)}')
 
# 2. Постоянная времени τ
u0, u_end = u[0], u[-1]
if u_end > u0:   # заряд: 63 % от установившегося значения
    u_tau = u0 + 0.632 * (u_end - u0)
    i_tau = next(i for i, v in enumerate(u) if v >= u_tau)
else:            # разряд: 37 % от начального значения
    u_tau = u_end + 0.368 * (u0 - u_end)
    i_tau = next(i for i, v in enumerate(u) if v <= u_tau)
tau = t[i_tau]
print(f'τ ≈ {tau:.4g} с')
 
# 3. График
plt.figure(figsize=(8, 5))
plt.plot(t, u, label='Напряжение на конденсаторе')
plt.axvline(tau, color='gray', linestyle='--')
plt.axhline(u_tau, color='gray', linestyle='--')
plt.plot(tau, u_tau, 'ro', label=f'τ ≈ {tau:.3g} с')
 
plt.title('Зависимость напряжения на конденсаторе от времени')
plt.xlabel('Время, с')
plt.ylabel('Напряжение, В')
plt.grid(True)
plt.legend()
 
# 4. Сохранение вместо plt.show()
plt.savefig('rc-plot.png', dpi=300)
print('График сохранён в rc-plot.png')