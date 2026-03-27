import matplotlib.pyplot as plt
import os
from matplotlib import rcParams
from matplotlib.ticker import AutoMinorLocator  

def plot_and_save(x, y, title, xlabel, ylabel, folder_path, filename, show_plot=False):

    minor_grid=True
    font_family='Times New Roman'
    # Убедимся, что папка существует
    os.makedirs(folder_path, exist_ok=True)

    # Настройка шрифтов
    rcParams['font.family'] = font_family
    rcParams.update({
        'font.size': 16,
        'axes.titlesize': 18,
        'axes.labelsize': 16,
        'xtick.labelsize': 15,
        'ytick.labelsize': 15,
        'figure.autolayout': True  # автоматическая подгонка макета
    })

    # Создаем график
    plt.figure(figsize=(16, 9))
    plt.plot(x, y, linewidth=2)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    
    # Основная сетка
    plt.grid(True, which='major', linestyle='-', linewidth=1, alpha=1)
    
    # Добавляем мелкую сетку (если включено)
    if minor_grid:
        plt.grid(True, which='minor', linestyle=':', linewidth=1, alpha=1)
        plt.minorticks_on()  # Включаем мелкие деления
    
    # Настройка осей для автоматического отображения мелких делений
    ax = plt.gca()
    ax.xaxis.set_minor_locator(AutoMinorLocator())  
    ax.yaxis.set_minor_locator(AutoMinorLocator())  

    # Формируем полный путь к файлу
    full_path = os.path.join(folder_path, f"{filename}.png")
    
    # Сохраняем
    plt.savefig(full_path, dpi=300, bbox_inches='tight')

    if show_plot:
        plt.show()
    else:
        plt.close()  # Освобождаем память
    
    print(f"График сохранён: {full_path}")
    return full_path


# Пример использования функции
if __name__ == "__main__":
    # Пример данных
    x = [1, 2, 3, 4, 5]
    y = [1, 2, 3, 4, 5]
   
    # Вызов функции с новыми параметрами
    plot_and_save(
        x=x,
        y=y,
        title="Зависимость y(x)",
        xlabel="Ось X",
        ylabel="Ось Y",
        folder_path="./plots",
        filename="example_plot",
        show_plot=True
    )