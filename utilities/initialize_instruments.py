import time

mock_flag=True

if mock_flag is True:
    from mock_devices.yokogawa.Yokogawa_OSA import YokogawaOSA
    from mock_devices.odl_650.OpticDelayLine_new import OpticDelayLine
    from mock_devices.ut_3005.VoltageDriverUT3005 import VoltageDriverUT3005
    from mock_devices.cdl_1015.CLD1015 import CLD1015
    from mock_devices.btf_100.btf_100 import BTF100
    from mock_devices.pm_400.PMDevice import PMDevicePM100D
    from mock_devices.rsa_device.RF306B import RF306B
    from mock_devices.oscilloscope.tektronix_DPO71604C import Oscilloscope


else:
    from devices.yokogawa.Yokogawa_OSA import YokogawaOSA
    from devices.odl_650.OpticDelayLine_new import OpticDelayLine
    from devices.ut_3005.VoltageDriverUT3005 import VoltageDriverUT3005
    from devices.cdl_1015.CLD1015 import CLD1015
    from devices.btf_100.btf_100 import BTF100
    from devices.pm_400.PMDevice import PMDevicePM100D
    from devices.rsa_device.RF306B import RF306B


from config import INSTRUMENTS

def initialize_instruments():
    """
    Инициализирует приборы на основе config.py INSTRUMENTS.
    Возвращает словарь с активными объектами приборов.
    """
    devices = {}
    cfg = INSTRUMENTS
    print("======= ИНИЦИАЛИЗАЦИЯ УСТРОЙСТВ =======")

    # 1. ODL
    if cfg["odl"]["enabled"]:
        try:
            port = cfg["odl"]["port"]
            odl = OpticDelayLine(port)
            odl.initialize()
            devices["odl"] = odl
            print(f"[OK] ODL -> {port}")
        except Exception as e:
            print(f"[FAIL] ODL: {e}")

    # 2. BTF
    if cfg["btf"]["enabled"]:
        try:
            port = cfg["btf"]["port"]
            btf = BTF100(port=port)
            devices["btf"] = btf
            print(f"[OK] BTF -> {port}")
        except Exception as e:
            print(f"[FAIL] BTF: {e}")

    # 3. OSA
    if cfg["yokogawa"]["enabled"]:
        try:
            yokogawa = YokogawaOSA()
            devices["yokogawa"] = yokogawa
            print("[OK] yokogawa")
        except Exception as e:
            print(f"[FAIL] yokogawa: {e}")

    # 4. RF
    if cfg["rf"]["enabled"]:
        try:
            rf_device = RF306B()
            devices["rf"] = rf_device
            print("[OK] RF")
        except Exception as e:
            print(f"[FAIL] RF: {e}")

    # 5. LD (Laser)
    if cfg["ld"]["enabled"]:
        try:
            ld = CLD1015()
            ld.turn_on_all()
            devices["ld"] = ld
            print("[OK] LD (ON)")
        except Exception as e:
            print(f"[FAIL] LD: {e}")

    # 6. UT (Power Supply)
    if cfg["ut"]["enabled"]:
        try:
            port = cfg["ut"]["port"]
            ut = VoltageDriverUT3005(port)
            ut.turn_on()
            devices["ut"] = ut
            print(f"[OK] UT -> {port}")
        except Exception as e:
            print(f"[FAIL] UT: {e}")

    # 7. PM (Power Meter)
    if cfg["pm"]["enabled"]:
        try:
            pm_device = PMDevicePM100D()
            devices["pm"] = pm_device
            print("[OK] PM")
        except Exception as e:
            print(f"[FAIL] PM: {e}")

    if cfg["oscilloscope"]["enabled"]:
        try:
            port = cfg["oscilloscope"]["port"]
            ip=cfg["oscilloscope"]["ip"]
            oscilloscope = Oscilloscope(ip=ip, port=port)
            devices["oscilloscope"] = oscilloscope
            print(f"[OK] oscilloscope -> {port}")
        except Exception as e:
            print(f"[FAIL] oscilloscope: {e}")
    return devices
