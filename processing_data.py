from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from scripts.read_from_txt import read_txt_xy
from scripts.plot_histogram_and_save import plot_histogram_and_save
from scripts.plot_and_save_xy import plot_and_save_xy

folder_path = r'C:\Users\namys_23hvwev\Documents\DATA\yoko_spectrum\yokogawa_measurements'

wavelength_data = []
power_data = []

for x in range(150):
    # Ищем файл для конкретного x с любым временем
    pattern = f"yokogawa_spectrum_number_{x}_March-31-2026_time_*.txt"
    matching_files = list(Path(folder_path).glob(pattern))
    
    if matching_files:
        # Берем первый найденный файл (должен быть один)
        full_path = matching_files[0]
        
        wavelength_arr, power_arr = read_txt_xy(full_path=full_path)
        max_index = np.argmax(power_arr)
        peak_wavelength = float(wavelength_arr[max_index])
        peak_power = float(power_arr[max_index])
        wavelength_data.append(peak_wavelength)
        power_data.append(peak_power)
        
        print(f"x={x}: {full_path.name}")
    else:
        print(f"Предупреждение: файл для x={x} не найден")
        # Можно добавить заглушку, чтобы сохранить порядок
        wavelength_data.append(np.nan)
        power_data.append(np.nan)

plot_histogram_and_save(data=wavelength_data, bins=100, title=
                        'Гистограмма длины волны. За 147 измерений. Установленная длина 1530nm', 
                        xlabel='Длина волны, нм', ylabel=None,
                            folder_path=r'C:\Users\namys_23hvwev\Documents\DATA\yoko_spectrum', 
                            filename="histogram_wavelength", show_plot=None

)