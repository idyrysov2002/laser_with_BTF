import os
import pandas as pd

def write_arrays_txt(*args, folder_path='.', filename='output.txt', header_lines=None):
    """
    Записывает массивы в текстовый файл (.txt) с разделением табуляцией.
    """
    arrays = []
    labels = []
    
    # 1. Валидация входных данных (массивы)
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
    
    # 3. Валидация header_lines
    if header_lines is not None:
        if not isinstance(header_lines, (list, tuple)):
            raise ValueError("Параметр header_lines должен быть списком или кортежем строк.")
        for i, line in enumerate(header_lines):
            if not isinstance(line, str):
                header_lines = list(header_lines)
                header_lines[i] = str(line)

    # 4. Создание папки
    os.makedirs(folder_path, exist_ok=True)
    
    if not filename.lower().endswith('.txt'):
        filename = f"{filename}.txt"
    
    filepath = os.path.join(folder_path, filename)
    
    # 5. Формирование DataFrame
    data_dict = {label: arr for label, arr in zip(labels, arrays)}
    df = pd.DataFrame(data_dict)
    
    # 6. Запись в файл
    with open(filepath, 'w', encoding='utf-8', newline='') as f:
        # Запись пользовательских заголовков
        if header_lines:
            for line in header_lines:
                f.write(f"{line}\n")
        
        # Запись таблицы с явным указанием разделителя строк
        # lineterminator='\n' гарантирует одну новую строку вместо возможной двойной
        df.to_csv(f, sep='\t', index=False)
    
    print(f"Данные успешно сохранены в:{filepath}")

# Пример использования:
if __name__ == "__main__":
    # Данные
    x = [1, 2, 3]
    y = [10, 20, 30]
    
    # Дополнительные строки в начале файла
    custom_headers = [
        "Отчет по измерениям",
        "Дата: 25.10.2023",
        "Оператор: Иванов И.И."
    ]
    
    write_arrays_txt(
        [x, 'Время'], 
        [y, 'Сигнал'], 
        header_lines=custom_headers, 
        folder_path='./output', 
        filename='result.txt'
    )