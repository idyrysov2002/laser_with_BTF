from pathlib import Path
from tqdm import tqdm
from scripts.create_map_and_save import create_map_and_save
from scripts.create_folder import create_date_folder, create_multiple_subfolders
from scripts.slice_current import slice_current
from scripts.read_from_txt import read_txt_xyz, read_txt_xy
from scripts.plot_and_save_xy import plot_and_save_xy
from scripts.copy_files import copy_files
from scripts.create_plot_grid import create_plot_grid
from scripts.plot_histogram_grid import plot_histogram_grid
import sys
import os
import numpy as np
from scripts.plot_histogram_and_save import plot_histogram_and_save
from scripts.calculate_FWHM_dBm import calculate_FWHM_dBm
from scripts.get_OSC_data_from_txt import get_OSC_data_from_txt
# Получаем путь к текущему файлу
current_dir = os.path.dirname(os.path.abspath(__file__))
# Получаем путь к родительской папке (где лежит config)
parent_dir = os.path.dirname(current_dir)

# Добавляем родительскую папку в пути поиска модулей
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Теперь этот импорт сработает
from config import PARAM_LABELS




def create_map():
   
    for wave in [1530, 1540, 1550]:
        for voltage in range(6):
            freq_data, current_data, delay_data =[],[],[]
            for current in range (100, 301, 50):
                for delay in range(0, 331, 10):
                    folder_path = rf'C:\Users\namys_23hvwev\Documents\DATA\data_from_lnf\laser_with_btf_March-31-2026_time_17-03-39\rf_measurements\wavelength_{wave}nm\voltage_{voltage}V\current_{current}mA\span_6.2GHz\measurement_number_1'
                    filename = rf'rf_spectrum_delay_{delay}ps_current_{current}mA_voltage_{voltage}V_wavelength_{wave}nm_span_6.2GHz_measurement_number_1.txt'
                    full_path=Path (folder_path)/filename
                    freq_arr, power_arr=read_txt_xy(full_path=full_path,header=1)
                    threshold_freq=0.2

                    mask = freq_arr >= threshold_freq
                    filtered_freq_arr = freq_arr[mask]
                    filtered_power_arr = power_arr[mask]

                    max_index = np.argmax(filtered_power_arr)
                    peak_power = float(filtered_power_arr[max_index])
                    peak_freq = float(filtered_freq_arr[max_index])

                    freq_data.append(peak_freq)
                    current_data.append(current)
                    delay_data.append(delay)
            x_arr = [current_data, 'Current, mA']
            y_arr = [delay_data, 'Delay, ps']
            z_arr = [freq_data, 'Frequency, GHz']
            create_map_and_save(x_arr=x_arr, 
                                y_arr=y_arr, 
                                z_arr=z_arr, 
                                title=f'Map from RF, freq>{threshold_freq}GHz wavelength_{wave}nm, voltage_{voltage}V', 
                                folder_path=rf'C:\Users\namys_23hvwev\Documents\DATA\data_from_lnf\laser_with_btf_March-31-2026_time_17-03-39\maps\wavelength_{wave}nm\voltage_{voltage}V', 
                                filename='map_rf_with_filter', 
                                show_plot=False)
create_map()






