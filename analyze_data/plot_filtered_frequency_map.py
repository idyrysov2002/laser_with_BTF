
import numpy as np
from scripts.create_map_and_save import create_map_and_save


def plot_filtered_frequency_map(
    current_data, 
    delay_data, 
    freq_data, 
    freq_min=None, 
    freq_max=None, 
    filename=None, 
    save_folder=None, 
    show_plot=False,
    map_title=None):
    """
    Строит тепловую карту после фильтрации данных по заданному диапазону частот.

    Из исходных массивов тока, задержки и частоты выбираются только те точки,
    частота которых находится в диапазоне от `freq_min` до `freq_max`.
    Полученные данные передаются в функцию `create_map_and_save()` для построения
    и, при необходимости, сохранения карты.

    Args:
    current_data (tuple | list):
    Пара `(current_array, current_label)`, где `current_array` — массив
    значений тока, а `current_label` — подпись оси.
    delay_data (tuple | list):
    Пара `(delay_array, delay_label)`, где `delay_array` — массив
    значений задержки, а `delay_label` — подпись оси.
    freq_data (tuple | list):
    Пара `(frequency_array, frequency_label)`, где `frequency_array` —
    массив значений частоты, а `frequency_label` — подпись цветовой шкалы.
    freq_min (float | int, optional):
    Нижняя граница диапазона частот. Если `None`, используется минимальное
    значение из `freq_data`.
    freq_max (float | int, optional):
    Верхняя граница диапазона частот. Если `None`, используется максимальное
    значение из `freq_data`.
    filename (str, optional):
    Имя файла для сохранения карты.
    save_folder (str, optional):
    Путь к папке для сохранения карты.
    show_plot (bool, optional):
    Если `True`, отображает карту после построения.
    map_title (str, optional):
    Заголовок тепловой карты.
    """

    
    current_arr, current_label = current_data
    delay_arr, delay_label = delay_data
    freq_arr, freq_label = freq_data
    
    
    current_arr = np.asarray(current_arr)
    delay_arr = np.asarray(delay_arr)
    freq_arr = np.asarray(freq_arr)
    
    if freq_min is None:
        freq_min = freq_arr.min()

    if freq_max is None:
        freq_max = freq_arr.max()
        
    freq_mask = (freq_arr >= freq_min) & (freq_arr <= freq_max)

    
    current_arr_filtered = current_arr[freq_mask]
    delay_arr_filtered = delay_arr[freq_mask]
    freq_arr_filtered = freq_arr[freq_mask]
    
    current_arr_filtered_data = [current_arr_filtered, current_label]
    delay_arr_filtered_data = [delay_arr_filtered, delay_label]
    freq_arr_filtered_data = [freq_arr_filtered, freq_label]
    
    create_map_and_save(
        x_arr=current_arr_filtered_data, 
        y_arr=delay_arr_filtered_data, 
        z_arr=freq_arr_filtered_data, 
        title=map_title, 
        folder_path=save_folder, 
        filename=filename, 
        show_plot=show_plot)


if __name__ == '__main__':
    current_arr = [100, 100, 100, 200, 200, 200, 300, 300,300]
    delay_arr = [0, 20, 40, 0, 20, 40, 0, 20, 40]
    freq_arr = [4, 1, 2, 6, 3, 5, 15, 3, 9]
    
    current_label = 'Current, mA'
    delay_label = 'Delay, ps'
    freq_label = 'Frequency, GHz'
    
    current_data = [current_arr, current_label]
    delay_data = [delay_arr, delay_label]
    freq_data = [freq_arr, freq_label]
    
    freq_min = 1
    freq_max = 9
    
    map_title = f'{freq_min}<= freq <= {freq_max}'
    plot_filtered_frequency_map(
        current_data=current_data, 
        delay_data=delay_data, 
        freq_data=freq_data, 
        freq_min=freq_min, 
        freq_max=freq_max, 
        filename=None, 
        save_folder=None, 
        show_plot=True,
        map_title=map_title
        )