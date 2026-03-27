import numpy as np

def generate_rf_spectrum(
    length=100,            # Количество точек
    x_min=1.614e+9,         # Начало диапазона (Гц)
    x_max=7.6155e+9,        # Конец диапазона (Гц)
    peak_pos_range=None,    # Диапазон положения пика. Если None, то от x_min до x_max
    peak_height_range=(45, 50),   # Диапазон высоты пика
    peak_width_range=(1e+3, 5e+3), # Диапазон ширины пика
    baseline=-105,          # Уровень шума 
    noise_level=3,          # Разброс шума 
    seed=None               # Seed (None = случайный каждый раз)
):
    """Генерирует RF спектр с одним случайным пиком"""
    
    # Установка seed только если он явно передан
    if seed is not None:
        np.random.seed(seed)
    
    # Ось X
    x = np.linspace(x_min, x_max, length)
    
    # Если диапазон позиции пика не задан, используем весь диапазон
    if peak_pos_range is None:
        peak_pos_range = (x_min, x_max)
    
    # Случайные параметры пика
    peak_center = np.random.uniform(*peak_pos_range)
    peak_height = np.random.uniform(*peak_height_range)
    peak_width = np.random.uniform(*peak_width_range)
    
    # Базовая линия
    y = np.ones(length) * baseline
    
    # Гауссов пик
    y += peak_height * np.exp(-((x - peak_center) ** 2) / (2 * peak_width ** 2))
    
    # Шум
    y += np.random.normal(0, noise_level, length)
    
    return x, y

# Tektronix RSA306B
class RF306B():
    # When you init this class, connection is established
    def __init__(self):
        print(self.__class__.__name__, 'inited!')

    def disconnect(self):
        print("rsa.DEVICE_Disconnect")

    def set_cf(self, val):
        print(f'set_cf, {val}')

    def set_refLevel(self, val):
        print(f'set_refLevel, {val}')

    def set_span(self, val):
        print(f'set_span, {val}')

    def set_rbw(self, val):
        print(f'set_rbw, {val}')

    def set_start(self, val):
        print(f'set_start, {val}')

    def set_stop(self, val):
        print(f'set_stop, {val}')

    def get_rf(self):
        freq,trace = generate_rf_spectrum()
        print('get_rf')
        return freq, trace
