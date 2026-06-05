import numpy as np
from pathlib import Path
from scripts.read_from_txt import read_txt_xy
from scripts.create_map_and_save import create_map_and_save
from scripts.get_OSC_data_from_txt import get_OSC_data_from_txt
DELAYS=np.arange(0, 301, 5) # в ps
CURRENTS=np.arange(100, 501, 50) # в mA
LINEWIDTH=[1, 2, 18] # в nm
WAVELENGTH=[ 1530, 1540, 1550, 1560] # в nm

# def map_rf():
#     for linewidth in LINEWIDTH:
        
#         for wavelength in WAVELENGTH:
#             current_data, delay_data, freq_data=[],[],[]
#             png_title=f'RF: span=1MHz, WL={wavelength}nm, LW={linewidth}nm'
#             save_folder=rf'Z:\data_for_laser_with_BTF\laser_with_btf_cir_SN_26736318_after_coupler_April-25-2026_time_15-47-22\maps\linewidth_{linewidth}nm\wavelength_{wavelength}nm'
#             filename=f'map_rf_span_1MHz_wavelength_{wavelength}nm_linewidth_{linewidth}nm'
#             for current in CURRENTS:
                
#                 for delay in DELAYS:
#                     rf_folder=rf'Z:\data_for_laser_with_BTF\laser_with_btf_cir_SN_26736318_after_coupler_April-25-2026_time_15-47-22\rf_measurements\linewidth_{linewidth}nm\wavelength_{wavelength}nm\current_{current}mA\span_1MHz\measurement_number_1'
#                     rf_txt=rf"rf_delay_{delay}ps_current_{current}mA_wavelength_{wavelength}nm_linewidth_{linewidth}nm_span_1MHz_measurement_number_1.txt"
#                     full_path=Path(rf_folder)/rf_txt
                    
#                     freq_arr, pow_arr = read_txt_xy(full_path=full_path)
#                     freq_arr, pow_arr=np.array(freq_arr), np.array(pow_arr)
#                     max_index=np.argmax(pow_arr)
                    
#                     max_freq=freq_arr[max_index]
                    
#                     current_data.append(current)
#                     delay_data.append(delay)
#                     freq_data.append(max_freq)
            
#             x_arr=[current_data, 'Current, mA']
#             y_arr=[delay_data, 'Delay, ps']
#             z_arr=[freq_data, 'Frequency, GHz']
#             create_map_and_save(
#             x_arr=x_arr, 
#             y_arr=y_arr, 
#             z_arr=z_arr, 
#             title=png_title, 
#             folder_path=save_folder, 
#             filename=filename, 
#             show_plot=False
#             )
                
    
                
def map_osc():
    for linewidth in LINEWIDTH:
        
        for wavelength in WAVELENGTH:
            current_data, delay_data, freq_data=[],[],[]
            png_title=f'OSC: WL={wavelength}nm, LW={linewidth}nm'
            save_folder=rf'Z:\data_for_laser_with_BTF\laser_with_btf_cir_SN_26736318_after_coupler_April-25-2026_time_15-47-22\maps\linewidth_{linewidth}nm\wavelength_{wavelength}nm'
            filename=f'map_OSC_wavelength_{wavelength}nm_linewidth_{linewidth}nm'
            for current in CURRENTS:
                
                for delay in DELAYS:
                    osc_folder=rf'Z:\data_for_laser_with_BTF\laser_with_btf_cir_SN_26736318_after_coupler_April-25-2026_time_15-47-22\oscilloscope_measurements\linewidth_{linewidth}nm\wavelength_{wavelength}nm\current_{current}mA'
                    osc_txt=rf"oscilloscope_peakdetect_delay_{delay}ps_current_{current}mA_wavelength_{wavelength}nm_linewidth_{linewidth}nm.txt"
                    osc_full_path=Path(osc_folder)/osc_txt
                    
                    
                    osc_dict=get_OSC_data_from_txt(txt_file_path=osc_full_path)
                    mean_freq=osc_dict['Mean_GHz']
                    current_data.append(current)
                    delay_data.append(delay)
                    freq_data.append(mean_freq)
            
            x_arr=[current_data, 'Current, mA']
            y_arr=[delay_data, 'Delay, ps']
            z_arr=[freq_data, 'Frequency, GHz']
            create_map_and_save(
            x_arr=x_arr, 
            y_arr=y_arr, 
            z_arr=z_arr, 
            title=png_title, 
            folder_path=save_folder, 
            filename=filename, 
            show_plot=False
            )
map_osc()