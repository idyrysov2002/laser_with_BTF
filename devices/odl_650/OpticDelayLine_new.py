import serial
import time
import re

class OpticDelayLine:
    def __init__(self, port="COM6", baudrate=9600, timeout=3):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.ser = None
        self.is_connected = False

    def initialize(self):
        """ Подключение к прибору"""
        try:
            if self.ser and self.ser.is_open:
                print("Порт уже открыт")
                return True

            self.ser = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                bytesize=serial.EIGHTBITS,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                timeout=self.timeout,
                xonxoff=False,
                rtscts=False,
                dsrdtr=False
            )
            self.is_connected = True
            print(f"Порт {self.port} открыт")
            return True
        except Exception as e:
            print(f"Ошибка подключения: {e}")
            self.is_connected = False
            return False

    def disconnect(self):
        """Закрыть соединение"""
        try:
            if self.ser and self.ser.is_open:
                self.ser.close()
                self.is_connected = False
                print("Порт закрыт")
            else:
                print("Порт уже закрыт")
        except Exception as e:
            print(f"Ошибка закрытия порта: {e}")

    def _send_and_read(self, command):
        """Внутренний метод для отправки команды и чтения ответа"""
        if not self.ser or not self.ser.is_open:
            raise Exception("Порт не открыт. Вызовите initialize()")

        try:
            # Отправка команды с окончанием строки \r\n
            full_command = f"{command}\r\n"
            self.ser.write(full_command.encode('ascii'))
            print(f"Отправлено: {command}")

            # Чтение ответа
            response = ""
            start = time.time()

            while time.time() - start < self.timeout:
                if self.ser.in_waiting > 0:
                    line = self.ser.readline().decode('ascii', errors='ignore').strip()
                    if line:
                        print(f"Получено: {line}")
                        response += line + "\n"

            return response.strip()
        except Exception as e:
            print(f"Ошибка обмена данными: {e}")
            return ""

    def get_time_delay(self):
        """Прочитать время задержки"""
        command = "T?"
        response = self._send_and_read(command)

        if not response:
            print("Прибор не ответил на запрос задержки")
            return None

        # Попытка извлечь число из ответа (например, если придет "100.000 ps" или просто "100.000")
        numbers = re.findall(r"[-+]?\d*\.\d+|\d+", response)
        if numbers:
            try:
                delay = float(numbers[0])
                print(f"Текущая задержка: {delay}")
                return delay
            except ValueError:
                print("Не удалось преобразовать ответ в число")
                return None
        else:
            print("В ответе не найдено числового значения")
            return None

    def set_time_delay(self, time_delay, max_attempts=5, pause_between_attempts=5.0):
        """
        Задать время задержки.
        Если ответ не 'Done', команда отправляется повторно до max_attempts раз.
        """
        command = f"T{time_delay}"
        attempt = 0

        print(f"Установка задержки: {time_delay}")

        while attempt < max_attempts:
            attempt += 1
            response = self._send_and_read(command)

            # Проверка на успешное завершение (регистронезависимая)
            if "done" in response.lower():
                print(f"Задержка установлена успешно (попытка {attempt})")
                return True

            print(f"Ответ не 'Done'. Попытка {attempt} из {max_attempts}")

            # Если это не последняя попытка, делаем паузу
            if attempt < max_attempts:
                print(f"Пауза {pause_between_attempts} сек перед повторной отправкой...")
                time.sleep(pause_between_attempts)

        print("Не удалось установить задержку после максимального количества попыток")
        return False


# Пример использования
if __name__=='__main__':
    # Создаем объект прибора
    odl=OpticDelayLine(port="COM6", baudrate=9600)

    # Инициализация
    odl.initialize()

    # Прочитать текущее время
    current_delay_before = odl.get_time_delay()
    print("Delay time before = ", current_delay_before)

    # Установить время задержки
    set_delay_time=100
    odl.set_time_delay(time_delay=set_delay_time)

    current_delay_after = odl.get_time_delay()
    print("Delay time after = ", current_delay_after)

    # Закрыть соединение
    # odl.disconnect()
