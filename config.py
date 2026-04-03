import itertools
import os
import time
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
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
RF_F_START_MAX = 0.2e+9
RF_F_STOP_MAX = 6.2e+9
RF_SPAN_MAX=6*GIGA
RF_RBW_MAX=1*MEGA

RF_SPAN_MIDDLE=100*MEGA
RF_RBW_MIDDLE=10*KILO

RF_SPAN_MIN=1*MEGA
RF_RBW_MIN=1*KILO

NUMBER_RF_MEASURE=1


VOLTAGES=[0, 1,2,3,4,5] # в V
DELAYS=np.arange(0, 331, 10) # в ps
CURRENTS=np.arange(100, 301, 50) # в mA
WAVELENGTH=[1530, 1540, 1550, 1560] # в nm
# LINEWIDTH=[1,2,18] # в nm

# VOLTAGES=[0] # в V
# DELAYS=np.arange(0, 10, 5) # в ps
# CURRENTS=np.arange(300, 401, 100) # в mA
# WAVELENGTH=[1530, 1540] # в nm
# OSCILLOSCOPE_MODES=['average', 'sample']
OSC_MODES=['average']
OSC_HOR_SCALES = [5e-10]

YOKO_RES_BIG_SPAN=0.02
YOKO_RES_SMALL_SPAN=0.02
YOKO_BIG_SPAN_START=1510
YOKO_BIG_SPAN_STOP=1570

# Словарь конфигурации приборов
# enabled: True/False - подключать или нет
# port: COM-порт (если нужен)

INSTRUMENTS = {
    "odl": {"enabled": True, "port": "COM6", "label": "d"},
    "btf": {"enabled": True, "port": "COM3"},
    "yoko": {"enabled": True},
    "rf": {"enabled": True},
    "ld": {"enabled": True},
    "ut": {"enabled": True, "port": "COM8"},
    "pm": {"enabled": False},
    "osc": {"enabled": True, "channel": "4", "ip": "123-223-233-233", "port": "4000"},
}

# Здесь задается порядок вложенных циклов.
# Быстрее всего менятся последний элемент SCAN_ORDER
SCAN_ORDER = ["wavelength","voltage", "current", "delay", "linewidth"]

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

PARAM_LABELS = {
    'frequensy_GHz': 'Frequency, GHz',
    'current_mA': 'Current, mA',
    'delay_ps': 'Delay, ps',
    'power_dBm':'Power, dBm',
    'wavelength_nm': "Wavelength, nm",
    'intensity_dBm': "Power, μW",
    'time_ns': "Time, ns",
    'voltage_V': "Voltage, V",
    'pm_400_mW': 'Power, mW',
    'smsr_dB': 'SMSR, dB'



}

map_data_buf={
    'pm_400':
        {
        'data':'',
        'label': PARAM_LABELS['pm_400_mW'],
        'title': '',
        'filename': 'power_meter'
        },

    'rf_freq_max':
        {
        'data':'',
        'label':PARAM_LABELS['frequensy_GHz'],
        'title': '',
        'filename': ''
        },
    'rf_freq_mid':
        {
        'data':'',
        'label':PARAM_LABELS['frequensy_GHz'],
        'title': '',
        'filename': ''
        },
    'rf_freq_min':
        {
        'data':'',
        'label':PARAM_LABELS['frequensy_GHz'],
        'title': '',
        'filename': ''
        },
    'rf_smsr_max':
        {
        'data':'',
        'label':PARAM_LABELS['smsr_dB'],
        'title': '',
        'filename': ''
        },
    'osc_mean_freq':
        {
        'data':'',
        'label':PARAM_LABELS['frequensy_GHz'],
        'title': '',
        'filename': ''
        },
    'osc_std_freq':
        {
        'data':'',
        'label':PARAM_LABELS['frequensy_GHz'],
        'title': '',
        'filename': ''
        },
}


data_collection={
    'pm_400':{
        'data': None,
        'unit': 'mW',
        
            },
    'rf_peak_freq_max':{
        'data': None,
        'unit': "GHz",

        
            },
    'rf_peak_freq_mid':{
        'data': None,
        'unit': 'GHz',
        'title': 'rf_peak_freq_mid'
            },

    
}