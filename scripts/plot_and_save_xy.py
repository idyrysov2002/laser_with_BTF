import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
from matplotlib.ticker import AutoMinorLocator

def plot_and_save_xy(x, y, title, xlabel, ylabel, 
                  folder_path=None, filename=None, show_plot=False):
    """
    Построить график с опциями показа и сохранения.
    
    Параметры:
    - x, y: данные для графика
    - title, xlabel, ylabel: подписи
    - folder_path: папка для сохранения (None = не сохранять)
    - filename: имя файла (None = не сохранять)
    - show_plot: показывать ли график (True/False)
    """
    # перевод в numpy
    x=np.array(x)
    y=np.array(y)
    # ========================
    # НАСТРОЙКИ ШРИФТОВ
    # ========================

    FONT_FAMILY = 'serif'
    FONT_SIZE_BASE = 16          # Базовый размер шрифта
    FONT_SIZE_TITLE = 16      # Заголовок осей (axes title)
    FONT_SIZE_LABEL = 20         # Подписи осей (X, Y)
    FONT_SIZE_TICK = 16          # Деления осей
    FONT_SIZE_TITLE_TEXT = 22   # Заголовок графика (plt.title)
    
    
    # ========================
    # ПОДГОТОВКА ПУТЕЙ
    # ========================
    full_path = None
    
    if folder_path is not None and filename is not None:
        # Защита от пустого пути
        if not folder_path or not folder_path.strip():
            folder_path = '.'
        
        # Убедимся, что папка существует
        os.makedirs(folder_path, exist_ok=True)

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
        'figure.autolayout': True  # автоматическая подгонка макета
    })

    # ========================
    # ПОСТРОЕНИЕ ГРАФИКА
    # ========================
    plt.figure(figsize=(16, 9))
    plt.plot(x, y, linewidth=2)
    if title is not None:
        plt.title(title, fontsize=FONT_SIZE_TITLE_TEXT, fontname=FONT_FAMILY)
    plt.xlabel(xlabel, fontsize=FONT_SIZE_LABEL, fontname=FONT_FAMILY)
    plt.ylabel(ylabel, fontsize=FONT_SIZE_LABEL, fontname=FONT_FAMILY)
    
    # Основная сетка
    plt.grid(True, which='major', linestyle='-', linewidth=1, alpha=1)
    
    
    # Настройка осей для автоматического отображения мелких делений
    ax = plt.gca()
    ax.xaxis.set_minor_locator(AutoMinorLocator())  
    ax.yaxis.set_minor_locator(AutoMinorLocator())  

    # ========================
    # СОХРАНЕНИЕ
    # ========================
    if folder_path is not None and filename is not None:
        full_path = os.path.join(folder_path, f"{filename}.png")
        plt.savefig(full_path, dpi=300, bbox_inches='tight')
        print(f"График сохранён: {full_path}")

    # ========================
    # ПОКАЗ ИЛИ ЗАКРЫТИЕ
    # ========================
    if show_plot:
        plt.show()
    else:
        plt.close()  # Освобождаем память
    
    return full_path

# ═══════════════════════════════════════════════════════════════
# ПРИМЕРЫ ИСПОЛЬЗОВАНИЯ
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    # Пример данных
    x = [1, 2, 3, 4, 5]
    y = [2, 4, 1, 5, 3]
   
    # ───────────────────────────────────────────────────────────
    # ТОЛЬКО ПОКАЗАТЬ (без сохранения)
    # ───────────────────────────────────────────────────────────
    plot_and_save_xy(
        x=x,
        y=y,
        title='График',
        xlabel="Ось X",
        ylabel="Ось Y",
        folder_path='graph',
        filename='example',
        show_plot=True #по умолчанию → показываем
    )
    
   