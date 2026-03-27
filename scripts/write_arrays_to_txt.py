import pandas as pd
import os

def write_arrays_txt(*args, folder_path='.', filename='output.txt'):
    """
    Записывает массивы в текстовый файл (.txt) с разделением табуляцией.
    
    Синтаксис:
        x_arr = [x_data, 'длина']
        y_arr = [y_data, 'размер']
        write_arrays_txt(x_arr, y_arr, folder_path='./output', filename='data.txt')
    
    Параметры:
        *args        — списки/кортежи [массив, заголовок]
        folder_path  — путь к папке
        filename     — имя файла (желательно с расширением .txt)
    """
    arrays = []
    labels = []
    
    # 1. Валидация входных данных
    for i, arg in enumerate(args):
        if not isinstance(arg, (list, tuple)) or len(arg) != 2:
            raise ValueError(f"Аргумент {i+1} должен быть списком/кортежем [массив, заголовок]")
        arr, label = arg
        arrays.append(arr)
        labels.append(label)
    
    if len(arrays) == 0:
        raise ValueError("Требуется передать хотя бы один массив.")
    
    # 2. Проверка одинаковой длины массивов
    length = len(arrays[0])
    for i, arr in enumerate(arrays):
        if len(arr) != length:
            raise ValueError(f"Все массивы должны быть одинаковой длины. Массив {i+1} ('{labels[i]}') имеет длину {len(arr)}, ожидалось {length}.")
    
    # 3. Создание папки, если нет
    os.makedirs(folder_path, exist_ok=True)
    
    # Проверка и добавление расширения .txt
    if not filename.lower().endswith('.txt'):
        filename = f"{filename}.txt"
    
    filepath = os.path.join(folder_path, filename)
    
    # 4. Формирование DataFrame и запись в TXT
    data_dict = {label: arr for label, arr in zip(labels, arrays)}
    df = pd.DataFrame(data_dict)
    
    # sep='\t' устанавливает разделитель табуляцию
    # encoding='utf-8' обеспечивает корректное отображение кириллицы
    df.to_csv(filepath, sep='\t', index=False, encoding='utf-8')
    
    print(f"Данные успешно сохранены в {filepath}\n")


if __name__ == "__main__":
    # Пример данных
    x_data = [1, 2, 3, 4, 5]
    y_data = [10, 20, 25, 40, 55]
    z_data = [0.1, 0.2, 0.3, 0.4, 0.5]

    # Формируем аргументы: [данные, имя столбца]
    col_x = [x_data, 'Время, с']
    col_y = [y_data, 'Напряжение, В']
    col_z = [z_data, 'Ток, А']

    # Вызов функции
    write_arrays_txt(
        col_x, col_y, col_z, 
        folder_path='./results', 
        filename='experiment_01.txt'
    )