import numpy as np
import os


def read_txt_xyz(full_path, header=1):
    """
    Читает txt файл с тремя столбцами.
    Тип возвращаемого значения: tuple[numpy.ndarray, numpy.ndarray, numpy.ndarray]
    """
    if not os.path.exists(full_path):
        print(f"Ошибка: Файл не найден по пути {full_path}")
        return None, None, None

    try:
        # Добавлен параметр encoding='windows-1251' для корректного чтения кириллицы
        data = np.loadtxt(
            full_path, skiprows=header, delimiter="\t", encoding="windows-1251"
        )

        if data.size == 0 or data.shape[1] < 3:
            print("Ошибка: В файле недостаточно данных или столбцов.")
            return None, None, None

        x = data[:, 0]
        y = data[:, 1]
        z = data[:, 2]

        return x, y, z

    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        return None, None, None

def read_txt_xy(full_path, header=1):
    """
    Читает txt файл с двумя столбцами (X, Y).
    Возвращает: x, y (массивы numpy) или None, None при ошибке.
    """
    if not os.path.exists(full_path):
        print(f"Ошибка: Файл не найден по пути {full_path}")
        return None, None  

    try:
        # Чтение данных
        data = np.loadtxt(
            full_path, 
            skiprows=header, 
            delimiter="\t", 
            encoding="windows-1251",
            ndmin=2  # Гарантия, что массив будет как минимум 2D, даже если одна строка
        )

        # Проверка на пустоту и количество столбцов
        if data.size == 0 or data.shape[1] < 2:
            print("Ошибка: В файле недостаточно данных или столбцов.")
            return None, None 

        x = data[:, 0]
        y = data[:, 1]
        
        return x, y

    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        return None, None
