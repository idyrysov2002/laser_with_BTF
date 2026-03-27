
import numpy as np
import matplotlib.pyplot as plt
import time
import os
def generate_oscilloscope_spectrum():
    """
    Генерирует случайный синусоидальный сигнал (осциллограмму). 

    Returns:
        x (np.ndarray): Ось времени/точек.
        y (np.ndarray): Значения сигнала.
    """
    # Длина сигнала
    length = 50
    x = np.arange(length)

    # Случайные параметры
    amplitude = np.random.uniform(1.0, 10.0)  # Амплитуда
    frequency = np.random.uniform(0.01, 0.15)  # Частота (циклов на точку)
    phase = np.random.uniform(0, 2 * np.pi)  # Фаза (в радианах)

    # Генерация синусоиды
    y = amplitude * np.sin(2 * np.pi * frequency * x + phase)

    return x, y

class Oscilloscope:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.sock = None
        self.connect()
        
    def connect(self):
        """Установка соединения с осциллографом"""
        print(f"Соединение установлено с {self.ip}:{self.port}")

    
    
    
    def sample_rate(self, rate):
        """Устанавливает частоту дискретизации осциллографа
        
        """
        rate=str(rate)
        return self.send_command(f"HORIZONTAL:MODE:SAMPLERATE {rate}", False)
        
    
        
    def acquire_mode(self, mode):
        """Устанавливает режим захвата сигнала."""
        print(f'acquire_mode={mode}')    
    
    def offset(self, channel, voltage):
        voltage=str(voltage)
        
        return self.send_command(f"CH{channel}:OFFSET {voltage}", False)
    
    def horizontal_scale(self, scale):
        """Устанавливает масштаб горизонтальной развертки"""
        print(f'horizontal_scale= {scale}')
    
    # def horizontal_recordlength(self, length):
    #     """Устанавливает длину записи (количество точек) для горизонтальной развертки.
    #     """
    #     # length=str(length)
    #     self.send_command("HORizontal:ACQLENGTH?", delay=0.1)
    #     return self.send_command(f"HORIZONTAL:MODE:RECORDLENGTH {length}", False)
    
    def horizontal_recordlength(self, length):
        """
        Устанавливает длину записи (количество точек) для горизонтальной развертки.
        """
        # Преобразуем в строку и отправляем команду согласно мануалу:
        # HORizontal:MODE:RECOrdlength <NR1>
        return self.send_command(f"HORizontal:MODE:RECOrdlength {int(length)}", False)
    
    def acquire_state(self, run):
        """Управляет состоянием захвата сигнала.
        
        Args:
            run (str): Команда управления. Допустимые значения:
                - 'ON'/'OFF' - включить/выключить захват
                - 'RUN' - начать захват
                - 'STOP' - остановить захват
        
        Returns:
            Ответ осциллографа или None, если read_response=False
        
        Raises:
            ValueError: Если передан недопустимый параметр
        """
        valid_states = ['ON', 'OFF', 'RUN', 'STOP']
        if run.upper() not in valid_states:
            raise ValueError(f"Invalid state. Valid states are: {', '.join(valid_states)}")
        
        return self.send_command(f"ACQUIRE:STATE {run.upper()}", False)
       
    def vertical_scale(self,channel,scale):
        channel=str(channel)
        scale=str(scale)
        
        return self.send_command(f"CH{channel}:SCALE {scale}", False) 

    def get_oscilloscope_data(self, channel):

        time_axis, voltage = generate_oscilloscope_spectrum()
        print("get_oscilloscope_data")
        return time_axis, voltage
    
    

    
    def trigger_level(self,challel,level):
        challel=str(challel)
        level=str(level)
        self.send_command("TRIGGER:A:MODE AUTO", False)  # Режим AUTO для гарантированного захвата
        self.send_command(f"TRIGGER:A:EDGE:SOURCE CH{challel}", False)
        self.send_command(f"TRIGGER:A:LEVEL {level}", False)  # Уровень триггера в 0V
        
        return

    def reset_settings(self):
       
        return  self.send_command("*RST", False)
    
    def select_channel(self, channel, state):
        """Управляет видимостью (включением/выключением) канала осциллографа.
        
        Args:
            channel (int): Номер канала (например, 1, 2, 3, 4).
            state (str): Состояние канала. Допустимые значения: 'ON' или 'OFF'.
            
        Returns:
            None: Команда отправляется без ожидания ответа от прибора.
            
        Raises:
            ValueError: Если передано недопустимое состояние.
            TypeError: Если номер канала не является целым числом.
        """
        # Проверка типа канала
        if not isinstance(channel, int) or channel < 1:
            raise TypeError("Номер канала должен быть положительным целым числом.")
        
        # Нормализация и проверка состояния
        valid_states = ['ON', 'OFF']
        state_upper = str(state).upper()
        
        if state_upper not in valid_states:
            raise ValueError(f"Недопустимое состояние '{state}'. Используйте: {', '.join(valid_states)}")
        
        # Формирование и отправка команды (например: SELECT:CH1 ON)
        return self.send_command(f"SELECT:CH{channel} {state_upper}", False)

    def trigger_mode(self,mode):
        """_summary_

        Args:
            mode (_str_): {auto|normal}


        Returns:
            _type_: _description_
        """
        return self.send_command(f"TRIGGER:A:MODE {mode}", False)
    def data_range(self,start,stop):
        self.send_command(f"DATA:START {start}", False)
        self.send_command(f"DATA:STOP {stop}", False)
        return
    def horizontal_position(self,channel,value):
        """_summary_

        Args:
            channel (_int_): выбираем канал
            value (_type_): значения от 0 до 100

        Returns:
            _type_: _description_
        """
        return self.send_command(f'REF{channel}:HORizontal:POSition {value}')

    def average_number_point(self, number):
        return self.send_command(f"ACQUIRE:NUMAVG {number}", False)

    def waiting_status(self):
        return self.send_command("*OPC?",False)
    
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

