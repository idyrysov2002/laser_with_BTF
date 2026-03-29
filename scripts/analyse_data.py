from pathlib import Path
from tqdm import tqdm
from create_map_and_save import create_map_and_save
from create_folder import create_date_folder, create_multiple_subfolders
from slice_current import slice_current
from read_from_txt import read_txt_xyz, read_txt_xy
from plot_and_save_xy import plot_and_save_xy
import sys
import os
import numpy as np
from plot_histogram_and_save import plot_histogram_and_save
# Получаем путь к текущему файлу
current_dir = os.path.dirname(os.path.abspath(__file__))
# Получаем путь к родительской папке (где лежит config)
parent_dir = os.path.dirname(current_dir)

# Добавляем родительскую папку в пути поиска модулей
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Теперь этот импорт сработает
from config import PARAM_LABELS


def read_txt_values(txt_file_path: str):
    # Инициализируем словарь значениями None
    info = {
        'Value': None, 
        'Mean': None, 
        'Min': None, 
        'Max': None, 
        'St Dev': None, 
        'Count': None
    }
    
    keys_order = ['Value', 'Mean', 'Min', 'Max', 'St Dev', 'Count']

    with open(txt_file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
        for i, line in enumerate(lines):
            if i >= len(keys_order):
                break
                
            line = line.strip()
            if not line:
                continue
            
            try:
                parts = line.split()
                number = float(parts[-1])
                current_key = keys_order[i]
                
                # Сохраняем сразу число
                info[current_key] = number
                
            except (IndexError, ValueError):
                continue

    return info





def create_map():
    main_folder=create_date_folder(base_path=r'C:\Users\namys_23hvwev\Documents\DATA\data_for_testing',prefix='analyse_osc_data')
    for wavelengh in tqdm([1530, 1540, 1550, 1560], desc="wavelengh"):
        for voltage in tqdm([0,1,2,3,4,5], desc="voltage"):
            mean_data, std_data=[],[]
            current_data,delay_data=[],[]
            for current in [300,400]:
                for delay in range(0, 301,5):
                    save_folder_path=create_multiple_subfolders(parent_folder=main_folder,folder_structure=f'wavelengh_{wavelengh}nm/voltage_{voltage}V')
                    folder_path=fr'C:\Users\namys_23hvwev\Documents\DATA\data_from_lnf\laser_with_btf_March-27-2026_time_14-22-55\oscilloscope_measurements\wavelength_{wavelengh}nm\voltage_{voltage}V\current_{current}mA\average\hor_scale_500.0ps'
                    filename=fr'average_hor_scale_500.0ps_delay_{delay}ps_current_{current}mA_voltage_{voltage}V_wavelength_{wavelengh}nm.txt'
                    full_path = Path(folder_path) / filename




                    data=read_txt_values(txt_file_path=full_path)
                    mean_data.append(data['Mean'])
                    std_data.append(data['St Dev'])
                    current_data.append(current)
                    delay_data.append(delay)
            current_arr=[current_data, 'Current (mA)']
            delay_arr=[delay_data, "Delay (ps)"]
            std_arr=[std_data,'St Dev Frequency (GHz)' ]
            mean_arr=[mean_data,'Mean Frequency  (GHz)']

            create_map_and_save(x_arr=current_arr, y_arr=delay_arr, z_arr=mean_arr, 
                                title="A map from the oscilloscope data", 
                                folder_path=save_folder_path, 
                                filename='mean_freq', 
                                show_plot=False)
            
            create_map_and_save(x_arr=current_arr, y_arr=delay_arr, z_arr=std_arr, 
                                title="A map from the oscilloscope data", 
                                folder_path=save_folder_path, 
                                filename='std_freq', 
                                show_plot=False)
        
def slise_data_osc():
    main_folder=r'C:\Users\namys_23hvwev\Documents\DATA\data_for_testing\analyse_osc_data_March-29-2026_time_01-29-10'
    for wavelengh in tqdm([1530, 1540, 1550, 1560], desc="wavelengh"):
        for voltage in tqdm([0,1,2,3,4,5], desc="voltage"):
            
            
            save_folder_path=create_multiple_subfolders(parent_folder=main_folder,folder_structure=f'wavelengh_{wavelengh}nm/voltage_{voltage}V')
            folder_path=fr'C:\Users\namys_23hvwev\Documents\DATA\data_for_testing\analyse_osc_data_March-29-2026_time_01-29-10\wavelengh_{wavelengh}nm\voltage_{voltage}V'
            filename=fr'mean_freq.txt'
            full_path = Path(folder_path) / filename
            current_data, delay_data, freq_data=read_txt_xyz(full_path=full_path,header=1)
        #     print('\n')
        #     for x in range(len(delay_data)):

                
        #         print(freq_data[x],current_data[x],delay_data[x])
                
        #     break
        # break
            

            for sl_current in [300, 400]:
                delay_arr, freq_arr=slice_current(slice_current=sl_current,current_arr=current_data, delay_arr=delay_data, freq_arr=freq_data)
                plot_and_save_xy(x=delay_arr, 
                                 y=freq_arr, 
                                 title=f'OSC: cрез при токе {sl_current}mA', 
                                 xlabel='Delay, ps', 
                                 ylabel='Frequency, GHz',
                                 folder_path=save_folder_path, 
                                 filename=f'osc_slice_current_{sl_current}mA', 
                                 show_plot=False)

def slise_data_rf():
    main_folder=r'C:\Users\namys_23hvwev\Documents\DATA\data_for_testing\analyse_osc_data_March-29-2026_time_01-29-10'
    for wavelengh in tqdm([1530, 1540, 1550, 1560], desc="wavelengh"):
        for voltage in tqdm([0,1,2,3,4,5], desc="voltage"):
            
            
            save_folder_path=create_multiple_subfolders(parent_folder=main_folder,folder_structure=f'wavelengh_{wavelengh}nm/voltage_{voltage}V')
            folder_path=fr'C:\Users\namys_23hvwev\Documents\DATA\data_for_testing\analyse_osc_data_March-29-2026_time_01-29-10\wavelengh_{wavelengh}nm\voltage_{voltage}V'
            filename=fr'map_freq_rf_with_filtr_0.5GHz.txt'
            full_path = Path(folder_path) / filename
            current_data, delay_data, freq_data=read_txt_xyz(full_path=full_path,header=1)
            

            
            

            



            for sl_current in [300, 400]:
                delay_arr, freq_arr=slice_current(slice_current=sl_current,current_arr=current_data, delay_arr=delay_data, freq_arr=freq_data)

                
                x = 0
                
                delay_arr, freq_arr=np.array(delay_arr), np.array(freq_arr)
                mask = freq_arr >= x
                filtered_freq_arr = freq_arr[mask]
                filtered_delay_arr = delay_arr[mask]
                plot_and_save_xy(x=filtered_delay_arr, 
                                 y=filtered_freq_arr, 
                                 title=f'RF: Срез при токе {sl_current}mA', 
                                 xlabel='Delay, ps', 
                                 ylabel='Frequency, GHz',
                                 folder_path=save_folder_path, 
                                 filename=f'rf_slice_current_{sl_current}mA_data_after_filtr', 
                                 show_plot=False)

def create_histigram_rf_map():
    main_folder=r'C:\Users\namys_23hvwev\Documents\DATA\data_for_testing\analyse_osc_data_March-29-2026_time_01-29-10'
    for wavelengh in tqdm([1530, 1540, 1550, 1560], desc="wavelengh"):
        for voltage in tqdm([0,1,2,3,4,5], desc="voltage"):
            
            
            save_folder_path=create_multiple_subfolders(parent_folder=main_folder,folder_structure=f'wavelengh_{wavelengh}nm/voltage_{voltage}V')
            folder_path=fr'C:\Users\namys_23hvwev\Documents\DATA\data_from_lnf\laser_with_btf_March-27-2026_time_14-22-55\rf_measurements\maps\wavelength_{wavelengh}nm\voltage_{voltage}V'
            filename=fr'rf_freq_span_6.2GHz.txt'
            full_path = Path(folder_path) / filename
            current_data, delay_data, freq_data=read_txt_xyz(full_path=full_path,header=1)
            bins=50
            plot_histogram_and_save(data=freq_data,
                                    bins=bins, 
                                    title="Гистограмма Freq(Peak power). Данные с maps", 
                                    xlabel="Значения, ГГц", 
                                    ylabel='Частотность, шт',
                                    folder_path=save_folder_path, 
                                    filename='histogram', 
                                    show_plot=False)






def get_freq_from_txt_with_filtr():
    main_folder=r'C:\Users\namys_23hvwev\Documents\DATA\data_for_testing\analyse_osc_data_March-29-2026_time_01-29-10'
    for wavelengh in tqdm([1530, 1540, 1550, 1560], desc="wavelengh"):
        for voltage in tqdm([0,1,2,3,4,5], desc="voltage"):
            freq_data=[]
            current_data,delay_data=[],[]
            for current in [300,400]:
                for delay in range(0, 301,5):

                    save_folder_path=create_multiple_subfolders(parent_folder=main_folder,folder_structure=f'wavelengh_{wavelengh}nm/voltage_{voltage}V')
                    folder_path=fr'C:\Users\namys_23hvwev\Documents\DATA\data_from_lnf\laser_with_btf_March-27-2026_time_14-22-55\rf_measurements\wavelength_{wavelengh}nm\voltage_{voltage}V\current_{current}mA\span_6.2GHz\measurement_number_1'
                    filename=fr'rf_spectrum_delay_{delay}ps_current_{current}mA_voltage_{voltage}V_wavelength_{wavelengh}nm_span_6.2GHz_measurement_number_1.txt'
                    full_path = Path(folder_path) / filename
                    freq_arr, power_arr=read_txt_xy(full_path=full_path,header=1)
                    threshold_freq=0.5
                    mask = freq_arr >= threshold_freq
                    filtered_freq_arr = freq_arr[mask]
                    filtered_power_arr = power_arr[mask]

                    max_index = np.argmax(filtered_power_arr)
                    peak_power = float(filtered_power_arr[max_index])
                    peak_freq = float(filtered_freq_arr[max_index])

                    freq_data.append(peak_freq)
                    current_data.append(current)
                    delay_data.append(delay)
            current_arr_arr=[current_data, 'Current, mA']
            delay_arr_arr=[delay_data, "Delay, ps"]
            freq_arr_arr=[freq_data,'Frequency (Peak power), GHz' ]

            create_map_and_save(x_arr=current_arr_arr, y_arr=delay_arr_arr, z_arr=freq_arr_arr, 
                                title="the map after filtering the RF data", 
                                folder_path=save_folder_path, 
                                filename='map_freq_rf_with_filtr_0.5GHz', 
                                show_plot=False)
# get_freq_from_txt_with_filtr()

slise_data_rf()










    


