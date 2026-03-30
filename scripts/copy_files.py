import os
import shutil

def copy_files(*filenames,old_folder_path, new_folder_path):
    """
    Копирует несколько файлов из одной папки в другую.
    
    Параметры:
    old_folder_path : str
        Путь к исходной папке.
    new_folder_path : str
        Путь к целевой папке (будет создана, если не существует).
    *filenames : str
        Переменное количество имен файлов для копирования.
        
    Возвращает:
    list
        Список полных путей к скопированным файлам.
    """
    
    if not filenames:
        print("Ошибка: Не передано ни одного имени файла.")
        return []

    # Создаем целевую папку, если её нет
    os.makedirs(new_folder_path, exist_ok=True)
    
    copied_paths = []
    failed_files = []

    for filename in filenames:
        source_path = os.path.join(old_folder_path, filename)
        dest_path = os.path.join(new_folder_path, filename)
        
        # Проверка существования
        if not os.path.exists(source_path):
            print(f"Файл не найден (пропущен): {source_path}")
            failed_files.append(filename)
            continue
        
        if not os.path.isfile(source_path):
            print(f"Объект не является файлом (пропущен): {source_path}")
            failed_files.append(filename)
            continue
        
        try:
            # Копирование с сохранением метаданных
            shutil.copy2(source_path, dest_path)
            copied_paths.append(dest_path)
        except Exception as e:
            print(f"Ошибка при копировании {filename}: {e}")
            failed_files.append(filename)

    # Формирование итогового сообщения
    count = len(copied_paths)
    
    if count == 0:
        print("Ни один файл не был скопирован.")
    elif count == 1:
        # Если скопирован ровно один файл -> выводим путь
        print(f'Файл успешно скопирован в {copied_paths[0]}')
    else:
        # Если 2 и больше -> общее сообщение
        print(f'{count} файлов успешно скопированы в папку: {new_folder_path}')

    if failed_files:
        print(f"Не удалось скопировать файлов: {len(failed_files)}")

    return copied_paths

# ═══════════════════════════════════════════════════════════════
# ПРИМЕРЫ ИСПОЛЬЗОВАНИЯ
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import os
    
    # Получаем домашнюю директорию для надежности
    home = os.path.expanduser("~")
    
    src = os.path.join(home, "Downloads")
    dst = os.path.join(home, "Documents", "Backup_Test")
    
    # Пример 1: Копирование одного файла
    print("--- Тест 1 (1 файл) ---")
    copy_files(src, dst, "topaz.pdf")
    
    # Пример 2: Копирование нескольких файлов
    print("\n--- Тест 2 (несколько файлов) ---")
    # Замените имена на реальные файлы из вашей папки Downloads для проверки
    copy_files(src, dst, "topaz.pdf", "image.png", "data.txt") 