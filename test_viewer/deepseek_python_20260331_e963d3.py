import os
import re
import shutil
from pathlib import Path

# Исходная папка
source_root = Path(r"C:\Users\namys_23hvwev\Documents\DATA\data_from_lnf\laser_with_btf_March-27-2026_time_14-22-55\rf_measurements")

# Целевая папка
target_root = Path(r"C:\Users\namys_23hvwev\Documents\DATA\map_data")

# Параметры
linewidth = "1nm"
span_new = "6GHz"  # заменяем 6.2GHz на 6GHz

def parse_filename(filename):
    """Парсит имя файла и возвращает параметры"""
    pattern = r'rf_spectrum_delay_(\d+)ps_current_(\d+)mA_voltage_(\d+)V_wavelength_(\d+)nm_span_([\d\.]+)GHz_measurement_number_(\d+)'
    match = re.match(pattern, filename)
    
    if match:
        return {
            'delay': match.group(1),
            'current': match.group(2),
            'voltage': match.group(3),
            'wavelength': match.group(4),
            'span': match.group(5),
            'measurement_number': match.group(6)
        }
    return None

def process_files():
    # Создаем целевую папку
    target_root.mkdir(parents=True, exist_ok=True)
    
    # Находим все txt файлы
    files = list(source_root.rglob("*.txt"))
    
    print(f"Найдено файлов: {len(files)}")
    
    moved_count = 0
    error_count = 0
    
    for file_path in files:
        print(f"\nОбработка: {file_path}")
        
        # Получаем имя файла без расширения
        filename = file_path.stem
        
        # Парсим имя
        params = parse_filename(filename)
        
        if not params:
            print(f"  !! Не удалось распарсить: {filename}")
            error_count += 1
            continue
        
        # Заменяем span 6.2 на 6
        if params['span'] == "6.2":
            params['span'] = "6"
        
        # Новое имя файла
        new_filename = f"rf_spectrum_delay_{params['delay']}ps_current_{params['current']}mA_voltage_{params['voltage']}V_wavelength_{params['wavelength']}nm_linewidth_{linewidth}_span_{params['span']}GHz_measurement_number_{params['measurement_number']}.txt"
        
        # Новый путь
        new_path = target_root / f"wavelength_{params['wavelength']}nm" / f"linewidth_{linewidth}" / f"voltage_{params['voltage']}V" / f"current_{params['current']}mA" / f"span_{params['span']}GHz" / f"measurement_number_{params['measurement_number']}"
        
        # Создаем папки
        new_path.mkdir(parents=True, exist_ok=True)
        
        # Полный путь к новому файлу
        new_file = new_path / new_filename
        
        # ПЕРЕМЕЩАЕМ файл
        shutil.move(str(file_path), str(new_file))
        
        print(f"  -> Перемещено в: {new_file}")
        moved_count += 1
    
    # После перемещения удаляем пустые папки в исходной директории
    print("\nУдаление пустых папок...")
    for root, dirs, files in os.walk(source_root, topdown=False):
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            try:
                if not os.listdir(dir_path):
                    os.rmdir(dir_path)
                    print(f"  Удалена пустая папка: {dir_path}")
            except OSError:
                pass
    
    print("\n" + "="*50)
    print(f"Готово!")
    print(f"Перемещено: {moved_count}")
    print(f"Ошибок: {error_count}")
    print(f"Целевая папка: {target_root}")

if __name__ == "__main__":
    process_files()