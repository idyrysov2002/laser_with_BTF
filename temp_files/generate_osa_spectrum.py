import numpy as np
import matplotlib.pyplot as plt

def generate_osa_spectrum(
    length=1000,            # Количество точек
    wave_min=1510,          # Начало диапазона (нм)
    wave_max=1570,          # Конец диапазона (нм)
    peak_pos_range=(1525,1565),    # Диапазон положения пика (нм)
    peak_height_range=(15, 16),      # Высота пика (дБм)
    peak_width_range=(0.001, 0.02),   # Ширина пика (нм)
    baseline=0,           # Уровень шума (дБм)
    noise_level=0.5,          # Разброс шума (дБ)
    seed=4               # Seed для воспроизводимости
):
    """Генерирует оптический спектр (OSA) с одним случайным пиком"""
    
    if seed is not None:
        np.random.seed(seed)
    
    # Ось X (длина волны)
    x = np.linspace(wave_min, wave_max, length)
    
    # Случайные параметры пика
    peak_center = np.random.uniform(*peak_pos_range)
    peak_height = np.random.uniform(*peak_height_range)
    peak_width = np.random.uniform(*peak_width_range)
    
    # Базовая линия (шумовой фон)
    y = np.ones(length) * baseline
    
    # Гауссов пик
    y += peak_height * np.exp(-((x - peak_center) ** 2) / (2 * peak_width ** 2))
    
    # Добавление шума
    y += np.random.normal(0, noise_level, length)
    
    return x, y

if __name__ == "__main__":
    x, y = generate_osa_spectrum()
    plt.plot(x, y)
    plt.show()