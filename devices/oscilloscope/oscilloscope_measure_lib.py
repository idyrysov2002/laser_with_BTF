import time
import numpy as np
from scripts.write_arrays_to_txt import write_arrays_txt
from scripts.plot_and_save_xy import plot_and_save_xy
from scripts.create_folder import create_multiple_subfolders
from scripts.number_with_decimal_prefix import number_with_decimal_prefix
from config import OSCILLOSCOPE_MODES
from config import OSCILLOSCOPE_HOR_SCALES


def oscilloscope_measurement(device, save_folder_path, filename, folder_structure="voltage/current", channel=4, save_png=None):
    """ 
    folder_structure: строка вида "voltage" или "voltage/current" или "a/b/c/d"
    """
    # 1. Разбиваем строку на части
    subfolders_list = [x.strip() for x in folder_structure.split('/') if x.strip()]

    for mode in OSCILLOSCOPE_MODES:
        device.acquire_mode(mode)

        for hor_scale in OSCILLOSCOPE_HOR_SCALES:
            # Вычисляем префикс
            scale_prefix = number_with_decimal_prefix(hor_scale)
            new_folder_structure=f'oscilloscope_measurements/{folder_structure}/{mode}/hor_scale_{scale_prefix}s'

            # 3. Создаем папки (всю цепочку)
            measurement_folder = create_multiple_subfolders(parent_folder=save_folder_path, 
                                                            folder_structure=new_folder_structure)

            

            # Формируем имя файла
            osc_filename = f"{mode}_hor_scale_{scale_prefix}s_{filename}"

            # Изменение горизонтального масштаба
            device.horizontal_scale(hor_scale)

            # Получение данных
            time_arr, voltage_arr = device.get_oscilloscope_data(channel=channel)
            time_arr, voltage_arr = np.array(time_arr), np.array(voltage_arr)

            # Перевод на ns
            time_arr = time_arr * 1e9
            x_label = "Time (ns)"
            y_label = "Voltage (V)"

            save_list_x = [time_arr, x_label]
            save_list_y = [voltage_arr, y_label]

            # Запись TXT
            write_arrays_txt(
                save_list_x,
                save_list_y,
                folder_path=measurement_folder,
                filename=osc_filename,
            )

            # Запись PNG (если нужно)
            if save_png is not None:
                plot_and_save_xy(
                    x=time_arr,
                    y=voltage_arr,
                    title=None,
                    folder_path=measurement_folder,
                    xlabel=x_label,
                    ylabel=y_label,
                    filename=osc_filename,
                    show_plot=False,
                )

            # Очистка памяти
            del time_arr, voltage_arr