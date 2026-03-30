import numpy as np
import matplotlib.pyplot as plt
import os

def calculate_FWHM_dBm(x_arr, y_arr, png_filename, save_folder_path):
    """
    Вычисляет полную ширину на половине максимальной мощности (FWHM) и строит график.
    
    Параметры:
    x_arr : array-like
        Массив координат (например, длина волны, частота или время).
    y_arr : array-like
        Массив значений мощности в единицах dBm.
    png_filename : str
        Имя файла для сохранения графика (без расширения .png).
    save_folder_path : str
        Путь к папке для сохранения графика.
        
    Возвращает:
    tuple
        (FWHM, full_path) - значение FWHM и полный путь к сохраненному файлу.
    """
    x = np.array(x_arr, dtype=float)
    y = np.array(y_arr, dtype=float)

    if len(x) != len(y) or len(x) < 2:
        raise ValueError("Массивы должны иметь одинаковую длину и содержать минимум 2 точки.")

    # 1. Находим индекс и значение пика
    max_idx = np.argmax(y)
    max_y = y[max_idx]
    max_x = x[max_idx]

    # Уровень половинной мощности (-3.0103 дБ от пика)
    half_max_y = max_y - 3.0103

    # Проверка: если весь сигнал ниже уровня половины (невозможно), возвращаем 0
    if np.all(y < half_max_y):
        fwhm = 0.0
        left_x = max_x
        right_x = max_x
    else:
        left_x = None
        right_x = None

        # 2. Поиск слева (от пика к началу)
        for i in range(max_idx, 0, -1):
            y_curr = y[i]
            y_prev = y[i-1]
            
            # Проверяем пересечение уровня
            if (y_curr >= half_max_y and y_prev < half_max_y):
                # Интерполяция
                dy = y_curr - y_prev
                if dy != 0:
                    t = (half_max_y - y_prev) / dy
                    left_x = x[i-1] + t * (x[i] - x[i-1])
                break
        
        # 3. Поиск справа (от пика к концу)
        for i in range(max_idx, len(y) - 1):
            y_curr = y[i]
            y_next = y[i+1]
            
            if (y_curr >= half_max_y and y_next < half_max_y):
                dy = y_next - y_curr
                if dy != 0:
                    t = (half_max_y - y_curr) / dy
                    right_x = x[i] + t * (x[i+1] - x[i])
                break
                
        if left_x is None or right_x is None:
            fwhm = 0.0
            if left_x is None:
                left_x = max_x
            if right_x is None:
                right_x = max_x
        else:
            fwhm = abs(right_x - left_x)

    # 4. Построение графика
    plt.figure(figsize=(10, 6))
    
    # Основной график
    plt.plot(x, y, 'r-', linewidth=2, label='Сигнал')
    
    # Точка максимума
    plt.plot(max_x, max_y, 'ro', markersize=8, label=f'Пик: {max_y:.2f} dBm')
    
    # Линия максимума
    plt.axhline(y=max_y, color='gray', linestyle='--', linewidth=1, alpha=0.7)
    plt.text(max_x, max_y + 0.5, f'{max_y:.2f} dBm', ha='center', fontsize=10)
    
    # Линия половины мощности
    plt.axhline(y=half_max_y, color='green', linestyle='--', linewidth=1.5, alpha=0.7, 
                label=f'Уровень -3.01 дБ: {half_max_y:.2f} dBm')
    plt.text(x.min() + (x.max()-x.min())*0.02, half_max_y, f'{half_max_y:.2f} dBm', 
             va='bottom', fontsize=10, color='green')
    
    # Вертикальные линии границ FWHM
    plt.axvline(x=left_x, color='blue', linestyle=':', linewidth=2, alpha=0.7)
    plt.axvline(x=right_x, color='blue', linestyle=':', linewidth=2, alpha=0.7)
    
    # Заштрихованная область FWHM
    plt.axvspan(left_x, right_x, alpha=0.2, color='blue', label=f'FWHM = {fwhm:.4f}')
    
    # Стрелка FWHM
    y_arrow = half_max_y - (max_y - half_max_y) * 0.3
    plt.annotate('', xy=(left_x, y_arrow), xytext=(right_x, y_arrow),
                 arrowprops=dict(arrowstyle='<->', color='blue', lw=2))
    plt.text((left_x + right_x) / 2, y_arrow - (max_y - half_max_y) * 0.15, 
             f'FWHM = {fwhm:.4f}', ha='center', va='top', fontsize=12, 
             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    # Подписи точек пересечения
    plt.plot(left_x, half_max_y, 'bo', markersize=6)
    plt.plot(right_x, half_max_y, 'bo', markersize=6)
    plt.text(left_x, half_max_y + 0.3, f'x₁={left_x:.4f}', ha='center', fontsize=9)
    plt.text(right_x, half_max_y + 0.3, f'x₂={right_x:.4f}', ha='center', fontsize=9)
    
    # Оформление
    plt.xlabel('X', fontsize=12)
    plt.ylabel('Мощность (dBm)', fontsize=12)
    plt.title(f'Анализ FWHM\nFWHM = {fwhm:.4f}', fontsize=14, fontweight='bold')
    plt.legend(loc='best', fontsize=10)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    # Создание пути к файлу
    os.makedirs(save_folder_path, exist_ok=True)
    full_path = os.path.join(save_folder_path, f"{png_filename}.png")
    
    # Сохранение графика
    plt.savefig(full_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    return fwhm, full_path


# Пример использования:
if __name__ == "__main__":
    # Создадим тестовые данные
    sigma = 1.0
    center = 5.0
    x_test = np.linspace(0, 10, 2000)
    
    y_linear = np.exp(-0.5 * ((x_test - center) / sigma)**2)
    y_dbm = 10 * np.log10(np.maximum(y_linear, 1e-20))
    
    # Вызов функции
    fwhm_value, file_path = calculate_FWHM_dBm(
        x_test, 
        y_dbm, 
        "fwhm_analysis", 
        "./plots"
    )
    
    print(f"Рассчитанный FWHM: {fwhm_value:.6f}")
    print(f"График сохранен: {file_path}")