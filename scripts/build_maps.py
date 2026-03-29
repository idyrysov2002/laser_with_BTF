from create_map_and_save import create_map_and_save

def build_maps(x_arr, y_arr, data_buf, save_folder_path):
    """
    Строит карты для каждого набора данных в словаре data_buf.
    
    Ожидаемая структура data_buf:
    {
        'key_name': {
            'data': [список_чисел] или '' или None,
            'label': 'Подпись оси Z',
            'title': 'Заголовок графика',
            'filename': 'имя_файла'
        }
    }
    """
    
    # ========================
    # ОБРАБОТКА КАЖДОГО ЭЛЕМЕНТА СЛОВАРЯ
    # ========================
    for key, value in data_buf.items():
        # 1. Пропускаем, если само значение ключа None или не словарь
        if value is None or not isinstance(value, dict):
            continue
        
        # 2. Извлекаем поля с безопасными значениями по умолчанию
        z_data = value.get('data')
        z_label = value.get('label', 'Z-axis')
        z_title = value.get('title', '')
        filename = value.get('filename', f'map_{key}')
        
        # ==========================================
        # ПРОВЕРКА НАЛИЧИЯ ДАННЫХ
        # ==========================================
        # Пропускаем, если data это пустая строка, None или пустой список
        if z_data is None or z_data == '':
            print(f"⚠️ Пропущено '{key}': поле 'data' пустое (None или '').")
            continue
            
        if isinstance(z_data, list) and len(z_data) == 0:
            print(f"⚠️ Пропущено '{key}': список данных пуст.")
            continue
            
        # Пропускаем, если список состоит только из None
        if isinstance(z_data, list) and all(v is None for v in z_data):
            print(f"⚠️ Пропущено '{key}': массив содержит только None.")
            continue
        # ==========================================

        try:
            # Формируем пакет данных в формате, который ждет create_map_and_save:
            # [массив_чисел, лейбл]
            z_arr_formatted = [z_data, z_label]
            
            # Если имя файла пустое, генерируем его из ключа
            if not filename:
                filename = f"map_{key}"
            
            # Создаём и сохраняем карту
            create_map_and_save(
                x_arr=x_arr,          
                y_arr=y_arr,          
                z_arr=z_arr_formatted,
                title=z_title, 
                folder_path=save_folder_path, 
                filename=filename, 
                show_plot=False
            )
            print(f"✅ Успешно построено: {key} -> {filename}.png")
            
        except Exception as e:
            print(f"❌ Ошибка при построении карты для '{key}': {e}")

# Пример использования с вашим форматом:
if __name__ == '__main__':
    # Заглушки для примера
    PARAM_LABELS = {'pm_400_mW': 'Мощность, мВт', 'frequensy_GHz': 'Частота, ГГц'}
    
    # Тестовые координаты (сетка 3x3)
    x_vals = [1, 2, 3, 1, 2, 3, 1, 2, 3]
    y_vals = [10, 10, 10, 20, 20, 20, 30, 30, 30]
    
    # Реальные данные для одного ключа
    real_data = [10.5, 12.1, 11.8, 15.0, 16.2, 14.9, 20.1, 21.5, 19.8]

    map_data_buf = {
        'pm_400': {
            'data': real_data,  # Заполнено числами
            'label': PARAM_LABELS['pm_400_mW'],
            'title': 'Распределение мощности',
            'filename': 'power_meter_400'
        },
        'rf_freq_max': {
            'data': '',  # Пустая строка - будет пропущено
            'label': PARAM_LABELS['frequensy_GHz'],
            'title': '',
            'filename': ''
        },
        'rf_empty_list': {
            'data': [],  # Пустой список - будет пропущено
            'label': 'Test',
            'title': '',
            'filename': ''
        },
        'rf_all_none': {
            'data': [None, None, None], # Только None - будет пропущено
            'label': 'Test',
            'title': '',
            'filename': ''
        }
    }

    build_maps(
        x_arr=[x_vals, 'Координата X'],
        y_arr=[y_vals, 'Координата Y'],
        data_buf=map_data_buf,
        save_folder_path='./maps/'
    )