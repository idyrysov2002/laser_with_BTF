from measure_libs.yokogawa_measure_lib import yoko_measurement
from devices.yokogawa.Yokogawa_OSA import YokogawaOSA
from devices.cdl_1015.CLD1015 import CLD1015
from devices.btf_100.btf_100 import BTF100
from scripts.create_folder import create_date_folder 
yoko=YokogawaOSA()

yoko_measurement(
                device=yoko, 
                save_folder_path=r'C:\Users\nsuln\Documents\Laser_with_BTF', 
                filename='', 
                folder_structure='bicolor_laser_PM_coupler_test_B21043779_port1-port3',
            save_png=True)

