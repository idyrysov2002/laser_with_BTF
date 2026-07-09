import numpy as np
import matplotlib.pyplot as plt
import os
from pathlib import Path
import sys


from read_from_txt import read_txt_xy
from plot_and_save_xy import plot_and_save_xy

# Получаем путь к текущему файлу
current_dir = os.path.dirname(os.path.abspath(__file__))
# Получаем путь к родительской папке (где лежит config)
parent_dir = os.path.dirname(current_dir)

# Добавляем родительскую папку в пути поиска модулей
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)


def plot_waterfall(
    x,                
    ys,               
    offsets,     
    x_label,
    y_label,
    z_label,
    elev=30,          
    azim=45,         
    roll=-3,
    save_folder_path=None,
    filename=None,
    show_plot=True            
):
    """
    Строит 3D-график типа "водопад" (waterfall plot) для визуализации множества серий данных.

    Каждая серия данных отображается как линия в 3D-пространстве, смещенная вдоль оси Y 
    на заданное значение offset. Это позволяет наглядно сравнивать изменение сигналов 
    или спектров во времени/по условиям без их перекрытия.

    Args:
        x (array-like): Массив значений по общей оси X (например, время или частота). 
                        Должен иметь одинаковую длину для всех серий.
        ys (list of array-like): Список массивов значений по оси Z (амплитуда/интенсивность). 
                                 Каждый элемент списка соответствует одной линии на графике.
        offsets (list of float, optional): Список смещений для каждой линии вдоль оси Y. 
                                           Если None, смещения генерируются автоматически 
                                           как np.arange(len(ys)).
        x_label (str): Подпись для оси X.
        y_label (str): Подпись для оси Y (ось смещения/категорий).
        z_label (str): Подпись для оси Z (ось значений).
        elev (float, optional): Угол возвышения камеры в градусах. По умолчанию 30.
        azim (float, optional): Азимутальный угол камеры в градусах. По умолчанию 45.
        roll (float, optional): Угол крена камеры в градусах. Поддерживается не всеми 
                                версиями Matplotlib. По умолчанию -3.
        save_folder_path (str, optional): Путь к директории для сохранения изображения. 
                                          Если None, файл не сохраняется.
        filename (str, optional): Имя файла для сохранения (без расширения). 
                                  Сохраняется как .png. Требуется наличие save_folder_path.
        show_plot (bool, optional): Если True, отображает график в интерактивном окне. 
                                    По умолчанию True.

    Returns:
        None: Функция ничего не возвращает, но может сохранить файл на диск 
              и/или отобразить график.

    Example:
        >>> import numpy as np
        >>> x = np.linspace(0, 10, 100)
        >>> ys = [np.sin(x + i) for i in range(5)]
        >>> plot_waterfall(x, ys, None, "Time", "Index", "Amplitude")
    """

    fig = plt.figure(figsize=(16, 9))
    ax = fig.add_subplot(111, projection='3d')

    n = len(ys)

    if offsets is None:
        offsets = np.arange(n)

    # нормализация для цвета
    colors = plt.cm.plasma(np.linspace(0, 1, n))
    # другие варианты 
    # 'viridis', 'inferno', 'turbo', 'YlOrRd'

    for i, (y, offset) in enumerate(zip(ys, offsets)):
        xs = x
        zs = y
        ys_line = np.full_like(xs, offset)

        ax.plot(xs, ys_line, zs, color=colors[i], linewidth=1)

    # подписи осей
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_zlabel(z_label)
    

    # установка углов
    ax.view_init(elev=elev, azim=azim)

    # roll работает не во всех версиях matplotlib
    try:
        ax.view_init(elev=elev, azim=azim, roll=roll)
    except TypeError:
        pass
    

    if save_folder_path is not None and filename is not None:
        full_path = os.path.join(save_folder_path, f"{filename}.png")
        plt.savefig(full_path, dpi=300, bbox_inches='tight')
        print(f"График сохранён: {full_path}")
    if show_plot:
        plt.tight_layout()
        plt.show()


filter_folder=r'C:\Users\namys_23hvwev\Documents\DATA\data_from_lnf\SOA_BTF100\linewidth_1nm'
wave_data, power_data = [],[]
ys = []
for wavelengt in range(1525, 1566):
    soa_full_path = Path(filter_folder)/rf'yokogawa_spectrum_SOA_wavelengh_{wavelengt}nm_linewidth_1nm_current_300mA.txt'

    wave_arr, power_arr = read_txt_xy(full_path=soa_full_path)
    mask = (wave_arr > 1400) & (wave_arr < 1600)
    power_arr=power_arr[mask]
    wave_arr=wave_arr[mask]
    max_index=np.argmax(power_arr)
    max_power=power_arr[max_index]
    power_arr=power_arr/max_power
    ys.append(power_arr)

    x = wave_arr

    





offsets = np.linspace(1525, 1566)


plot_waterfall(
    x,
    ys,
    offsets=offsets,
    x_label='Wavelength, nm',
    y_label='Filter wavelength, nm',
    z_label='Power, a.u.',
    elev=30,
    azim=45,
    roll=-3,
    save_folder_path=r'C:\Users\namys_23hvwev\Documents\laser_with_BTF',
    filename='waterfall'
)

