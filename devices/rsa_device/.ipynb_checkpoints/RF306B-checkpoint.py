# -*- coding: utf-8 -*-

from devices_new.rsa_device.rsa_api_full_N import *
import numpy as np

def print_settings(settings):
    pass
#print("________Settings________")
#for sett in settings._fields_:
#	print(sett[0] + ":", eval(f"settings.{sett[0]}"))
#	print("------------------------")


# Tektronix RSA306B
class RF306B():
	# When you init this class, connection is established
	def __init__(self):
		print_settings(Spectrum_Settings())
		search_connect()
        self.cf = 2.4453e9
		self.refLevel = -20
		self.span = 6.2e9
		self.rbw = 10e3
		self.start = 9e3
		self.stop = 6.2e9
		#print_settings(get_spectrum_settings())

	#def set_conf(self):
		self.specSet = config_spectrum(self.cf, self.refLevel, self.span, self.rbw, self.start, self.stop)
		print(self.__class__.__name__, 'inited!')

		#print_settings(self.specSet)

	def __del__(self):
		rsa.DEVICE_Disconnect()
        
	def set_cf(self, val):
		self.cf = val
		self.specSet = config_spectrum(self.cf, self.refLevel, self.span, self.rbw, self.start, self.stop)

	def set_refLevel(self, val):
		self.refLevel = val
		self.specSet = config_spectrum(self.cf, self.refLevel, self.span, self.rbw, self.start, self.stop)

	def set_span(self, val):
		self.span = val
		self.specSet = config_spectrum(self.cf, self.refLevel, self.span, self.rbw, self.start, self.stop)

	def set_rbw(self, val):
		self.rbw = val
		self.specSet = config_spectrum(self.cf, self.refLevel, self.span, self.rbw, self.start, self.stop)

	def set_start(self, val):
		self.start = val
		self.specSet = config_spectrum(self.cf, self.refLevel, self.span, self.rbw, self.start, self.stop)

	def set_stop(self, val):
		self.stop = val
		self.specSet = config_spectrum(self.cf, self.refLevel, self.span, self.rbw, self.start, self.stop)

	def get_rf(self):
		''' Returns X and Y separatly in the form of numpy arrays'''
		trace = acquire_spectrum(self.specSet)
		freq = create_frequency_array(self.specSet)

		return freq, trace

	def get_peak_power_and_freq(self, freq, trace):
		return peak_power_detector(freq, trace)

	def config_param(self, cf, refLevel, span, rbw, start, stop):
		self.cf = cf
		self.refLevel = refLevel
		self.span = span
		self.rbw = rbw
		self.start = start
		self.stop = stop self.specSet = config_spectrum(self.cf, self.refLevel, self.span, self.rbw, self.start, self.stop)
