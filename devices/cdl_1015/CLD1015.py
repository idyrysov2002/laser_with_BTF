import pyvisa as visa
import time
class CLD1015():
	def __init__(self, device_name = 'USB::4883::32847::M00324473'):
		self.rm = visa.ResourceManager()
		try:
			self.cld = self.rm.open_resource(device_name)
			print(self.__class__.__name__, 'inited!')
		except Exception as e:
			print(e)
			print('No deivce found. Devices registered in the system:')
			self.rm.list_resources()
			exit(0)
	
	def __del__(self):
		self.cld.close()
		self.rm.close()   

	def turn_on_tec(self, temp = 25):
		self.cld.write('SOUR2:TEMP:SPO {:.2f}'.format(temp))
		self.cld.write('OUTP2:STAT ON')

	def turn_on_laser(self, current = 50e-3):
		self.cld.write('OUTP1:STAT ON')
		self.cld.write('SOUR1:CURR:LEV:AMPL {:.2f}'.format(current))

	def set_current(self, current):
		# перевод мА на А
		current_mA=current/1000
		self.cld.write('SOUR1:CURR:LEV:AMPL {:.4f}'.format(current_mA))
		print(f'Set laser current {current}mA')

	def set_temp(self, temp):
		self.cld.write('SOUR2:TEMP:SPO {:.2f}'.format(temp))
		return(temp)

	def turn_off_tec(self):
		self.cld.write('OUTP2:STAT OFF')

	def turn_off_laser(self):
		self.cld.write('OUTP1:STAT OFF')

	def turn_off_all(self):
		self.set_current(0)
		print('set current 0')
		time.sleep(1)
	
		self.turn_off_laser()
		print('laser is OFF')
		time.sleep(2)
		
		self.turn_off_tec()
		print('tec is OFF')
		
		
	def turn_on_all(self):
		self.turn_on_tec()
		print('tec is ON')
		time.sleep(2)
		
		self.turn_on_laser()
		print('laser is ON')
if __name__ == "__main__":
	LD = CLD1015()
	LD.turn_on_all()
	LD.set_current(300)
    
	
	
  
  
  
  
  
  
  
  
  
  
  


  

