import matplotlib.pyplot as plt
def plot_voltage_vs_time(time_list, voltage_list, max_voltage):
  
    plt.figure(figsize=(10, 6))
    plt.plot(time_list, voltage_list, 'b-', label='U(t)', linewidth=1.5)
    plt.title('Зависимость напряжения на входе АЦП от времени', fontsize=14, fontweight='bold')
    plt.xlabel('Время, с', fontsize=12)
    plt.ylabel('Напряжение, В', fontsize=12)
    plt.ylim(0, max_voltage * 1.05)
    
    if time_list:
        plt.xlim(0, max(time_list))
        
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend(loc='upper right')
    plt.tight_layout()
    plt.show()
def plot_sampling_period_hist(time_list):

    if len(time_list) < 2:
        print("Недостаточно данных для построения гистограммы периодов дискретизации")
        return
    sampling_periods = [time_list[i] - time_list[i - 1] for i in range(1, len(time_list))]
    plt.figure(figsize=(10, 6))
    plt.hist(sampling_periods, bins=30, color='skyblue', edgecolor='black', alpha=0.75)
    plt.title('Распределение количества измерений по их продолжительности', fontsize=14, fontweight='bold')
    plt.xlabel('Период дискретизации dt, с', fontsize=12)
    plt.ylabel('Количество измерений', fontsize=12)
    plt.xlim(0, 0.06)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()