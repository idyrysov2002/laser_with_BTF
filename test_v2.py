import numpy as np

# Пример данных (замените на ваши массивы)
delay_data = np.array([10, 20, 30, 40, 50])
freq_data = np.array([5,  15, 8,  25, 3])

x = 10  # Пороговое значение

# Создаем маску: оставляем только те элементы, где freq_data >= x
# (логическое условие "не меньше х")
mask = freq_data >= x

# Применяем маску к обоим массивам
filtered_freq = freq_data[mask]
filtered_delay = delay_data[mask]

print(f"Исходные freq: {freq_data}")
print(f"Исходные delay: {delay_data}")
print(f"Порог x: {x}")
print("-" * 30)
print(f"Отфильтрованные freq: {filtered_freq}")
print(f"Отфильтрованные delay: {filtered_delay}")