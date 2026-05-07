def number_with_decimal_prefix(number: float) -> str:
    """
    Преобразует число в строку c приставкой Мега
    """
    MEGA = 1e+6
    result = f"{number / MEGA}M"
    
    # Сначала убираем нули, потом точку (даже если она осталась)
    result = result.rstrip('0').rstrip('.')
    # Если последний символ всё ещё точка, удаляем её
    if result and result[-1] == '.':
        result = result[:-1]
    return result

if __name__ == "__main__":
    print(number_with_decimal_prefix(6.2e+9))    # 6200M
    print(number_with_decimal_prefix(100e+6))    # 100M
    print(number_with_decimal_prefix(1e+6))      # 1M
    print(number_with_decimal_prefix(2.5e+6))    # 2.5M