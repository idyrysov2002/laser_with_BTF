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
from scripts.number_with_decimal_prefix import number_with_decimal_prefix

from measure_libs.oscilloscope_measure_lib import oscilloscope_measurement
from measure_libs.yokogawa_measure_lib import yoko_measurement
from pathlib import Path
from scripts.create_map_and_save import create_map_and_save

# импорт настроек
from config import NANO, OSC_MODE,STABILIZATION_TIME,OSC_VER_SCALE,OSC_CHANNEL
from config import RF_SPAN_MAX,RF_SPAN_MID,RF_SPAN_MIN
from config import LINEWIDTH, WAVELENGTH, CURRENTS, DELAYS
from config import NUMBER_RF_MEASURE, BTF_COM, ODL_COM, MAIN_SAVE_PATH
from config import RF_F_START_MAX,RF_F_STOP_MAX, DATA_FOLDER_PREFIX
from config import RF_RBW_MAX, RF_RBW_MID, RF_RBW_MIN, RF_LEVEL, OSC_IP, OSC_PORT
from config import PM_DURATION, PM_POINTS
from config import RF_6200MHz_NAME, RF_100MHz_NAME, RF_1MHz_NAME, GIGA

from config_maps import MAPS_CONFIG
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
from devices.pm_400.PMDevice import PMDevicePM100D, measure_average_power


# from mock_devices.yokogawa.Yokogawa_OSA import YokogawaOSA
# from measure_libs.rf_measure_lib import rf_measurement
# from mock_devices.rsa_device.RF306B import RF306B
# from mock_devices.odl_650.OpticDelayLine_new import OpticDelayLine
# from mock_devices.cdl_1015.CLD1015 import CLD1015
# from mock_devices.btf_100.btf_100 import BTF100
# from mock_devices.oscilloscope.tektronix_DPO71604C import Oscilloscope
# from measure_libs.yokogawa_measure_lib import yoko_measurement
# from mock_devices.pm_400.PMDevice import PMDevicePM100D, measure_average_power




def build_maps(data_map, save_folder_structure, linewidth, wavelength):
    """
    Построение тепловых карт для всех измерений из data_map.

    Аргументы:
        data_map: dict - словарь с данными
            Обязательные ключи: 'current' (ось X), 'delay' (ось Y)
            Остальные ключи: любые названия измерений для построения карт
        save_folder_structure: str - путь для сохранения карт
        linewidth: float - ширина линии (для заголовка)
        wavelength: float - длина волны (для заголовка)

    Функция автоматически построит карту для каждого ключа в data_map,
    кроме 'current' и 'delay', используя их как координаты точек.
    """
    
    # Получаем данные для осей
    x_arr = data_map['current']
    y_arr = data_map['delay']
    x_label = "Current, mA"
    y_label = "Delay, ps"
    
    # Создаем папку
    folder_path = Path(save_folder_structure)
    folder_path.mkdir(parents=True, exist_ok=True)
    
    # Проходим по всем измерениям (исключая current и delay)
    for meas_name, meas_values in data_map.items():
        if meas_name in ['current', 'delay']:
            continue
            
        # Берем настройки из конфига или используем значения по умолчанию
        if meas_name in MAPS_CONFIG:
            z_label = MAPS_CONFIG[meas_name]['label']
            title_name = MAPS_CONFIG[meas_name]['title']
        else:
            z_label = "Value"
            title_name = meas_name
        
        # Формируем заголовок и имя файла
        title = f'{title_name}: LW={linewidth}nm, WL={wavelength}nm'
        filename = f'{meas_name}_lw_{linewidth}nm_wl_{wavelength}nm'
        
        # Создаем карту
        create_map_and_save(
            x_arr=[x_arr, x_label],
            y_arr=[y_arr, y_label],
            z_arr=[meas_values, z_label],
            title=title,
            folder_path=folder_path,
            filename=filename,
            show_plot=False
        )


def main():


    try:
        
        
        # ИНИЦИАЛИЗАЦИЯ ПРИБОРОВ
        btf = BTF100(port=BTF_COM)
        pm_device = PMDevicePM100D()
        odl = OpticDelayLine(port=ODL_COM)
        odl.initialize()
        rf_device = RF306B()
        LD = CLD1015()
        LD.turn_on_all()

        # yoko=YokogawaOSA(write_TR='C')


        osc=Oscilloscope(ip=OSC_IP, port=OSC_PORT)

        # осцилограф: настройки
        osc.acquire_mode(mode=OSC_MODE)
        osc.vertical_scale(channel=OSC_CHANNEL,scale=OSC_VER_SCALE)
        

        

        

        params = itertools.product(LINEWIDTH, WAVELENGTH, CURRENTS, DELAYS)

        # === словарь для сбора данных ===

        collected_data = {
            'current':[],
            'delay': [],
            'pm_400': [],
            'rf_peak_freq_span_6200MHz': [], 
            'rf_peak_freq_span_100MHz': [], 
            'rf_peak_freq_span_1MHz': [],
            'osc_mean_freq':[],
        }
    
        
        
        current_prev = None
        delay_prev = None
        linewidth_prev = None
        wavelength_prev = None
    
        main_folder = create_date_folder(base_path=MAIN_SAVE_PATH, prefix=DATA_FOLDER_PREFIX)
        for idx, (linewidth, wavelength,current, delay) in enumerate(params, 1):
            
            base_folder_structure = f"lw_{linewidth}nm/wl_{wavelength}nm/current_{current}mA"
            base_filename = f'delay_{delay}ps_current_{current}mA_wl_{wavelength}nm_lw_{linewidth}nm'
            png_title_point=f'lw={linewidth}nm, wl={wavelength}nm, I={current}mA, t={delay}ps'
            maps_folder_structure = f'{main_folder}/maps/lw_{linewidth}nm/wl_{wavelength}nm'


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
            
            pm_power = measure_average_power(pm_device=pm_device,duration=PM_DURATION,aver_point=PM_POINTS)
            
            
            
            rf_max_dict=rf_measurement(
                rf_device=rf_device, 
                N=NUMBER_RF_MEASURE, 
                save_folder_path=main_folder,
                folder_structure=base_folder_structure,
                span_name=RF_6200MHz_NAME,
                filename=base_filename, 
                rf_rbw=RF_RBW_MAX,
                f_start=RF_F_START_MAX, 
                f_stop=RF_F_STOP_MAX,
                rf_level=RF_LEVEL, 
                png_title_point=png_title_point,
                save_png=True)

            rf_peak_freq_6200MHz=rf_max_dict["peak_freq"]
        
            
            rf_mid_dict= rf_measurement(
                rf_device=rf_device, 
                N=NUMBER_RF_MEASURE, 
                save_folder_path=main_folder,
                folder_structure=base_folder_structure,
                span_name=RF_100MHz_NAME,
                filename=base_filename, 
                rf_rbw=RF_RBW_MID,
                f_span=RF_SPAN_MID, 
                f_center=rf_peak_freq_6200MHz, 
                rf_level=RF_LEVEL, 
                png_title_point=png_title_point,
                save_png=True)
            
            rf_peak_freq_100MHz=rf_mid_dict["peak_freq"]
    
            
            rf_min_dict = rf_measurement(
                rf_device=rf_device, 
                N=NUMBER_RF_MEASURE, 
                save_folder_path=main_folder,
                folder_structure=base_folder_structure,
                span_name=RF_1MHz_NAME,
                filename=base_filename, 
                rf_rbw=RF_RBW_MIN,
                f_center=rf_peak_freq_100MHz, 
                f_span=RF_SPAN_MIN,rf_level=RF_LEVEL,
                png_title_point=png_title_point,
                save_png=True)
            
            rf_peak_freq_1MHz=rf_min_dict["peak_freq"]
            
            
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
            collected_data['rf_peak_freq_span_6200MHz'].append(rf_peak_freq_6200MHz/GIGA)
            collected_data['rf_peak_freq_span_100MHz'].append(rf_peak_freq_100MHz/GIGA)
            collected_data['rf_peak_freq_span_1MHz'].append(rf_peak_freq_1MHz/GIGA)
            collected_data['osc_mean_freq'].append(osc_mean_freq)
            
            if current == CURRENTS[-1] and delay == DELAYS[-1]:
                
                build_maps(data_map=collected_data, 
                           save_folder_structure=maps_folder_structure, 
                           linewidth=linewidth, 
                           wavelength=wavelength)
                
                # Очищаем словарь
                collected_data = {
                                'current':[],
                                'delay': [],
                                'pm_400': [],
                                'rf_peak_freq_span_6200MHz': [], 
                                'rf_peak_freq_span_100MHz': [], 
                                'rf_peak_freq_span_1MHz': [],
                                'osc_mean_freq':[],
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