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
from pathlib import Path
import numpy as np

# импорт настроек
from config import* 
# ===================
# импорт драйверов
# ===================

# from devices.yokogawa.OSA_Yokogawa_new import OSA_Yokogawa_new
# from devices.btf_100.btf_100 import BTF100
from measure_libs.rf_measure_lib import rf_measurement
from devices.rsa_device.RF306B import RF306B
from devices.odl_650.OpticDelayLine_new import OpticDelayLine
from devices.ut_3005.VoltageDriverUT3005 import VoltageDriverUT3005
from devices.cdl_1015.CLD1015 import CLD1015
from devices.btf_100.btf_100 import BTF100
from devices.oscilloscope.tektronix_DPO71604C import Oscilloscope
oscilloscope=Oscilloscope(ip="10.2.60.150", port=4000)
oscilloscope.trigger_level(challel=4,level=-0.050)



# === Определение имён для папок спанов (с Hz) ===
max_span = f'span_{number_with_decimal_prefix(RF_SPAN_MAX)}Hz'
middle_span = f'span_{number_with_decimal_prefix(RF_SPAN_MIDDLE)}Hz'
min_span = f'span_{number_with_decimal_prefix(RF_SPAN_MIN)}Hz'

# ============================================================
# Функция для построение 6 карт для одного напряжения
# ============================================================


def build_voltage_maps(voltage, main_folder, data_buf, wavelength):
    """Внутренняя функция: строит 6 тепловых карт для заданного напряжения."""
    
    
    # Фильтруем данные по напряжению
    mask = np.array(data_buf['voltage']) == voltage
    
    # Папка для карт этого напряжения
    plot_subfolder = Path(main_folder) / f"rf_measurements/maps/wavelength_{wavelength}nm/voltage_{voltage}V"
    plot_subfolder.mkdir(parents=True, exist_ok=True)
    
    # Данные для осей
    x = np.array(data_buf['current'])[mask]
    y = np.array(data_buf['delay'])[mask]
    
    # === Конфигурация карт (6 карт: freq + amplitude для каждого span) ===
    # rf_freq_* в Hz, нужно перевести в GHz (делим на 1e+9)
    maps_config = [
        (np.array(data_buf['rf_freq_max']) / 1e+9, f'rf_freq_{max_span}', 'Frequency (GHz)', max_span),
        (data_buf['rf_peak_amplitude_max'], f'rf_peak_amplitude_{max_span}', 'Peak Amplitude (dBm)', max_span),
        (data_buf['pm_400'], f'power_meter', 'Power, mW',''),
        (data_buf['rf_smsr_max'], f'rf_smsr_{max_span}', 'SMSR (dB)', max_span),
        (data_buf['osc_mean_freq'], f"osc_mean_freq_{OSCILLOSCOPE_MODES}_hor_scale_{number_with_decimal_prefix(OSCILLOSCOPE_HOR_SCALES)}s",'Frequency (GHz)', ''),
        (data_buf['osc_std'], f"osc_std_{OSCILLOSCOPE_MODES}_hor_scale_{number_with_decimal_prefix(OSCILLOSCOPE_HOR_SCALES)}s",'Frequency (GHz)', '')
    ]
    
    for z_raw, fname_suffix, z_label, span_label in maps_config:
        z = np.array(z_raw)[mask]
        create_map_and_save(
            x_arr=[x.tolist(), "Current (mA)"],
            y_arr=[y.tolist(), "Delay (ps)"],
            z_arr=[z.tolist(), z_label],
            title=f"Voltage {voltage}V, ({span_label})",
            folder_path=plot_subfolder,
            filename=f"{fname_suffix}",
            show_plot=False  
        )


def main():

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
    
    

    for wavelength in WAVELENGTH:
        btf.set_wavelength(wavelength)

        params = itertools.product(VOLTAGES, CURRENTS, DELAYS)

        # === Буфер для сбора данных ===
        collected_data = {
            'voltage': [], 'current': [], 'delay': [],
            'rf_freq_max': [], 'rf_peak_amplitude_max': [],
            'pm_400': [],
            'rf_smsr_max': [],'osc_freq':[], "osc_std":[]
        }
        
        current_voltage_batch = None
        
        voltage_prev = -1
        current_prev = -1
        delay_prev = -1
        
        
        

        for idx, (voltage, current, delay) in enumerate(params, 1):

            base_folder_structure=f"wavelength_{wavelength}nm/voltage_{voltage}V/current_{current}mA"
            base_filename=f'delay_{delay}ps_current_{current}mA_voltage_{voltage}V_wavelength_{wavelength}nm' 

            # === Построение карт при смене напряжения ===
            if current_voltage_batch is not None and voltage != current_voltage_batch:
                build_voltage_maps(current_voltage_batch, main_folder, collected_data, wavelength)
            current_voltage_batch = voltage
            
            
            
            

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
            pm_power = measure_average_power(pm_device)


            
            # === Каждый спан в своей папке ===
            max_span_info=rf_measurement(
                rf_device=rf_device, N=NUMBER_RF_MEASURE, save_folder_path=main_folder,folder_structure=base_folder_structure,
                filename=base_filename, rf_rbw=RF_RBW_MAX,
                f_start=RF_F_START_MAX, f_stop=RF_F_STOP_MAX, save_png=True)

            rf_peak_freq_max=max_span_info["peak_freq"], 
            rf_peak_power_max=max_span_info["peak_power"]
            rf_smsr_max=max_span_info['smsr']
            # rf_freq_mid, rf_amplitude_mid ,rf_smsr_mid = rf_measurement(
            #     rf_device=rf_device, N=NUMBER_RF_MEASURE, save_folder_path=main_folder,folder_structure=base_folder_structure,
            #     filename=base_filename, rf_rbw=RF_RBW_MIDDLE,
            #     f_span=RF_SPAN_MIDDLE, f_center=rf_freq_max, save_png=True)

            
            # rf_freq_min, rf_amplitude_min, rf_smsr_min = rf_measurement(
            #     rf_device=rf_device, N=NUMBER_RF_MEASURE, save_folder_path=main_folder,folder_structure=base_folder_structure,
            #     filename=base_filename, rf_rbw=RF_RBW_MIN,
            #     f_center=rf_freq_mid, f_span=RF_SPAN_MIN, save_png=True)

            osc_dict=oscilloscope_measurement(device=oscilloscope, save_folder_path=main_folder, filename=base_filename, folder_structure=base_folder_structure, channel=4, save_png=True)
            osc_key = (OSCILLOSCOPE_MODES,OSCILLOSCOPE_HOR_SCALES)
            item = osc_dict[osc_key]
            osc_freq_GHz = item['stats']['mean_GHz']
            osc_std_GHz=item['stats']['stddev_GHz']


            # === Заполнение буфера для карт ===
            collected_data['voltage'].append(voltage)
            collected_data['current'].append(current)
            collected_data['delay'].append(delay)
            collected_data['rf_peak_freq_max'].append(rf_peak_freq_max)
            collected_data['rf_peak_power_max'].append(rf_peak_power_max)
            collected_data['pm_400'].append(pm_power)
            collected_data['rf_smsr_max'].append(rf_smsr_max)
            collected_data['osc_freq'].append(osc_freq_GHz)
            collected_data['osc_std'].append(osc_std_GHz)
            
            # collected_data['rf_freq_mid'].append(rf_freq_mid)
            # collected_data['rf_peak_amplitude_mid'].append(rf_amplitude_mid)
            # collected_data['rf_freq_min'].append(rf_freq_min)
            # collected_data['rf_peak_amplitude_min'].append(rf_amplitude_min)
            

        
        # === Построение карт для ПОСЛЕДНЕГО напряжения ===
        if current_voltage_batch is not None:
            build_voltage_maps(current_voltage_batch, main_folder, collected_data, wavelength)

        
        
        
    

if __name__ == "__main__":
    main()