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


# импорт настроек
from config import NANO, OSC_MODE,STABILIZATION_TIME,OSC_VER_SCALE,OSC_CHANNEL
from config import RF_SPAN_MAX,RF_SPAN_MID,RF_SPAN_MIN
from config import LINEWIDTH, WAVELENGTH, CURRENTS, DELAYS
from config import NUMBER_RF_MEASURE
from config import RF_F_START_MAX,RF_F_STOP_MAX
from config import RF_RBW_MAX, RF_RBW_MID, RF_RBW_MIN, RF_LEVEL


# ===================
# импорт драйверов
# ===================

from devices.yokogawa.Yokogawa_OSA import YokogawaOSA
from measure_libs.rf_measure_lib import rf_measurement
from devices.rsa_device.RF306B import RF306B
from devices.odl_650.OpticDelayLine_new import OpticDelayLine
from devices.cdl_1015.CLD1015 import CLD1015
from devices.btf_100.btf_100 import BTF100
from devices.oscilloscope.tektronix_DPO71604C import Oscilloscope
from measure_libs.yokogawa_measure_lib import yoko_measurement



# === Определение имён для папок спанов (с Hz) ===
max_span = f'6000MHz'
mid_span = f'100MHz'
min_span = f'1MHz'



def build_maps(linewidth, wavelength, folder_structure, data_buf):
    """Внутренняя функция тепловых карт для заданного напряжения."""
    
    
    
    # Папка для карт этого напряжения
    folder_path = Path(folder_structure)
    if not folder_path.exists():
        folder_path.mkdir(parents=True, exist_ok=True)
    
    # Данные для осей
    x = np.array(data_buf['current'])
    y = np.array(data_buf['delay'])
    
    # === Конфигурация карт ===
    maps_config = [
        ('pm_400', f'pm400_wavelength_{wavelength}nm_linewidth_{linewidth}nm', 'Power, mW', ''),
        (np.array(data_buf['rf_peak_freq_max']) / 1e+9, f'rf_peak_freq_{max_span}_wavelength_{wavelength}nm_linewidth_{linewidth}nm', 'Frequency, GHz', max_span),
        (np.array(data_buf['rf_peak_freq_mid']) / 1e+9, f'rf_peak_freq_{mid_span}_wavelength_{wavelength}nm_linewidth_{linewidth}nm', 'Frequency, GHz', mid_span),
        (np.array(data_buf['rf_peak_freq_min']) / 1e+9, f'rf_peak_freq_{min_span}_wavelength_{wavelength}nm_linewidth_{linewidth}nm', 'Frequency, GHz', min_span),
        ('osc_mean_freq', f'osc_mean_freq_wavelength_{wavelength}nm_linewidth_{linewidth}nm', 'Frequency, GHz', ''),
    ]
    
    for z_raw, fname_suffix, z_label, span_label in maps_config:
        # Обработка PM400
        if z_raw == 'pm_400':
            z = np.array(data_buf['pm_400'])
            create_map_and_save(
                x_arr=[x.tolist(), "Current, mA"],
                y_arr=[y.tolist(), "Delay, ps"],
                z_arr=[z.tolist(), z_label],
                title=f"PM400: LW={linewidth}nm, WL={wavelength}nm",
                folder_path=folder_path,
                filename=f"{fname_suffix}",
                show_plot=False
            )
            continue
        
        # Обработка осциллографа
        if z_raw == 'osc_mean_freq':
            z = np.array(data_buf['osc_mean_freq'])
            create_map_and_save(
                x_arr=[x.tolist(), "Current, mA"],
                y_arr=[y.tolist(), "Delay, ps"],
                z_arr=[z.tolist(), z_label],
                title=f"OSC: LW={linewidth}nm, WL={wavelength}nm",
                folder_path=folder_path,
                filename=f"{fname_suffix}",
                show_plot=False
            )
            continue
        
        # Обычные числовые данные
        z = np.array(z_raw)
        create_map_and_save(
            x_arr=[x.tolist(), "Current, mA"],
            y_arr=[y.tolist(), "Delay, ps"],
            z_arr=[z.tolist(), z_label],
            title=f"RF: LW={linewidth}nm, WL={wavelength}nm, span={span_label}",
            folder_path=folder_path,
            filename=f"{fname_suffix}",
            show_plot=False
        )


def main():


    try:
        
        # ========================
        # ИНИЦИАЛИЗАЦИЯ ПРИБОРОВ
        # ========================
        # ========================
        btf = BTF100(port='COM11')
        pm_device = PMDevicePM100D()
        odl = OpticDelayLine('COM10')
        odl.initialize()
        rf_device = RF306B()
        LD = CLD1015()
        LD.turn_on_all()
        
        osc=Oscilloscope(ip="10.2.60.150", port=4000)
        # Установливаем режим (например, sample, average)
        osc.acquire_mode(mode=OSC_MODE)
        osc.vertical_scale(channel=OSC_CHANNEL,scale=OSC_VER_SCALE)

        # yoko=YokogawaOSA(write_TR='C')

        

        params = itertools.product(LINEWIDTH, WAVELENGTH, CURRENTS, DELAYS)

        # === Буфер для сбора данных ===
        collected_data = {
            'current': [], 'delay': [],
            'pm_400': [],
            'rf_peak_freq_max': [], 
            'rf_peak_freq_mid': [], 
            'rf_peak_freq_min': [],
            'osc_mean_freq':[],
        }
    
        
        
        current_prev = None
        delay_prev = None
        linewidth_prev = None
        wavelength_prev = None
    
        data_prefix='laser_BTF'
        main_folder = create_date_folder(base_path="Z:/data_for_laser_with_BTF", prefix=data_prefix)
        for idx, (linewidth, wavelength,current, delay) in enumerate(params, 1):
            
            base_folder_structure = f"linewidth_{linewidth}nm/wavelength_{wavelength}nm/current_{current}mA"
            base_filename = f'delay_{delay}ps_current_{current}mA_wavelength_{wavelength}nm_linewidth_{linewidth}nm'
            png_title_point=f'LW={linewidth}nm, WL={wavelength}nm, Current={current}mA, Delay={delay}ps'
            maps_folder_structure = f'{main_folder}/maps/linewidth_{linewidth}nm/wavelength_{wavelength}nm'


            # === НАСТРОЙКА ОБОРУДОВАНИЯ ===
            linewidth_next = linewidth
            if linewidth_prev!=linewidth_next:
                btf.set_linewidth(linewidth)
                linewidth_prev=linewidth_next
            
            wavelength_next = wavelength
            if wavelength_prev!=wavelength_next:
                btf.set_wavelength(wavelength)
                wavelength_prev=wavelength_next
            
    
            current_next = current
            if current_prev != current_next:
                LD.set_current(current=current)
                current_prev = current_next
            
            delay_next = delay
            if delay_prev != delay_next:
                odl.set_time_delay(time_delay=delay)
                delay_prev = delay_next
            
            time.sleep(STABILIZATION_TIME)
            

            # === ИЗМЕРЕНИЯ ===
            
            # осциллограф, установка триегра в уровне 50%
            osc.set_triger_50()
            
            pm_power = measure_average_power(pm_device=pm_device,duration=1,aver_point=3)
            
            
            # === Каждый спан в своей папке ===
            rf_max_dict=rf_measurement(
                rf_device=rf_device, 
                N=NUMBER_RF_MEASURE, 
                save_folder_path=main_folder,
                folder_structure=base_folder_structure,
                filename=base_filename, 
                rf_rbw=RF_RBW_MAX,
                f_start=RF_F_START_MAX, 
                f_stop=RF_F_STOP_MAX,
                rf_level=RF_LEVEL, 
                png_title_point=png_title_point,
                save_png=True)

            rf_peak_freq_max=rf_max_dict["peak_freq"]
        
            
            rf_mid_dict= rf_measurement(
                rf_device=rf_device, 
                N=NUMBER_RF_MEASURE, 
                save_folder_path=main_folder,
                folder_structure=base_folder_structure,
                filename=base_filename, 
                rf_rbw=RF_RBW_MID,
                f_span=RF_SPAN_MID, 
                f_center=rf_peak_freq_max, 
                rf_level=RF_LEVEL, 
                png_title_point=png_title_point,
                save_png=True)
            
            rf_peak_freq_mid=rf_mid_dict["peak_freq"]
    
            
            rf_min_dict = rf_measurement(
                rf_device=rf_device, 
                N=NUMBER_RF_MEASURE, 
                save_folder_path=main_folder,
                folder_structure=base_folder_structure,
                filename=base_filename, 
                rf_rbw=RF_RBW_MIN,
                f_center=rf_peak_freq_mid, 
                f_span=RF_SPAN_MIN,rf_level=RF_LEVEL,
                png_title_point=png_title_point,
                save_png=True)
            
            rf_peak_freq_min=rf_min_dict["peak_freq"]
            
            
            osc_dict=oscilloscope_measurement(
                device=osc,mode=OSC_MODE, 
                duration=10*NANO, 
                save_folder_path=main_folder, 
                filename=base_filename, 
                folder_structure=base_folder_structure, 
                channel=4, 
                png_title_point=png_title_point,
                save_png=True
                )   
            
            osc_mean_freq=osc_dict['mean_GHz']
            
            # if (np.where(CURRENTS == current)[0][0] in [0, len(CURRENTS)//2, len(CURRENTS)-1] and 
            #                 np.where(DELAYS == delay)[0][0] in [0, len(DELAYS)//2, len(DELAYS)-1]):
            #     yoko_measurement(
            #         device=yoko, 
            #         save_folder_path=main_folder,
            #         filename=base_filename,
            #         folder_structure=base_folder_structure,
            #         png_title_point=png_title_point,
            #         save_png=True
            #     )

            # === Заполнение буфера ===
            collected_data['current'].append(current)
            collected_data['delay'].append(delay)
            collected_data['pm_400'].append(pm_power)
            collected_data['rf_peak_freq_max'].append(rf_peak_freq_max)
            collected_data['rf_peak_freq_mid'].append(rf_peak_freq_mid)
            collected_data['rf_peak_freq_min'].append(rf_peak_freq_min)
            collected_data['osc_mean_freq'].append(osc_mean_freq)
            
            if current == CURRENTS[-1] and delay == DELAYS[-1]:
                
                build_maps(
                    linewidth=linewidth,
                    wavelength=wavelength,
                    folder_structure=maps_folder_structure,
                    data_buf=collected_data
                )
                
                # Очищаем буфер для следующего напряжения
                collected_data = {
                    'current': [], 'delay': [],
                    'pm_400': [],
                    'rf_peak_freq_max': [], 
                    'rf_peak_freq_mid': [], 
                    'rf_peak_freq_min': [],
                    'osc_mean_freq': [],
                }
            
        
       
            
        print('Данные успешно сняты')
    finally:
        try:
            osc.disconnect()
            odl.disconnect()
            LD.turn_off_all()
            btf.disconnect()
        except Exception as e:
            print(f"Ошибка при отключении: {e}")

        

if __name__ == "__main__":
    main()