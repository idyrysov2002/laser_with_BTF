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
from config import NANO
from config import RF_SPAN_MAX,RF_SPAN_MID,RF_SPAN_MIN
from config import LINEWIDTH, WAVELENGTH, VOLTAGES, CURRENTS, DELAYS
from config import NUMBER_RF_MEASURE
from config import RF_F_START_MAX,RF_F_STOP_MAX
from config import RF_RBW_MAX, RF_RBW_MID, RF_RBW_MIN


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
mid_span = f'span_{number_with_decimal_prefix(RF_SPAN_MID)}Hz'
min_span = f'span_{number_with_decimal_prefix(RF_SPAN_MIN)}Hz'



def build_voltage_maps(voltage, linewidth, wavelength, folder_structure, data_buf):
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
        ('pm_400', 'power_meter', 'Power, mW', ''),
        (np.array(data_buf['rf_peak_freq_max']) / 1e+9, f'rf_peak_freq_{max_span}', 'Frequency, GHz', max_span),
        (np.array(data_buf['rf_peak_freq_mid']) / 1e+9, f'rf_peak_freq_{mid_span}', 'Frequency, GHz', mid_span),
        (np.array(data_buf['rf_peak_freq_min']) / 1e+9, f'rf_peak_freq_{min_span}', 'Frequency, GHz', min_span),
        ('osc_mean_freq', 'osc_mean_freq', 'Frequency, GHz', ''),
    ]
    
    for z_raw, fname_suffix, z_label, span_label in maps_config:
        # Обработка PM400
        if z_raw == 'pm_400':
            z = np.array(data_buf['pm_400'])
            create_map_and_save(
                x_arr=[x.tolist(), "Current, mA"],
                y_arr=[y.tolist(), "Delay, ps"],
                z_arr=[z.tolist(), z_label],
                title=f"PM400: linewidth {linewidth}nm, wavelength {wavelength}nm, voltage {voltage}V",
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
                title=f"OSC: linewidth {linewidth}nm, wavelength {wavelength}nm, voltage {voltage}V",
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
            title=f"linewidth {linewidth}nm, wavelength {wavelength}nm, voltage {voltage}V, ({span_label})",
            folder_path=folder_path,
            filename=f"{fname_suffix}",
            show_plot=False
        )


def main():


    try:
        
        # ========================
        # ИНИЦИАЛИЗАЦИЯ ПРИБОРОВ
        # ========================
        btf = BTF100(port='COM11')
        pm_device = PMDevicePM100D()
        odl = OpticDelayLine('COM10')
        odl.initialize()
        rf_device = RF306B()
        LD = CLD1015()
        LD.turn_on_all()
        ut = VoltageDriverUT3005('COM8')
        ut.turn_on()
        
        osc=Oscilloscope(ip="10.2.60.150", port=4000)
        osc.trigger_level(channel=4,level=-0.050)
        # Установливаем режим (например, sample, average)
        osc.acquire_mode(mode='average')

        # Установливаем длительность сигнала
        osc.duration_time(duration=10*NANO)

        # yoko=YokogawaOSA()

        

        params = itertools.product(LINEWIDTH, WAVELENGTH, VOLTAGES, CURRENTS, DELAYS)

        # === Буфер для сбора данных ===
        collected_data = {
            'voltage': [], 'current': [], 'delay': [],
            'pm_400': [],
            'rf_peak_freq_max': [], 
            'rf_peak_freq_mid': [], 
            'rf_peak_freq_min': [],
            'osc_mean_freq':[],
        }
    
        
        voltage_prev = None
        current_prev = None
        delay_prev = None
        linewidth_prev = None
        wavelength_prev = None
        
        main_folder = create_date_folder(base_path="Z:/data_for_laser_with_BTF", prefix='laser_with_btf')
        for idx, (linewidth, wavelength, voltage, current, delay) in enumerate(params, 1):
            base_folder_structure = f"linewidth_{linewidth}nm/wavelength_{wavelength}nm/voltage_{voltage}V/current_{current}mA"
            base_filename = f'delay_{delay}ps_current_{current}mA_voltage_{voltage}V_wavelength_{wavelength}nm_linewidth_{linewidth}nm'


            # === НАСТРОЙКА ОБОРУДОВАНИЯ ===
            linewidth_next = linewidth
            if linewidth_prev!=linewidth_next:
                btf.set_linewidth(linewidth)
                linewidth_prev=linewidth_next
            
            wavelength_next = wavelength
            if wavelength_prev!=wavelength_next:
                btf.set_wavelength(wavelength)
                wavelength_prev=wavelength_next
            
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
            
            time.sleep(2)
            

            # === ИЗМЕРЕНИЯ ===
            
            # Сброс статистики осциллографа
            osc.clear()
            
            pm_power = measure_average_power(pm_device=pm_device,duration=1,aver_point=5)
            
            # === Каждый спан в своей папке ===
            rf_max_dict=rf_measurement(
                rf_device=rf_device, N=NUMBER_RF_MEASURE, save_folder_path=main_folder,folder_structure=base_folder_structure,
                filename=base_filename, rf_rbw=RF_RBW_MAX,
                f_start=RF_F_START_MAX, f_stop=RF_F_STOP_MAX, save_png=False)

            rf_peak_freq_max=rf_max_dict["peak_freq"]
        
            
            rf_mid_dict= rf_measurement(
                rf_device=rf_device, N=NUMBER_RF_MEASURE, save_folder_path=main_folder,folder_structure=base_folder_structure,
                filename=base_filename, rf_rbw=RF_RBW_MID,
                f_span=RF_SPAN_MID, f_center=rf_peak_freq_max, save_png=False)
            
            rf_peak_freq_mid=rf_mid_dict["peak_freq"]
    
            
            rf_min_dict = rf_measurement(
                rf_device=rf_device, N=NUMBER_RF_MEASURE, save_folder_path=main_folder,folder_structure=base_folder_structure,
                filename=base_filename, rf_rbw=RF_RBW_MIN,
                f_center=rf_peak_freq_mid, f_span=RF_SPAN_MIN, save_png=False)
            
            rf_peak_freq_min=rf_min_dict["peak_freq"]
            
            
            osc_dict=oscilloscope_measurement(
                device=osc,mode='average', 
                duration=10*NANO, 
                save_folder_path=main_folder, 
                filename=base_filename, 
                folder_structure=base_folder_structure, 
                channel=4, save_png=False)   
            osc_mean_freq=osc_dict['mean_GHz']
            
            


            # === Заполнение буфера ===
            collected_data['voltage'].append(voltage)
            collected_data['current'].append(current)
            collected_data['delay'].append(delay)
            collected_data['pm_400'].append(pm_power)
            collected_data['rf_peak_freq_max'].append(rf_peak_freq_max)
            collected_data['rf_peak_freq_mid'].append(rf_peak_freq_mid)
            collected_data['rf_peak_freq_min'].append(rf_peak_freq_min)
            collected_data['osc_mean_freq'].append(osc_mean_freq)
            
            # === ПРОВЕРКА: Закончился ли полный цикл для текущего напряжения? ===
            # Так как DELAYS меняется быстрее всего, а CURRENTS предпоследний,
            # конец набора данных для одного Voltage наступает, когда 
            # текущий ток ПОСЛЕДНИЙ и текущая задержка ПОСЛЕДНЯЯ.
            if current == CURRENTS[-1] and delay == DELAYS[-1]:
                
                maps_folder_structure = f'{main_folder}/maps/linewidth_{linewidth}nm/wavelength_{wavelength}nm/voltage_{voltage}V'
                
                print(f"Данные для V={voltage} собраны. Строю карты...")
                build_voltage_maps(
                    voltage=voltage,
                    linewidth=linewidth,
                    wavelength=wavelength,
                    folder_structure=maps_folder_structure,
                    data_buf=collected_data
                )
                
                # Очищаем буфер для следующего напряжения
                collected_data = {
                    'voltage': [], 'current': [], 'delay': [],
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
            ut.turn_off_and_close_COM()
            btf.disconnect()
        except Exception as e:
            print(f"Ошибка при отключении: {e}")

        

if __name__ == "__main__":
    main()