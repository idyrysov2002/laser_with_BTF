import itertools
import os
import time
import numpy as np
import csv
import logging
from datetime import datetime

# Импорт драйверов приборов
from yokogawa.OSA_Yokogawa_new import OSA_Yokogawa_new
from any_functions import create_data_folder, write_xy_to_txt
from btf_100.btf_100 import BTF100
from rsa_device.rf_measure_lib import rf_measurement
from rsa_device.RF306B import RF306B 
from odl_650.OpticDelayLine import OpticDelayLine
from ut_3005.VoltageDriverUT3005 import VoltageDriverUT3005
from cdl_1015.CLD1015 import CLD1015
from PMDevice import PMDevicePM100D

# Импорт констант и списков параметров
from config import *

# ========================
# НАСТРОЙКА ЛОГГЕРА
# ========================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("experiment.log", encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ========================
# ИНИЦИАЛИЗАЦИЯ ПРИБОРОВ
# ========================
logger.info("Инициализация приборов...")
try:
    odl = OpticDelayLine('COM6')
    btf = BTF100(port="COM3")
    osa = OSA_Yokogawa_new()
    rf_device = RF306B()
    LD = CLD1015()
    ut = VoltageDriverUT3005('COM8')
    pm_device = PMDevicePM100D()
    logger.info("Все приборы успешно инициализированы.")
except Exception as e:
    logger.error(f"Ошибка инициализации приборов: {e}")
    raise e

# ========================
# ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
# ========================

def measure_average_power(pm_device):
    """Измеряет мощность 3 раза и возвращает среднее в мВт"""
    duration = 1
    aver_point = 3
    power_values = []
    for _ in range(aver_point):
        try:
            power = pm_device.get_power()
            power_values.append(power)
            time.sleep(duration / aver_point)
        except Exception as e:
            logger.warning(f"Ошибка измерения мощности PM: {e}")
            power_values.append(0.0)
    
    if not power_values:
        return 0.0
        
    avg_pm_power = np.mean(power_values) * 1000  # перевод в мВт
    return float(avg_pm_power)

def run_rf_sequence(run_index, folder_path):
    """
    Выполняет полный цикл РФ измерений (Max -> Middle -> Min Span).
    run_index: номер прогона (1, 2, 3) для именования файлов.
    Возвращает: (peak_freq_min, peak_power_min)
    """
    try:
        # 1. БОЛЬШОЙ СПАН
        file_name_max = f'rf_run_{run_index}_max_span'
        peak_freq_max, peak_power_max = rf_measurement(
            rf_device=rf_device, N=NUMBER_RF_MEASURE, folder_path=folder_path,
            txt_filename=file_name_max, f_start=RF_F_START_MAX, f_stop=RF_F_STOP_MAX
        )
        
        # 2. СРЕДНИЙ СПАН
        RF_F_START_MIDDLE = peak_freq_max - RF_SPAN_MIDDLE / 2
        RF_F_STOP_MIDDLE = peak_freq_max + RF_SPAN_MIDDLE / 2
        file_name_middle = f'rf_run_{run_index}_middle_span'
        peak_freq_middle, peak_power_middle = rf_measurement(
            rf_device=rf_device, N=NUMBER_RF_MEASURE, folder_path=folder_path,
            txt_filename=file_name_middle, f_start=RF_F_START_MIDDLE, f_stop=RF_F_STOP_MIDDLE
        )
        
        # 3. МАЛЕНЬКИЙ СПАН
        RF_F_START_MIN = peak_freq_middle - RF_SPAN_MIN / 2
        RF_F_STOP_MIN = peak_freq_middle + RF_SPAN_MIN / 2
        file_name_min = f'rf_run_{run_index}_min_span'
        peak_freq_min, peak_power_min = rf_measurement(
            rf_device=rf_device, N=NUMBER_RF_MEASURE, folder_path=folder_path,
            txt_filename=file_name_min, f_start=RF_F_START_MIN, f_stop=RF_F_STOP_MIN
        )
        
        return peak_freq_min, peak_power_min
    except Exception as e:
        logger.error(f"Ошибка в RF последовательности (прогон {run_index}): {e}")
        return None, None

def run_osa_sequence(run_index, folder_path, linewidth):
    """
    Выполняет полный цикл OSA измерений (Wide -> Narrow Span).
    run_index: номер прогона (1, 2) для именования файлов.
    Возвращает: (peak_wavelength, peak_power)
    """
    try:
        # 1. ШИРОКИЙ СПАН
        YOKO_l_START_WIDE = "1510nm"
        YOKO_l_STOP_WIDE = "1570nm"
        osa.set_start(YOKO_l_START_WIDE)
        osa.set_stop(YOKO_l_STOP_WIDE)
        time.sleep(0.5) # Небольшая задержка на установку
        x_wide, y_wide = osa.get_os()
        
        filename_wide = f'osa_run_{run_index}_wide_span'
        write_xy_to_txt(X=x_wide, Y=y_wide, x_label='Длина волны, нм', y_label='Мощность', 
                        folder_path=folder_path, file_name=filename_wide)
        
        # Поиск пика для узкого спана
        if len(y_wide) == 0:
            logger.warning("OSA Wide Span: нет данных")
            return None, None

        max_index = np.argmax(y_wide)
        peak_x_wide = float(x_wide[max_index])
        
        # 2. УЗКИЙ СПАН
        F_CENTER = peak_x_wide
        YOKO_l_START_NARROW = F_CENTER - linewidth
        YOKO_l_STOP_NARROW = F_CENTER + linewidth
        
        osa.set_start(YOKO_l_START_NARROW)
        osa.set_stop(YOKO_l_STOP_NARROW)
        time.sleep(0.5)
        x_narrow, y_narrow = osa.get_os()
        
        filename_narrow = f'osa_run_{run_index}_narrow_span'
        write_xy_to_txt(X=x_narrow, Y=y_narrow, x_label='Длина волны, нм', y_label='Мощность', 
                        folder_path=folder_path, file_name=filename_narrow)
        
        if len(y_narrow) == 0:
            return peak_x_wide, float(y_wide[max_index]) # Вернуть данные широкого, если узкий пуст

        max_index_narrow = np.argmax(y_narrow)
        return float(x_narrow[max_index_narrow]), float(y_narrow[max_index_narrow])
        
    except Exception as e:
        logger.error(f"Ошибка в OSA последовательности (прогон {run_index}): {e}")
        return None, None

def init_summary_file(filepath):
    """Создает заголовок CSV файла, если он не существует"""
    if not os.path.exists(filepath):
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                'Timestamp', 'Voltage', 'Current', 'Delay', 'Linewidth', 'Wavelength',
                'RF_Freq_Avg', 'RF_Power_Avg', 'OSA_Wavelength_Avg', 'OSA_Power_Avg', 'PM_Power_mW'
            ])

def write_summary_row(filepath, data_dict):
    """Дописывает строку результатов в CSV"""
    with open(filepath, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            data_dict['timestamp'],
            data_dict['voltage'],
            data_dict['current'],
            data_dict['delay'],
            data_dict['linewidth'],
            data_dict['wavelength'],
            data_dict['rf_freq_avg'],
            data_dict['rf_power_avg'],
            data_dict['osa_wl_avg'],
            data_dict['osa_power_avg'],
            data_dict['pm_power']
        ])

# ========================
# ОСНОВНОЙ ЦИКЛ ЭКСПЕРИМЕНТА
# ========================

def main():
    main_folder_path = create_data_folder(prefix='laser_with_BTF')
    summary_path = os.path.join(main_folder_path, 'summary.csv')
    init_summary_file(summary_path)
    
    logger.info(f"Папка эксперимента: {main_folder_path}")
    logger.info(f"Начало перебора параметров. Всего комбинаций: {len(VOLTAGES)*len(CURRENTS)*len(DELAYS)*len(LINEWIDTH)*len(WAVELENGTH)}")

    # Генерируем все возможные комбинации параметров
    params_combinations = itertools.product(VOLTAGES, CURRENTS, DELAYS, LINEWIDTH, WAVELENGTH)
    
    # Счетчик для логов
    total_combinations = len(VOLTAGES)*len(CURRENTS)*len(DELAYS)*len(LINEWIDTH)*len(WAVELENGTH)
    current_combo = 0

    try:
        for voltage, current, delay, linewidth, wavelength in params_combinations:
            current_combo += 1
            
            # 1. Формируем путь и проверяем, не измерено ли уже (Resume)
            folder_name = (
                f"voltage_{voltage}/"
                f"current_{current}/"
                f"delay_{delay}/"
                f"btf_linewidth_{linewidth}/"
                f"wavelength_{wavelength}"
            )
            full_path = os.path.join(main_folder_path, folder_name)
            
            if os.path.exists(full_path):
                # Проверяем, есть ли уже файл summary с такими параметрами (упрощенная проверка)
                # Лучше проверять наличие файлов внутри, но для скорости проверим папку
                # Если папка есть и в ней есть файлы rf_run_3_min_span.txt, значит готово
                check_file = os.path.join(full_path, 'rf_run_3_min_span.txt')
                if os.path.exists(check_file):
                    logger.info(f"[{current_combo}/{total_combinations}] Пропущено (уже измерено): {folder_name}")
                    continue
            
            logger.info(f"[{current_combo}/{total_combinations}] Измерение: V={voltage}, I={current}, D={delay}, LW={linewidth}, WL={wavelength}")
            
            # 2. Создаем папку
            os.makedirs(full_path, exist_ok=True)

            # 3. Настраиваем оборудование
            try:
                ut.set_voltage(voltage=voltage)
                time.sleep(1)
                LD.set_current(current=current)
                time.sleep(1)
                odl.set_time_delay(time_delay=delay)
                time.sleep(1)
                btf.set_linewidth(linewidth)
                time.sleep(1)
                btf.set_wavelength(wavelength)
                time.sleep(1)
            except Exception as e:
                logger.error(f"Ошибка установки параметров приборов: {e}")
                continue

            # 4. ИЗМЕРЕНИЕ РФА (3 прогона)
            rf_freqs = []
            rf_powers = []
            for i in range(1, 4): # 1, 2, 3
                logger.debug(f"  РФА прогон {i}/3...")
                freq, power = run_rf_sequence(run_index=i, folder_path=full_path)
                if freq is not None:
                    rf_freqs.append(freq)
                    rf_powers.append(power)
                time.sleep(0.5) # Пауза между прогонами
            
            rf_freq_avg = np.mean(rf_freqs) if rf_freqs else 0.0
            rf_power_avg = np.mean(rf_powers) if rf_powers else 0.0

            # 5. ИЗМЕРЕНИЕ OSA (2 прогона)
            osa_wls = []
            osa_powers = []
            for i in range(1, 3): # 1, 2
                logger.debug(f"  OSA прогон {i}/2...")
                wl, power = run_osa_sequence(run_index=i, folder_path=full_path, linewidth=linewidth)
                if wl is not None:
                    osa_wls.append(wl)
                    osa_powers.append(power)
                time.sleep(0.5)
            
            osa_wl_avg = np.mean(osa_wls) if osa_wls else 0.0
            osa_power_avg = np.mean(osa_powers) if osa_powers else 0.0

            # 6. ИЗМЕРЕНИЕ ОПТИЧЕСКОЙ МОЩНОСТИ (PM)
            pm_power = measure_average_power(pm_device)

            # 7. СОХРАНЕНИЕ В СВОДНУЮ ТАБЛИЦУ
            data = {
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'voltage': voltage,
                'current': current,
                'delay': delay,
                'linewidth': linewidth,
                'wavelength': wavelength,
                'rf_freq_avg': rf_freq_avg,
                'rf_power_avg': rf_power_avg,
                'osa_wl_avg': osa_wl_avg,
                'osa_power_avg': osa_power_avg,
                'pm_power': pm_power
            }
            write_summary_row(summary_path, data)
            
            logger.info(f"  -> Завершено. RF Freq: {rf_freq_avg:.2f}, OSA WL: {osa_wl_avg:.2f}, PM: {pm_power:.2f} мВт")

    except KeyboardInterrupt:
        logger.warning("Эксперимент прерван пользователем (Ctrl+C)")
    except Exception as e:
        logger.error(f"Критическая ошибка эксперимента: {e}")
    finally:
        logger.info("Эксперимент завершен. Файлы сохранены.")
        

if __name__ == "__main__":
    main()