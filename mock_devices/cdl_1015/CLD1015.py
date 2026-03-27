import pyvisa as visa
import time
class CLD1015():

    def __init__(self, device_name="USB::4883::32847::M00324473"):
        print(self.__class__.__name__, "inited!")

    def disconnect(self):
        print("LD: disconnect")

    def turn_on_tec(self, temp = 25):
        print("LD: turn_on_tec")

    def turn_on_laser(self, current = 50e-3):
        print("LD: turn_on_laser")

    def set_current(self, current):
        print(f'LD: Set laser current {current}mA')

    def turn_off_tec(self):
        print("LD: turn_off_tec")

    def turn_off_laser(self):
        print("LD: turn_off_laser")

    def turn_off_all(self):
        print("LD: turn_off_all")

    def turn_on_all(self):
        print("LD: turn_on_all")
if __name__ == "__main__":
	LD = CLD1015()
	LD.turn_on_all()
	LD.set_current(300)
