import numpy as np
from scripts.create_folder import create_multiple_subfolders
from scripts.write_arrays_to_txt import write_arrays_txt
from scripts.plot_and_save_xy import plot_and_save_xy
from scripts.calculate_smsr import calculate_smsr
from scripts.number_with_decimal_prefix import number_with_decimal_prefix
from config import PARAM_LABELS
def rf_measurement(rf_device, N: int, save_folder_path: str, filename: str,folder_structure,
                   rf_rbw: float, f_start=None, f_stop=None, 
                   f_span=None, f_center=None, rf_level=-20, save_png=None):
    """
    Выполняет серию из N измерений на RF устройстве.
    
    Требования к частоте:
    - Либо (f_start и f_stop)
    - Либо (f_center и f_span)
    """
    
    # Проверка корректности входных данных частоты
    has_start_stop = (f_start is not None and f_stop is not None)
    has_center_span = (f_center is not None and f_span is not None)
    
    if not has_start_stop and not has_center_span:
        raise ValueError("Необходимо задать либо пару (f_start, f_stop), либо пару (f_center, f_span)")
    
    # Нормализация параметров (чтобы в config_param ушли все значения)
    if has_center_span and not has_start_stop:
        # Есть центр и_span, считаем start/stop
        f_start = f_center - f_span / 2
        f_stop = f_center + f_span / 2
    elif has_start_stop and not has_center_span:
        # Есть start/stop, считаем центр и span
        f_center = (f_start + f_stop) / 2
        f_span = f_stop - f_start
            
    peak_powers_data = []
    peak_freqs_data = []
    smsr_data = []

    
    for i in range(N):
        
        # Собираем всю цепочку в одну строку
        full_structure = f"rf_measurements/{folder_structure}/span_{number_with_decimal_prefix(f_span)}Hz/measurement_number_{i+1}"
        
        # Создаем все папки сразу
        measurement_folder = create_multiple_subfolders(parent_folder=save_folder_path, folder_structure=full_structure)
        
        # имя txt, png файла
        measurement_file_name = 'rf_spectrum_'+filename + f"_span_{number_with_decimal_prefix(f_span)}Hz_measurement_number_{i+1}"
        
        try:
            #  Настройка устройства
            rf_device.set_span(f_span)
            rf_device.set_cf(f_center)
            rf_device.set_rbw(rf_rbw)
            rf_device.set_start(f_start)
            rf_device.set_stop(f_stop)
            rf_device.set_refLevel(rf_level)
            
            # Получение данных
            freqs, powers = rf_device.get_rf()
            
            # # удаляем первые точки
            # freqs, powers=freqs[10:], powers[10:]
            
            
            
            # Проверка на пустые данные
            if len(freqs) <= 1 or len(powers) <= 1:
                print(f"Измерение {i+1}: Пропущено (недостаточно данных).")
                return 0,0
            
            # Находим пиковые значения
            max_index = np.argmax(powers)
            peak_power = float(powers[max_index])
            peak_freq = float(freqs[max_index])
            smsr, smsr_info= calculate_smsr(freq_arr=freqs, peak_arr=powers)

            peak_powers_data.append(peak_power)
            peak_freqs_data.append(peak_freq)
            smsr_data.append(smsr)
    
            x_label = PARAM_LABELS['frequensy_GHz']
            y_label = PARAM_LABELS['power_dBm']
            
            
            # перевод на ГГц
            freqs=freqs/1e+9
            
            save_list_x = [freqs, x_label]
            save_list_y = [powers, y_label]

            peak_freq_GHz=peak_freq/1e+9
            png_title=f'Peak power: {peak_power:.2f}dBm, Freq(Peak power): {peak_freq_GHz:.2f}GHz, SMSR: {smsr:.2f}dB'

            # Сохраняем данные в созданную подпапку
            write_arrays_txt(save_list_x, save_list_y, folder_path=measurement_folder, filename=measurement_file_name)
            
            if save_png is not None:
                plot_and_save_xy(x=freqs, y=powers, title=png_title, 
                                folder_path=measurement_folder, xlabel=x_label, ylabel=y_label,
                                filename=measurement_file_name, show_plot=False)
                
            freqs,powers=[],[]
            
        except Exception as e:
            print(f"Измерение {i+1} failed with error: {e}")
            continue
    
    
    
    avg_peak_power = np.mean(peak_powers_data)
    avg_peak_freq = np.mean(peak_freqs_data)
    avg_smsr=np.mean(smsr_data)

    
    return {'peak_freq':float(avg_peak_freq), 'peak_power': float(avg_peak_power), 'smsr': float(avg_smsr)}