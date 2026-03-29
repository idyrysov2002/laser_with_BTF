import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
from matplotlib.ticker import AutoMinorLocator

def plot_histogram_and_save(data, bins=10, title=None, xlabel=None, ylabel=None,
                            folder_path=None, filename=None, show_plot=True):
    """
    Построить гистограмму с опциями показа и сохранения.
    """
    
    # ========================
    # ПОДГОТОВКА ПУТЕЙ
    # ========================
    full_path = None
    
    if folder_path is not None and filename is not None:
        if not folder_path or not folder_path.strip():
            folder_path = '.'
        os.makedirs(folder_path, exist_ok=True)
        full_path = os.path.join(folder_path, f"{filename}.png")

    # ========================
    # НАСТРОЙКИ ШРИФТОВ
    # ========================
    FONT_FAMILY = 'Times New Roman'
    FONT_SIZE_BASE = 22
    FONT_SIZE_TITLE = 22
    FONT_SIZE_LABEL = 22
    FONT_SIZE_TICK = 22  # Чуть увеличил для наглядности
    FONT_SIZE_TITLE_TEXT = 24
    
    FIG_SIZE = (16, 9)
    SAVE_DPI = 300

    # ========================
    # НАСТРОЙКА СТИЛЯ
    # ========================
    rcParams['font.family'] = FONT_FAMILY
    rcParams.update({
        'font.size': FONT_SIZE_BASE,
        'axes.titlesize': FONT_SIZE_TITLE,
        'axes.labelsize': FONT_SIZE_LABEL,
        'xtick.labelsize': FONT_SIZE_TICK,
        'ytick.labelsize': FONT_SIZE_TICK,
        'figure.autolayout': True
    })

    # ========================
    # ПОСТРОЕНИЕ ГИСТОГРАММЫ
    # ========================
    fig, ax = plt.subplots(figsize=FIG_SIZE) # Получаем доступ к объекту осей 'ax'
    
    ax.hist(data, bins=bins, edgecolor='black', linewidth=1, alpha=0.8)
    
    if title is not None:
        ax.set_title(title, fontsize=FONT_SIZE_TITLE_TEXT, fontname=FONT_FAMILY)
    if xlabel is not None:
        ax.set_xlabel(xlabel, fontsize=FONT_SIZE_LABEL, fontname=FONT_FAMILY)
    if ylabel is not None:
        ax.set_ylabel(ylabel, fontsize=FONT_SIZE_LABEL, fontname=FONT_FAMILY)

    # ========================
    # ДОБАВЛЕНИЕ МЕЛКИХ ДЕЛЕНИЙ (НОВОЕ)
    # ========================
    # Включаем минорные тики на обеих осях
    ax.minorticks_on()
    
    # Настраиваем вид минорных тиков (черточки)
    # length=5 - длина черточки, width=1 - толщина, color='black' - цвет
    ax.tick_params(axis='both', which='minor', length=7, width=1.5, color='black')
    
    # Если хочешь добавить легкую сетку по мелким делениям, раскомментируй строку ниже:
    # ax.grid(which='minor', linestyle=':', linewidth=0.5, alpha=0.5)

    # ========================
    # СОХРАНЕНИЕ
    # ========================
    if full_path is not None:
        plt.savefig(full_path, dpi=SAVE_DPI, bbox_inches='tight')
        print(f"График сохранён: {full_path}\n")

    # ========================
    # ПОКАЗ ИЛИ ЗАКРЫТИЕ
    # ========================
    if show_plot:
        plt.show()
    else:
        plt.close()
    
    return full_path

if __name__ == "__main__":
    # Пример данных (нормальное распределение)
    data = np.random.randn(1000) * 10 + 500
   
    # ───────────────────────────────────────────────────────────
    # ТОЛЬКО ПОКАЗАТЬ (без сохранения)
    # ───────────────────────────────────────────────────────────
    plot_histogram_and_save(
        data=data,
        title="Распределение данных",
        xlabel="Значения",
        ylabel="Количество попаданий в интервал, шт"
        # folder_path и filename не указаны → не сохраняем
        # show_plot=True по умолчанию → показываем
    )