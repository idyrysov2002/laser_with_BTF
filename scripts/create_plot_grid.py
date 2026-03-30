import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
from matplotlib.ticker import AutoMinorLocator

def create_plot_grid(data_list, save_folder_path, png_filename, 
                     main_title=None, show_plot=False):
    """
    Универсальная функция для построения сетки графиков (1x1, 1x2, 2x2).
    Автоматически определяет размер сетки в зависимости от количества данных.
    
    Параметры:
    ----------
    data_list : list of dicts or tuples
        Список данных для каждого подграфика. Каждый элемент может быть:
        1. Словарем: {'x': [...], 'y': [...], 'xlabel': '...', 'ylabel': '...', 'title': '...'}
        2. Кортежем/списком: ([x_data, 'xlabel'], [y_data, 'ylabel'], 'title')
        
        Если title не нужен, можно передать None.
        
    save_folder_path : str
        Путь к папке для сохранения.
    png_filename : str
        Имя файла без расширения.
    main_title : str, optional
        Общий заголовок всей фигуры.
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
        print(f"Предупреждение: Передано {n_plots} графиков. Будут отображены только первые 4.")
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
        Приводит входные данные к единому виду: dict с ключами x, y, xlabel, ylabel, title.
        Поддерживает формат: ([x, 'label'], [y, 'label'], 'title')
        """
        if isinstance(item, dict):
            return {
                'x': np.array(item.get('x', [])),
                'y': np.array(item.get('y', [])),
                'xlabel': item.get('xlabel', ''),
                'ylabel': item.get('ylabel', ''),
                'title': item.get('title', '')
            }
        elif isinstance(item, (list, tuple)) and len(item) >= 3:
            # Ожидаем: ([x_arr, x_lbl], [y_arr, y_lbl], title_str)
            x_part = item[0]
            y_part = item[1]
            title_part = item[2] if len(item) > 2 else None
            
            x_arr = np.array(x_part[0]) if isinstance(x_part, (list, tuple)) else np.array(x_part)
            x_lbl = str(x_part[1]) if isinstance(x_part, (list, tuple)) and len(x_part)>1 else ''
            
            y_arr = np.array(y_part[0]) if isinstance(y_part, (list, tuple)) else np.array(y_part)
            y_lbl = str(y_part[1]) if isinstance(y_part, (list, tuple)) and len(y_part)>1 else ''
            
            return {
                'x': x_arr,
                'y': y_arr,
                'xlabel': x_lbl,
                'ylabel': y_lbl,
                'title': title_part
            }
        else:
            raise ValueError(f"Неверный формат данных в элементе списка: {item}")

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
    TITLE_ALPHA = 0.9

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
        figsize = (16, 9)
    elif n_plots == 2:
        figsize = (16, 6)
    else:
        figsize = (16, 9)
        
    fig, axs = plt.subplots(nrows, ncols, figsize=figsize)
    
    # Превращаем axs в список для удобной итерации, даже если график один
    if n_plots == 1:
        axs = [axs]
    else:
        axs = axs.flatten()

    # Стиль плашки
    title_bbox_props = dict(boxstyle='round,pad=0.5', facecolor=COLOR_TITLE_BG, 
                            edgecolor='none', alpha=TITLE_ALPHA)

    for i, ax in enumerate(axs):
        if i >= n_plots:
            # Если сетка 2x2, а данных 3, скрываем лишний пустой график
            ax.axis('off')
            continue
            
        data = parsed_data[i]
        x, y = data['x'], data['y']
        x_lbl, y_lbl = data['xlabel'], data['ylabel']
        sub_title = data['title']

        if len(x) == 0 or len(y) == 0:
            ax.text(0.5, 0.5, 'Нет данных', ha='center', va='center', transform=ax.transAxes)
            continue
            
        # Линия
        ax.plot(x, y, linewidth=2, color='#1f77b4') 
        
        # Подписи осей
        if x_lbl:
            ax.set_xlabel(x_lbl, fontsize=FONT_SIZE_LABEL, fontname=FONT_FAMILY)
        if y_lbl:
            ax.set_ylabel(y_lbl, fontsize=FONT_SIZE_LABEL, fontname=FONT_FAMILY)
        
        # Сетка
        ax.grid(True, which='major', linestyle='-', linewidth=1, alpha=1.0)
        ax.xaxis.set_minor_locator(AutoMinorLocator())
        ax.yaxis.set_minor_locator(AutoMinorLocator())
        ax.grid(which='minor', linestyle=':', linewidth=0.5, alpha=0.5)

        # Заголовок внутри графика
        if sub_title:
            y_min, y_max = np.min(y), np.max(y)
            y_range = y_max - y_min
            
            if y_range > 0:
                title_y_pos = y_max + (y_range * 0.05)
            else:
                title_y_pos = y_max + 1
            
            curr_x_min, curr_x_max = ax.get_xlim()
            title_x_pos = (curr_x_min + curr_x_max) / 2
            
            ax.text(title_x_pos, title_y_pos, sub_title, 
                    fontsize=FONT_SIZE_TITLE_AXES, 
                    fontweight='bold',
                    color=COLOR_TITLE_TEXT,
                    fontname=FONT_FAMILY,
                    verticalalignment='bottom',
                    horizontalalignment='center',
                    bbox=title_bbox_props)
            
            current_ylim = ax.get_ylim()
            new_ylim_top = title_y_pos + (y_range * 0.15)
            ax.set_ylim(current_ylim[0], new_ylim_top)

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
        print(f"График ({nrows}x{ncols}) сохранён: {full_path}")

    # ========================
    # ПОКАЗ ИЛИ ЗАКРЫТИЕ
    # ========================
    if show_plot:
        plt.show()
    else:
        plt.close()
    
    return full_path

# ═══════════════════════════════════════════════════════════════
# ПРИМЕРЫ ИСПОЛЬЗОВАНИЯ
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    x = np.linspace(0, 10, 200)
    
    # Подготовка данных в удобном формате: ([x, label], [y, label], 'Title')
    plot_sin = ([x, "Время (с)"], [np.sin(x), "Амплитуда (В)"], "Синусоида")
    plot_cos = ([x, "Частота (Гц)"], [np.cos(x), "Мощность (дБ)"], "Косинусоида")
    plot_exp = ([x, "Длина (м)"], [np.exp(-x/2), "Затухание"], "Экспонента")
    plot_sq = ([x, "X"], [np.sin(x)**2, "Y"], "Квадрат синуса")

    # --- Сценарий 1: Только 2 графика (будет 1x2) ---
    create_plot_grid(
        data_list=[plot_sin, plot_cos],
        save_folder_path="./plots_dynamic",
        png_filename="layout_1x2",
        main_title="Пример сетки 1x2 (два графика)",
        show_plot=False
    )

    # --- Сценарий 2: 3 графика (будет 2x2, последний пустой) ---
    create_plot_grid(
        data_list=[plot_sin, plot_cos, plot_exp],
        save_folder_path="./plots_dynamic",
        png_filename="layout_2x2_three",
        main_title="Пример сетки 2x2 (три графика)",
        show_plot=False
    )
    
    # --- Сценарий 3: 4 графика (полная сетка 2x2) ---
    create_plot_grid(
        data_list=[plot_sin, plot_cos, plot_exp, plot_sq],
        save_folder_path="./plots_dynamic",
        png_filename="layout_2x2_full",
        main_title="Пример сетки 2x2 (четыре графика)",
        show_plot=True # Покажем последний пример
    )