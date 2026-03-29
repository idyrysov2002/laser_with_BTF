
import itertools
import os
import time
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib import rcParams
from scripts.create_folder import create_date_folder
from pathlib import Path


from measure_libs.oscilloscope_measure_lib import oscilloscope_measurement
from measure_libs.yokogawa_measure_lib import yoko_measurement
from measure_libs.rf_measure_lib import rf_measurement


# импорт настроек
from config import*
# ===================
# импорт драйверов
# ===================
from devices.pm_400.PMDevice import PMDevicePM100D
from devices.yokogawa.Yokogawa_OSA import YokogawaOSA
from devices.rsa_device.RF306B import RF306B
from devices.odl_650.OpticDelayLine_new import OpticDelayLine
from devices.ut_3005.VoltageDriverUT3005 import VoltageDriverUT3005
from devices.cdl_1015.CLD1015 import CLD1015
from devices.btf_100.btf_100 import BTF100
from devices.oscilloscope.tektronix_DPO71604C import Oscilloscope




def main():


    try:
        main_folder = create_date_folder(base_path="Z:/data_for_laser_with_BTF", prefix='laser_with_btf')
        # ========================
        # ИНИЦИАЛИЗАЦИЯ ПРИБОРОВ
        # ========================
        btf = BTF100(port='COM11')
        odl = OpticDelayLine('COM10')
        odl.initialize()
        rf_device = RF306B()
        LD = CLD1015()
        LD.turn_on_all()
        ut = VoltageDriverUT3005('COM8')
        ut.turn_on()
        
        osc=Oscilloscope(ip="10.2.60.150", port=4000)
        osc.trigger_level(challel=4,level=-0.050)
        osc.horizontal_recordlength(5000)
        osc.vertical_scale(channel=4,scale=0.02)


        yoko=YokogawaOSA()

        for wavelength in WAVELENGTH:
            # Установка длины волны
            btf.set_wavelength(wavelength)

            params = itertools.product(VOLTAGES, CURRENTS, DELAYS)

            
            
            voltage_prev = -1
            current_prev = -1
            delay_prev = -1
            
            
            

            for idx, (voltage, current, delay) in enumerate(params, 1):

                base_folder_structure=f"wavelength_{wavelength}nm/voltage_{voltage}V/current_{current}mA"
                base_filename=f'delay_{delay}ps_current_{current}mA_voltage_{voltage}V_wavelength_{wavelength}nm' 

                
                # === НАСТРОЙКА ОБОРУДОВАНИЯ ===
                
                voltage_next = voltage
                if voltage_prev != voltage_next:
                    ut.set_voltage(voltage=voltage)
                    voltage_prev = voltage_next
                
                current_next = current
                if current_prev != current_next:
                    LD.set_current(current=current)
                    current_prev = current_next
                
                delay_next = delay
                if delay_prev != delay_next:
                    odl.set_time_delay(time_delay=delay)
                    delay_prev = delay_next
                
                time.sleep(3)
                

                # === Каждый спан в своей папке ===
                rf_max_dict=rf_measurement(
                    rf_device=rf_device, N=NUMBER_RF_MEASURE, save_folder_path=main_folder,folder_structure=base_folder_structure,
                    filename=base_filename, rf_rbw=RF_RBW_MAX,
                    f_start=RF_F_START_MAX, f_stop=RF_F_STOP_MAX, save_png=True)

                
                

                osc_dict=oscilloscope_measurement(device=osc, save_folder_path=main_folder, filename=base_filename, folder_structure=base_folder_structure, channel=4, save_png=True)
                
    
                yoko_dict=yoko_measurement(
                    device=yoko,
                    save_folder_path=main_folder, 
                    filename=base_filename,
                    folder_structure=base_folder_structure,
                    res=YOKO_RES_BIG_SPAN,
                    wave_start=YOKO_BIG_SPAN_START,
                    wave_stop=YOKO_BIG_SPAN_STOP,
                    save_png=True)


            
          
    finally:
        try:
            osc.disconnect()
            odl.disconnect()
            LD.turn_off_all()
            ut.turn_off_and_close_COM()
            btf.disconnect()
        except Exception as e:
            print(f"Ошибка при отключении: {e}")

        

if __name__ == "__main__":
    main()