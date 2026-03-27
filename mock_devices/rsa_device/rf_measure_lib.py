import numpy as np
from any_functions import create_subfolder
from scripts.write_arrays_to_txt import write_arrays_txt
from scripts.plot_and_save_xy import plot_and_save_xy

def rf_measurement(rf_device, N: int, folder_path: str, filename: str,
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
            
    peak_powers = []
    peak_freqs = []

    for i in range(N):
        # Создаем подпапку для конкретного измерения
        measurement_folder = create_subfolder(folder_path, f'MeasurementNumber_{i+1}') 
        filename_with_number = filename + f"_{i+1}"
        
        try:
            #  Настройка устройства
            rf_device.set_span(f_span)
            rf_device.set_cf(f_center)
            rf_device.set_rbw(rf_rbw)
            rf_device.set_start(f_start)
            rf_device.set_stop(f_stop)
            
            # Получение данных
            freqs, powers = rf_device.get_rf()
            
            # удаляем первые 3 точки
            freqs, powers=freqs[3:], powers[3:]
            
            
            
            # Проверка на пустые данные
            if len(freqs) <= 1 or len(powers) <= 1:
                print(f"Измерение {i+1}: Пропущено (недостаточно данных).")
                return 0,0
            
            # Находим пиковые значения
            max_index = np.argmax(powers)
            peak_power = float(powers[max_index])
            peak_freq = float(freqs[max_index])
            
            peak_powers.append(peak_power)
            peak_freqs.append(peak_freq)
            
            x_label = 'Frequency, GHz'
            y_label = 'Amplitude, dBm'
            
            
            # перевод на ГГц
            freqs=freqs/1e+9
            
            save_list_x = [freqs, x_label]
            save_list_y = [powers, y_label]

            # Сохраняем данные в созданную подпапку
            write_arrays_txt(save_list_x, save_list_y, folder_path=measurement_folder, filename=filename_with_number)
            
            if save_png is not None:
                plot_and_save_xy(x=freqs, y=powers, title='Radio frequency spectrum', 
                                folder_path=measurement_folder, xlabel=x_label, ylabel=y_label,
                                filename=filename_with_number, show_plot=False)
                
            freqs,powers=[],[]
            
        except Exception as e:
            print(f"Измерение {i+1} failed with error: {e}")
            continue
    
    
    
    avg_peak_power = np.mean(peak_powers)
    avg_peak_freq = np.mean(peak_freqs)
    
    return float(avg_peak_freq), float(avg_peak_power)