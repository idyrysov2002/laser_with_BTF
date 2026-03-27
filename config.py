# ─────────────────────────────────────────────────────────────
# ДЕСЯТИЧНЫЕ ПРИСТАВКИ
# ─────────────────────────────────────────────────────────────
TERA = 1e+12
GIGA = 1e+9
MEGA = 1e+6
KILO = 1e+3
MILLI = 1e-3
MICRO = 1e-6
NANO = 1e-9
PICO = 1e-12

STABILIZATION_TIME=3

# ─────────────────────────────────────────────────────────────
# НАСТРОЙКИ РАДИОЧАСТОТНИКА
# ─────────────────────────────────────────────────────────────
RF_LEVEL=-20
RF_F_START_MAX = 9*KILO
RF_F_STOP_MAX = 6.2*GIGA
RF_SPAN_MAX=6.2*GIGA
RF_RBW_MAX=1*MEGA

RF_SPAN_MIDDLE=100*MEGA
RF_RBW_MIDDLE=10*KILO

RF_SPAN_MIN=1*MEGA
RF_RBW_MIN=1*KILO

NUMBER_RF_MEASURE=2


CURRENTS=[100,200,300,400]
DELAYS=[100,200,300]
WAVELENGTH=[1525,1550,1565]
LINEWIDTH=[1,2,3]
VOLTAGES=[0,1,2,3]

YOKOGAWA_RES_BIG_SPAN=0.02
YOKOGAWA_RES_SMALL_SPAN=0.02
YOKOGAWA_BIG_SPAN_START=1510
YOKOGAWA_BIG_SPAN_STOP=1570


# Словарь конфигурации приборов
# enabled: True/False - подключать или нет
# port: COM-порт (если нужен)
INSTRUMENTS = {
    "odl": {"enabled": True, "port": "COM6", "label": "d"},
    "btf": {"enabled": True, "port": "COM3"},
    "yokogawa": {"enabled": True},
    "rf": {"enabled": True},
    "ld": {"enabled": True},
    "ut": {"enabled": True, "port": "COM8"},
    "pm": {"enabled": False},
    "oscilloscope": {"enabled": True, "channel": "4", "ip": "123-223-233-233", "port": "4000"},
}

# Здесь задается порядок вложенных циклов.
# Быстрее всего менятся последний элемент SCAN_ORDER
SCAN_ORDER = ["wavelength","voltage", "current", "delay", "linewidth"]

OSCILLOSCOPE_MODES=['average', 'sample']
OSCILLOSCOPE_HOR_SCALES = [2 * NANO, 10 * NANO]

PARAM_UNITS = {
    "voltage": "V",
    "current": "mA",
    "delay": "ps",
    "linewidth": "nm",
    "wavelength": "nm",
}

PARAM_NAMES = {
    "voltage": "voltage",
    "current": "current",
    "delay": "delay",
    "linewidth": "linewidth",
    "wavelength": "wavelength",
}

# Порядок параметров в имени файла (только для активных)
FILENAME_PARAM_ORDER = ["voltage", "current", "delay", "wavelength", "linewidth"]
