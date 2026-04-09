from pathlib import Path
import numpy as np
from scripts.create_folder import create_date_folder
from scripts.read_from_txt import read_txt_xy
from scripts.plot_and_save_xy import plot_and_save_xy
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter1d


def plot_graph_sao():
    soa_folder_path=r'C:\Users\namys_23hvwev\Documents\DATA\data_from_lnf\SOA_BTF100_contour_April-03-2026_time_18-29-27\yokogawa_measurements\current_300mA\linewidth_1nm'
    save_folder=r'C:\Users\namys_23hvwev\Documents\DATA\data_from_lnf\analysis_data_April-07-2026_time_00-43-48'
    wave_data, pow_data = [], []
    for wavelength in range(1525,1566):
        filename=rf'yokogawa_spectrum_SOA_wavelengh_{wavelength}nm_linewidth_1nm_current_300mA.txt'
        full_path=Path(soa_folder_path)/filename

        wave_arr, pow_arr = read_txt_xy(full_path=full_path, header=1)
        # wave_arr, pow_arr = np.array(wave_arr), np.array(pow_arr)
        max_index=np.argmax(pow_arr)
        peak_wave=float(wave_arr[max_index])
        peak_pow = float(pow_arr[max_index])

        # перевод на микроватт
        peak_pow=peak_pow*1000

        wave_data.append(peak_wave)
        pow_data.append(peak_pow)


    plot_and_save_xy(
        x=wave_data, 
        y=pow_data, 
        title="SOA, peak power (wavelength), current 300 mA, linewidth 1 nm", 
        xlabel='Wavelength, nm', 
        ylabel = 'Power, µW', 
        folder_path=save_folder, 
        filename='soa_peak_power_vs_wavelength_current_300mA_linewidth_1nm', 
        show_plot=True
    )


def plot_graph_filter():
    save_folder=r'C:\Users\namys_23hvwev\Documents\DATA\data_from_lnf\analysis_data_April-07-2026_time_00-43-48'

    filter_folder_path =r'C:\Users\namys_23hvwev\Documents\DATA\data_from_lnf\filter_BTF100_contour_April-03-2026_time_15-57-41\yokogawa_measurements\current_300mA\linewidth_1nm'

    wave_data, pow_data = [], []
    for wavelength in range(1525,1566):
        filename=rf'yokogawa_spectrum_filter_wavelengh_{wavelength}nm_linewidth_1nm_current_300mA.txt'
        full_path=Path(filter_folder_path)/filename

        wave_arr, pow_arr = read_txt_xy(full_path=full_path, header=1)
        # wave_arr, pow_arr = np.array(wave_arr), np.array(pow_arr)
        max_index=np.argmax(pow_arr)
        peak_wave=float(wave_arr[max_index])
        peak_pow = float(pow_arr[max_index])

        # перевод на микроватт
        peak_pow=peak_pow*1000

        wave_data.append(peak_wave)
        pow_data.append(peak_pow)


    plot_and_save_xy(
        x=wave_data, 
        y=pow_data, 
        title="filter, peak power (wavelength), current 300 mA, linewidth 1 nm", 
        xlabel='Wavelength, nm', 
        ylabel = 'Power, µW', 
        folder_path=save_folder, 
        filename='filter_peak_power_vs_wavelength_current_300mA_linewidth_1nm', 
        show_plot=True
    )

def plot_graph_filter_integer():
    save_folder=r'C:\Users\namys_23hvwev\Documents\DATA\data_from_lnf\analysis_data_April-07-2026_time_00-43-48'

    plot_title="filter, sum power (wavelength), current 300 mA, linewidth 1 nm"
    plot_filename='filter_sum_power_vs_wavelength_current_300mA_linewidth_1nm'
    x_label='Wavelength, nm'
    y_label='Power, mW'
    filter_folder_path =r'C:\Users\namys_23hvwev\Documents\DATA\data_from_lnf\filter_BTF100_contour_April-03-2026_time_15-57-41\yokogawa_measurements\current_300mA\linewidth_1nm'

    wave_data, pow_data = [], []
    for wavelength in range(1525,1566):
        filename=rf'yokogawa_spectrum_filter_wavelengh_{wavelength}nm_linewidth_1nm_current_300mA.txt'
        full_path=Path(filter_folder_path)/filename

        wave_arr, pow_arr = read_txt_xy(full_path=full_path, header=1)
        sum_pow=np.sum(pow_arr)


        wave_data.append(wavelength)
        pow_data.append(sum_pow)


    plot_and_save_xy(
        x=wave_data, 
        y=pow_data, 
        title=plot_title, 
        xlabel=x_label, 
        ylabel = y_label, 
        folder_path=save_folder, 
        filename=plot_filename, 
        show_plot=True
    )

def plot_graph_soa_integer():
    save_folder=r'C:\Users\namys_23hvwev\Documents\DATA\data_from_lnf\analysis_data_April-07-2026_time_00-43-48'

    plot_title="soa, sum power (wavelength), current 300 mA, linewidth 1 nm"
    plot_filename='soa_sum_power_vs_wavelength_current_300mA_linewidth_1nm'
    x_label='Wavelength, nm'
    y_label='Power, mW'
    filter_folder_path =r'C:\Users\namys_23hvwev\Documents\DATA\data_from_lnf\SOA_BTF100_contour_April-03-2026_time_18-29-27\yokogawa_measurements\current_300mA\linewidth_1nm'

    wave_data, pow_data = [], []
    for wavelength in range(1525,1566):
        filename=rf'yokogawa_spectrum_SOA_wavelengh_{wavelength}nm_linewidth_1nm_current_300mA.txt'
        full_path=Path(filter_folder_path)/filename

        wave_arr, pow_arr = read_txt_xy(full_path=full_path, header=1)
        sum_pow=np.sum(pow_arr)


        wave_data.append(wavelength)
        pow_data.append(sum_pow)


    plot_and_save_xy(
        x=wave_data, 
        y=pow_data, 
        title=plot_title, 
        xlabel=x_label, 
        ylabel = y_label, 
        folder_path=save_folder, 
        filename=plot_filename, 
        show_plot=True
    )


# def ratio_soa_filter():
#     save_folder=r'C:\Users\namys_23hvwev\Documents\DATA\data_from_lnf\analysis_data_April-07-2026_time_00-43-48'

#     filter_data = r'C:\Users\namys_23hvwev\Documents\DATA\data_from_lnf\filter_BTF100_contour_April-03-2026_time_15-57-41\yokogawa_measurements\current_300mA\linewidth_1nm'
    
    
#     soa_data=r'C:\Users\namys_23hvwev\Documents\DATA\data_from_lnf\SOA_BTF100_contour_April-03-2026_time_18-29-27\yokogawa_measurements\current_300mA\linewidth_1nm'
#     plot_title = '$P_soa(\lamda)/P_filter(\lamda)$'
#     plot_filename='soa_sum_power_vs_wavelength_current_300mA_linewidth_1nm'
#     x_label='Wavelength, nm'
#     y_label=None
#     wave_data, pow_data = [], []
#     for wavelength in range(1525,1566):
#         soa_filename=rf'yokogawa_spectrum_SOA_wavelengh_{wavelength}nm_linewidth_1nm_current_300mA.txt'
#         filter_filename = rf'yokogawa_spectrum_filter_wavelengh_{wavelength}nm_linewidth_1nm_current_300mA.txt'

#         filter_full_path=Path(filter_data)/filter_filename
#         soa_full_path=Path(soa_data)/soa_filename



#         filter_wave_arr, filter_pow_arr = read_txt_xy(full_path=filter_full_path)
#         soa_wave_arr, soa_pow_arr = read_txt_xy(full_path=soa_full_path)

#         power_ratio=
        
        

def ratio_power_meter():
    save_folder=r'C:\Users\namys_23hvwev\Documents\DATA\data_from_lnf\analysis_data_April-07-2026_time_00-43-48'

    folder_data = r'C:\Users\namys_23hvwev\Documents\DATA\data_from_lnf\PM_April-03-2026_time_19-40-59'
    
    plot_title = r'data from PM400, $\frac{P_{\mathrm{filter}}(\lambda)}{P_{\mathrm{SOA}}(\lambda)}$'
    plot_filename='ratio_soa-filter-power_meter_current_300mA_linewidth_1nm'
    x_label='Wavelength, nm'
    y_label='Power Ratio (a.u.)'
    wave_data, pow_data = [], []
    
    soa_filename='soa_power_meter_current_300mA_linewidth_1nm.txt'
    filter_filename = 'filter_power_meter_current_300mA_linewidth_1nm.txt'

    filter_full_path=Path(folder_data)/filter_filename
    soa_full_path=Path(folder_data)/soa_filename



    filter_wave_arr, filter_pow_arr = read_txt_xy(full_path=filter_full_path)
    soa_wave_arr, soa_pow_arr = read_txt_xy(full_path=soa_full_path)

    ratio= filter_pow_arr/soa_pow_arr

    plot_and_save_xy(
        x=soa_wave_arr, 
        y=ratio, 
        title=plot_title, 
        xlabel=x_label, 
        ylabel = y_label, 
        folder_path=save_folder, 
        filename=plot_filename, 
        show_plot=''
    )


    



def norm_soa():
    save_folder=r'C:\Users\namys_23hvwev\Documents\DATA\data_from_lnf\analysis_data_April-07-2026_time_00-43-48\soa_peak_normalization'

    plot_title="soa, peak normalization, current 300 mA, linewidth 1 nm"
    plot_filename='soa_peak normalization_current_300mA_linewidth_1nm'
    x_label='Wavelength, nm'
    y_label='Power, mW'
    filter_folder_path =r'C:\Users\namys_23hvwev\Documents\DATA\data_from_lnf\SOA_BTF100_contour_April-03-2026_time_18-29-27\yokogawa_measurements\current_300mA\linewidth_1nm'

    for wavelength in range(1525,1566):
        filename=rf'yokogawa_spectrum_SOA_wavelengh_{wavelength}nm_linewidth_1nm_current_300mA.txt'
        full_path=Path(filter_folder_path)/filename

        wave_arr, pow_arr = read_txt_xy(full_path=full_path, header=1)
        max_index = np.argmax(pow_arr)
        max_pow=pow_arr[max_index]
        
        for x in range(len(pow_arr)):
            pow_arr[x] =pow_arr[x]/ max_pow

        plot_and_save_xy(
            x=wave_arr, 
            y=pow_arr, 
            title=plot_title, 
            xlabel=x_label, 
            ylabel = y_label, 
            folder_path=save_folder, 
            filename=f'wavelength_{wavelength}nm_{plot_filename}', 
            show_plot=False
        )
def smooth(y, box_pts=5):
    """
    y: массив данных
    box_pts: ширина окна сглаживания (нечетное число, например 3, 5, 7)
    """
    box = np.ones(box_pts)/box_pts
    # mode='same' возвращает массив той же длины, что и входной
    y_smooth = np.convolve(y, box, mode='same')
    return y_smooth

import numpy as np

def calculate_fwhm(x_arr, y_arr):
    """
    Вычисляет FWHM (Full Width at Half Maximum) для заданных данных.
    
    Параметры:
    x_arr : array-like
        Массив значений по оси X (например, длины волн)
    y_arr : array-like
        Массив значений по оси Y (например, мощность/интенсивность)
    
    Возвращает:
    fwhm : float
        Ширина пика на половине максимальной высоты.
        Возвращает np.nan, если пик не найден или данные некорректны.
    peak_x : float
        Положение максимума по оси X.
    peak_y : float
        Значение максимума по оси Y.
    """
    # Преобразуем в numpy-массивы
    x = np.asarray(x_arr)
    y = np.asarray(y_arr)
    
    # Проверяем, что массивы не пустые и одинаковой длины
    if len(x) != len(y) or len(x) == 0:
        return np.nan, np.nan, np.nan
    
    # Находим индекс и значение максимума
    max_idx = np.argmax(y)
    peak_x = x[max_idx]
    peak_y = y[max_idx]
    
    # Если максимум <= 0, то FWHM не имеет смысла
    if peak_y <= 0:
        return np.nan, peak_x, peak_y
    
    # Вычисляем половину максимума
    half_max = peak_y / 2.0
    
    # Находим все точки, где y >= half_max
    above_half = y >= half_max
    
    # Находим левую границу: последняя точка слева от пика, где y >= half_max
    left_indices = np.where((x < peak_x) & above_half)[0]
    # Находим правую границу: первая точка справа от пика, где y >= half_max
    right_indices = np.where((x > peak_x) & above_half)[0]
    
    # Если не нашли границы с обеих сторон — возвращаем nan
    if len(left_indices) == 0 or len(right_indices) == 0:
        return np.nan, peak_x, peak_y
    
    # Берем крайние точки на уровне половины высоты
    x_left = x[left_indices[-1]]   # самая правая из левых точек
    x_right = x[right_indices[0]]  # самая левая из правых точек
    
    # Вычисляем FWHM
    fwhm = x_right - x_left
    
    return fwhm, peak_x, peak_y

import numpy as np

import numpy as np

def get_gaussian_y(x_array, fwhm, x_0, A):
    """
    Вычисляет значения гаусса для заданного массива X.
    
    Параметры:
    x_array : ndarray
        Общая сетка координат X (например, от 1520 до 1570).
    fwhm : float
        Ширина пика.
    x_0 : float
        Центр пика.
    A : float
        Амплитуда (высота).
        
    Возвращает:
    y : ndarray
        Массив значений Y той же длины, что и x_array.
    """
    # Переводим FWHM в Sigma
    sigma = fwhm / 2.3548200450309493
    
    # Формула Гаусса
    y = A * np.exp(-0.5 * ((x_array - x_0) / sigma)**2)
    
    return y

def filter_soa():
    filter_folder=r'C:\Users\namys_23hvwev\Documents\DATA\data_from_lnf\filter_BTF100\linewidth_1nm'
    soa_folder=r'C:\Users\namys_23hvwev\Documents\DATA\data_from_lnf\SOA_BTF100\linewidth_1nm'
    global_max=0
    for wave in range(1525,1566):
        filter_full_path = Path(filter_folder)/rf'yokogawa_spectrum_filter_wavelengh_{wave}nm_linewidth_1nm_current_300mA.txt'
        sao_full_path=Path(soa_folder)/rf'yokogawa_spectrum_SOA_wavelengh_{wave}nm_linewidth_1nm_current_300mA.txt'
        sao_wave_arr, sao_pow_arr = read_txt_xy(full_path=sao_full_path)
        filter_wave_arr, filter_pow_arr = read_txt_xy(full_path=filter_full_path)
        mask = (sao_wave_arr > 1520) & (sao_wave_arr < 1570)

        filter_pow_arr=filter_pow_arr[mask]
        sao_pow_arr=sao_pow_arr[mask]
        sao_wave_arr=sao_wave_arr[mask]

        ratio_pow=filter_pow_arr/sao_pow_arr
        max_index = np.argmax(ratio_pow)
        peak_ratio_pow = float(ratio_pow[max_index])
        
        if peak_ratio_pow>global_max:
            global_max=peak_ratio_pow

    x_global = np.linspace(1520, 1570, 2000)
    
    plt.figure(figsize=(12, 6)) # Рекомендуется создать фигуру явно
    for wave in range(1525,1566):
        filter_full_path = Path(filter_folder)/rf'yokogawa_spectrum_filter_wavelengh_{wave}nm_linewidth_1nm_current_300mA.txt'
        sao_full_path=Path(soa_folder)/rf'yokogawa_spectrum_SOA_wavelengh_{wave}nm_linewidth_1nm_current_300mA.txt'
        sao_wave_arr, sao_pow_arr = read_txt_xy(full_path=sao_full_path)
        filter_wave_arr, filter_pow_arr = read_txt_xy(full_path=filter_full_path)
        mask = (sao_wave_arr > 1520) & (sao_wave_arr < 1570)

        filter_pow_arr=filter_pow_arr[mask]
        sao_pow_arr=sao_pow_arr[mask]
        sao_wave_arr=sao_wave_arr[mask]

        ratio_pow=filter_pow_arr/sao_pow_arr
        max_index = np.argmax(ratio_pow)
        peak_ratio_pow = float(ratio_pow[max_index])
        # peak_ratio_wave=float(sao_wave_arr[max_index]) 


        # fwhm, peak_x, peak_y=calculate_fwhm(x_global, ratio_pow)
        #  # Считаем гаусс на ОБЩЕЙ сетке x_global
        # y = get_gaussian_y(x_array=x_global, fwhm=fwhm, x_0=peak_x, A=peak_y)
        
        # Нормируем
        ratio_pow= ratio_pow / global_max
        
        
        # Рисуем по общей сетке x_global
        plt.plot(sao_wave_arr, ratio_pow, label=f'WL {wave}')
    # Отображение легенды
    plt.legend(title='Легенды')
    plt.show()






if __name__=="__main__":
    filter_soa()
    
    # create_date_folder(base_path=r'C:\Users\namys_23hvwev\Documents\DATA\data_from_lnf',prefix='analysis_data')

