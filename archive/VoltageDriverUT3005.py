import serial
import time
class VoltageDriverUT3005():
	def __init__(self, serial_port = 'COM4'):
		self.ser = serial.Serial(port = serial_port, bytesize = serial.EIGHTBITS, parity = serial.PARITY_NONE, stopbits = serial.STOPBITS_ONE, timeout =1)
		self.ser.baudrate = 9600
		if (self.ser.is_open == True):
			time.sleep(0.5)
			print ('Voltage Driver is connected')


	def set_voltage(self, voltage):
		message = 'VSET1:{:.2f}'.format(voltage)
		self.ser.write((message).encode())
		time.sleep(0.5)
		print('Set voltage = ', voltage)

	def turn_on(self):
		message = 'OUT1'
		self.ser.write((message).encode())
		time.sleep(0.5)
		print('The output is on')

	def turn_off(self):
		message = 'OUT0'
		self.ser.write((message).encode())
		time.sleep(0.5)
		print('The output is off')

	def receive(self):
		line = self.ser.readline()
		return line.decode('utf-8').rstrip()

	def get_real_voltage(self):
		message = 'VOUT1?'
		self.ser.write((message).encode())
		answer = self.receive()
		time.sleep(0.5)
		return float(answer)
	
	def close(self):
		"""Закрыть COM-порт."""
		if self.ser and self.ser.is_open:
			self.turn_off() # Безопасно выключаем выход перед закрытием
			self.ser.close()
			time.sleep(0.5)
			print('Voltage Driver is closed')

if __name__=="__main__":
	ut=VoltageDriverUT3005('COM8')
	ut.turn_on()
	voltage=27
	ut.set_voltage(voltage)
	a=ut.get_real_voltage()
	print('Real voltage = ',a)