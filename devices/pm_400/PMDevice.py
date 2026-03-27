import pyvisa as visa
import time
import numpy as np
class PMDevicePM100D():
    def __init__(self, device_name = 'USB0::0x1313::0x8075::P5001126::INSTR', wl = 1064):
        self.rm = visa.ResourceManager()
        try:
            self.pm = self.rm.open_resource(device_name)
            print(self.__class__.__name__, 'inited!')
            self.pm.write('CORR:WAV {}'.format(wl))
        except Exception as e:
            print(e)
            print('No dece found. Devices registered in the system:')
            self.rm.list_resources()
            exit(0)


    def disconnect(self):
        """ Отключить соединение"""
        self.pm.control_ren(False)
        self.pm.close()
        self.rm.close()
        print('Power meter is disconnect')

    def get_power(self):
        power = float(self.pm.query('measure:power?'))
        time.sleep(0.1)
        return(power)

    def set_wl(self, wl = 1070):
        self.pm.write('CORR:WAV {}'.format(wl))
        return wl
    
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
    print('Сurrent pm power =',current_pm_power,'mW')