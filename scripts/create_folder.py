import os
import datetime

def create_date_folder(base_path, prefix=None):
    """
    Создаёт новую папку с временной меткой в указанной директории.

    Args:
        base_path (str, optional): Путь к основной директории, где будет создана папка.
        prefix (str, optional): Префикс для имени папки. Если не указан, имя состоит
                                только из временной метки. По умолчанию None.
    Returns:
        str: Полный путь к созданной папке.
    """
    timestamp = datetime.datetime.now().strftime("%B-%d-%Y_time_%H-%M-%S")
    if prefix:
        folder_name = f"{prefix}_{timestamp}"
    else:
        folder_name = timestamp
    full_path = os.path.join(base_path, folder_name)
    os.makedirs(full_path, exist_ok=True)
    return full_path

def create_subfolder(parent_folder_path, subfolder_name):
    """
    Создаёт подпапку внутри указанной родительской директории

    """
    subfolder = os.path.join(parent_folder_path, subfolder_name)
    os.makedirs(subfolder, exist_ok=True)
    return subfolder



def create_multiple_subfolders(parent_folder, folder_structure):
    """
    Создает цепочку вложенных папок внутри parent_folder.
    
    Аргументы:
        parent_folder (str): Путь к основной директории.
        folder_structure (str): Строка с путями через слэш, например "voltage/current/delay".
        
    Возвращает:
        str: Полный путь к самой глубокой созданной папке.
    """
    # Разбиваем строку на части и фильтруем пустые значения (на случай лишних слэшей)
    subfolders = [x.strip() for x in folder_structure.split('/') if x.strip()]
    
    if not subfolders:
        return parent_folder

    # Собираем полный путь
    # os.path.join корректно обработает список папок для любой ОС (Windows/Linux/Mac)
    full_path = os.path.join(parent_folder, *subfolders)
    
    # Создаем все промежуточные папки сразу
    os.makedirs(full_path, exist_ok=True)
    
    return full_path