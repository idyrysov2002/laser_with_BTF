from measure_libs.yokogawa_measure_lib import yoko_measurement
from devices.yokogawa.Yokogawa_OSA import YokogawaOSA
from devices.cdl_1015.CLD1015 import CLD1015
from devices.btf_100.btf_100 import BTF100
from scripts.create_folder import create_date_folder 


def main():
    
    try:
        yoko=YokogawaOSA()
        
        ld=CLD1015()
        
        btf=BTF100(port="COM11")
        
        main_path="Z:/data_for_laser_with_BTF"
        folder_prefix='BTF100_contour'
        
        save_folder_path=create_date_folder(base_path=main_path, prefix=folder_prefix)
        for current in [400]:
            
            ld.set_current(current=current)
            
            for linewidth in range(1, 2,1):
                
                btf.set_linewidth(linewidth=linewidth)
                
                for wavelengh in range(1525, 1566, 1):
                    
                    btf.set_wavelength(wavelength=wavelengh)
                    
                    base_file_name=f'SOA_wavelengh_{wavelengh}nm_linewidth_{linewidth}nm_current_{current}mA'
                    base_folder_structure=f'current_{current}mA/linewidth_{linewidth}nm'
                    
                    yoko_measurement(device=yoko, 
                                    save_folder_path=save_folder_path, 
                                    filename=base_file_name, 
                                    folder_structure=base_folder_structure,
                                    res=0.05,
                                    wave_start=1350, 
                                    wave_stop=1700, 
                                    save_png=True)
    finally:
        yoko.close_connect()
        
                    
if __name__=="__main__":
    main()
            
