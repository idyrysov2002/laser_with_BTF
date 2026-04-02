import socket
import numpy as np
import matplotlib.pyplot as plt
import time
import os


class Oscilloscope:
    def __init__(self, ip, port):
        print(f'Oscilloscope подключен, IP={ip}, port={port}')
        
    def generate_osc_data():
        # Параметры
        n_points = 1000
        duration_ns = 10.0  # Длительность 10 нс, как на ваших графиках
        
        # Случайная частота от 1 до 6 ГГц
        freq_hz = np.random.uniform(1e9, 6e9)
        
        # Случайная фаза от 0 до 2*pi
        phase_rad = np.random.uniform(0, 2 * np.pi)
        
        # Массив времени (в секундах для расчета, но отображать будем в нс)
        time_arr = np.linspace(0, duration_ns * 1e-9, n_points)
        
        # Генерация синуса
        voltage_arr = np.sin(2 * np.pi * freq_hz * time_arr + phase_rad)
        
        return time_arr, voltage_arr
        
        
    def disconnect(self):
        print("Разрыв соединения с осциллографом")
        
    def sample_rate(self, rate):
        print(f'sample_rate_{rate}')
        
    
    def acquire_mode(self, mode):
       print(f'acquire_mode_{mode}')   
    
    def offset(self, channel, voltage):
        print(f"offset_channel_{channel}_voltage{voltage}V")
    
    def horizontal_scale(self, scale):
        print(f'horizontal_scale_{scale}V')
    
    def horizontal_recordlength(self, length):
        print(f"horizontal_recordlength_{length}")
        
    
    def acquire_state(self, run):
        print(f"acquire_state_{run}")
       
    def vertical_scale(self,channel,scale):
        print(f'vertical_scale_channel_{channel}_scale_{scale}')
         

    def get_oscilloscope_data(self, channel):
        time_axis, voltage=self.generate_osc_data()
        return time_axis, voltage

    
    def trigger_level(self,challel,level):
        print(f'trigger_level_challel_{challel}_level_{level}')

    def reset_settings(self):
        print('reset_settings')
       
        
    
    def select_channel(self, channel, state):
        print(f'select_channel_{channel}_state_{state}')
        

    def trigger_mode(self,mode):
       print(f"trigger_mode_{mode}")

    def data_range(self,start,stop):
        pass
    def horizontal_position(self,channel,value):
        pass

    def average_number_point(self, number):
        pass

    def waiting_status(self):
        pass
    
    def measure_freq_stats(self, channel):
        """
        Имитирует измерение частоты со статистикой для тестирования.
        Возвращает случайные данные в диапазоне 1-6 ГГц и фиксированный счетчик 50.
        
        Args:
            channel (int): Номер канала (1-4) - используется только для логирования, если нужно
        
        Returns:
            dict: Словарь со сгенерированной статистикой
        """
        
        # Диапазон частот 1-6 ГГц (в Герцах для внутренних расчетов)
        f_min = 1e9
        f_max = 6e9
        
        # Генерируем случайные значения для статистики в этом диапазоне
        # Создаем виртуальный набор из 50 измерений для корректного расчета mean/std/min/max
        virtual_measurements = np.random.uniform(f_min, f_max, 50)
        
        value = np.random.uniform(f_min, f_max)       # Текущее значение (случайное)
        mean_val = np.mean(virtual_measurements)      # Среднее
        min_val = np.min(virtual_measurements)        # Минимум
        max_val = np.max(virtual_measurements)        # Максимум
        stddev_val = np.std(virtual_measurements)     # Стандартное отклонение
        count = 50                                    # Фиксированное число измерений
        
        return {
            'value_GHz': value / 1e9,
            'mean_GHz': mean_val / 1e9,
            'min_GHz': min_val / 1e9,
            'max_GHz': max_val / 1e9,
            'std_GHz': stddev_val / 1e9,
            'count': float(count)
        }
                
if __name__=="__main__":

    # Настройки
    osciloscope_IP = "10.2.60.150"
    osciloscope_PORT = 4000
    osciloscope_channel = 4 # Измените на нужный канал
    offset=0
    ver_scale=0.02
    trigger_level=-0.055
    LENGTH=5000



    
    
    # Инициализация соединения
    osc = Oscilloscope(osciloscope_IP, osciloscope_PORT)

    x,y=osc.get_oscilloscope_data(osciloscope_channel)

    plt.plot(x,y)
    plt.show()

