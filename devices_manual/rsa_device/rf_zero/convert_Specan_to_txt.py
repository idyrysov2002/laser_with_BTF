import xml.etree.ElementTree as ET

# Имена файлов
INPUT_FILE = '1.Specan'   # Имя вашего файла с XML данными
OUTPUT_FILE = 'result.txt' # Имя файла, куда сохранится результат

def parse_rsa_xml(input_path, output_path):
    try:
        # Парсинг XML дерева
        tree = ET.parse(input_path)
        root = tree.getroot()

        # Поиск элемента Waveform (где лежат данные)
        # Используем поиск по тегу, так как структура может быть вложенной
        waveform = root.find('.//Waveform')

        if waveform is None:
            print("Ошибка: Не найден тег Waveform в XML файле.")
            return

        # Извлечение параметров оси X
        x_start = float(waveform.find('XStart').text)
        x_stop = float(waveform.find('XStop').text)
        
        # Извлечение всех значений амплитуды (Y)
        y_values = [float(y.text) for y in waveform.findall('y')]
        count = len(y_values)

        if count < 2:
            print("Ошибка: Недостаточно данных для построения графика (меньше 2 точек).")
            return

        # Расчет шага частоты
        # Формула линейной развертки: Step = (Stop - Start) / (Count - 1)
        step = (x_stop - x_start) / (count - 1)

        # Запись в файл
        with open(output_path, 'w', encoding='utf-8') as f:
            # Заголовок (можно убрать, если нужен чистый файл)
            f.write("Frequency_Hz\tAmplitude_dBm\n")
            
            for i, y in enumerate(y_values):
                # Вычисляем частоту для текущей точки
                freq = x_start + (i * step)
                # Записываем в файл: Частота [TAB] Амплитуда
                f.write(f"{freq:.6f}\t{y:.6f}\n")

        print(f"Успешно! Обработано точек: {count}")
        print(f"Результат сохранен в файл: {output_path}")

    except FileNotFoundError:
        print(f"Ошибка: Файл '{input_path}' не найден. Проверьте имя и путь.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

if __name__ == "__main__":
    parse_rsa_xml(INPUT_FILE, OUTPUT_FILE)