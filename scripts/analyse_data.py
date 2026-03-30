from pathlib import Path
from tqdm import tqdm
from create_map_and_save import create_map_and_save
from create_folder import create_date_folder, create_multiple_subfolders
from slice_current import slice_current
from read_from_txt import read_txt_xyz, read_txt_xy
from plot_and_save_xy import plot_and_save_xy
from copy_files import copy_files
from create_plot_grid import create_plot_grid
from plot_histogram_grid import plot_histogram_grid
import sys
import os
import numpy as np
from plot_histogram_and_save import plot_histogram_and_save
from calculate_FWHM_dBm import calculate_FWHM_dBm
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
        


def slise_data():
    main_folder=main_folder=r'C:\Users\namys_23hvwev\Documents\DATA\data_for_testing\analysis_data_March-30-2026_time_17-55-28'
    for wavelengh in tqdm([1530, 1540, 1550, 1560], desc="wavelengh"):
        for voltage in tqdm([0,1,2,3,4,5], desc="voltage"):
            
            
            save_folder_path=create_multiple_subfolders(parent_folder=main_folder,folder_structure=f'wavelengh_{wavelengh}nm/voltage_{voltage}V')
            folder_path=fr'C:\Users\namys_23hvwev\Documents\DATA\data_for_testing\analysis_data_March-30-2026_time_17-55-28\wavelengh_{wavelengh}nm\voltage_{voltage}V'
            filename1='map_freq_rf_with_filtr_0.5GHz.txt'
            filename2='mean_freq.txt'
            filename3='rf_freq_span_6.2GHz.txt'
            full_path1 = Path(folder_path) / filename1
            full_path2 = Path(folder_path) / filename2
            full_path3 = Path(folder_path) / filename3

            current_data, delay_data, freq_data_filtr=read_txt_xyz(full_path=full_path1,header=1)
            current_data, delay_data, freq_data_mean=read_txt_xyz(full_path=full_path2,header=1)
            current_data, delay_data, freq_data_without_filtr=read_txt_xyz(full_path=full_path3,header=1)


            
            for sl_current in [300, 400]:
                delay_arr_filtr, freq_arr_filtr=slice_current(slice_current=sl_current,current_arr=current_data, delay_arr=delay_data, freq_arr=freq_data_filtr)
                delay_arr_mean, freq_arr_mean=slice_current(slice_current=sl_current,current_arr=current_data, delay_arr=delay_data, freq_arr=freq_data_mean)
                delay_arr_without_filtr, freq_arr_without_filtr=slice_current(slice_current=sl_current,current_arr=current_data, delay_arr=delay_data, freq_arr=freq_data_without_filtr)
                data_list_filtr=([delay_arr_filtr, 'Delay, ps'], [freq_arr_filtr, 'Frequency, GHz'], 'RF, frequency after filter 0.5 GHz')
                data_list_mean=([delay_arr_mean, 'Delay, ps'], [freq_arr_mean, 'Frequency, GHz'], 'OSC')
                data_list_without_filtr=([delay_arr_without_filtr, 'Delay, ps'], [freq_arr_without_filtr, 'Frequency, GHz'], 'RF')
                data_list=[data_list_filtr,data_list_mean,data_list_without_filtr]
                create_plot_grid(
                    data_list=data_list, 
                    save_folder_path=save_folder_path, 
                    png_filename=f'slice_current_{sl_current}mA', 
                     main_title=f"Slice, Current {sl_current}mA, Voltage {voltage}V, Wavelength {wavelengh}nm", 
                     show_plot=False

                )

def create_histigram_map():
    main_folder=r'C:\Users\namys_23hvwev\Documents\DATA\data_for_testing\analysis_data_March-30-2026_time_17-55-28'
    for wavelengh in tqdm([1530, 1540, 1550, 1560], desc="wavelengh"):
        for voltage in tqdm([0,1,2,3,4,5], desc="voltage"):
            
            
            save_folder_path=create_multiple_subfolders(parent_folder=main_folder,folder_structure=f'wavelengh_{wavelengh}nm/voltage_{voltage}V')
            folder_path=fr'C:\Users\namys_23hvwev\Documents\DATA\data_for_testing\analysis_data_March-30-2026_time_17-55-28\wavelengh_{wavelengh}nm\voltage_{voltage}V'
            filename1='map_freq_rf_with_filtr_0.5GHz.txt'
            filename2='mean_freq.txt'
            filename3='rf_freq_span_6.2GHz.txt'
            full_path1 = Path(folder_path) / filename1
            full_path2 = Path(folder_path) / filename2
            full_path3 = Path(folder_path) / filename3

            current_data, delay_data, freq_data_filtr=read_txt_xyz(full_path=full_path1,header=1)
            current_data, delay_data, freq_data_mean=read_txt_xyz(full_path=full_path2,header=1)
            current_data, delay_data, freq_data_without_filtr=read_txt_xyz(full_path=full_path3,header=1)

            bins=50
            data_list_1=[freq_data_filtr,'RF, frequency after filter 0.5 GHz']
            data_list_2=[freq_data_mean,'OSC']
            data_list_3=[freq_data_without_filtr,'RF']
            data_list=[data_list_1,data_list_2,data_list_3]
            plot_histogram_grid(data_list=data_list, 
                                x_label="Частота, ГГц", 
                                y_label="Кол-во, шт", 
                                save_folder_path=save_folder_path, 
                                png_filename=f'histogram_voltage_{voltage}V_wavelength_{wavelengh}nm', 
                                main_title='Распределение частоты', 
                                bins=bins, 
                                show_plot=False)
            
           






def get_freq_from_txt_with_filtr():
    main_folder=r'C:\Users\namys_23hvwev\Documents\DATA\data_for_testing\analysis_data_March-30-2026_time_17-55-28'
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
                                title=f"The map after filtering the RF data, Voltage_{voltage}V, Wavelength_{wavelengh}nm", 
                                folder_path=save_folder_path, 
                                filename='map_freq_rf_with_filtr_0.5GHz', 
                                show_plot=False)



def calculate_FWHM():
    save_folder_prefix='analys_FWHM'
    main_folder=create_date_folder(base_path=r'C:\Users\namys_23hvwev\Documents\DATA\data_for_testing',prefix=save_folder_prefix)
    for wavelength in [1525, 1550, 1565]:
        for span in ['big', 'small']:
            for linewidth in range(1,18,2):
                filepath=rf"C:\Users\namys_23hvwev\Documents\DATA\data_for_testing\usefull_data\osa_data_March-14-2026_time_19-03-30\osa_{span}_span_wavelength_{wavelength}nm_linewidth_{linewidth}nm.txt"
                wave_arr, intensity_arr=read_txt_xy(full_path=filepath,header=1)
                # print(type(wave_arr))
                

                calculate_FWHM_dBm(
                    x_arr=wave_arr, 
                    y_arr=intensity_arr, 
                    png_filename=f'calculate_FWHM_wavelength_{wavelength}nm_{span}_span_linewidth_{linewidth}', 
                    save_folder_path=main_folder
                    )



def copy_data():
    save_folder_prefix='analysis_data'
    main_folder=create_date_folder(base_path=r'C:\Users\namys_23hvwev\Documents\DATA\data_for_testing',prefix=save_folder_prefix)
    for wavelengh in tqdm([1530, 1540, 1550, 1560], desc="wavelengh"):
        for voltage in tqdm([0,1,2,3,4,5], desc="voltage"):
            old_folder_path=rf'C:\Users\namys_23hvwev\Documents\DATA\data_from_lnf\laser_with_btf_March-27-2026_time_14-22-55\rf_measurements\maps\wavelength_{wavelengh}nm\voltage_{voltage}V'
            new_folder_path=fr'C:\Users\namys_23hvwev\Documents\DATA\data_for_testing\analysis_data_March-30-2026_time_17-55-28\wavelengh_{wavelengh}nm\voltage_{voltage}V'
            filename1='rf_freq_span_6.2GHz.png'
            filename2='rf_freq_span_6.2GHz.txt'
            copy_files(
                    filename1, filename2,old_folder_path=old_folder_path,
                    new_folder_path=new_folder_path)



if __name__=="__main__":
    create_histigram_map()











    


