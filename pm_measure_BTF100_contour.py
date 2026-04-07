from measure_libs.yokogawa_measure_lib import yoko_measurement
from devices.yokogawa.Yokogawa_OSA import YokogawaOSA
from devices.cdl_1015.CLD1015 import CLD1015
from devices.btf_100.btf_100 import BTF100
from scripts.create_folder import create_date_folder 
from devices.pm_400.PMDevice import PMDevicePM100D, measure_average_power
from scripts.plot_and_save_xy import plot_and_save_xy
from scripts.write_arrays_to_txt import write_arrays_txt

def main():
    
    try:
        pm_device=PMDevicePM100D()
        
        ld=CLD1015()
        ld.turn_on_all()
        
        btf=BTF100(port="COM11")
        
        main_path="Z:/data_for_laser_with_BTF"
        folder_prefix='PM'
        
        save_folder_path=create_date_folder(base_path=main_path, prefix=folder_prefix)
        for current in [300]:
            
            ld.set_current(current=current)
            
            for linewidth in [1]:
                
                btf.set_linewidth(linewidth=linewidth)
                
                pm_data, wavelengh_data=[],[]
                
                for wavelengh in range(1525, 1566, 1):
                    
                    btf.set_wavelength(wavelength=wavelengh)
                    pm_data.append(measure_average_power(pm_device=pm_device,duration=3,aver_point=5))
                    wavelengh_data.append(wavelengh)
                plot_and_save_xy(
                    x=wavelengh_data, 
                    y=pm_data, 
                    title=f'data from filter, power meter, current {current}mA, linewidth {linewidth}nm', 
                    xlabel='Wavelength, nm', 
                    ylabel='Power, mW', 
                  folder_path=save_folder_path, 
                  filename=f'filter_power_meter_current_{current}mA_linewidth_{linewidth}nm', show_plot=False
                )
                x_arr=[wavelengh_data, 'Wavelength, nm']
                y_arr=[pm_data, 'Power, mW']
                write_arrays_txt(x_arr, y_arr, folder_path=save_folder_path, filename=f'filter_power_meter_current_{current}mA_linewidth_{linewidth}nm')                 
                    
                    
                    
                    
    finally:
        pm_device.disconnect()
        ld.turn_off_all()
                    
if __name__=="__main__":
    main()
            
