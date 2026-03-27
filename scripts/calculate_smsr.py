import numpy as np
import matplotlib.pyplot as plt
import random
import numpy as np
from scripts.read_from_txt import read_txt_xy
def calculate_smsr(freq_arr, peak_arr):
    """
    Вычисляет SMSR (Side Mode Suppression Ratio).
    
    Параметры:
    freq_arr: массив частот
    peak_arr: массив мощностей пиков (единица измерения - дБм)
    
    Возвращает:
    smsr: разность между главным пиком и следующим наибольшим (единица измерения - dB)
    """
    freq_arr = np.array(freq_arr)
    peak_arr = np.array(peak_arr)

    if len(peak_arr) < 2:
        raise ValueError("Для расчета SMSR необходимо как минимум два пика.")

    # Поиск главного пика
    index_max_peak = np.argmax(peak_arr)
    first_max_peak = float(peak_arr[index_max_peak])
    first_max_peak_freq = float(freq_arr[index_max_peak])

    # Поиск второго пика
    # Создаем копию, чтобы не менять исходный массив, и маскируем главный пик
    peak_arr_copy = peak_arr.copy()
    peak_arr_copy[index_max_peak] = -np.inf  # Исключаем главный пик из поиска
    
    index_second_max_peak = np.argmax(peak_arr_copy)
    second_max_peak = float(peak_arr_copy[index_second_max_peak])
    second_max_peak_freq = float(freq_arr[index_second_max_peak])

    # Расчет SMSR
    smsr = first_max_peak - second_max_peak

    return smsr, {
        "main_freq": first_max_peak_freq,
        "main_power": first_max_peak,
        "side_freq": second_max_peak_freq,
        "side_power": second_max_peak
    }
