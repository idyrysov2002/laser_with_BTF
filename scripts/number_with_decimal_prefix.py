def number_with_decimal_prefix(number: float) -> str:
    """
    Преобразует число в строку с метрическими приставками.
    Поддерживает диапазоны от пико (p) до пета (P).
    
    Большие: k, M, G, T, P
    Маленькие: m, μ, n, p
    """
    # Приставки: от пико до пета
    # Индекс 6 соответствует базовой единице (без приставки)
    prefixes = ['p', 'n', 'μ', 'm', '', 'k', 'M', 'G', 'T', 'P']
    base_index = 4  # Индекс пустой строки (базовый уровень)
    
    magnitude = base_index
    abs_number = abs(number)

    # Если число >= 1000, идем вверх по шкале
    while abs_number >= 1000 and magnitude < len(prefixes) - 1:
        abs_number /= 1000.0
        magnitude += 1
    
    # Если число < 1, идем вниз по шкале
    while abs_number < 1 and abs_number > 0 and magnitude > 0:
        abs_number *= 1000.0
        magnitude -= 1

    # Форматируем число: убираем лишние нули
    if abs_number == int(abs_number):
        formatted = f"{int(abs_number)}{prefixes[magnitude]}"
    else:
        # Округляем до 1 знака и убираем trailing zeros
        formatted = f"{abs_number:.1f}{prefixes[magnitude]}".rstrip('0').rstrip('.')

    # Возвращаем знак минус, если число было отрицательным
    return '-' + formatted if number < 0 else formatted

if __name__ == "__main__":
    # Примеры использования
    print(number_with_decimal_prefix(62000))        # 62k
    print(number_with_decimal_prefix(6200000))      # 6.2M
    print(number_with_decimal_prefix(0.5))          # 500m
    print(number_with_decimal_prefix(0.000062))     # 62μ
    print(number_with_decimal_prefix(0.000000062))  # 62n
    print(number_with_decimal_prefix(0.000000000062)) # 62p
    print(number_with_decimal_prefix(500))          # 500
    print(number_with_decimal_prefix((-2000000)))  # -2M
