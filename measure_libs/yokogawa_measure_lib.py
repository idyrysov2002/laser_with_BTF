import time
import numpy as np
from typing import Tuple, Optional
from scripts.write_arrays_to_txt import write_arrays_txt
from scripts.plot_and_save_xy import plot_and_save_xy
from scripts.create_folder import create_multiple_subfolders
from config import PARAM_LABELS

def yoko_measurement(device, save_folder_path: str, filename: str, folder_structure: str,
                   res: float,
                   wave_start: str, 
                   wave_stop: str, save_png=True):
    # Формируем новую путь
    new_folder_structure=f'yokogawa_measurements/{folder_structure}'
    new_save_folder_path=create_multiple_subfolders(parent_folder=save_folder_path,folder_structure=new_folder_structure)

    # Формируем новое имя файла
    new_filename=f"yokogawa_spectrum_{filename}"
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
    peak_intensity = float(ampl_arr[max_index])

    # Записываем данные в .txt файл

    x_label = PARAM_LABELS['wavelength_nm']
    y_label = PARAM_LABELS['intensity_dBm']
    save_list_x=[wave_arr,x_label]
    save_list_y=[ampl_arr,y_label]

    write_arrays_txt(
        save_list_x, save_list_y, folder_path=new_save_folder_path, filename=new_filename
    )
    png_title=f"Peak Power: {peak_intensity:..4f}μW,Wavelength(Peak power): {peak_wave}nm"
    if save_png is not None:
        plot_and_save_xy(
            x=wave_arr,
            y=ampl_arr,
            title=png_title,
            folder_path=new_save_folder_path,
            xlabel=x_label,
            ylabel=y_label,
            filename=new_filename,
            show_plot=False,
        )
    return {'peak_wave':float(peak_wave),'peak_intensity':float(peak_intensity)}
