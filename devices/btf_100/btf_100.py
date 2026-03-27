# -*- coding: utf-8 -*-
"""
BTF-100: Класс управления оптическим фильтром OZ Optics
Минимальная версия
"""

import serial
import time
from typing import Tuple, Optional


class BTF100:
    """Класс для управления фильтром BTF-100."""
    
    # Диапазоны параметров
    MIN_WAVELENGTH = 1525.0    # нм
    MAX_WAVELENGTH = 1565.0    # нм
    MIN_LINEWIDTH = 1.0        # нм
    MAX_LINEWIDTH = 18.0       # нм
    BAUDRATE = 115200          # скорость подключения
    
    def __init__(self, port):
        """
        Инициализация объекта.
        
        Args:
            port (str): COM-порт (например, 'COM6')
            timeout (float): Таймаут чтения в секундах
        """
        self.port = port
        self.timeout = 2.0
        self.ser: Optional[serial.Serial] = None
        self._connected = False
    
    # ─────────────────────────────────────────────────────────────
    # 1. ПОДКЛЮЧЕНИЕ / ОТКЛЮЧЕНИЕ
    # ─────────────────────────────────────────────────────────────
    
    def connect(self) -> bool:
        """
        1. Подключение к устройству.
        
        Returns:
            bool: True если успешно
        """
        try:
            self.ser = serial.Serial(
                port=self.port,
                baudrate=self.BAUDRATE,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS,
                timeout=self.timeout
            )
            time.sleep(1.0)
            self.ser.reset_input_buffer()
            self.ser.reset_output_buffer()
            
            # Отключаем эхо команд
            self._send('E0', wait=0.5)
            
            # Проверка связи
            response = self._send('DEV?', wait=1.0)
            if 'Device:' in response and 'BTF' in response:
                print(f"Подключено: {self.port}")
                self._connected = True
                return True
            else:
                self.disconnect()
                print(f"Устройство не найдено")
                return False
        except Exception as e:
            print(f"Ошибка: {e}")
            return False
    
    def disconnect(self):
        """4. Отключение от устройства."""
        if self.ser and self.ser.is_open:
            self.ser.close()
        self.ser = None
        self._connected = False
        print("🔌 Отключено")
    
    # ─────────────────────────────────────────────────────────────
    # 2. УСТАНОВКА ПАРАМЕТРОВ
    # ─────────────────────────────────────────────────────────────
    
    def set_wavelength(self, wavelength: float):
        """
        Установка только длины волны (ширина полосы не меняется).
        
        Args:
            wavelength (float): Длина волны в нм (1525-1565)
        """
        if not (self.MIN_WAVELENGTH <= wavelength <= self.MAX_WAVELENGTH):
            raise ValueError(f"Длина волны: {self.MIN_WAVELENGTH}-{self.MAX_WAVELENGTH} нм")
        
        command = f"W{wavelength:.2f}"
        self._send(command, wait=3.0)
        print(f"WL={wavelength} нм")
    
    def set_linewidth(self, linewidth: float):
        """
        Установка только ширины полосы (длина волны не меняется).
        
        Args:
            linewidth (float): Ширина полосы в нм (1-18)
        """
        if not (self.MIN_LINEWIDTH <= linewidth <= self.MAX_LINEWIDTH):
            raise ValueError(f"Ширина полосы: {self.MIN_LINEWIDTH}-{self.MAX_LINEWIDTH} нм")
        
        # Получаем текущую длину волны
        current_wl, _ = self.get_wavelength()
        if current_wl is None:
            current_wl = 1550.0
        
        # Команда: W<w>,<l> (запятая!)
        command = f"W{current_wl:.2f},{linewidth:.2f}"
        self._send(command, wait=3.0)
        print(f"BW={linewidth} нм")
    
    def set_wavelength_and_linewidth(self, wavelength: float, linewidth: float):
        """
        Установка длины волны И ширины полосы одновременно.
        
        Args:
            wavelength (float): Длина волны в нм (1525-1565)
            linewidth (float): Ширина полосы в нм (1-18)
        """
        if not (self.MIN_WAVELENGTH <= wavelength <= self.MAX_WAVELENGTH):
            raise ValueError(f"Длина волны: {self.MIN_WAVELENGTH}-{self.MAX_WAVELENGTH} нм")
        if not (self.MIN_LINEWIDTH <= linewidth <= self.MAX_LINEWIDTH):
            raise ValueError(f"Ширина полосы: {self.MIN_LINEWIDTH}-{self.MAX_LINEWIDTH} нм")
        
        # Правильный формат: запятая!
        command = f"W{wavelength:.2f},{linewidth:.2f}"
        self._send(command, wait=3.0)
        print(f"WL={wavelength} нм, BW={linewidth} нм")
    
    # ─────────────────────────────────────────────────────────────
    # 3. ПОЛУЧЕНИЕ ПАРАМЕТРОВ
    # ─────────────────────────────────────────────────────────────
    
    def get_wavelength(self) -> Tuple[Optional[float], Optional[float]]:
        """
        Получение текущей длины волны и ширины полосы.
        
        Returns:
            tuple: (длина_волны, ширина_полосы)
        """
        response = self._send('W?', wait=1.0)
        
        try:
            # Парсинг: Current WL(1550.00), LW(5.00nm) Done
            wl_start = response.find('WL(') + 3
            wl_end = response.find(')', wl_start)
            wavelength = float(response[wl_start:wl_end])
            
            lw_start = response.find('LW(') + 3
            lw_end = response.find('nm)', lw_start)
            linewidth = float(response[lw_start:lw_end])
            
            return wavelength, linewidth
        except:
            return None, None
    
    def get_info(self) -> str:
        """Получение полной информации об устройстве."""
        return self._send('DEV?', wait=1.0)
    
    # ─────────────────────────────────────────────────────────────
    # ВНУТРЕННИЕ МЕТОДЫ
    # ─────────────────────────────────────────────────────────────
    
    def _send(self, command: str, wait: float = 1.0) -> str:
        """Отправка команды и получение ответа."""
        if not self.ser:
            raise RuntimeError("Не подключено")
        
        self.ser.write(f"{command}\r\n".encode())
        time.sleep(wait)
        
        response = ""
        while self.ser.in_waiting:
            response += self.ser.read(self.ser.in_waiting).decode('utf-8', errors='replace')
        
        if 'Error' in response:
            raise RuntimeError(f"Ошибка устройства: {response}")
        
        return response.strip()