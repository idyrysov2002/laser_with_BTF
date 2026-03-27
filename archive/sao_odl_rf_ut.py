import itertools
import os
import sys
import time
import logging
import numpy as np
from datetime import datetime
from pathlib import Path
from tqdm import tqdm

# Импорт настроек
from config import *

# Импорт библиотек измерений и построения
from any_functions import create_data_folder
from write_arrays_to_excel import write_arrays_excel
from create_map_and_save import create_map_and_save

# Импорт драйверов
from devices.rsa_device.rf_measure_lib import rf_measurement
from devices.rsa_device.RF306B import RF306B
from devices.odl_650.OpticDelayLine import OpticDelayLine
from devices.ut_3005.VoltageDriverUT3005 import VoltageDriverUT3005
from devices.cdl_1015.CLD1015 import CLD1015
from devices.pm_400.PMDevice import PMDevicePM100D, measure_average_power

# ================= КОНФИГУРАЦИЯ =================
# Время стабилизации после изменения параметров (сек)
SETTLING_TIME = 1.0 
# Интервал автосохранения (шагов)
AUTOSAVE_INTERVAL = 10 
# =================================================

def setup_logging(main_folder):
    """Настройка логирования в файл и консоль"""
    log_file = Path(main_folder) / "experiment.log"
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    return logging.getLogger(__name__)

def _build_voltage_maps(voltage, main_folder, data_buf):
    """Построение тепловых карт для заданного напряжения"""
    plot_subfolder = Path(main_folder) / f"voltage_{voltage}V" / "maps"
    plot_subfolder.mkdir(parents=True, exist_ok=True)
    
    mask = np.array(data_buf['voltage']) == voltage
    if not np.any(mask):
        return

    x = np.array(data_buf['current'])[mask]
    y = np.array(data_buf['delay'])[mask]
    
    maps_config = [
        (data_buf['rf_freq_max'], 'rf_freq_max', 'Частота, ГГц (max span)'),
        (data_buf['rf_pow_max'],  'rf_pow_max',  'Мощность, дБм (max span)'),
        (data_buf['rf_freq_mid'], 'rf_freq_mid', 'Частота, ГГц (mid span)'),
        (data_buf['rf_pow_mid'],  'rf_pow_mid',  'Мощность, дБм (mid span)'),
        (data_buf['rf_freq_min'], 'rf_freq_min', 'Частота, ГГц (min span)'),
        (data_buf['rf_pow_min'],  'rf_pow_min',  'Мощность, дБм (min span)'),
        (data_buf['power_meter_avg'], 'power_meter_avg', 'Мощность, mW'),
    ]
    
    for z_raw, fname_suffix, z_label in maps_config:
        z = np.array(z_raw)[mask]
        # Проверка на пустые данные
        if len(z) == 0:
            continue
        try:
            create_map_and_save(
                x_arr=[x.tolist(), "Ток, мА"],
                y_arr=[y.tolist(), "Задержка, пс"],
                z_arr=[z.tolist(), z_label],
                title=f"U = {voltage}В, {z_label}",
                folder_path=plot_subfolder,
                filename=f"RF_{fname_suffix}",
                show_plot=False
            )
        except Exception as e:
            logging.error(f"Ошибка построения карты {fname_suffix}: {e}")

def save_intermediate_excel(data_lists, main_folder, filename='results_temp.xlsx'):
    """Сохранение промежуточных результатов в Excel"""
    try:
        idx_arr = [data_lists['idx'], 'number']
        time_arr = [data_lists['time'], 'time']
        voltage_arr = [data_lists['voltage'], 'voltage_V']
        delay_arr = [data_lists['delay'], 'delay_ps']
        current_arr = [data_lists['current'], 'current_mA']
        power_meter_avg_arr = [data_lists['power_meter_avg'], 'power_meter_avg_mW']
        rf_freq_max_arr = [data_lists['rf_freq_max'], 'rf_peak_freq_max_GHz']
        rf_pow_max_arr = [data_lists['rf_pow_max'], 'rf_peak_power_max_dBm']
        rf_freq_mid_arr = [data_lists['rf_freq_mid'], 'rf_peak_freq_middle_GHz']
        rf_pow_mid_arr = [data_lists['rf_pow_mid'], 'rf_peak_power_middle_dBm']
        rf_freq_min_arr = [data_lists['rf_freq_min'], 'rf_peak_freq_min_GHz']
        rf_pow_min_arr = [data_lists['rf_pow_min'], 'rf_peak_power_min_dBm']
       

        write_arrays_excel(
            idx_arr, time_arr, voltage_arr, delay_arr,
            current_arr, power_meter_avg_arr,
            rf_freq_max_arr, rf_pow_max_arr,
            rf_freq_mid_arr, rf_pow_mid_arr,
            rf_freq_min_arr, rf_pow_min_arr,
            folder_path=main_folder, filename=filename
        )
    except Exception as e:
        logging.warning(f"Не удалось сохранить промежуточный Excel: {e}")
        

def main():
    # Создаем папку ДО инициализации приборов для логов
    main_folder = create_data_folder(prefix='laser_with_BTF')
    logger = setup_logging(main_folder)
    logger.info(f"Начало эксперимента. Папка: {main_folder}")

    try:
        # === ИНИЦИАЛИЗАЦИЯ ПРИБОРОВ ===
        logger.info("Инициализация приборов...")
        
        
        odl = OpticDelayLine('COM12')
        odl.go_to_home_position()
        
        rf_device = RF306B()
        LD = CLD1015()
        LD.turn_on_all()

        ut = VoltageDriverUT3005('COM8')
        ut.turn_on()

        pm_device = PMDevicePM100D()
        logger.info("Все приборы инициализированы")

        # === Подготовка данных ===
        params = list(itertools.product(VOLTAGES, CURRENTS, DELAYS))
        total_steps = len(params)
        logger.info(f"Всего шагов измерений: {total_steps}")

        # Буфер данных (словарь списков)
        data_lists = {
            'idx': [], 'time': [], 'voltage': [], 'current': [], 'delay': [],
            'linewidth': [], 'wavelength': [], 'power_meter_avg': [],
            'rf_freq_max': [], 'rf_pow_max': [], 'rf_freq_mid': [], 'rf_pow_mid': [],
            'rf_freq_min': [], 'rf_pow_min': [],
        }

        current_voltage_batch = None
        # Переменные для отслеживания состояния приборов
        state = {
            'voltage': -1, 'current': -1, 'delay': -1, 
            'linewidth': -1, 'wavelength': -1
        }

        # === ЦИКЛ ИЗМЕРЕНИЙ ===
        for idx, (voltage, current, delay) in enumerate(tqdm(params, desc="Измерение"), 1):
            
            # 1. Построение карт при смене напряжения
            if current_voltage_batch is not None and voltage != current_voltage_batch:
                logger.info(f"Построение карт для напряжения {current_voltage_batch}В...")
                _build_voltage_maps(current_voltage_batch, main_folder, data_lists)
            current_voltage_batch = voltage

            # 2. Пути к файлам
            rf_folder = Path(main_folder) / f"voltage_{voltage}V" / "rf_measurements" / f"current_{current}mA"
            rf_folder.mkdir(parents=True, exist_ok=True)
            

            # 3. Настройка оборудования (только если изменилось)
            if state['voltage'] != voltage:
                ut.set_voltage(voltage=voltage)
                state['voltage'] = voltage
                logger.debug(f"Напряжение установлено: {voltage}В")
            
            if state['current'] != current:
                LD.set_current(current=current)
                state['current'] = current
                logger.debug(f"Ток установлен: {current}мА")
            
            if state['delay'] != delay:
                odl.set_time_delay(time_delay=delay)
                state['delay'] = delay
            
            time.sleep(SETTLING_TIME)

            # 4. Измерения (с обработкой ошибок на каждом этапе)
            try:
                power_meter_avg = measure_average_power(pm_device=pm_device)
                
                base_filename = f"delay_{delay}ps_"

                rf_freq_max, rf_pow_max = rf_measurement(
                    rf_device=rf_device, N=NUMBER_RF_MEASURE, folder_path=rf_folder,
                    filename=base_filename+'rf_max_span', rf_rbw=RF_RBW_MAX,
                    f_start=RF_F_START_MAX, f_stop=RF_F_STOP_MAX, save_png=True)

                rf_freq_mid, rf_pow_mid = rf_measurement(
                    rf_device=rf_device, N=NUMBER_RF_MEASURE, folder_path=rf_folder,
                    filename=base_filename+'rf_middle_span', rf_rbw=RF_RBW_MIDDLE,
                    f_span=RF_SPAN_MIDDLE, f_center=rf_freq_max, save_png=True)

                rf_freq_min, rf_pow_min = rf_measurement(
                    rf_device=rf_device, N=NUMBER_RF_MEASURE, folder_path=rf_folder,
                    filename=base_filename+'rf_min_span', rf_rbw=RF_RBW_MIN,
                    f_center=rf_freq_mid, f_span=RF_SPAN_MIN, save_png=True)

               

            except Exception as e:
                logger.error(f"Ошибка измерения на шаге {idx}: {e}", exc_info=True)
                # Заполняем NaN, чтобы не сбить индексы
                power_meter_avg = np.nan
                rf_freq_max, rf_pow_max = np.nan, np.nan
                rf_freq_mid, rf_pow_mid = np.nan, np.nan
                rf_freq_min, rf_pow_min = np.nan, np.nan
                

            # 5. Накопление данных
            data_lists['idx'].append(idx)
            data_lists['time'].append(datetime.now())
            data_lists['voltage'].append(voltage)
            data_lists['current'].append(current)
            data_lists['delay'].append(delay)
            data_lists['power_meter_avg'].append(power_meter_avg)
            data_lists['rf_freq_max'].append(rf_freq_max)
            data_lists['rf_pow_max'].append(rf_pow_max)
            data_lists['rf_freq_mid'].append(rf_freq_mid)
            data_lists['rf_pow_mid'].append(rf_pow_mid)
            data_lists['rf_freq_min'].append(rf_freq_min)
            data_lists['rf_pow_min'].append(rf_pow_min)
           

            # 6. Промежуточное сохранение (защита от потери данных)
            if idx % AUTOSAVE_INTERVAL == 0:
                save_intermediate_excel(data_lists, main_folder)
                logger.info(f"Промежуточное сохранение на шаге {idx}/{total_steps}")

        # === ФИНАЛИЗАЦИЯ ===
        # Построение карт для ПОСЛЕДНЕГО напряжения
        if current_voltage_batch is not None:
            logger.info("Построение карт для последнего напряжения...")
            _build_voltage_maps(current_voltage_batch, main_folder, data_lists)

        # Финальное сохранение Excel
        logger.info("Сохранение финальных результатов...")
        save_intermediate_excel(data_lists, main_folder, filename='results.xlsx')
        
        logger.info("Эксперимент успешно завершен!")

    except KeyboardInterrupt:
        logger.warning("Эксперимент прерван пользователем (Ctrl+C)")
    except Exception as e:
        logger.critical(f"Критическая ошибка: {e}", exc_info=True)
    finally:
        # Гарантированное отключение приборов
        try:
            odl.disconnect()
            LD.turn_off_all()
            ut.out_off_and_close_COM()
            pm_device.disconnect()  
        except Exception as e:
            print(f"Ошибка при отключении: {e}")
        # Финальное сохранение даже при ошибке
        if 'data_lists' in locals() and data_lists['idx']:
            save_intermediate_excel(data_lists, main_folder, filename='results_FINAL.xlsx')
            logger.info("Данные сохранены в results_FINAL.xlsx")

if __name__ == "__main__":
    main()