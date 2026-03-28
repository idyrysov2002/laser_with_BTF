import time
import numpy as np
from typing import Tuple, Optional, Dict, Any
from scripts.write_arrays_to_txt import write_arrays_txt
from scripts.plot_and_save_xy import plot_and_save_xy
from scripts.create_folder import create_subfolder, create_multiple_subfolders
from scripts.number_with_decimal_prefix import number_with_decimal_prefix
from config import OSC_MODES, PARAM_LABELS, GIGA, OSC_HOR_SCALES



def oscilloscope_measurement(device, save_folder_path, filename, folder_structure="folder_1/folder_2", channel=4, save_png=None):
    # Создаем словарь для сохранения статистики
    results = {}
    for mode in OSC_MODES:
        device.acquire_mode(mode)

        for hor_scale in OSC_HOR_SCALES:
            # Изменение горизонтального масштаба
            device.horizontal_scale(hor_scale)
            
            # Вычисляем префикс
            scale_prefix = number_with_decimal_prefix(hor_scale)
            
            new_folder_structure=f'oscilloscope_measurements/{folder_structure}/{mode}/hor_scale_{scale_prefix}s'
            
            # Создаем вложенные папки
            measurement_folder = create_multiple_subfolders(parent_folder=save_folder_path,folder_structure=new_folder_structure)

            # Формируем имя файла
            osc_filename = f"{mode}_hor_scale_{scale_prefix}s_{filename}"

            # Получение данных
            time_arr, voltage_arr = device.get_oscilloscope_data(channel=channel)
            time_arr, voltage_arr = np.array(time_arr), np.array(voltage_arr)
            
            # Измерение частоты
            stats = device.measure_freq_stats(4)
            png_title = (
                        f"{mode.upper()}, "
                        f"Value: {stats['value_GHz']:.2f}GHz, "
                        f"Mean: {stats['mean_GHz']:.2f}GHz, "
                        f"Min: {stats['min_GHz']:.2f}GHz, "
                        f"Max: {stats['max_GHz']:.2f}GHz, "
                        f"St Dev: {stats['stddev_GHz']:.2f}GHz, "
                        f"Count: {stats['count']}"
                        )
            
            
            header_1=f'Value, GHz\t{stats['value_GHz']}'
            header_2=f'Mean, GHz\t{stats['mean_GHz']}'
            header_3=f'Min, GHz\t{stats['min_GHz']}'
            header_4=f'Max, GHz\t{stats['max_GHz']}'
            header_5=f'St Dev, GHz\t{stats['stddev_GHz']}'
            header_6=f'Count\t{stats['count']}'
            header_lines=[header_1,header_2,header_3,header_4,header_5,header_6]

            # Перевод на ns
            time_arr = time_arr * GIGA
            x_label = PARAM_LABELS['time_ns']
            y_label = PARAM_LABELS['voltage_V']

            save_list_x = [time_arr, x_label]
            save_list_y = [voltage_arr, y_label]

            # Запись TXT
            write_arrays_txt(
                save_list_x,
                save_list_y,
                folder_path=measurement_folder,
                filename=osc_filename,
                header_lines=header_lines
            )

            # Запись PNG (если нужно)
            if save_png is not None:
                plot_and_save_xy(
                    x=time_arr,
                    y=voltage_arr,
                    title=png_title,
                    folder_path=measurement_folder,
                    xlabel=x_label,
                    ylabel=y_label,
                    filename=osc_filename,
                    show_plot=False,
                )
            # Сохраняем результат в словарь
            key = (mode, hor_scale)
            results[key] = {'stats': stats}

    return results

        
            
            