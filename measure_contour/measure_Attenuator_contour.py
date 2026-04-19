from measure_libs.yokogawa_measure_lib import yoko_measurement
from devices.yokogawa.Yokogawa_OSA import YokogawaOSA
from devices.cdl_1015.CLD1015 import CLD1015
from scripts.create_folder import create_date_folder 
from devices.ut_3005.VoltageDriverUT3005 import VoltageDriverUT3005
import numpy as np
def main():
    CURRENTS=[300]
    VOLTAGES=np.arange(0, 6.1, 0.2)
    
    try:
        yoko=YokogawaOSA()
        
        ld=CLD1015()
        ld.turn_on_all()
        
        
        ut = VoltageDriverUT3005('COM8')
        ut.turn_on()
        
        main_path="Z:/data_for_laser_with_BTF"
        folder_prefix='Attenuator'
        
        save_folder_path=create_date_folder(base_path=main_path, prefix=folder_prefix)
        for current in CURRENTS:
            
            ld.set_current(current=current)
            
            for voltage in VOLTAGES:
                
                ut.set_voltage(voltage=voltage)
                
                
                    
                base_file_name=f'Attenuator_voltage_{voltage}V_current_{current}mA'
                base_folder_structure=f''
                yoko_measurement(
                                device=yoko, 
                                save_folder_path=save_folder_path, 
                                filename=base_file_name, 
                                folder_structure=base_folder_structure,
                                save_png=True)
    finally:
        yoko.close_connect()
        ld.turn_off_all()
        
                    
if __name__=="__main__":
    main()
            
