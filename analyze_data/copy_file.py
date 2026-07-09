import os
import shutil


def copy_file(file_name, old_folder_path, new_folder_path):
    """
    Копирует один файл из одной папки в другую.

    Parameters
    ----------
    file_name : str
        Имя файла.
    old_folder_path : str
        Исходная папка.
    new_folder_path : str
        Папка назначения.

    Returns
    -------
    str | None
        Путь к скопированному файлу или None при ошибке.
    """

    os.makedirs(new_folder_path, exist_ok=True)

    source_path = os.path.join(old_folder_path, file_name)
    dest_path = os.path.join(new_folder_path, file_name)

    if not os.path.isfile(source_path):
        print(f"Файл не найден: {source_path}")
        return None

    try:
        shutil.copy2(source_path, dest_path)
        print(f"Файл успешно скопирован в {dest_path}")
        return dest_path
    except Exception as e:
        print(f"Ошибка при копировании '{file_name}': {e}")
        return None

# ═══════════════════════════════════════════════════════════════
# ПРИМЕРЫ ИСПОЛЬЗОВАНИЯ
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    file_name = "optical_spectrum_tunable_filter_July-01-2026_time_17-37-19.png"
    old_folder=r'C:\Users\namys\Documents\laser_with_BTF'
    new_folder=r'C:\Users\namys\Documents'
    copy_file(
    file_name=file_name,
    old_folder_path=old_folder,
    new_folder_path=new_folder
)