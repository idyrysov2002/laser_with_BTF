import os
import json
import re

# Путь к корневой папке с данными (измените при необходимости)
# Скрипт должен лежать внутри или рядом с папкой rf_measurements
root_dir = r"C:\Users\namys_23hvwev\Documents\DATA\data_from_lnf\laser_with_btf_March-27-2026_time_14-22-55\rf_measurements"

data_structure = {}

print("Сканирование файлов...")

for w_path in os.listdir(root_dir):
    if not w_path.startswith("wavelength_"): continue
    wavelength = w_path.split("_")[1].replace("nm", "")
    
    dir_w = os.path.join(root_dir, w_path)
    for v_path in os.listdir(dir_w):
        if not v_path.startswith("voltage_"): continue
        voltage = v_path.split("_")[1].replace("V", "")
        
        dir_v = os.path.join(dir_w, v_path)
        for c_path in os.listdir(dir_v):
            if not c_path.startswith("current_"): continue
            current = c_path.split("_")[1].replace("mA", "")
            
            dir_c = os.path.join(dir_v, c_path)
            for s_path in os.listdir(dir_c):
                if not s_path.startswith("span_"): continue
                span = s_path.split("_")[1].replace("GHz", "")
                
                dir_s = os.path.join(dir_c, s_path)
                for m_path in os.listdir(dir_s):
                    if not m_path.startswith("measurement_number_"): continue
                    meas_num = m_path.split("_")[2]
                    
                    dir_m = os.path.join(dir_s, m_path)
                    # Ищем файл спектра
                    files = [f for f in os.listdir(dir_m) if f.startswith("rf_spectrum_delay_") and f.endswith(".txt")]
                    
                    if not files: continue
                    
                    file_name = files[0]
                    
                    # Парсим имя файла, чтобы достать параметры, если они там дублируются, 
                    # но нам важнее путь.
                    # Пример имени: rf_spectrum_delay_0ps_current_300mA_voltage_0V_wavelength_1530nm_span_6.2GHz_measurement_number_1.txt
                    
                    if wavelength not in data_structure: data_structure[wavelength] = {}
                    if voltage not in data_structure[wavelength]: data_structure[wavelength][voltage] = {}
                    if meas_num not in data_structure[wavelength][voltage]: data_structure[wavelength][voltage][meas_num] = {}
                    if span not in data_structure[wavelength][voltage][meas_num]: data_structure[wavelength][voltage][meas_num][span] = {}
                    
                    # Сохраняем относительный путь к файлу и список доступных задержек (извлечем из имен файлов)
                    # Нам нужно собрать список всех доступных Delay для построения оси X позже, 
                    # но пока просто сохраним шаблон пути.
                    
                    # Извлекаем Delay из имени файла для метаданных
                    delay_match = re.search(r"delay_(\d+)ps", file_name)
                    delay = int(delay_match.group(1)) if delay_match else 0
                    
                    # Сохраняем путь относительно root_dir, чтобы HTML мог его найти
                    rel_path = os.path.relpath(os.path.join(dir_m, file_name), root_dir)
                    
                    if "files" not in data_structure[wavelength][voltage][meas_num][span]:
                        data_structure[wavelength][voltage][meas_num][span]["files"] = []
                    
                    data_structure[wavelength][voltage][meas_num][span]["files"].append({
                        "delay": delay,
                        "path": rel_path.replace("\\", "/") # Для URL
                    })

# Сортируем файлы по задержке внутри каждой группы
for w in data_structure:
    for v in data_structure[w]:
        for m in data_structure[w][v]:
            for s in data_structure[w][v][m]:
                data_structure[w][v][m][s]["files"].sort(key=lambda x: x["delay"])

output_file = "data_index.json"
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(data_structure, f, indent=2)

print(f"Готово! Файл {output_file} создан в текущей папке.")
print("Теперь откройте index.html в той же папке.")