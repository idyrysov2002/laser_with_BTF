from pathlib import Path
import numpy as np

from scripts.read_from_txt import read_txt_xy
from scripts.plot_and_save_xy import plot_and_save_xy


def soa_power_integer():
    save_folder=r'C:\Users\namys_23hvwev\Documents\DATA\data_from_lnf\analysis_data_April-07-2026_time_00-43-48'
    soa_folder=r'C:\Users\namys_23hvwev\Documents\DATA\data_from_lnf\SOA_BTF100\linewidth_1nm'
    wave_data, power_data = [],[]
    for wavelengt in range(1525, 1566):
        soa_full_path = Path(soa_folder)/rf'yokogawa_spectrum_SOA_wavelengh_{wavelengt}nm_linewidth_1nm_current_300mA.txt'

        wave_arr, power_arr = read_txt_xy(full_path=soa_full_path)

        sum_power = np.sum(power_arr)
        wave_data.append(wavelengt)
        power_data.append(sum_power)
    
    plot_and_save_xy(
        x=wave_data, 
        y=power_data, 
        title='SOA, $\sum_i power_i$', 
        xlabel="Wavelength, nm", 
        ylabel='Power, mW', 
        folder_path=r'C:\Users\namys_23hvwev\Documents\DATA\data_from_lnf\analysis_data_April-07-2026_time_00-43-48', 
        filename='SOA_sum_power_i', 
        show_plot=True
    )


def filter_power_integer():
    save_folder=r'C:\Users\namys_23hvwev\Documents\DATA\data_from_lnf\analysis_data_April-07-2026_time_00-43-48'
    filter_folder=r'C:\Users\namys_23hvwev\Documents\DATA\data_from_lnf\filter_BTF100\linewidth_1nm'
    wave_data, power_data = [],[]
    for wavelengt in range(1525, 1566):
        soa_full_path = Path(filter_folder)/rf'yokogawa_spectrum_filter_wavelengh_{wavelengt}nm_linewidth_1nm_current_300mA.txt'

        wave_arr, power_arr = read_txt_xy(full_path=soa_full_path)

        sum_power = np.sum(power_arr)
        wave_data.append(wavelengt)
        power_data.append(sum_power)
    
    plot_and_save_xy(
        x=wave_data, 
        y=power_data, 
        title='filter, $\sum_i power_i$', 
        xlabel="Wavelength, nm", 
        ylabel='Power, mW', 
        folder_path=save_folder, 
        filename='filter_sum_power_i', 
        show_plot=True
    )






if __name__=='__main__':
    filter_power_integer()

