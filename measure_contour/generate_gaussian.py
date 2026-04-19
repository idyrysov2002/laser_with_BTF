import numpy as np
import matplotlib.pyplot as plt

def generate_gaussian(x_arr, x_peak, y_peak, fwhm):
    """
    Генерирует значения гауссовой кривой для заданной сетки x.
    
    Параметры:
    x_arr   : array-like - сетка координат X
    x_peak  : float      - координата X центра пика
    y_peak  : float      - высота пика (амплитуда)
    fwhm    : float      - полная ширина на половине высоты
    
    Возвращает:
    y_gauss : ndarray    - массив значений Y гауссовой кривой
    """
    # 1. Вычисляем sigma из FWHM
    # FWHM = 2 * sqrt(2 * ln(2)) * sigma
    sigma = fwhm / (2 * np.sqrt(2 * np.log(2)))
    
    # 2. Вычисляем Гаусс
    # y = A * exp( -(x - x0)^2 / (2 * sigma^2) )
    y_gauss = y_peak * np.exp(-((x_arr - x_peak)**2) / (2 * sigma**2))
    
    return y_gauss

# --- Пример использования ---

# 1. Задаем входные данные
x_data = np.linspace(0, 10, 500)  # Ваша сетка
x_peak_val = 5.0                   # Координата пика X
y_peak_val = 10.0                  # Координата пика Y (высота)
fwhm_val = 2.0                     # Ширина пика

# 2. Получаем значения гаусса
y_gauss = generate_gaussian(x_data, x_peak_val, y_peak_val, fwhm_val)

# 3. Рисуем
plt.figure(figsize=(10, 6))
plt.plot(x_data, y_gauss, 'b-', linewidth=2, label='Gaussian Fit')
plt.axvline(x=x_peak_val, color='r', linestyle='--', alpha=0.5, label=f'Peak X={x_peak_val}')
plt.axhline(y=y_peak_val/2, color='g', linestyle=':', alpha=0.5, label='Half Max')
plt.scatter([x_peak_val], [y_peak_val], color='red', zorder=5)
plt.title(f'Gaussian Curve (FWHM={fwhm_val})')
plt.xlabel('X')
plt.ylabel('Y')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()