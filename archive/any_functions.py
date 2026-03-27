import numpy as np
import matplotlib.pyplot as plt
import os
import  time
import datetime
from matplotlib import rcParams
from matplotlib.ticker import AutoMinorLocator 
import itertools
from pathlib import Path

# # Импорт утилит
# from scripts.write_arrays_to_excel import write_arrays_excel
# from scripts.create_map_and_save import create_map_and_save

# # Импорт библиотек измерений
# from devices.yokogawa.osa_measure_lib import osa_measurement
# from devices.rsa_device.rf_measure_lib import rf_measurement

# # Импорт драйверов (Симуляторы)
# from mock_devices.btf_100_Simulator import BTF100Simulator as BTF100
# from mock_devices.CLD1015_Simulator import CLD1015Simulator as CLD1015
# from mock_devices.OpticDelayLine_Simulator import OpticDelayLineSimulator as OpticDelayLine
# from mock_devices.PMDevicePM100D_Simulator import PMDevicePM100DSimulator as PMDevicePM100D, measure_average_power
# from mock_devices.RF306B_Simulator import RF306BSimulator as RF306B
# from mock_devices.VoltageDriverUT3005Simulator import VoltageDriverUT3005Simulator as VoltageDriverUT3005
# from mock_devices.OSA_Yokogawa_new_Simulator import OSA_Yokogawa_new_Simulator as OSA_Yokogawa_new

# Импорт настроек из config.py
from config import (
    INSTRUMENTS, SCAN_SEQUENCE,
    VOLTAGES, CURRENTS, DELAYS, LINEWIDTH, WAVELENGTH,
    NUMBER_RF_MEASURE, RF_RBW_MAX, RF_F_START_MAX, RF_F_STOP_MAX,
    RF_RBW_MIDDLE, RF_SPAN_MIDDLE, RF_RBW_MIN, RF_SPAN_MIN,
    OSA_RES_BIG_SPAN, OSA_RES_SMALL_SPAN,
    FILENAME_PARAM_ORDER, PARAM_NAMES, PARAM_UNITS
)

PARAM_TO_DEVICE = {
    'voltage': 'ut',
    'current': 'ld',
    'delay': 'odl',
    'linewidth': 'btf',
    'wavelength': 'btf'
}

PARAM_TO_LIST = {
    'voltage': VOLTAGES,
    'current': CURRENTS,
    'delay': DELAYS,
    'linewidth': LINEWIDTH,
    'wavelength': WAVELENGTH
}





def time_prefix():
    """
    Генерирует строку с текущей датой и временем в формате 'Month-DD-YYYY_time_HH-MM-SS'.

    Returns:
        str: Строка с временной меткой, например: 'February-03-2026_time_14-30-45'.
    """
    timestamp = datetime.datetime.now().strftime("%B-%d-%Y_time_%H-%M-%S")
    return timestamp



def get_scan_iterator(instruments_cfg, sequence, param_to_device, param_to_list):
    """Генерирует итератор и список активных параметров на основе конфига."""
    active_lists = []
    active_params = []

    print("=== ПЛАН СКАНИРОВАНИЯ ===")
    for param_name in sequence:
        device_key = param_to_device.get(param_name)
        if device_key and instruments_cfg.get(device_key, {}).get("enabled"):
            if param_name in param_to_list:
                active_lists.append(param_to_list[param_name])
                active_params.append(param_name)
                print(
                    f"[ВКЛ] {param_name:12} -> {len(param_to_list[param_name])} значений (Прибор: {device_key})"
                )
            else:
                print(f"[WARN] Параметр {param_name} указан, но нет списка значений!")
        else:
            print(f"[ПРОП] {param_name:12} (Прибор {device_key} отключен)")
    print("===========================\n")

    if not active_lists:
        return itertools.product([None]), []
    return itertools.product(*active_lists), active_params





def shutdown_instruments(devices):
    """
    Корректно отключает все активные приборы.
    """
    print("\n=== ОТКЛЮЧЕНИЕ ПРИБОРОВ ===")

    if "ld" in devices:
        try:
            devices["ld"].turn_off_laser()
            time.sleep(0.5)
            devices["ld"].turn_off_tec()
            print("[OK] LD (OFF)")
        except Exception as e:
            print(f"[WARN] LD shutdown failed: {e}")

    if "ut" in devices:
        try:
            devices["ut"].set_voltage(0)
            time.sleep(0.5)
            devices["ut"].turn_off()
            print("[OK] UT (OFF)")
        except Exception as e:
            print(f"[WARN] UT shutdown failed: {e}")

    if "odl" in devices:
        try:
            devices["odl"].set_time_delay(0)
            devices["odl"].close()
            print("[OK] ODL (CLOSED)")
        except Exception as e:
            print(f"[WARN] ODL shutdown failed: {e}")

    if "btf" in devices:
        try:
            devices["btf"].set_linewidth(0)
            devices["btf"].close()
            print("[OK] BTF (CLOSED)")
        except Exception as e:
            print(f"[WARN] BTF shutdown failed: {e}")

    for name in ["osa", "rf", "pm"]:
        if name in devices:
            try:
                if hasattr(devices[name], "close"):
                    devices[name].close()
                print(f"[OK] {name.upper()} (CLOSED)")
            except Exception as e:
                print(f"[WARN] {name.upper()} shutdown failed: {e}")

    print("===========================\n")


def get_active_params(instruments_cfg, sequence, param_to_device):
    """Возвращает список активных параметров на основе включенных приборов."""
    active_params = []
    for param_name in sequence:
        device_key = param_to_device.get(param_name)
        if device_key and instruments_cfg.get(device_key, {}).get("enabled"):
            active_params.append(param_name)
    return active_params


def build_filename_params(current_settings, active_params, param_units, param_names):
    """Строит строку параметров для имени файла."""
    parts = []
    for param in active_params:
        if param in current_settings:
            value = current_settings[param]
            unit = param_units.get(param, "")
            name = param_names.get(param, param)
            parts.append(f"{name}_{value}{unit}")
    return "_".join(parts)


def build_folder_structure(main_folder, current_settings, active_params, param_units):
    """Строит иерархию папок на основе активных параметров."""
    folder_path = Path(main_folder)
    for param in active_params[:2]:
        if param in current_settings:
            value = current_settings[param]
            unit = param_units.get(param, "")
            folder_name = f"{param}_{value}{unit}"
            folder_path = folder_path / folder_name
    folder_path.mkdir(parents=True, exist_ok=True)
    return folder_path


def get_scan_iterator(instruments_cfg, sequence, param_to_device, param_to_list):
    """Генерирует итератор и список активных параметров на основе конфига."""
    active_lists = []
    active_params = []

    print("=== ПЛАН СКАНИРОВАНИЯ ===")
    for param_name in sequence:
        device_key = param_to_device.get(param_name)
        if device_key and instruments_cfg.get(device_key, {}).get("enabled"):
            if param_name in param_to_list:
                active_lists.append(param_to_list[param_name])
                active_params.append(param_name)
                print(
                    f"[ВКЛ] {param_name:12} -> {len(param_to_list[param_name])} значений (Прибор: {device_key})"
                )
            else:
                print(f"[WARN] Параметр {param_name} указан, но нет списка значений!")
        else:
            print(f"[ПРОП] {param_name:12} (Прибор {device_key} отключен)")
    print("===========================\n")

    if not active_lists:
        return itertools.product([None]), []
    return itertools.product(*active_lists), active_params
