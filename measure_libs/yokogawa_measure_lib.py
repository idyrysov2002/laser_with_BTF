import time
import numpy as np
from typing import Tuple, Optional
from scripts.write_arrays_to_txt import write_arrays_txt
from scripts.plot_and_save_xy import plot_and_save_xy


def osa_measurement(osa_devices, folder_path: str, filename: str, 
                   res: float,
                   wave_start: str, 
                   wave_stop: str, save_png=None) -> Tuple[float, float]:
    # Установка разрешения
    osa_devices.set_resolution(res)

    # Установка диапазона длин волн
    osa_devices.set_start(wave_start)   
    osa_devices.set_stop(wave_stop)

    # Получение данных
    wave_arr, ampl_arr = osa_devices.get_os()

    # Находим пиковые значения
    max_index = np.argmax(ampl_arr)
    peak_wave = float(wave_arr[max_index])
    peak_intensity = float(ampl_arr[max_index])

    # Записываем данные в .txt файл

    x_label = "Wavelength (nm)"
    y_label = "Intensity (dBm) "
    save_list_x=[wave_arr,x_label]
    save_list_y=[ampl_arr,y_label]
    write_arrays_txt(
        save_list_x, save_list_y, folder_path=folder_path, filename=filename
    )
    png_title=f"Peak intensity: {peak_intensity:..2f}dBm, Wavelength(Peak intensity): {peak_wave:..2f}nm"
    if save_png is not None:
        plot_and_save_xy(
            x=wave_arr,
            y=ampl_arr,
            title=png_title,
            folder_path=folder_path,
            xlabel=x_label,
            ylabel=y_label,
            filename=filename,
            show_plot=False,
        )
    return {'peak_wave':float(peak_wave),'peak_intensity':float(peak_intensity)}
