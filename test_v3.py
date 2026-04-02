import numpy as np
import matplotlib.pyplot as plt

def generate_simple_osc():
    # Параметры
    n_points = 1000
    duration_ns = 10.0  # Длительность 10 нс, как на ваших графиках
    
    # Случайная частота от 1 до 6 ГГц
    freq_hz = np.random.uniform(1e9, 6e9)
    
    # Случайная фаза от 0 до 2*pi
    phase_rad = np.random.uniform(0, 2 * np.pi)
    
    # Массив времени (в секундах для расчета, но отображать будем в нс)
    time_arr = np.linspace(0, duration_ns * 1e-9, n_points)
    
    # Генерация синуса
    voltage_arr = np.sin(2 * np.pi * freq_hz * time_arr + phase_rad)
    
    return time_arr, voltage_arr, freq_hz

# Пример использования с построением графика
if __name__ == "__main__":
    t, v, f = generate_simple_osc()
    
    print(f"Частота: {f/1e9:.2f} ГГц")
    
    plt.figure(figsize=(10, 5))
    plt.plot(t * 1e9, v) # Переводим время в нс для оси X
    plt.title(f"Sine Wave: {f/1e9:.2f} GHz")
    plt.xlabel("Time (ns)")
    plt.ylabel("Voltage (V)")
    plt.grid(True)
    plt.show()