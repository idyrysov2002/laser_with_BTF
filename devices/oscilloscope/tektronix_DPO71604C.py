import socket
import numpy as np
import matplotlib.pyplot as plt
import time
import os

class Oscilloscope:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.sock = None
        self.connect()
        
    def connect(self):
        """Установка соединения с осциллографом"""
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(1.0)
        self.sock.connect((self.ip, self.port))
        print(f"Соединение установлено с {self.ip}:{self.port}")

    def send_command(self, cmd, read_response=True, delay=0.2):
        """Отправка команды на осциллограф"""
        self.sock.sendall(f"{cmd}\n".encode())
        time.sleep(delay)
        
        if not read_response:
            return None
            
        response = b''
        while True:
            try:
                chunk = self.sock.recv(4096)
                if not chunk:
                    break
                response += chunk
                if b'\n' in response:
                    break
            except socket.timeout:
                print(f"Timeout при выполнении команды: {cmd}")
                return None
        return response.decode().strip()
    
    
    def sample_rate(self, rate):
        """Устанавливает частоту дискретизации осциллографа
        
        """
        rate=str(rate)
        return self.send_command(f"HORIZONTAL:MODE:SAMPLERATE {rate}", False)
        
    
        
    def acquire_mode(self, mode):
        """Устанавливает режим захвата сигнала.
        
        Args:
            mode (str): Режим работы. Допустимые значения:
                - 'SAMPLE' - обычный режим
                - 'PEAKDETECT' - обнаружение пиков
                - 'HIRES' - высокое разрешение
                - 'AVERAGE' - усреднение
                - 'WFMDB' - база данных сигналов
                - 'ENVELOPE' - огибающая
        
        Returns:
            Ответ осциллографа или None, если read_response=False
        """
        return self.send_command(f"ACQUIRE:MODE {mode}", False)    
    
    def offset(self, channel, voltage):
        voltage=str(voltage)
        
        return self.send_command(f"CH{channel}:OFFSET {voltage}", False)
    
    def horizontal_scale(self, scale):
        """Устанавливает масштаб горизонтальной развертки"""
        scale=str(scale)
                
        return self.send_command(f"HORIZONTAL:MAIN:SCALE {scale}", False)
    
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
        """
        Получение данных с осциллографа.
        """
        channel = str(channel)
        
        #  Настройка источника
        self.send_command(f"DATA:SOURCE CH{channel}", False)
        self.send_command("DATA:ENCDG ASCII", False)
        
        # ЗАПРОС РЕАЛЬНОЙ ДЛИНЫ ЗАПИСИ 
        rec_len_str = self.send_command("HORizontal:ACQLENGTH?", delay=0.2)
        
        if not rec_len_str:
            raise ValueError("Не удалось получить длину записи (HORizontal:ACQLENGTH?).")
        
        try:
            rec_len = int(float(rec_len_str))
            if rec_len <= 0:
                raise ValueError(f"Некорректная длина записи: {rec_len}")
        except ValueError as e:
            print(f"Warning: Ошибка парсинга длины записи, используем запасное значение 1000. Ошибка: {e}")
            rec_len = 1000

        # Установка диапазона передачи данных ПОЛНОСТЬЮ (от 1 до rec_len)
        self.send_command(f"DATA:START 1", False)
        self.send_command(f"DATA:STOP {rec_len}", False)
        
        # Получение данных
        data_str = self.send_command("CURVE?", delay=2)
        
        if not data_str:
            raise ValueError("Нет данных от осциллографа (CURVE? вернул пустоту).")
        
        # Обработка заголовка ответа
        if data_str.startswith("CURVE "):
            data_str = data_str[6:]
        
        # Парсинг данных
        y_data = np.fromstring(data_str, sep=',', dtype=float)
        
        # Проверка: совпадает ли количество полученных точек с запрошенными
        if len(y_data) != rec_len:
            print(f"Warning: Ожидалось {rec_len} точек, получено {len(y_data)}. Возможно, обрезано.")

        # Получение параметров масштабирования
        ymult_str = self.send_command("WFMOUTPRE:YMULT?", delay=0.2)
        yzero_str = self.send_command("WFMOUTPRE:YZERO?", delay=0.2)
        yoff_str = self.send_command("WFMOUTPRE:YOFF?", delay=0.2)
        xincr_str = self.send_command("WFMOUTPRE:XINCR?", delay=0.2)

        if not all([ymult_str, yzero_str, yoff_str, xincr_str]):
            raise ValueError("Не удалось получить параметры масштабирования.")

        ymult = float(ymult_str)
        yzero = float(yzero_str)
        yoff = float(yoff_str)
        xincr = float(xincr_str)
        
        # Конвертация в физические величины
        voltage = (y_data - yoff) * ymult + yzero
        
        actual_len = len(voltage)
        time_axis = np.arange(actual_len) * xincr
        
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

