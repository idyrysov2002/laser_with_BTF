import numpy as np
import pyvisa as visa
import matplotlib.pyplot as plt


def generate_osa_spectrum(
    length=100,  # Количество точек
    wave_min=1510,  # Начало диапазона (нм)
    wave_max=1570,  # Конец диапазона (нм)
    peak_pos_range=None,  # Диапазон положения пика (нм). Если None, то от wave_min до wave_max
    peak_height_range=(20, 21),  # Высота пика (дБм)
    peak_width_range=(0.001, 0.02),  # Ширина пика (нм)
    baseline=-60,  # Уровень шума/базовой линии (дБм)
    noise_level=0.5,  # Разброс шума (дБ)
    seed=None,  # Seed для воспроизводимости (None = случайный каждый раз)
):
    """Генерирует оптический спектр (OSA) с одним случайным пиком"""

    # Установка seed только если он явно передан
    if seed is not None:
        np.random.seed(seed)

    # Ось X (длина волны)
    x = np.linspace(wave_min, wave_max, length)

    # Если диапазон позиции пика не задан, используем весь диапазон волн
    if peak_pos_range is None:
        peak_pos_range = (wave_min, wave_max)

    # Случайные параметры пика
    peak_center = np.random.uniform(*peak_pos_range)
    peak_height = np.random.uniform(*peak_height_range)
    peak_width = np.random.uniform(*peak_width_range)

    # Базовая линия (шумовой фон)
    y = np.ones(length) * baseline

    # Гауссов пик
    y += peak_height * np.exp(-((x - peak_center) ** 2) / (2 * peak_width**2))

    # Добавление шума
    y += np.random.normal(0, noise_level, length)

    return x, y


class YokogawaOSA:
    """Класс для управления оптическим анализатором спектра Yokogawa через VISA.
    длина волны, разрешение, спан и др. задается в нм.
    Например, set_center(1550) устанавливает центр на длине волны 1550 нм
    """
    def __init__(self, dev_IP="TCPIP0::10.2.60.60::inst0::INSTR"):

        print(self.__class__.__name__, "inited!")

    def close_connect(self):
        print("Сonnection is closed")

    def set_start(self, val):
        print(f"set_start, {val}nm")

    def set_stop(self, val):
        print(f"set_stop, {val}nm")

    def set_resolution(self, val):
        print(f"set_resolution, {val}nm")

    def get_os(self):
        # Генерация тестового сигнала мощности
        x, y = generate_osa_spectrum()
        print("оптический спектр получен")
        return x, y


if __name__=="__main__":
    # Создание экземпляра класса
    osa = YokogawaOSA()

    # Настройка диапазона измерений 
    osa.set_start(1540)
    osa.set_stop(1590)

    # Запуск измерения и получение данных
    wave_arr, ampl_arr = osa.get_os()

    # Визуализация результатов
    plt.plot(wave_arr, ampl_arr)
    plt.show()

    # Закрытие соединения
    # osa.close_connect()
