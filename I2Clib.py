import RPi.GPIO as GPIO
import smbus

class I2c(object):
	def __init__(self,add):
		self.address = add
		self.bus = smbus.SMBus(1)
		print 'I2C '+str(self.address)+' is initialized'
	
	def require_repeated_start():
		subprocess.check_call('chmod 666 /sys/module/i2c_bcm2708/parameters/combined',shell=true)
		subprocess.check_call('echo -n 1 > sys//module/i2c_bcm2708/parameters/combined', shell=True)

	def write8(self,register,value):
		value = value & 0xFF
		self.bus.write_byte_data(self.address,register,value)
		print str(value) + ' transmitted at '+str(self.address) 
