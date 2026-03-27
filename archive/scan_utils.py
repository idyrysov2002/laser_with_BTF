# scan_utils.py
import itertools
import config
import os
# Маппинг: параметр -> прибор
PARAM_TO_INSTR = {
    'voltage':    'ut',
    'current':    'ld',
    'delay':      'odl',
    'linewidth':  'btf',
    'wavelength': 'btf', 
}

PARAM_UNITS = {
    'voltage':    'V',
    'current':    'mA',
    'delay':      'ps',
    'linewidth':  'nm',
    'wavelength': 'nm',
}
# Все параметры и их значения
ALL_PARAMS = {
    'voltage':    config.VOLTAGES,
    'current':    config.CURRENTS,
    'delay':      config.DELAYS,
    'linewidth':  config.LINEWIDTH,
    'wavelength': config.WAVELENGTH,
}

def get_active_param_names(verbose=False):
    """
    Возвращает список имен параметров, которые соответствуют включенным приборам.
    Порядок определяется config.SCAN_ORDER.
    """
    active_names = []
    
    if verbose:
        print("\n=== АКТИВНЫЕ ПАРАМЕТРЫ ===")
    
    for param_name in config.SCAN_ORDER:
        if param_name not in ALL_PARAMS:
            continue
        
        instr_key = PARAM_TO_INSTR.get(param_name)
        is_enabled = config.INSTRUMENTS.get(instr_key, {}).get('enabled', False)
        
        if is_enabled:
            active_names.append(param_name)
            if verbose:
                print(f"[ВКЛ] {param_name:12} (прибор: {instr_key})")
        else:
            if verbose:
                print(f"[ОТКЛ] {param_name:12} (прибор: {instr_key})")
    
    if verbose:
        print("===========================\n")
    
    return active_names

def get_scan_generator():
    """
    Декартово произведение ТОЛЬКО из включенных приборов.
    Порядок определяется config.SCAN_ORDER.
    """
    active_names = get_active_param_names(verbose=True)
    active_lists = [ALL_PARAMS[name] for name in active_names]
    
    if not active_lists:
        return iter([])
    
    # Декартово произведение ТОЛЬКО активных параметров
    product_iterator = itertools.product(*active_lists)
    
    for values in product_iterator:
        yield dict(zip(active_names, values))

def generate_file_paths(step, active_names):
    """
    Формирует структуру папок и имя файла на основе текущего шага и активных параметров.
    
    Правила:
    1. Folder: Порядок scan_order, активные, БЕЗ последнего элемента.
    2. Filename: Обратный порядок, ВСЕ активные элементы.
    3. Единицы измерения обязательны.
    """
    if not active_names:
        return "", "scan_data.txt"

    # 1. Структура папок (все кроме последнего)
    folder_parts = []
    # Берем все активные параметры, кроме последнего (inner loop)
    for param_name in active_names[:-1]:
        value = step.get(param_name)
        unit = PARAM_UNITS.get(param_name, '')
        folder_parts.append(f"{param_name}_{value}{unit}")
    
    base_folder_structure = os.path.join(*folder_parts) if folder_parts else ""

    # 2. Имя файла (обратный порядок, все параметры)
    filename_parts = []
    # Проходим в обратном порядке
    for param_name in reversed(active_names):
        value = step.get(param_name)
        unit = PARAM_UNITS.get(param_name, '')
        filename_parts.append(f"{param_name}_{value}{unit}")
    
    base_filename = "_".join(filename_parts)
    
    return base_folder_structure, base_filename

if __name__=="__main__":
    