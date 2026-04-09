from pathlib import Path

def get_OSC_data_from_txt(txt_file_path):
    """
    Извлекает метаданные из TXT файла осциллографа.
    
    Args:
        txt_file_path: путь к файлу
    
    Returns:
        dict: словарь с ключами Value_GHz, Mean_GHz, Min_GHz, Max_GHz, St_Dev_GHz, Count
    """
    result = {}
    
    # Ключи, которые нужно извлечь
    target_keys = ['Value_GHz', 'Mean_GHz', 'Min_GHz', 'Max_GHz', 'St_Dev_GHz', 'Count']
    
    try:
        with open(txt_file_path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Разделяем по табуляции
            parts = line.split('\t')
            if len(parts) >= 2:
                key = parts[0].strip()
                if key in target_keys:
                    # Пробуем преобразовать в число
                    try:
                        # Count может быть целым, остальные - float
                        if key == 'Count':
                            result[key] = int(float(parts[1].strip()))
                        else:
                            result[key] = float(parts[1].strip())
                    except ValueError:
                        result[key] = parts[1].strip()
        
        # Проверяем, что все ключи найдены
        missing_keys = set(target_keys) - set(result.keys())
        if missing_keys:
            print(f"⚠️ Предупреждение: не найдены ключи {missing_keys} в файле {txt_file_path}")
        
    except Exception as e:
        print(f"❌ Ошибка чтения файла {txt_file_path}: {e}")
    
    return result


# Пример использования:
if __name__ == "__main__":
    folder_path=r'C:\Users\namys_23hvwev\Documents\DATA\data_from_lnf\laser_with_btf_March-31-2026_time_17-03-39\oscilloscope_measurements\wavelength_1550nm\voltage_2V\current_200mA\average\hor_scale_500.0ps'
    file_name=r'oscillogram_average_hor_scale_500.0ps_delay_0ps_current_200mA_voltage_2V_wavelength_1550nm.txt'
    full_path=Path(folder_path) / file_name
    data = get_OSC_data_from_txt(txt_file_path=full_path)
    
    print(data)