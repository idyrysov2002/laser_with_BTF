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
        print(self.__class__.__name__, "inited!")

    def connect(self) -> bool:
        print(f"BTF: connect")

    def disconnect(self):
        print(f"BTF: disconnect")

    def set_wavelength(self, wavelength: float):
        print(f"BTF: set_wavelength, {wavelength}nm")

    def set_linewidth(self, linewidth: float):
        print(f"BTF: set_linewidth, {linewidth}nm")
