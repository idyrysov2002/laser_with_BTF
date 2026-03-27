import numpy as np
import matplotlib.pyplot as plt
def generate_rf_spectrum(
    length=1000,        # Количество точек
    x_min=5.614e+9,           # начало диапазона
    x_max=5.6155e+9,          # конец диапазона
    peak_pos_range=(5.6146e+9, 5.6148e+9),  # Диапазон, где может появиться пик
    peak_height_range=(45, 50),  # Диапазон высоты пика
    peak_width_range=(1e+3, 5e+3),     # Диапазон ширины пика
    baseline=-105,            # Уровень шума 
    noise_level=3,            # Разброс шума 
    seed=42           # Фиксированный seed для воспроизводимости (опционально)
):
    """Генерирует спектр с одним случайным пиком"""
    
    if seed is not None:
        np.random.seed(seed)
    
    # Ось X
    x = np.linspace(x_min, x_max, length)
    
    # Случайные параметры пика
    peak_center = np.random.uniform(*peak_pos_range)
    peak_height = np.random.uniform(*peak_height_range)
    peak_width = np.random.uniform(*peak_width_range)
    
    # Базовая линия
    y = np.ones(length) * baseline
    
    # Пик (гауссова форма для плавности, но параметры — случайные)
    y += peak_height * np.exp(-((x - peak_center) ** 2) / (2 * peak_width ** 2))
    
    # Шум
    y += np.random.normal(0, noise_level, length)
    
   
    
    return x, y

if __name__ == "__main__":
    x, y = generate_rf_spectrum()
    plt.plot(x,y)
    plt.show()