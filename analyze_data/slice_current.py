def slice_current(slice_current, current_arr, delay_arr, freq_arr):
    """
    Находит значения в delay_arr и freq_arr, соответствующие заданному току.
    
    Аргументы:
    - slice_current: float/int, искомое значение тока.
    - current_arr: list, массив значений тока.
    - delay_arr: list, массив задержек.
    - freq_arr: list, массив частот.
    
    Возвращает:
    - (delay_slice, freq_slice): кортеж списков найденных значений.
    
    Ошибки:
    - ValueError: если длины массивов не совпадают.
    - IndexError: если искомый ток не найден в массиве.
    """
    
    
    #  Проверка длин массивов (они должны быть одинаковыми)
    if not (len(current_arr) == len(delay_arr) == len(freq_arr)):
        raise ValueError(
            f"Длины массивов не совпадают! "
            f"current: {len(current_arr)}, delay: {len(delay_arr)}, freq: {len(freq_arr)}"
        )
    
    if len(current_arr) == 0:
        raise ValueError("Массивы не могут быть пустыми.")

    # Поиск индексов, где ток совпадает
    # Используем небольшую погрешность (epsilon) для сравнения float чисел, 
    # так как прямое сравнение 0.1 + 0.2 == 0.3 часто ложно.
    epsilon = 1e-9
    indices = [
        i for i, val in enumerate(current_arr) 
        if abs(val - slice_current) < epsilon
    ]
    
    # 4. Обработка случая, когда ток не найден
    if not indices:
        raise IndexError(
            f"Значение тока {slice_current} не найдено в массиве. "
            f"Доступный диапазон: [{min(current_arr)}, {max(current_arr)}]"
        )
    
    # 5. Формирование результата
    delay_slice = [delay_arr[i] for i in indices]
    freq_slice = [freq_arr[i] for i in indices]
    
    return delay_slice, freq_slice

if __name__=="__main__":
    c_arr = [1.0, 2.0, 3.0, 4.0]
    d_arr = [10, 20, 30, 40]
    f_arr = [100, 200, 300, 400]

    try:
        d_res, f_res = slice_current(2.0, c_arr, d_arr, f_arr)
        print(f"Успех (одно): Delay={d_res}, Freq={f_res}")
    except Exception as e:
        print(f"Ошибка: {e}")
    # Вывод: Успех (одно): Delay=[20], Freq=[200]