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