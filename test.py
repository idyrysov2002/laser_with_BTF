from pathlib import Path
import numpy as np
from scripts.create_folder import create_date_folder
from scripts.read_from_txt import read_txt_xyz
from scripts.plot_and_save_xy import plot_and_save_xy
import matplotlib.pyplot as plt
from scripts.create_map_and_save import create_map_and_save
from scripts.get_OSC_data_from_txt import get_OSC_data_from_txt

def filter_map_osc():
    
    
    for wavelength in [1530, 1540, 1550, 1560]:
        save_folder=rf'Z:\data_for_laser_with_BTF\useful_DATA\laser_with_btf_cir_SN_26736318_after_coupler_April-18-2026_time_15-38-09\maps\wavelength_{wavelength}nm'
        current_data, delay_data, freq_data=[],[],[]
        for current in range(100, 501, 20):
            for delay in range(0, 331, 10): 
               
                folder_path=rf'Z:\data_for_laser_with_BTF\useful_DATA\laser_with_btf_cir_SN_26736318_after_coupler_April-18-2026_time_15-38-09\oscilloscope_measurements\wavelength_{wavelength}nm\current_{current}mA'
                file_name=rf'oscillogram_average_duration_10ns_delay_{delay}ps_current_{current}mA_wavelength_{wavelength}nm_linewidth_1nm.txt'
                full_path=Path(folder_path)/file_name
                osc_dict=get_OSC_data_from_txt(txt_file_path=full_path)
                
                freq=osc_dict['Mean_GHz']
                
                current_data.append(current)
                delay_data.append(delay)
                freq_data.append(freq)
        freq_arr = np.array(freq_data)
        freq_mask= np.where(freq_arr > 2.4, np.nan, freq_arr)
        x_arr=[current_data, 'Current, mA']
        y_arr=[delay_data, 'Delay, ps']
        z_arr=[freq_mask, 'Frequency, GHz']
        create_map_and_save(
        x_arr=x_arr, 
        y_arr=y_arr, 
        z_arr=z_arr, 
        title=f'OSC: LW=1nm, WL={wavelength}nm', 
        folder_path=save_folder, 
        filename=f'osc_after_mask_linewidth_1nm_wavelength_{wavelength}nm', 
        show_plot=True
        )
        
                
filter_map_osc()