import pyvisa as visa
import time
import random
import numpy as np
class PMDevicePM100D():
    def __init__(self, device_name = 'USB0::0x1313::0x8075::P5001126::INSTR', wl = 1064):
        print(self.__class__.__name__, 'inited!')

    def disconnect(self):
        print('Power meter is disconnect')

    def get_power(self):
        print("PM: get_power")
        power = random.randint(1, 500)/10000
        return(power)

def measure_average_power(pm_device):
    duration = 1
    aver_point = 3
    power_values = []
    for _ in range(aver_point):  
        power = pm_device.get_power()
        power_values.append(power)
        time.sleep(duration / aver_point)
    
    # Вычисляем среднее и переводим в мВт
    avg_pm_power = np.mean(power_values) * 1000 
    return round(avg_pm_power, 4)


if __name__ == "__main__":
    pm_device=PMDevicePM100D()
    current_pm_power = measure_average_power(pm_device)
    print(f'Сurrent pm power = {current_pm_power}mW')
