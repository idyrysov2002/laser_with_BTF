import numpy as np
import pyvisa as visa
import matplotlib.pyplot as plt

class YokogawaOSA:
    """Класс для управления оптическим анализатором спектра Yokogawa через VISA.
    длина волны, разрешение, спан и др. задается в нм.
    Например, set_center(1550) устанавливает центр на длине волны 1550 нм
    """
    def __init__(self, dev_IP="TCPIP0::10.2.60.60::inst0::INSTR"):
        self.rm = visa.ResourceManager()
        self.device = self.rm.open_resource(dev_IP)
        self.device.timeout = None

        print(self.__class__.__name__, "inited!")

        self.TR_type = "TRA"
        self.multiplier = 1e9
        print(self.device.query("*idn?"))

    def close_connect(self):
        """Сlose the connection"""
        self.device.close()
        print("Сonnection is closed")

    def set_center(self, val):
        """val example: 1550 (nm)"""
        self.device.write(":sens:wav:cent" + " " + f"{val}nm")

    def set_log_scale(self):
        self.device.write(":DISPLAY:TRACE:Y1:SPACING LOGarithmic")

    def set_lin_scale(self):
        self.device.write(":DISPLAY:TRACE:Y1:SPACING LINear")

    def set_span(self, val):
        """val example: 10 (nm)"""
        self.device.write(":sens:wav:span" + " " + f"{val}nm")

    def set_start(self, val):
        """val example: 1500 (nm)"""
        self.device.write(":sens:wav:star" + " " + f"{val}nm")

    def set_stop(self, val):
        """val example: 1600 (nm)"""
        self.device.write(":sens:wav:stop" + " " + f"{val}nm")

    def set_resolution(self, val):
        """val example: 0.5 (nm)"""
        self.device.write(":sens:band:res" + " " + f"{val}nm")

    def peform_zeroing(self):
        self.device.send(":cal:wav:zero ONCE")

    def disable_zeroing(self):
        self.device.write(":cal:wav:zero OFF")

    def idn(self):
        print("IDN: " + self.device.query("*IDN?"))

    def get_os(self):
        """Returns X and Y separately as numpy arrays"""
        self.device.write("INITiate:IMMediate;*wai")

        data_x = self.device.query(":TRAC:X?" + " " + self.TR_type)
        x = np.array([float(i) * self.multiplier for i in data_x.split(",")])

        data_y = self.device.query(":TRAC:Y?" + " " + self.TR_type)
        y = np.array([float(i) for i in data_y.split(",")])

        return x, y

    def get_data(self):
        data_x = self.device.query(":TRAC:X?" + " " + self.TR_type)
        x = np.array([float(i) * self.multiplier for i in data_x.split(",")])

        data_y = self.device.query(":TRAC:Y?" + " " + self.TR_type)
        y = np.array([float(i) for i in data_y.split(",")])
        return x, y

    def set_sens_mode(self, mode="nhld"):
        """val example: nhld, naut, normal, mid"""
        self.device.write(":sens:sense" + " " + mode)

    def set_sweep_speed(self, speed="2x"):
        """val example: 1x, 2x"""
        self.device.write(":sens:sweep:speed" + " " + speed)

    def get_os_y(self):
        """Returns Y separately as numpy arrays"""
        data_y = self.device.query(":TRAC:Y?" + " " + self.TR_type)
        y = np.array([float(i) for i in data_y.split(",")])
        return y
if __name__=="__main__":
    # Создание экземпляра класса
    osa = YokogawaOSA()

    # Настройка диапазона измерений 
    osa.set_start(1540)
    osa.set_stop(1590)

    # Запуск измерения и получение данных
    wave_arr, ampl_arr = osa.get_os()

    # Визуализация результатов
    plt.plot(wave_arr, ampl_arr)
    plt.show()

    # Закрытие соединения
    # osa.close_connect()
