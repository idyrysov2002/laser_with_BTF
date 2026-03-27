import serial
import time
import re

class OpticDelayLine:
    def __init__(self, serial_port='COM6'):
        print(f'Optic Delay Line connected (Port: {serial_port})')

    def initialize(self):
        print(f'Optic Delay Line initalized')

    def set_time_delay(self, time_delay):
        print(f'set_time_delay {time_delay}')
    def disconnect(self):
        print("ODL: disconnect")


# Пример использования
if __name__=='__main__':
    # Создаем объект прибора
    odl = OpticDelayLine(serial_port="COM6")

    # Инициализация
    odl.initialize()

    # Установить время задержки
    set_delay_time=100
    odl.set_time_delay(time_delay=set_delay_time)


    # Закрыть соединение
    # odl.disconnect()
