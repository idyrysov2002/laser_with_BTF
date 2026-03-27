import os
import numpy as np
import matplotlib.pyplot as plt

def create_map_and_save(x_arr, y_arr, z_arr, title=None, folder_path=None, filename=None, show_plot=True):
    """
    Построить контурную карту (heatmap) с опциями показа и сохранения.
    TXT сохраняется ПЕРЕД графиком (данные всегда записываются).
    """

    # ========================
    # НАСТРОЙКИ ШРИФТОВ
    # ========================
    # FONT_FAMILY = 'Times New Roman'
    FONT_FAMILY = "Times New Roman"
    FONT_SIZE_LABEL = 20
    FONT_SIZE_TICK_COLORBAR = 18
    FONT_SIZE_TITLE_TEXT = 25

    # ========================
    # РАСПАКОВКА ДАННЫХ
    # ========================
    x, x_label = x_arr
    y, y_label = y_arr
    z, z_label = z_arr

    # Конвертация в numpy
    current_values = np.array(x)
    delay_values = np.array(y)
    map_values = np.array(z)

    # ПРОВЕРКА ДЛИН
    if not (len(current_values) == len(delay_values) == len(map_values)):
        raise ValueError("Длины массивов X, Y и Z должны совпадать!")
    # ========================
    # ПОДГОТОВКА ПУТЕЙ
    # ========================
    png_path = None
    txt_path = None

    if folder_path is not None and filename is not None:
        os.makedirs(folder_path, exist_ok=True)
        png_path = os.path.join(folder_path, f"{filename}.png")
        txt_path = os.path.join(folder_path, f"{filename}.txt")

    # ========================
    # СОХРАНЕНИЕ TXT (ВСЕГДА, ДО ГРАФИКА)
    # ========================
    if txt_path is not None:
        try:
            with open(txt_path, 'w', encoding='utf-8') as file:
                txt_header = f'{x_label}\t{y_label}\t{z_label}'
                file.write(txt_header + "\n")
                for xi, yi, zi in zip(current_values, delay_values, map_values):
                    file.write(f"{xi}\t{yi}\t{zi}\n")
            print(f"Данные сохранены: {txt_path}")
        except Exception as e:
            print(f"Ошибка сохранения TXT: {e}")

    # ========================
    # ПРОВЕРКА ДАННЫХ (ЧТОБЫ НЕ БЫЛО (0,0))
    # ========================
    if len(current_values) == 0 or len(delay_values) == 0 or len(map_values) == 0:
        print("ПРЕДУПРЕЖДЕНИЕ: Нет данных для построения графика (массивы пустые).")
        return

    # Проверка на уникальные значения (нужно минимум 2 для контура)
    current_unique = np.unique(current_values)
    delay_unique = np.unique(delay_values)

    if len(current_unique) < 2 or len(delay_unique) < 2:
        print("ПРЕДУПРЕЖДЕНИЕ: Недостаточно уникальных значений для контурной карты.")
        print(f"   Уникальных X: {len(current_unique)}, Уникальных Y: {len(delay_unique)}")
        return

    # ========================
    # ПОДГОТОВКА МАТРИЦЫ
    # ========================
    map_matrix = np.full((len(delay_unique), len(current_unique)), np.nan)

    for i, delay in enumerate(delay_unique):
        for j, current in enumerate(current_unique):
            mask = (current_values == current) & (delay_values == delay)
            if np.any(mask):
                map_matrix[i, j] = map_values[mask][0]

    # ========================
    # ПОСТРОЕНИЕ ГРАФИКА
    # ========================
    plt.figure(figsize=(16, 9))
    X, Y = np.meshgrid(current_unique, delay_unique)

    vmin = np.nanmin(map_matrix)
    vmax = np.nanmax(map_matrix)

    contour = plt.contourf(X, Y, map_matrix, vmin=vmin, vmax=vmax,cmap="viridis")
    if title:
        plt.title(title, fontsize=FONT_SIZE_TITLE_TEXT, fontname=FONT_FAMILY)

    cbar = plt.colorbar(contour)
    cbar.set_label(z_label, fontsize=FONT_SIZE_LABEL, fontname=FONT_FAMILY)
    cbar.ax.yaxis.set_tick_params(labelsize=FONT_SIZE_TICK_COLORBAR)

    plt.xlabel(x_label, fontsize=FONT_SIZE_LABEL, fontname=FONT_FAMILY)
    plt.ylabel(y_label, fontsize=FONT_SIZE_LABEL, fontname=FONT_FAMILY)
    ax = plt.gca()
    ax.tick_params(axis='both', labelsize=FONT_SIZE_TICK_COLORBAR)
    plt.grid(True, which='major', linestyle='-', linewidth=0.8, alpha=0.4, color='black')
    plt.tight_layout()
    # ========================
    # СОХРАНЕНИЕ PNG И ВЫВОД
    # ========================
    if png_path is not None:
        try:
            plt.savefig(png_path, dpi=300, bbox_inches='tight')
            print(f"График сохранён: {png_path}")
        except Exception as e:
            print(f"Ошибка сохранения графика: {e}")

    if show_plot:
        plt.show()

    plt.close()

if __name__ == "__main__":
    current = np.repeat([10, 20, 30, 40, 50], 4)      # Ток, мА
    delay = np.tile([0, 50, 100, 150], 5)             # Задержка, пс
    power = np.random.uniform(0.5, 2.0, len(current)) # Мощность, мВт

    # Вызов функции
    create_map_and_save(
        x_arr=[current, 'Ток, мА'],
        y_arr=[delay, 'Задержка, пс'],
        z_arr=[power, 'Мощность, мВт'],
        title='Зависимость мощности от тока и задержки',
        folder_path='maps',
        filename='map',
        show_plot=True
        
        
        
    )
