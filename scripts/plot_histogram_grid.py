import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
from matplotlib.ticker import AutoMinorLocator

def plot_histogram_grid(data_list, x_label, y_label, save_folder_path, png_filename, 
                        main_title=None, bins=30, show_plot=False):
    """
    Построение сетки гистограмм (1x1, 1x2, 2x2) с общими подписями осей.
    
    Параметры:
    ----------
    data_list : list of tuples or dicts
        Список данных для гистограмм. Каждый элемент должен содержать массив данных и заголовок.
        Формат элемента:
        1. Кортеж: (data_array, 'Title')
        2. Словарь: {'data': [...], 'title': '...'}
        
    x_label : str
        Общая подпись для оси X (для всех графиков).
    y_label : str
        Общая подпись для оси Y (для всех графиков).
        
    save_folder_path : str
        Путь к папке для сохранения.
    png_filename : str
        Имя файла без расширения.
    main_title : str, optional
        Общий заголовок всей фигуры.
    bins : int, optional
        Количество столбцов (бинов) в гистограмме. По умолчанию 30.
    show_plot : bool
        Показывать график сразу (False по умолчанию).
        
    Возвращает:
    -----------
    str
        Полный путь к сохраненному файлу.
    """

    n_plots = len(data_list)
    
    if n_plots == 0:
        raise ValueError("Список данных не может быть пустым.")
    if n_plots > 4:
        print(f"Предупреждение: Передано {n_plots} гистограмм. Будут отображены только первые 4.")
        data_list = data_list[:4]
        n_plots = 4

    # Определение размера сетки
    if n_plots == 1:
        nrows, ncols = 1, 1
    elif n_plots == 2:
        nrows, ncols = 1, 2
    else: # 3 или 4
        nrows, ncols = 2, 2

    # ========================
    # РАСПАКОВКА ДАННЫХ
    # ========================
    def unpack_data(item):
        """
        Приводит входные данные к виду: {'data': array, 'title': str}
        """
        if isinstance(item, dict):
            return {
                'data': np.array(item.get('data', [])),
                'title': item.get('title', '')
            }
        elif isinstance(item, (list, tuple)) and len(item) >= 2:
            # Ожидаем: (data_array, title_str)
            data_arr = np.array(item[0])
            title_str = str(item[1]) if len(item) > 1 else ''
            return {
                'data': data_arr,
                'title': title_str
            }
        else:
            # Если передан просто массив без заголовка
            return {
                'data': np.array(item),
                'title': ''
            }

    parsed_data = [unpack_data(item) for item in data_list]

    # ========================
    # НАСТРОЙКИ ШРИФТОВ (Единый стиль)
    # ========================
    FONT_FAMILY = 'serif'
    FONT_SIZE_BASE = 16
    FONT_SIZE_TITLE_AXES = 18
    FONT_SIZE_LABEL = 20
    FONT_SIZE_TICK = 16
    FONT_SIZE_MAIN_TITLE = 22
    
    COLOR_TITLE_BG = 'white'
    COLOR_TITLE_TEXT = 'black'
    TITLE_ALPHA = 0

    # ========================
    # ПОДГОТОВКА ПУТЕЙ
    # ========================
    full_path = None
    if save_folder_path and png_filename:
        if not save_folder_path.strip():
            save_folder_path = '.'
        os.makedirs(save_folder_path, exist_ok=True)
        full_path = os.path.join(save_folder_path, f"{png_filename}.png")

    # ========================
    # НАСТРОЙКА СТИЛЯ
    # ========================
    rcParams['font.family'] = FONT_FAMILY
    rcParams.update({
        'font.size': FONT_SIZE_BASE,
        'axes.titlesize': FONT_SIZE_TITLE_AXES,
        'axes.labelsize': FONT_SIZE_LABEL,
        'xtick.labelsize': FONT_SIZE_TICK,
        'ytick.labelsize': FONT_SIZE_TICK,
        'figure.titlesize': FONT_SIZE_MAIN_TITLE,
        'figure.autolayout': True
    })

    # ========================
    # ПОСТРОЕНИЕ ГРАФИКА
    # ========================
    # figsize адаптируется под количество графиков
    if n_plots == 1:
        figsize = (10, 6)
    elif n_plots == 2:
        figsize = (16, 6)
    else:
        figsize = (16, 10)
        
    fig, axs = plt.subplots(nrows, ncols, figsize=figsize)
    
    # Превращаем axs в список для удобной итерации
    if n_plots == 1:
        axs = [axs]
    else:
        axs = axs.flatten()

    # Стиль плашки
    title_bbox_props = dict(boxstyle='round,pad=0.5', facecolor=COLOR_TITLE_BG, 
                            edgecolor='none', alpha=TITLE_ALPHA)

    for i, ax in enumerate(axs):
        if i >= n_plots:
            ax.axis('off')
            continue
            
        item = parsed_data[i]
        data = item['data']
        sub_title = item['title']

        if len(data) == 0:
            ax.text(0.5, 0.5, 'Нет данных', ha='center', va='center', transform=ax.transAxes)
            continue
            
        # Построение гистограммы
        # color='#1f77b4' - стандартный синий цвет matplotlib
        # edgecolor='black' - черные границы столбцов для четкости
        ax.hist(data, bins=bins, color='#1f77b4', edgecolor='black', alpha=0.7, linewidth=1.2)
        
        # Установка общих подписей осей
        ax.set_xlabel(x_label, fontsize=FONT_SIZE_LABEL, fontname=FONT_FAMILY)
        ax.set_ylabel(y_label, fontsize=FONT_SIZE_LABEL, fontname=FONT_FAMILY)
        
        # Сетка
        # ax.grid(True, which='major', linestyle='-', linewidth=1, alpha=1.0, axis='y') # Для гистограмм чаще нужна сетка только по Y
        ax.xaxis.set_minor_locator(AutoMinorLocator())
        ax.yaxis.set_minor_locator(AutoMinorLocator())
        # ax.grid(which='minor', linestyle=':', linewidth=0.5, alpha=0.5, axis='y')

        # Заголовок внутри графика (над данными)
        if sub_title:
            # Получаем текущие пределы осей после построения гистограммы
            curr_x_min, curr_x_max = ax.get_xlim()
            curr_y_min, curr_y_max = ax.get_ylim()
            
            y_range = curr_y_max - curr_y_min
            
            # Позиция Y: чуть выше максимума
            title_y_pos = curr_y_max + (y_range * 0.05)
            if y_range == 0:
                title_y_pos = curr_y_max + 1
            
            # Позиция X: центр
            title_x_pos = (curr_x_min + curr_x_max) / 2
            
            ax.text(title_x_pos, title_y_pos, sub_title, 
                    fontsize=FONT_SIZE_TITLE_AXES, 
                    fontweight='bold',
                    color=COLOR_TITLE_TEXT,
                    fontname=FONT_FAMILY,
                    verticalalignment='bottom',
                    horizontalalignment='center',
                    bbox=title_bbox_props)
            
            # Расширяем лимит Y, чтобы заголовок влез
            new_ylim_top = title_y_pos + (y_range * 0.15)
            ax.set_ylim(curr_y_min, new_ylim_top)

    # Отступы
    plt.subplots_adjust(hspace=0.3, wspace=0.25)

    # Общий заголовок
    if main_title:
        fig.suptitle(main_title, fontsize=FONT_SIZE_MAIN_TITLE, fontweight='bold', y=0.98, fontname=FONT_FAMILY)

    # ========================
    # СОХРАНЕНИЕ
    # ========================
    if full_path:
        plt.savefig(full_path, dpi=300, bbox_inches='tight')
        print(f"Гистограмма ({nrows}x{ncols}) сохранена: {full_path}")

    # ========================
    # ПОКАЗ ИЛИ ЗАКРЫТИЕ
    # ========================
    if show_plot:
        plt.show()
    else:
        plt.close()
    
    return full_path

# ═══════════════════════════════════════════════════════════════
# ПРИМЕР ИСПОЛЬЗОВАНИЯ
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    # Генерация тестовых данных (нормальное распределение)
    data1 = np.random.normal(loc=0, scale=1, size=1000)
    data2 = np.random.normal(loc=2, scale=1.5, size=1000)
    data3 = np.random.normal(loc=-1, scale=0.8, size=1000)
    data4 = np.random.normal(loc=1, scale=2, size=1000)

    # Формат данных: (массив_данных, 'Заголовок')
    hist1 = (data1, "Распределение А")
    hist2 = (data2, "Распределение Б")
    hist3 = (data3, "Распределение В")
    hist4 = (data4, "Распределение Г")

    # Пример вызова для 3 гистограмм
    plot_histogram_grid(
        data_list=[hist1, hist2, hist3],
        x_label="Значение (ед.)",
        y_label="Частота (кол-во)",
        save_folder_path="./plots_hist",
        png_filename="histogram_grid_3",
        main_title="Статистический анализ распределений",
        bins=40,          # Количество столбцов
        show_plot=True
    )