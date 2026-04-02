from devices.yokogawa.Yokogawa_OSA import YokogawaOSA
import datetime
import time
from devices.btf_100.btf_100 import BTF100
from measure_libs.yokogawa_measure_lib import yoko_measurement
yoko=YokogawaOSA()
save_folder_path=r'C:\Users\namys_23hvwev\Documents\DATA\yoko_spectrum'

for x in range(100000000000):

    timestamp = datetime.datetime.now().strftime("%B-%d-%Y_time_%H-%M-%S")
    filename=f'number_{x}_{timestamp}'
    yoko_measurement(device=yoko, save_folder_path=save_folder_path, filename=filename, folder_structure='',
                    res=0.02,
                    wave_start=1510, 
                    wave_stop=1580, save_png=True)

    




 
        