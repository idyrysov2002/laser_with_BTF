import itertools
import os
import time
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib import rcParams
from any_functions import create_data_folder
from devices.yokogawa.osa_measure_lib import osa_measurement
from write_arrays_to_excel import write_arrays_excel
from create_map_and_save import create_map_and_save


# импорт настроек
from config import *
# ===================
# импорт драйверов
# ===================

# from devices.yokogawa.OSA_Yokogawa_new import OSA_Yokogawa_new
# from devices.btf_100.btf_100 import BTF100
# from devices.rsa_device.rf_measure_lib import rf_measurement
# from devices.rsa_device.RF306B import RF306B
# from devices.odl_650.OpticDelayLine import OpticDelayLine
# from devices.ut_3005.VoltageDriverUT3005 import VoltageDriverUT3005
# from devices.cdl_1015.CLD1015 import CLD1015
# from devices.pm_400.PMDevice import PMDevicePM100D, measure_average_power

from mock_devices.btf_100_Simulator import BTF100Simulator as BTF100
from mock_devices.CLD1015_Simulator import CLD1015Simulator as CLD1015
from mock_devices.OpticDelayLine_Simulator import OpticDelayLineSimulator as OpticDelayLine
from mock_devices.PMDevicePM100D_Simulator import PMDevicePM100DSimulator as PMDevicePM100D,measure_average_power
from mock_devices.RF306B_Simulator import RF306BSimulator as RF306B
from mock_devices.VoltageDriverUT3005Simulator import VoltageDriverUT3005Simulator as VoltageDriverUT3005
from mock_devices.OSA_Yokogawa_new_Simulator import OSA_Yokogawa_new_Simulator as OSA_Yokogawa_new
from devices.rsa_device.rf_measure_lib import rf_measurement


def initialize_instruments():
    """
    Инициализирует приборы на основе config.py
    Возвращает словарь с активными объектами приборов
    """
    devices = {}
    cfg = INSTRUMENTS

    print("--- Запуск инициализации ---")

    # 1. ODL
    if cfg.get("odl", {}).get("enabled"):
        try:
            port = cfg["odl"].get("port", "COM6")
            odl = OpticDelayLine(port)
            odl.initialize()
            devices["odl"] = odl
            print(f"[OK] ODL -> {port}")
        except Exception as e:
            print(f"[FAIL] ODL: {e}")

    # 2. BTF
    if cfg.get("btf", {}).get("enabled"):
        try:
            port = cfg["btf"].get("port", "COM3")
            btf = BTF100(port=port)
            devices["btf"] = btf
            print(f"[OK] BTF -> {port}")
        except Exception as e:
            print(f"[FAIL] BTF: {e}")

    # 3. OSA
    if cfg.get("osa", {}).get("enabled"):
        try:
            osa = OSA_Yokogawa_new()
            devices["osa"] = osa
            print("[OK] OSA")
        except Exception as e:
            print(f"[FAIL] OSA: {e}")

    # 4. RF
    if cfg.get("rf", {}).get("enabled"):
        try:
            rf_device = RF306B()
            devices["rf"] = rf_device
            print("[OK] RF")
        except Exception as e:
            print(f"[FAIL] RF: {e}")

    # 5. LD (Laser)
    if cfg.get("ld", {}).get("enabled"):
        try:
            ld = CLD1015()
            ld.turn_on_tec()
            time.sleep(1)
            ld.turn_on_laser()
            devices["ld"] = ld
            print("[OK] LD (ON)")
        except Exception as e:
            print(f"[FAIL] LD: {e}")

    # 6. UT (Power Supply)
    if cfg.get("ut", {}).get("enabled"):
        try:
            port = cfg["ut"].get("port", "COM8")
            ut = VoltageDriverUT3005(port)
            ut.turn_on()
            devices["ut"] = ut
            print(f"[OK] UT -> {port}")
        except Exception as e:
            print(f"[FAIL] UT: {e}")

    # 7. PM (Power Meter)
    if cfg.get("pm", {}).get("enabled"):
        try:
            pm_device = PMDevicePM100D()
            devices["pm"] = pm_device
            print("[OK] PM")
        except Exception as e:
            print(f"[FAIL] PM: {e}")

    print("-----------------------------")
    return devices


# # ========================
# # ИНИЦИАЛИЗАЦИЯ ПРИБОРОВ
# # ========================
# odl = OpticDelayLine('COM6')
# odl.initialize()

# btf = BTF100(port="COM3")
# osa = OSA_Yokogawa_new()
# rf_device = RF306B()
# LD = CLD1015()
# LD.turn_on_tec()
# time.sleep(1)
# LD.turn_on_laser()

# ut = VoltageDriverUT3005('COM8')
# ut.turn_on()

# pm_device = PMDevicePM100D()


# ============================================================
# Функция для построение 6 карт для одного напряжения
# ============================================================


def _build_voltage_maps(voltage, main_folder, data_buf):
    """Внутренняя функция: строит 7 тепловых карт (6 RF и мощемер) для заданного напряжения."""
    from pathlib import Path
    import numpy as np
    
    # Фильтруем данные по напряжению
    mask = np.array(data_buf['voltage']) == voltage
    
    # Папка для карт этого напряжения
    plot_subfolder = Path(main_folder) / f"voltage_{voltage}V" / "maps"
    plot_subfolder.mkdir(parents=True, exist_ok=True)
    
    # Данные для осей
    x = np.array(data_buf['current'])[mask]
    y = np.array(data_buf['delay'])[mask]
    
    maps_config = [
        (data_buf['rf_freq_max'], 'rf_freq_max', 'Частота, ГГц (max span)'),
        (data_buf['rf_pow_max'],  'rf_pow_max',  'Мощность, дБм (max span)'),
        (data_buf['rf_freq_mid'], 'rf_freq_mid', 'Частота, ГГц (mid span)'),
        (data_buf['rf_pow_mid'],  'rf_pow_mid',  'Мощность, дБм (mid span)'),
        (data_buf['rf_freq_min'], 'rf_freq_min', 'Частота, ГГц (min span)'),
        (data_buf['rf_pow_min'],  'rf_pow_min',  'Мощность, дБм (min span)'),
        (data_buf['power_meter_avg'],  'power_meter_avg',  'Мощность, mW'),
    ]
    
    for z_raw, fname_suffix, z_label in maps_config:
        z = np.array(z_raw)[mask]
        create_map_and_save(
            x_arr=[x.tolist(), "Ток, мА"],
            y_arr=[y.tolist(), "Задержка, пс"],
            z_arr=[z.tolist(), z_label],
            title=f"U = {voltage}В, {z_label}",
            folder_path=plot_subfolder,
            filename=f"RF_{fname_suffix}",
            show_plot=False  # 👈 True только для отладки
        )


def main():
    main_folder = create_data_folder(base_path=r'c:\Users\study\Documents\data_for_testing', prefix='exp')
    
    params = itertools.product(VOLTAGES, CURRENTS, DELAYS, LINEWIDTH, WAVELENGTH)

    # === Буфер для сбора данных ===
    collected_data = {
        'voltage': [], 'current': [], 'delay': [],
        'rf_freq_max': [], 'rf_pow_max': [],
        'rf_freq_mid': [], 'rf_pow_mid': [],
        'rf_freq_min': [], 'rf_pow_min': [],'power_meter_avg': []
    }
    
    current_voltage_batch = None

    # === Списки для Excel ===
    idx_data, time_data, voltage_data, delay_data = [], [], [], []
    current_data, linewidth_data, wavelength_data, power_meter_avg_data = [], [], [], []
    rf_freq_max_data, rf_pow_max_data = [], []
    rf_freq_mid_data, rf_pow_mid_data = [], []
    rf_freq_min_data, rf_pow_min_data = [], []
    osa_peak_wave_big_data, osa_peak_ampl_big_data = [], []
    osa_peak_wave_small_data, osa_peak_ampl_small_data = [], []
    voltage_prev=-1
    current_prev=-1
    delay_prev=-1
    linewidth_prev=-1
    wavelength_prev=-1
    for idx, (voltage, current, delay, linewidth, wavelength) in enumerate(params, 1):

        # === Построение карт при смене напряжения ===
        if current_voltage_batch is not None and voltage != current_voltage_batch:
            _build_voltage_maps(current_voltage_batch, main_folder, collected_data)
        current_voltage_batch = voltage

        rf_folder_name = (f"voltage_{voltage}V/rf_measurements/current_{current}mA")
        osa_folder_name = (f"voltage_{voltage}V/osa_measurements/current_{current}mA")
        rf_full_path = os.path.join(main_folder, rf_folder_name)
        osa_full_path = os.path.join(main_folder, osa_folder_name)
        

        # === НАСТРОЙКА ОБОРУДОВАНИЯ ===
        voltage_next=voltage
        if voltage_prev!=voltage_next:
            ut.set_voltage(voltage=voltage)
            voltage_prev=voltage_next
        
        current_next=current
        if current_prev!=current_next:
            LD.set_current(current=current)
            current_prev=current_next
        
        delay_next=delay
        if delay_prev!=delay_next:
            odl.set_time_delay(time_delay=delay)
            delay_prev=delay_next


        linewidth_next=linewidth
        if linewidth_prev!=linewidth_next:
            btf.set_linewidth(linewidth)
            linewidth_prev=linewidth_next
        
        wavelength_next=wavelength
        if wavelength_prev!=wavelength_next:
            btf.set_wavelength(wavelength)
            wavelength_prev=wavelength_next
        
        time.sleep(1)
        

        # === ИЗМЕРЕНИЯ ===
        power_meter_avg = measure_average_power(pm_device=pm_device)
        
        
        base_filename=f"delay_{delay}ps_linewidth{linewidth}nm_wavelength{wavelength}nm_"
        

        rf_freq_max, rf_pow_max = rf_measurement(
            rf_device=rf_device, N=NUMBER_RF_MEASURE, folder_path=rf_full_path,
            filename=base_filename+'rf_max_span', rf_rbw=RF_RBW_MAX,
            f_start=RF_F_START_MAX, f_stop=RF_F_STOP_MAX, save_png=True)

        
        rf_freq_mid, rf_pow_mid = rf_measurement(
            rf_device=rf_device, N=NUMBER_RF_MEASURE, folder_path=rf_full_path,
            filename=base_filename+'rf_middle_span', rf_rbw=RF_RBW_MIDDLE,f_span=RF_SPAN_MIDDLE,f_center=rf_freq_max, save_png=True)

        
        rf_freq_min, rf_pow_min = rf_measurement(
            rf_device=rf_device, N=NUMBER_RF_MEASURE, folder_path=rf_full_path,
            filename=base_filename+'rf_min_span', rf_rbw=RF_RBW_MIN,
           f_center=rf_freq_mid, f_span=RF_SPAN_MIN,save_png=True)

        osa_peak_wave_big, osa_peak_ampl_big = osa_measurement(
            osa_devices=osa, folder_path=osa_full_path, filename=base_filename+'osa_big_span',
            res=OSA_RES_BIG_SPAN, wave_start='1510nm', wave_stop='1570nm', save_png=True)

        osa_peak_wave_small, osa_peak_ampl_small = osa_measurement(
            osa_devices=osa, folder_path=osa_full_path, filename=base_filename+'osa_small_span',
            res=OSA_RES_SMALL_SPAN, wave_start=osa_peak_wave_big-linewidth,
            wave_stop=osa_peak_wave_big+linewidth, save_png=True)


        # === НАКОПЛЕНИЕ ДАННЫХ ===
        idx_data.append(idx)
        time_data.append(datetime.now())
        voltage_data.append(voltage)
        delay_data.append(delay)
        current_data.append(current)
        linewidth_data.append(linewidth)
        wavelength_data.append(wavelength)
        power_meter_avg_data.append(power_meter_avg)
        rf_freq_max_data.append(rf_freq_max)
        rf_pow_max_data.append(rf_pow_max)
        rf_freq_mid_data.append(rf_freq_mid)
        rf_pow_mid_data.append(rf_pow_mid)
        rf_freq_min_data.append(rf_freq_min)
        rf_pow_min_data.append(rf_pow_min)
        osa_peak_wave_big_data.append(osa_peak_wave_big)
        osa_peak_ampl_big_data.append(osa_peak_ampl_big)
        osa_peak_wave_small_data.append(osa_peak_wave_small)
        osa_peak_ampl_small_data.append(osa_peak_ampl_small)

        # === Заполнение буфера для карт ===
        collected_data['voltage'].append(voltage)
        collected_data['current'].append(current)
        collected_data['delay'].append(delay)
        collected_data['rf_freq_max'].append(rf_freq_max)
        collected_data['rf_pow_max'].append(rf_pow_max)
        collected_data['rf_freq_mid'].append(rf_freq_mid)
        collected_data['rf_pow_mid'].append(rf_pow_mid)
        collected_data['rf_freq_min'].append(rf_freq_min)
        collected_data['rf_pow_min'].append(rf_pow_min)
        collected_data['power_meter_avg'].append(power_meter_avg)


        

    # === Построение карт для ПОСЛЕДНЕГО напряжения ===
    if current_voltage_batch is not None:
        _build_voltage_maps(current_voltage_batch, main_folder, collected_data)

    
    idx_arr = [idx_data, 'number']
    time_arr = [time_data, 'time']
    voltage_arr = [voltage_data, 'voltage_V']
    delay_arr = [delay_data, 'delay_ps']
    current_arr = [current_data, 'current_mA']
    power_meter_avg_arr = [power_meter_avg_data, 'power_meter_avg_mW']
    linewidth_arr = [linewidth_data, 'linewidth_nm']
    wavelength_arr = [wavelength_data, 'wavelength_nm']
    rf_freq_max_arr = [rf_freq_max_data, 'rf_peak_freq_max_GHz']
    rf_pow_max_arr = [rf_pow_max_data, 'rf_peak_power_max_dBm']
    rf_freq_mid_arr = [rf_freq_mid_data, 'rf_peak_freq_middle_GHz']
    rf_pow_mid_arr = [rf_pow_mid_data, 'rf_peak_power_middle_dBm']
    rf_freq_min_arr = [rf_freq_min_data, 'rf_peak_freq_min_GHz']
    rf_pow_min_arr = [rf_pow_min_data, 'rf_peak_power_min_dBm']
    osa_peak_wave_big_arr = [osa_peak_wave_big_data, 'osa_peak_wave_big_nm']
    osa_peak_ampl_big_arr = [osa_peak_ampl_big_data, 'osa_peak_ampl_big_dBm']
    osa_peak_wave_small_arr = [osa_peak_wave_small_data, 'osa_peak_wave_small_nm']
    osa_peak_ampl_small_arr = [osa_peak_ampl_small_data, 'osa_peak_ampl_small_dBm']

    write_arrays_excel(
        idx_arr, time_arr, voltage_arr, delay_arr,
        current_arr, linewidth_arr, wavelength_arr, power_meter_avg_arr,
        rf_freq_max_arr, rf_pow_max_arr,
        rf_freq_mid_arr, rf_pow_mid_arr,
        rf_freq_min_arr, rf_pow_min_arr,
        osa_peak_wave_big_arr, osa_peak_ampl_big_arr,
        osa_peak_wave_small_arr, osa_peak_ampl_small_arr,
        folder_path=main_folder, filename='results.xlsx')  


if __name__ == "__main__":
    main()
