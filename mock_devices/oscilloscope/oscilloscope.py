import socket
import numpy as np
import matplotlib.pyplot as plt
import time
from scipy.fft import fft, fftfreq
from scipy.signal import windows
import os





class Oscilloscope:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        print(self.__class__.__name__, "inited!")

    def connect(self):
        """Установка соединения с осциллографом"""
        print(f"Соединение установлено с {self.ip}:{self.port}")

    def sample_rate(self, rate):
        """Устанавливает частоту дискретизации осциллографа"""
        pass

    def ACQUIRE_MODE(self, mode):
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
        print(f"ACQUIRE_MODE - {mode}")

    def offset(self, channel, voltage):
        pass

    def HORIZONTAL_SCALE(self, scale):
        """Устанавливает масштаб горизонтальной развертки (сек/дел)"""
        print(f"HORIZONTAL_SCALE - {scale}")

    