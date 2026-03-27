import time
import numpy as np
import os
from typing import Tuple, Optional
from scripts.write_arrays_to_txt import write_arrays_txt
from scripts.plot_and_save_xy import plot_and_save_xy
from scripts.create_folder import create_multiple_subfolders


def osa_measurement(device, save_folder_path: str, folder_structure, filename: str, 
                   res: float,
                   wave_start: str, 
                   wave_stop: str, save_png=None):
    new_folder_structure=f'yokogawa_measurements/{folder_structure}/span_{wave_stop-wave_start}nm'
    new_filename=f'span_{wave_stop-wave_start}nm_{filename}'
    new_save_folder_path=create_multiple_subfolders(parent_folder=save_folder_path,folder_structure=new_folder_structure)

    # Установка разрешения
    device.set_resolution(res)

    # Установка диапазона длин волн
    device.set_start(wave_start)   
    device.set_stop(wave_stop)

    # Получение данных
    wave_arr, ampl_arr = device.get_os()

    # Находим пиковые значения
    max_index = np.argmax(ampl_arr)
    peak_wave = float(wave_arr[max_index])
    peak_ampl = float(ampl_arr[max_index])

    # Записываем данные в .txt файл

    x_label = "Wavelength (nm)"
    y_label = "Intensity (dBm) "
    save_list_x=[wave_arr,x_label]
    save_list_y=[ampl_arr,y_label]
    write_arrays_txt(
        save_list_x, save_list_y, folder_path=new_save_folder_path, filename=filename
    )

    if save_png is not None:
        plot_and_save_xy(
            x=wave_arr,
            y=ampl_arr,
            title=None,
            folder_path=new_save_folder_path,
            xlabel=x_label,
            ylabel=y_label,
            filename=filename,
            show_plot=False,
        )
    return float(peak_wave),float(peak_ampl)
