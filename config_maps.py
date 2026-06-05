from pathlib import Path
from scripts.create_map_and_save import create_map_and_save
def build_maps(data_map, save_folder_structure, linewidth, wavelength):
    """
    Построение тепловых карт для всех измерений из data_map.

    Аргументы:
        data_map: dict - словарь с данными
            Обязательные ключи: 'current' (ось X), 'delay' (ось Y)
            Остальные ключи: любые названия измерений для построения карт
        save_folder_structure: str - путь для сохранения карт
        linewidth: float - ширина линии (для заголовка)
        wavelength: float - длина волны (для заголовка)

    Функция автоматически построит карту для каждого ключа в data_map,
    кроме 'current' и 'delay', используя их как координаты точек.
    """
    
    # Получаем данные для осей
    x_arr = data_map['current']
    y_arr = data_map['delay']
    x_label = "Current, mA"
    y_label = "Delay, ps"
    
    # Создаем папку
    folder_path = Path(save_folder_structure)
    folder_path.mkdir(parents=True, exist_ok=True)
    
    # Проходим по всем измерениям (исключая current и delay)
    for meas_name, meas_values in data_map.items():
        if meas_name in ['current', 'delay']:
            continue
            
        # Берем настройки из конфига или используем значения по умолчанию
        if meas_name in MAPS_CONFIG:
            z_label = MAPS_CONFIG[meas_name]['label']
            title_name = MAPS_CONFIG[meas_name]['title']
        else:
            z_label = "Value"
            title_name = meas_name
        
        # Формируем заголовок и имя файла
        title = f'{title_name}: LW={linewidth}nm, WL={wavelength}nm'
        filename = f'{meas_name}_lw_{linewidth}nm_wl_{wavelength}nm'
        
        # Создаем карту
        create_map_and_save(
            x_arr=[x_arr, x_label],
            y_arr=[y_arr, y_label],
            z_arr=[meas_values, z_label],
            title=title,
            folder_path=folder_path,
            filename=filename,
            show_plot=False
        )
MAPS_CONFIG = {
    'pm_400': {
        'label': 'Power, mW',
        'title': 'pm_400',
                },

    'rf_peak_freq_span_6200MHz': {
        'label': 'Frequency, GHz',
        'title': 'rf_peak_freq',
        },
    'rf_peak_freq_span_100MHz': {
        'label': 'Frequency, GHz',
        'title': 'rf_peak_freq',

        },
    'rf_peak_freq_span_1MHz': {
        'label': 'Frequency, GHz',
        'title': 'rf_peak_freq',
        
    },
    'osc_mean_freq': {
        'label': 'Frequency, GHz',
        'title': 'osc_mean_freq',       
    }
}




# Данные уже готовы (списки одной длины)
x_values = [1, 1, 2, 2, 3, 3]
y_values = [10, 20, 10, 20, 10, 20]

data_map = {
    'current': x_values,
    'delay': y_values, 
    'pm_400': [1.5, 1.6, 1.7, 1.8, 1.9, 2.0],
    'rf_peak_freq_span_6200MHz': [100, 101, 102, 103, 104, 105],
    'rf_peak_freq_span_100MHz': [100, 101, 102, 103, 104, 105],
    'rf_peak_freq_span_1MHz': [100, 101, 102, 103, 104, 105],
    'osc_mean_freq': [10, 10.1, 10.2, 10.3, 10.4, 10.5],
}
if __name__ == "__main__":
    # Построение
    build_maps(
        data_map=data_map,
        save_folder_structure="./results/maps",
        linewidth=5,
        wavelength=1550
    )


