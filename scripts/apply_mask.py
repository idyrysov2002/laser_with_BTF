import os
import numpy as np
import matplotlib.pyplot as plt
from create_map_and_save import create_map_and_save
from scripts.read_from_txt import read_txt_xyz

# ============================================================
# ФУНКЦИЯ ПРИМЕНЕНИЯ МАСКИ 
# ============================================================
def apply_mask(x, y, z, 
               x_min=None, x_max=None, 
               y_min=None, y_max=None):
    """
    Применить маску к данным по границам осей X и Y.

    Args:
        x (array): Массив координат X
        y (array): Массив координат Y
        z (array): Массив значений Z
        x_min (float, optional): Минимальная граница по оси X. Defaults to None.
        x_max (float, optional): Максимальная граница по оси X. Defaults to None.
        y_min (float, optional): Минимальная граница по оси Y. Defaults to None.
        y_max (float, optional): Максимальная граница по оси Y. Defaults to None.

    Returns:
        tuple: Кортеж из трёх отфильтрованных массивов (x_filtered, y_filtered, z_filtered)
    """
    x = np.array(x)
    y = np.array(y)
    z = np.array(z)

    # Создаём маску
    mask = np.ones(len(x), dtype=bool)

    if x_min is not None:
        mask &= (x >= x_min)
    if x_max is not None:
        mask &= (x <= x_max)
    if y_min is not None:
        mask &= (y >= y_min)
    if y_max is not None:
        mask &= (y <= y_max)

    # Применяем маску
    x_filtered = x[mask]
    y_filtered = y[mask]
    z_filtered = z[mask]

    print(f"Маска: было {len(x)} точек, осталось {len(x_filtered)} точек")

    return x_filtered, y_filtered,z_filtered


# ============================================================
# ПРИМЕР ИСПОЛЬЗОВАНИЯ
# ============================================================
if __name__ == "__main__":

    filepath=r"C:\Users\study\Documents\LAB_424\test\maps\RF_rf_freq_max.txt"
    current, delay, freqs = read_txt_xyz(full_path=filepath)
    freqs = freqs/1e+9
    current_min=0
    current_max=500
    delay_min=0
    delay_max=300
    x_label='Current, mA'
    y_label='Delay, ps'
    z_label='Frequency, GHz'
    map_title = "Frequency vs current vs delay"

    current_filtered, delay_filtered, freqs_filtered = apply_mask(
        x=current, y=delay, z=freqs, x_min=300, x_max=500,y_min=delay_min,y_max=delay_max
    )
    x_arr=[current_filtered,x_label]
    y_arr=[delay_filtered,y_label]
    z_arr=[freqs_filtered, z_label]
    create_map_and_save(
        x_arr=x_arr, y_arr=y_arr, z_arr=z_arr, title=map_title, folder_path=None, filename=None, show_plot=True
    )
