from pathlib import Path
import matplotlib.pyplot as plt
from tqdm import tqdm
from scripts.create_map_and_save import create_map_and_save
from scripts.create_folder import create_date_folder, create_multiple_subfolders
from scripts.slice_current import slice_current
from scripts.read_from_txt import read_txt_xyz, read_txt_xy
from scripts.plot_and_save_xy import plot_and_save_xy
from scripts.copy_files import copy_files
from scripts.create_plot_grid import create_plot_grid
from scripts.plot_histogram_grid import plot_histogram_grid
import sys
import os
import numpy as np
from scripts.plot_histogram_and_save import plot_histogram_and_save
from scripts.calculate_FWHM_dBm import calculate_FWHM_dBm
from scripts.get_OSC_data_from_txt import get_OSC_data_from_txt
# Получаем путь к текущему файлу
current_dir = os.path.dirname(os.path.abspath(__file__))
# Получаем путь к родительской папке (где лежит config)
parent_dir = os.path.dirname(current_dir)

# Добавляем родительскую папку в пути поиска модулей
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)
VOLTAGES=[0, 1, 2, 3, 4, 5] # в V
DELAYS=np.arange(0, 331, 10) # в ps
CURRENTS=np.arange(100, 501, 50) # в mA
WAVELENGTH=[1540, 1550, 1560] # в nm
LINEWIDTH=[1] # в nm

def osc():

    data_folder=r'C:\Users\namys_23hvwev\Documents\DATA\data_from_lnf\laser_with_btf_April-10-2026_time_16-39-14'
    for linewidth in LINEWIDTH:
        for wavelength in WAVELENGTH:
            for voltage in VOLTAGES:
                freq_data, current_data, delay_data=[],[],[]
                for current in CURRENTS:
                    for delay in DELAYS:

                        osc_folder_name=rf'C:\Users\namys_23hvwev\Documents\DATA\data_from_lnf\laser_with_btf_April-10-2026_time_16-39-14\oscilloscope_measurements\linewidth_{linewidth}nm\wavelength_{wavelength}nm\voltage_{voltage}V\current_{current}mA\average\duration_10ns'
                        osc_filename=rf'oscillogram_average_duration_10ns_delay_{delay}ps_current_{current}mA_voltage_{voltage}V_wavelength_{wavelength}nm_linewidth_{linewidth}nm.txt'
                        osc_full_path=Path(osc_folder_name)/osc_filename

                        osc_dict=get_OSC_data_from_txt(osc_full_path)

                        mean_freq=osc_dict['Mean_GHz']
                        
                        freq_data.append(mean_freq)
                        current_data.append(current)
                        delay_data.append(delay)
                # freq_data=np.array(freq_data)
                # current_data=np.array(current_data)
                # delay_data=np.array(delay_data)


                # mask=freq_data<=6.2e+9
                # current_data=current_data[mask]
                # delay_data=delay_data[mask]
                # freq_data=freq_data[mask]
                x_arr=[current_data, 'Current, mA']
                y_arr=[delay_data, 'Delay, ps']
                z_arr=[freq_data, 'Frequensy, GHz']

                create_map_and_save(
                    x_arr=x_arr, 
                    y_arr=y_arr, 
                    z_arr=z_arr, 
                    title=f'wavelength_{wavelength}nm, voltage_{voltage}V', 
                    folder_path=r'C:\Users\namys_23hvwev\Documents\DATA\data_from_lnf\laser_with_btf_April-10-2026_time_16-39-14\analysis_data', 
                    filename=f'osc_frequency_map_wavelenghth_{wavelength}nm_voltage_{voltage}V', 
                    show_plot=False

                )

def rf():

    data_folder=r'C:\Users\namys_23hvwev\Documents\DATA\data_from_lnf\laser_with_btf_April-10-2026_time_16-39-14'
    for linewidth in LINEWIDTH:
        for wavelength in WAVELENGTH:
            for voltage in VOLTAGES:
                freq_data, current_data, delay_data=[],[],[]
                for current in CURRENTS:
                    for delay in DELAYS:

                        rf_folder_name=rf'C:\Users\namys_23hvwev\Documents\DATA\data_from_lnf\laser_with_btf_April-10-2026_time_16-39-14\rf_measurements\linewidth_{linewidth}nm\wavelength_{wavelength}nm\voltage_{voltage}V\current_{current}mA\span_6GHz\measurement_number_1'
                        rf_filename=rf'rf_spectrum_delay_{delay}ps_current_{current}mA_voltage_{voltage}V_wavelength_{wavelength}nm_linewidth_1nm_span_6GHz_measurement_number_1.txt'
                        rf_full_path=Path(rf_folder_name)/rf_filename

                        freq_arr, power_arr=read_txt_xy(rf_full_path)

                        max_index=np.argmax(power_arr)
                        freq=freq_arr[max_index]

                        
                        
                        freq_data.append(freq)
                        current_data.append(current)
                        delay_data.append(delay)
                # freq_data=np.array(freq_data)
                # current_data=np.array(current_data)
                # delay_data=np.array(delay_data)


                # mask=freq_data<=6.2e+9
                # current_data=current_data[mask]
                # delay_data=delay_data[mask]
                # freq_data=freq_data[mask]
                x_arr=[current_data, 'Current, mA']
                y_arr=[delay_data, 'Delay, ps']
                z_arr=[freq_data, 'Frequensy, GHz']

                create_map_and_save(
                    x_arr=x_arr, 
                    y_arr=y_arr, 
                    z_arr=z_arr, 
                    title=f'wavelength_{wavelength}nm, voltage_{voltage}V', 
                    folder_path=r'C:\Users\namys_23hvwev\Documents\DATA\data_from_lnf\laser_with_btf_April-10-2026_time_16-39-14\analysis_data', 
                    filename=f'rf_frequency_map_wavelenghth_{wavelength}nm_voltage_{voltage}V', 
                    show_plot=False

                )



def Attenuator():
    folder_path=rf'C:\Users\namys_23hvwev\Documents\DATA\data_from_lnf\Attenuator_port2-port1_April-09-2026_time_18-31-03\yokogawa_measurements'
    voltage_arr, peak_arr=[],[]
    
    for voltage in np.arange(0, 6.2, 0.2):
        full_path=Path(folder_path)/rf'yokogawa_spectrum_Attenuator_voltage_{voltage}V_current_300mA.txt'
        wave_arr, pow_arr = read_txt_xy(full_path=full_path)
        
        max_index=np.argmax(pow_arr)
        peak_pow=pow_arr[max_index]

        if voltage==0:
            norm_peak=peak_pow


        voltage_arr.append(voltage)
        peak_arr.append(peak_pow)

    plot_and_save_xy(
        x=voltage_arr, 
        y=peak_arr/norm_peak, 
        title='Attenuator: port2->port1', 
        xlabel='Voltage, V', 
        ylabel="Peak power, a.u.", 
        folder_path=None, 
        filename=None, 
        show_plot=True

    )
def ratio_Attenuator():
    folder_path2=rf'C:\Users\namys_23hvwev\Documents\DATA\data_from_lnf\Attenuator_port2-port1_April-09-2026_time_18-31-03\yokogawa_measurements'
    folder_path1=rf'C:\Users\namys_23hvwev\Documents\DATA\data_from_lnf\Attenuator_port1-port2_April-09-2026_time_18-14-35\yokogawa_measurements'
    voltage_arr, peak_arr1=[],[]
    peak_arr2=[]
    
    for voltage in np.arange(0, 6.2, 0.2):
        full_path1=Path(folder_path1)/rf'yokogawa_spectrum_Attenuator_voltage_{voltage}V_current_300mA.txt'
        full_path2=Path(folder_path2)/rf'yokogawa_spectrum_Attenuator_voltage_{voltage}V_current_300mA.txt'



        wave_arr1, pow_arr1 = read_txt_xy(full_path=full_path1)
        wave_arr2, pow_arr2 = read_txt_xy(full_path=full_path2)
        
        max_index1=np.argmax(pow_arr1)
        peak_pow1=pow_arr1[max_index1]

        max_index2=np.argmax(pow_arr2)
        peak_pow2=pow_arr2[max_index2]

        if voltage==0:
            norm_peak1=peak_pow1
            norm_peak2=peak_pow2


        voltage_arr.append(voltage)
        peak_arr1.append(peak_pow1)
        peak_arr2.append(peak_pow2)



    plot_and_save_xy(
        x=voltage_arr, 
        y=(peak_arr1/norm_peak1)/(peak_arr2/norm_peak2), 
        title='Ratio attenuator: port1 / port2', 
        xlabel='Voltage, V', 
        ylabel="Peak power1 / Peak power2, a.u.", 
        folder_path=None, 
        filename=None, 
        show_plot=True

    )


def coupler_black_blue():
    folder_path=rf'C:\Users\namys_23hvwev\Documents\DATA\data_from_lnf\coupler_black-blue_April-09-2026_time_16-20-30\yokogawa_measurements'
    # save_folder=rf'C:\Users\namys_23hvwev\Documents\DATA\data_from_lnf\13-april_analysis_data'

    wavelength_data, peak_pow_data=[],[]
    max_peak=0
    for wavelength in range(1525, 1566):
        full_path=Path(folder_path)/rf"yokogawa_spectrum_black_blue_wavelengh_{wavelength}nm_linewidth_1nm_current_300mA.txt"

        wave_arr, pow_arr = read_txt_xy(full_path)
        max_index=np.argmax(pow_arr)

        peak_pow=pow_arr[max_index]
        peak_wave=wave_arr[max_index]
        
        if peak_pow>max_peak:
            max_peak=peak_pow


        wavelength_data.append(wavelength)
        peak_pow_data.append(peak_pow)

    plot_and_save_xy(
        x=wavelength_data, 
        y=peak_pow_data/max_peak, 
        title='=', 
        xlabel='Wavelength, nm', 
        ylabel="=", 
        folder_path=None, 
        filename=None, 
        show_plot=True

    )

def transmission_coefficient():
    for wavelength in [1550]:
        soa_full_path=rf"C:\Users\namys_23hvwev\Documents\DATA\data_from_lnf\soa_April-09-2026_time_19-12-08\yokogawa_measurements\yokogawa_spectrum_soa_wavelengh_{wavelength}nm_linewidth_1nm_current_300mA.txt"
        coupler_full_path=fr"C:\Users\namys_23hvwev\Documents\DATA\data_from_lnf\coupler_black-blue_April-09-2026_time_16-20-30\yokogawa_measurements\yokogawa_spectrum_black_blue_wavelengh_1550nm_linewidth_1nm_current_300mA.txt"


        wave_arr_soa, pow_arr_soa = read_txt_xy(soa_full_path)
        wave_arr_coupler, pow_arr_coupler = read_txt_xy(coupler_full_path)

        mask_soa = (wave_arr_soa >= 1510) & (wave_arr_soa <= 1580)
        mask_coupler = (wave_arr_coupler >= 1510) & (wave_arr_coupler <= 1580)
        wave_arr_soa, pow_arr_soa=wave_arr_soa[mask_soa], pow_arr_soa[mask_soa]
        wave_arr_coupler, pow_arr_coupler=wave_arr_coupler[mask_coupler], pow_arr_coupler[mask_coupler]
        norm_coef=np.max(pow_arr_coupler/pow_arr_soa)
        # plt.plot(wave_arr_soa, pow_arr_soa, label='soa')
        # plt.plot(wave_arr_coupler, pow_arr_coupler)
        plt.plot(wave_arr_coupler, pow_arr_coupler/pow_arr_soa)
        # plt.legend(title='Легенды')
        plt.title(r'black-blue: $\frac{P_{coupler}(\lambda)}{P_{soa}(\lambda)}$',fontsize=20)
        plt.show()





def SOA_integer():
    folder_path=rf'C:\Users\namys_23hvwev\Documents\DATA\data_from_lnf\soa_April-09-2026_time_19-12-08\yokogawa_measurements'
    max_peak=0
    norm_data=[]
    wavelength_data, peak_pow_data=[],[]
    for wavelength in range(1525, 1566):
        full_path=Path(folder_path)/rf'yokogawa_spectrum_soa_wavelengh_{wavelength}nm_linewidth_1nm_current_300mA.txt'

        wave_arr, pow_arr = read_txt_xy(full_path)

        max_index=np.argmax(pow_arr)

        peak_pow=pow_arr[max_index]

        if max_peak<=peak_pow:
            max_peak=peak_pow

        wavelength_data.append(wavelength)
        peak_pow_data.append(np.sum(pow_arr))

    plot_and_save_xy(
        x=wavelength_data, 
        y=peak_pow_data, 
        title='=', 
        xlabel='Wavelength, nm', 
        ylabel="=", 
        folder_path=None, 
        filename=None, 
        show_plot=True

    )


def calculate_FWHM_lin_scale(x_arr, y_arr):
    """
    Вычисляет FWHM (Full Width at Half Maximum) для данных с линейной шкалой.
    
    Параметры:
    x_arr : array-like
        Массив значений по оси X.
    y_arr : array-like
        Массив значений по оси Y.
        
    Возвращает:
    fwhm : float
        Полная ширина на половине высоты.
    """
    x = np.asarray(x_arr)
    y = np.asarray(y_arr)
    
    if len(x) != len(y):
        raise ValueError("Длины массивов x и y должны совпадать")
    
    if len(x) < 2:
        return 0.0
    
    # Находим максимальное значение Y и его индекс
    max_y = np.max(y)
    min_y = np.min(y)
    
    # Если сигнал постоянный или нулевой, FWHM не определен
    if max_y == min_y:
        return 0.0
    
    # Уровень половины высоты (относительно базовой линии, если нужно, 
    # но обычно FWHM считается от нуля до пика, если не указан фон.
    # Здесь предполагаем классический вариант: half_max = max_y / 2.
    # Если есть значительный фон, лучше использовать: half_max = min_y + (max_y - min_y) / 2
    half_max = min_y + (max_y - min_y) / 2.0
    
    # Находим индексы, где кривая пересекает уровень half_max
    # Ищем переходы через уровень half_max
    # Создаем булев массив: где y >= half_max
    above_half_max = y >= half_max
    
    # Находим границы областей, где сигнал выше половины максимума
    # diff покажет места перехода False->True (начало) и True->False (конец)
    diffs = np.diff(above_half_max.astype(int))
    
    # Индексы начал и концов участков выше half_max
    start_indices = np.where(diffs == 1)[0]
    end_indices = np.where(diffs == -1)[0]
    
    # Если нет пересечений или сигнал всегда выше/ниже
    if len(start_indices) == 0 or len(end_indices) == 0:
        return 0.0
    
    # Нам нужен самый широкий пик вокруг глобального максимума
    # Найдем индекс максимума
    max_idx = np.argmax(y)
    
    # Найдем участок, содержащий индекс максимума
    selected_start_idx = None
    selected_end_idx = None
    
    for s, e in zip(start_indices, end_indices):
        if s <= max_idx <= e:
            selected_start_idx = s
            selected_end_idx = e
            break
            
    # Если максимум находится на границе или алгоритм не нашел участок,
    # попробуем взять ближайший участок
    if selected_start_idx is None:
        # Попробуем найти ближайший переход
        # Это упрощение, в большинстве случаев пик будет внутри участка
        if len(start_indices) > 0 and len(end_indices) > 0:
             # Берем первый и последний, если пик один
             selected_start_idx = start_indices[0]
             selected_end_idx = end_indices[-1]
        else:
             return 0.0

    # Теперь уточняем положение пересечений с помощью линейной интерполяции
    # Левая точка пересечения
    idx_left = selected_start_idx
    # Проверяем границы
    if idx_left < 0 or idx_left >= len(x) - 1:
        return 0.0
        
    x1, x2 = x[idx_left], x[idx_left + 1]
    y1, y2 = y[idx_left], y[idx_left + 1]
    
    # Линейная интерполяция: x = x1 + (half_max - y1) * (x2 - x1) / (y2 - y1)
    if y2 == y1:
        x_left = x1
    else:
        x_left = x1 + (half_max - y1) * (x2 - x1) / (y2 - y1)
        
    # Правая точка пересечения
    idx_right = selected_end_idx
    if idx_right < 0 or idx_right >= len(x) - 1:
        return 0.0
        
    x1_r, x2_r = x[idx_right], x[idx_right + 1]
    y1_r, y2_r = y[idx_right], y[idx_right + 1]
    
    if y2_r == y1_r:
        x_right = x1_r
    else:
        x_right = x1_r + (half_max - y1_r) * (x2_r - x1_r) / (y2_r - y1_r)
        
    fwhm = x_right - x_left
    
    return fwhm
def generate_gaussian(x_arr, x_peak, y_peak, fwhm):
    """
    Генерирует значения гауссовой кривой для заданной сетки x.
    
    Параметры:
    x_arr   : array-like - сетка координат X
    x_peak  : float      - координата X центра пика
    y_peak  : float      - высота пика (амплитуда)
    fwhm    : float      - полная ширина на половине высоты
    
    Возвращает:
    y_gauss : ndarray    - массив значений Y гауссовой кривой
    """
    # 1. Вычисляем sigma из FWHM
    # FWHM = 2 * sqrt(2 * ln(2)) * sigma
    sigma = fwhm / (2 * np.sqrt(2 * np.log(2)))
    
    # 2. Вычисляем Гаусс
    # y = A * exp( -(x - x0)^2 / (2 * sigma^2) )
    y_gauss = y_peak * np.exp(-((x_arr - x_peak)**2) / (2 * sigma**2))
    
    return y_gauss
def filter():
    soa_path=r"C:\Users\namys_23hvwev\Documents\DATA\data_from_lnf\soa_April-09-2026_time_19-12-08\yokogawa_measurements\yokogawa_spectrum_soa_wavelengh_1526nm_linewidth_1nm_current_300mA.txt"

    soa_wave, soa_pow=read_txt_xy(soa_path)
    mask1 = (soa_wave >= 1510) & (soa_wave <= 1580)
    soa_wave, soa_pow=soa_wave[mask1], soa_pow[mask1]

    norm_coef=0
    for wavelength in range(1525, 1566):
        full_path=fr"C:\Users\namys_23hvwev\Documents\DATA\data_from_lnf\filter_April-09-2026_time_18-51-26\yokogawa_measurements\yokogawa_spectrum_filter_wavelengh_{wavelength}nm_linewidth_1nm_current_300mA.txt"

        wave_arr, pow_arr_filter = read_txt_xy(full_path)
        wave_arr, pow_arr_filter=np.array(wave_arr), np.array(pow_arr_filter)
        mask3=(wave_arr >= 1510) & (wave_arr <= 1580)
        wave_arr, pow_arr_filter=wave_arr[mask3], pow_arr_filter[mask3]


        if np.max(pow_arr_filter/soa_pow)>norm_coef:
            norm_coef=np.max(pow_arr_filter/soa_pow)


    for wavelength in range(1525, 1566):
        full_path=fr"C:\Users\namys_23hvwev\Documents\DATA\data_from_lnf\filter_April-09-2026_time_18-51-26\yokogawa_measurements\yokogawa_spectrum_filter_wavelengh_{wavelength}nm_linewidth_1nm_current_300mA.txt"

        wave_arr, pow_arr_filter = read_txt_xy(full_path)
        wave_arr, pow_arr_filter=np.array(wave_arr), np.array(pow_arr_filter)
        mask3=(wave_arr >= 1510) & (wave_arr <= 1580)
        wave_arr, pow_arr_filter=wave_arr[mask3], pow_arr_filter[mask3]

        ratio=pow_arr_filter/soa_pow/norm_coef
        max_index_ratio=np.argmax(ratio)
        peak_pow=ratio[max_index_ratio]
        peak_wave=wave_arr[max_index_ratio]
        fwhm=calculate_FWHM_lin_scale(wave_arr, ratio)
        print(wavelength, fwhm)
        y_gauss=generate_gaussian(x_arr=wave_arr, x_peak=peak_wave, y_peak=peak_pow, fwhm=fwhm)
        # plt.plot(wave_arr, pow_arr_filter/soa_pow/norm_coef, label=f'WL={wavelength}')
        plt.plot(wave_arr, y_gauss, label=f'WL={wavelength}')

    # plt.legend(title='Легенды')
    # ax = plt.gca() # получаем текущие оси

    # # Левый верхний угол
    # # (0, 1) - это левый верхний угол области осей в координатах transAxes
    # ax.text(0.02, 0.98, 'Спектр фильтра нормированный на спектр SOA.\nПотом нормированный на 1', 
    #         transform=ax.transAxes,
    #         fontsize=10, verticalalignment='top', horizontalalignment='left',
    #         bbox=dict(facecolor='white', alpha=0, edgecolor='none'))

    # # Правый нижний угол
    # # (1, 0) - это правый нижний угол
    # ax.text(0.98, 0.02, f'SOA Current: 300 mA\nFilter Tuning Range: 1525-1565 nm', 
    #         transform=ax.transAxes,
    #         fontsize=9, verticalalignment='bottom', horizontalalignment='right',
    #         bbox=dict(facecolor='white', alpha=0.8, edgecolor='none'))
    plt.title('Спектр фильтра нормированный на спектр SOA\nПотом нормированный на 1',fontsize=14)
    plt.xlabel('Wavelength, nm', fontsize=14)
    plt.ylabel('Power, a.u.',fontsize=14)
    plt.show()

    
        






if __name__=='__main__':
    filter()


                        



