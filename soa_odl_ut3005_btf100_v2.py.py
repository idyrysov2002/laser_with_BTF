import itertools
import os
import time
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib import rcParams
from scripts.create_folder import create_date_folder
from scripts.write_arrays_to_excel import write_arrays_excel
from scripts.write_arrays_to_txt import write_arrays_txt
from scripts.create_map_and_save import create_map_and_save
from scripts.number_with_decimal_prefix import number_with_decimal_prefix
from devices.pm_400.PMDevice import PMDevicePM100D, measure_average_power
from measure_libs.oscilloscope_measure_lib import oscilloscope_measurement
from measure_libs.yokogawa_measure_lib import yoko_measurement
from pathlib import Path
import numpy as np

# импорт настроек
from config import* 
# ===================
# импорт драйверов
# ===================

from devices.yokogawa.Yokogawa_OSA import YokogawaOSA
from measure_libs.rf_measure_lib import rf_measurement
from devices.rsa_device.RF306B import RF306B
from devices.odl_650.OpticDelayLine_new import OpticDelayLine
from devices.ut_3005.VoltageDriverUT3005 import VoltageDriverUT3005
from devices.cdl_1015.CLD1015 import CLD1015
from devices.btf_100.btf_100 import BTF100
from devices.oscilloscope.tektronix_DPO71604C import Oscilloscope




# === Определение имён для папок спанов (с Hz) ===
max_span = f'span_{number_with_decimal_prefix(RF_SPAN_MAX)}Hz'
middle_span = f'span_{number_with_decimal_prefix(RF_SPAN_MIDDLE)}Hz'
min_span = f'span_{number_with_decimal_prefix(RF_SPAN_MIN)}Hz'
delay_check_points = {DELAYS[0], DELAYS[len(DELAYS) // 2], DELAYS[-1]}



def main():


    try:
        main_folder = create_date_folder(base_path="Z:/data_for_laser_with_BTF", prefix='laser_with_btf')
        # ========================
        # ИНИЦИАЛИЗАЦИЯ ПРИБОРОВ
        # ========================
        btf = BTF100(port='COM11')
        pm_device = PMDevicePM100D()
        odl = OpticDelayLine('COM10')
        odl.initialize()
        # osa = OSA_Yokogawa_new()
        rf_device = RF306B()
        LD = CLD1015()
        LD.turn_on_all()
        ut = VoltageDriverUT3005('COM8')
        ut.turn_on()
        
        osc=Oscilloscope(ip="10.2.60.150", port=4000)
        osc.trigger_level(challel=4,level=-0.050)

        yoko=YokogawaOSA()

        for wavelength in WAVELENGTH:
            # Установка длины волны
            btf.set_wavelength(wavelength)

            params = itertools.product(VOLTAGES, CURRENTS, DELAYS)

            
            
            current_voltage_batch = None
            
            voltage_prev = -1
            current_prev = -1
            delay_prev = -1
            
            pm_power_data=[]
            rf_peak_freq_max_data=[]
            rf_smsr_max_data=[]

            

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
                

                # === ИЗМЕРЕНИЯ ===
                pm_power_data.append(measure_average_power(pm_device))

                


                
                # === Каждый спан в своей папке ===
                rf_max_dict=rf_measurement(
                    rf_device=rf_device, N=NUMBER_RF_MEASURE, save_folder_path=main_folder,folder_structure=base_folder_structure,
                    filename=base_filename, rf_rbw=RF_RBW_MAX,
                    f_start=RF_F_START_MAX, f_stop=RF_F_STOP_MAX, save_png=True)

                rf_peak_freq_max=rf_max_dict["peak_freq"]
                rf_peak_power_max=rf_max_dict["peak_power"]
                rf_smsr_max=rf_max_dict['smsr']
                

                osc_dict=oscilloscope_measurement(device=osc, save_folder_path=main_folder, filename=base_filename, folder_structure=base_folder_structure, channel=4, save_png=True)
                osc_key = (OSC_MODES,OSC_HOR_SCALES)
                item = osc_dict[osc_key]
                osc_mean_freq_GHz = item['stats']['mean_GHz']
                osc_std_GHz=item['stats']['stddev_GHz']

                
                if delay in delay_check_points:
                    yoko_dict=yoko_measurement(
                    device=yoko,
                    save_folder_path=main_folder, 
                    filename=base_filename,
                    folder_structure=base_folder_structure,
                    res=YOKO_RES_BIG_SPAN,
                    wave_start=YOKO_BIG_SPAN_START,
                    wave_stop=YOKO_BIG_SPAN_STOP,
                    save_png=True)


                # === Заполнение буфера для карт ===
                map_data_buf['pm_400']['data'] = pm_power_data
                map_data_buf['pm_400']['title']=None
                map_data_buf['pm_400']['filename']='power_meter_heatmap'

                map_data_buf['rf_freq_max']['data']=rf_peak_freq_max_data
                map_data_buf['rf_freq_max']['title']=f'Voltage {voltage}V, Frequensy(Peak power), {max_span}'
                map_data_buf['rf_freq_max']['filename']=f'{max_span}_voltage_{voltage}V'
                

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