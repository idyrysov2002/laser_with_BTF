import itertools
import os
import time
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
from measure_libs.rf_measure_lib import rf_measurement
from measure_libs.yokogawa_measure_lib import osa_measurement
from devices.pm_400.PMDevice import measure_average_power
from scripts.create_folder import create_subfolder
from utilities.scan_utils import get_scan_generator,generate_file_paths, get_active_param_names
from utilities.initialize_instruments import initialize_instruments
from scripts.create_folder import create_date_folder
from scripts.number_with_decimal_prefix import number_with_decimal_prefix
from measure_libs.oscilloscope_measure_lib import oscilloscope_measurement

from config import*

# === Определение имён для папок спанов ===
rf_max_span_name = f"span_{number_with_decimal_prefix(RF_SPAN_MAX)}Hz"
rf_middle_span_name = f"span_{number_with_decimal_prefix(RF_SPAN_MIDDLE)}Hz"
rf_min_span_name = f"span_{number_with_decimal_prefix(RF_SPAN_MIN)}Hz"
yokogawa_big_span_name='span_for_wavelength'
yokogawa_small_span_name='span_for_linewidth'


def main():
    pm_avg_mW_data=[]
    rf_freq_max_data,rf_amplitude_max_data, rf_smsr_max_data = [],[],[]
    rf_freq_middle_data, rf_amplitude_middle_data, rf_smsr_middle_data = [], [], []
    rf_freq_min_data, rf_amplitude_min_data, rf_smsr_min_data = [], [], []
    yokogawa_peak_wave_big_data, yokogawa_peak_ampl_big_data = [], []
    yokogawa_peak_wave_small_data, yokogawa_peak_ampl_small_data=[],[]

    voltage_prev = -1
    current_prev = -1
    linewidth_prev = -1
    delay_prev = -1
    wavelength_prev = -1

    # Получаем список активных параметров
    active_params = get_active_param_names(verbose=True)

    # ИНИЦИАЛИЗАЦИЯ ПРИБОРОВ
    devices = initialize_instruments()
    print("Доступные приборы:", list(devices.keys()))

    # создаем корневую папку для хранения данных (один раз)
    main_folder = create_date_folder(base_path=r"C:\Users\namys_23hvwev\Documents\DATA\data_for_testing", prefix="exp_simulator")

    # СОЗДАЕМ ВЛОЖЕННЫЕ ЦИКЛЫ
    params_generator = get_scan_generator()

    for idx, step in enumerate(params_generator, 1):

        delay = step.get("delay", None)
        current = step.get('current', None)
        voltage = step.get('voltage', None)
        wavelength = step.get("wavelength", None) 
        linewidth = step.get("linewidth", None) 

        base_folder_structure, base_filename = generate_file_paths(step, active_params) 

        # === НАСТРОЙКА ОБОРУДОВАНИЯ ===
        if 'ut' in devices:
            voltage_next = voltage
            if voltage_next != voltage_prev:
                devices['ut'].set_voltage(voltage=voltage)
                voltage_prev = voltage_next
        if "odl" in devices:
            delay_next = delay
            if delay_next != delay_prev:
                devices["odl"].set_time_delay(time_delay=delay)
                delay_prev = delay_next

        if "btf" in devices:
            linewidth_next = linewidth
            if linewidth_next != linewidth_prev:
                devices["btf"].set_linewidth(linewidth)
                linewidth_prev = linewidth_next

            wavelength_next = wavelength
            if wavelength_next != wavelength_prev:
                devices["btf"].set_wavelength(wavelength)
                wavelength_prev = wavelength_next

        if "ld" in devices:
            current_next = current
            if current_next != current_prev:
                devices["ld"].set_current(current=current)
                current_prev = current_next

        # ВРЕМЯ ДЛЯ СТАБИЛИЗАЦИИ
        time.sleep(STABILIZATION_TIME)

        if "pm" in devices:
            pm_avg_mW = measure_average_power(pm_device=devices["pm"])

        if "rf" in devices:

            rf_freq_max, rf_amplitude_max, rf_smsr_max= rf_measurement(
                rf_device=devices['rf'], N=NUMBER_RF_MEASURE, save_folder_path=main_folder,folder_structure=base_folder_structure,
                filename=base_filename, rf_rbw=RF_RBW_MAX,
                f_start=RF_F_START_MAX, f_stop=RF_F_STOP_MAX, save_png=True)

            
            rf_freq_mid, rf_amplitude_mid ,rf_smsr_mid = rf_measurement(
                rf_device=devices['rf'], N=NUMBER_RF_MEASURE, save_folder_path=main_folder,folder_structure=base_folder_structure,
                filename=base_filename, rf_rbw=RF_RBW_MIDDLE,
                f_span=RF_SPAN_MIDDLE, f_center=rf_freq_max, save_png=True)

            
            rf_freq_min, rf_amplitude_min, rf_smsr_min = rf_measurement(
                rf_device=devices['rf'], N=NUMBER_RF_MEASURE, save_folder_path=main_folder,folder_structure=base_folder_structure,
                filename=base_filename, rf_rbw=RF_RBW_MIN,
                f_center=rf_freq_mid, f_span=RF_SPAN_MIN, save_png=True)

        if 'yokogawa' in devices:

            # Большой спан
            yokogawa_peak_wave_big, yokogawa_peak_ampl_big=osa_measurement(
                device=devices["yokogawa"], 
                save_folder_path=main_folder, 
                folder_structure=base_folder_structure, 
                filename=base_filename,
                res=YOKO_RES_BIG_SPAN,
                wave_start=YOKO_BIG_SPAN_START,
                wave_stop=YOKO_BIG_SPAN_STOP,
                save_png=True)

            yokogawa_peak_wave_big_data.append(yokogawa_peak_wave_big)
            yokogawa_peak_ampl_big_data.append(yokogawa_peak_ampl_big)

            YOKOGAWA_SMALL_SPAN_START = yokogawa_peak_wave_big - 2 * linewidth
            YOKOGAWA_SMALL_SPAN_STOP = yokogawa_peak_wave_big + 2 * linewidth

            # Малый спан
            yokogawa_peak_wave_small, yokogawa_peak_ampl_small = osa_measurement(
                device=devices["yokogawa"],
                save_folder_path=main_folder,
                folder_structure=base_folder_structure,
                filename=base_filename,
                res=YOKO_RES_SMALL_SPAN,
                wave_start=YOKOGAWA_SMALL_SPAN_START,
                wave_stop=YOKOGAWA_SMALL_SPAN_STOP,
                save_png=True,
            )
            yokogawa_peak_wave_small_data.append(yokogawa_peak_wave_small)
            yokogawa_peak_ampl_small_data.append(yokogawa_peak_ampl_small)

        if 'oscilloscope' in devices:
            oscilloscope_measurement(device=devices['oscilloscope'], save_folder_path=main_folder, filename=base_filename, folder_structure=base_folder_structure, channel=4, save_png=True)


if __name__ == "__main__":
    main()
