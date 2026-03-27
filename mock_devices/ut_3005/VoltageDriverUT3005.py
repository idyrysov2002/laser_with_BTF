import serial
import time
class VoltageDriverUT3005():
	def __init__(self, serial_port = 'COM4'):
		print ('Voltage Driver is connected')


	def set_voltage(self, voltage):
		print(f'Set voltage {voltage}V')

	def turn_on(self):
		print('The output is on')

	def turn_off(self):
		print('The output is off')

	def receive(self):
		line = self.ser.readline()
		return line.decode('utf-8').rstrip()

	def out_off_and_close_COM(self):
		"""Отключить OUT и закрыть COM-порт."""
		if self.ser and self.ser.is_open:
			self.turn_off() # Безопасно выключаем выход перед закрытием
			self.ser.close()
			time.sleep(0.5)
			print('Voltage Driver is closed')
	
		

if __name__=="__main__":
	ut=VoltageDriverUT3005('COM8')
	ut.turn_on()
	voltage=4
	ut.set_voltage(voltage)