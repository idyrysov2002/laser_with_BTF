import os


def write_xy_to_txt(
    X,
    Y,
    x_label: str = "X",
    y_label: str = "Y",
    folder_path: str = "./output",
    txt_file_name: str = "data.txt") -> str:
    """
    Записывает два массива данных в текстовый файл в формате TSV.
    
    Параметры:
        X : Массив значений для оси X
        Y : Массив значений для оси Y
        x_label (str): Заголовок столбца X (по умолчанию "X")
        y_label (str): Заголовок столбца Y (по умолчанию "Y")
        folder_path (str): Путь к папке для сохранения файла (по умолчанию "./output")
        txt_file_name (str): Имя файла (по умолчанию "data.txt")
    
    Возвращает:
        str: Полный путь к созданному файлу
    
    Исключения:
        ValueError: Если длины массивов X и Y не совпадают
    """
    
    
    # Проверка длины массивов
    if len(X) != len(Y):
        raise ValueError(f"Длины массивов не совпадают: len(X)={len(X)}, len(Y)={len(Y)}")
    
    # Добавляем расширение .txt если его нет
    if not txt_file_name.lower().endswith('.txt'):
        txt_file_name += '.txt'
    
    # Создаем полный путь к файлу
    full_path = os.path.abspath(os.path.join(folder_path, txt_file_name))
    
    # Создаем папку если она не существует
    os.makedirs(folder_path, exist_ok=True)
    
    # Записываем данные в файл
    with open(full_path, 'w', encoding='utf-8') as file:
        # Заголовок
        file.write(f"{x_label}\t{y_label}\n")
        
        # Данные построчно
        for x, y in zip(X, Y):
            file.write(f"{x}\t{y}\n")
    
    return full_path


if __name__ == "__main__":
   
    # Пример использования
    print("\n" + "=" * 60)
    print("ПРИМЕР ИСПОЛЬЗОВАНИЯ")
    print("=" * 60)
    
    X_data = [0, 1, 2]
    Y_data = [0, 1, 4 ]
    
    result_path = write_xy_to_txt(
        X=X_data,
        Y=Y_data,
        x_label="X (сек)",
        y_label="Y (м)",
        folder_path="./output",
        txt_file_name="example_data.txt"
    )
    
    print(f"\nФайл сохранён: {result_path}")
