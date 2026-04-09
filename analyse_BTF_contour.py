from pathlib import Path
import numpy as np

from scripts.read_from_txt import read_txt_xy
from scripts.plot_and_save_xy import plot_and_save_xy

def contour():
    filter_folder=r'C:\Users\namys_23hvwev\Documents\DATA\data_from_lnf\filter_BTF100\linewidth_1nm'
    soa_folder=r'C:\Users\namys_23hvwev\Documents\DATA\data_from_lnf\SOA_BTF100\linewidth_1nm'

    for wave in range(1525,1566):
        filter_full_path = Path(filter_folder)/rf'yokogawa_spectrum_filter_wavelengh_{wave}nm_linewidth_1nm_current_300mA.txt'
        sao_full_path=Path(soa_folder)/rf'yokogawa_spectrum_SOA_wavelengh_{wave}nm_linewidth_1nm_current_300mA.txt'
        sao_wave_arr, sao_pow_arr = read_txt_xy(full_path=sao_full_path)
        filter_wave_arr, filter_pow_arr = read_txt_xy(full_path=filter_full_path)

        ratio_pow=filter_pow_arr/sao_pow_arr

        max_index=np.argmax(ratio_pow)
        peak_ratio_pow = float(ratio_pow[max_index])

        ratio_pow=ratio_pow/peak_ratio_pow

        mask = (sao_wave_arr > 1520) & (sao_wave_arr < 1570)
        x_plot = sao_wave_arr[mask] 
        y_plot = ratio_pow[mask] 



    