import RPi.GPIO as GPIO
import smbus
import math
import time

class I2C(object):
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

	def write16(self,register,value):
		value = value & 0xFFFF
		self.bus.write_word_data(self.address,register,value)
		print str(value) + ' transmitted at '+str(self.address)

	def readU8(self,register):
		result = self.bus.read_byte_data(self.address,register)
		print 'Received :' + str(result)
		return result

	def readS8(self,register):
		result = self.bus.read_byte_data(self.address,register)
		if result > 127:
			result -= 256
		print 'Received :' + str(result)
		return result

	def readU16(self,register,little_endian=True):
		result = self.bus.read_word_data(self.address,register) & 0xFFFF
		if not little_endian :
			result = ((result<<8)&0xFF00) + (result>>8)
		print 'Received :' + str(result)
		return result

	def readS16(self,register,little_endian=True):
		result = readU16(register,little_endian)
		if result > 32767:
			result -= 65536
		return result


#LSM9DS0

class LSM9DS0():


	LSM9DS0_CTRL_REG5_XM  =	0x24
    LSM9DS0_CTRL_REG6_XM  =	0x25
	LSM9DS0_CTRL_REG7_XM  =	0x26

	LSM9DS0_WHO_AM_I_G = 0x0F
    LSM9DS0_CTRL_REG1_G = 0x20
    LSM9DS0_CTRL_REG3_G = 0x22
    LSM9DS0_CTRL_REG4_G = 0x23
    LSM9DS0_OUT_X_L_G =	0x28
    LSM9DS0_OUT_X_H_G =	0x29
    LSM9DS0_OUT_Y_L_G =	0x2A
    LSM9DS0_OUT_Y_H_G =	0x2B
    LSM9DS0_OUT_Z_L_G =	0x2C
	LSM9DS0_OUT_Z_H_G =	0x2D

	LSM9DS0_OUT_TEMP_L_XM =	0x05
	LSM9DS0_OUT_TEMP_H_XM =	0x06

	LSM9DS0_STATUS_REG_M =	0x07
    LSM9DS0_OUT_X_L_M =	0x08
    LSM9DS0_OUT_X_H_M =	0x09
    LSM9DS0_OUT_Y_L_M =	0x0A
    LSM9DS0_OUT_Y_H_M =	0x0B
    LSM9DS0_OUT_Z_L_M =	0x0C
	LSM9DS0_OUT_Z_H_M =	0x0D

	LSM9DS0_WHO_AM_I_XM = 0x0F
    LSM9DS0_INT_CTRL_REG_M = 0x12
    LSM9DS0_INT_SRC_REG_M =	0x13
    LSM9DS0_CTRL_REG1_XM =	0x20
    LSM9DS0_CTRL_REG2_XM =	0x21
    LSM9DS0_CTRL_REG5_XM =	0x24
    LSM9DS0_CTRL_REG6_XM =	0x25
	LSM9DS0_CTRL_REG7_XM = 0x26

	LSM9DS0_OUT_X_L_A =	0x28
    LSM9DS0_OUT_X_H_A =	0x29
    LSM9DS0_OUT_Y_L_A =	0x2A
    LSM9DS0_OUT_Y_H_A =	0x2B
    LSM9DS0_OUT_Z_L_A =	0x2C
	LSM9DS0_OUT_Z_H_A =	0x2D

	__scales = {
        0.88: [0, 0.73],
        1.30: [1, 0.92],
        1.90: [2, 1.22],
        2.50: [3, 1.52],
        4.00: [4, 2.27],
        4.70: [5, 2.56],
        5.60: [6, 3.03],
        8.10: [7, 4.35],
	}

	def __init__(self):

		self.mag = I2C(0x1D)
		self.acc = I2C(0x1D)
		self.gyr = I2C(0x6B)

		self.mag.write8(self.LSM9DS0_CTRL_REG5_XM, 0b11110000) 
        self.mag.write8(self.LSM9DS0_CTRL_REG6_XM, 0b00000000) 
		self.mag.write8(self.LSM9DS0_CTRL_REG7_XM, 0b00000000)

		self.accel.write8(self.LSM9DS0_CTRL_REG1_XM, 0b01100111) 
		self.accel.write8(self.LSM9DS0_CTRL_REG2_XM, 0b00100000)

		self.gyro.write8(self.LSM9DS0_CTRL_REG1_G, 0b00001111) 
		self.gyro.write8(self.LSM9DS0_CTRL_REG4_G, 0b00110000)

	def rawAccel(self):
		aX = self.acc.readU8(self.LSM9DS0_OUT_X_L_A) | self.accel.readU8(self.LSM9DS0_OUT_X_H_A) << 8
		aY = self.accel.readU8(self.LSM9DS0_OUT_Y_L_A) | self.accel.readU8(self.LSM9DS0_OUT_Y_H_A) << 8
		aZ = self.accel.readU8(self.LSM9DS0_OUT_Z_L_A) | self.accel.readU8(self.LSM9DS0_OUT_Z_H_A) << 8

		accelArr = [accelX, accelY, accelZ]

		for i in range(len(accelArr)):
			if(accelArr[i] > 32767) :
				accelArr[i] -= 65536

		return accelArr

	def rawMag(self):
        magX = self.mag.readU8(self.LSM9DS0_OUT_X_L_M) | self.mag.readU8(self.LSM9DS0_OUT_X_H_M) << 8
        magY = self.mag.readU8(self.LSM9DS0_OUT_Y_L_M) | self.mag.readU8(self.LSM9DS0_OUT_Y_H_M) << 8
        magZ = self.mag.readU8(self.LSM9DS0_OUT_Z_L_M) | self.mag.readU8(self.LSM9DS0_OUT_Z_H_M) << 8

        magArr = [magX, magY, magZ]

        for i in range(len(magArr)):
            if magArr[i] > 32767:
                magArr[i] -= 65536

	return magArr

	'''def head(self):
		self.__declDegrees = 0
        self.__declMinutes = 0
		self.__declination = (degrees + minutes / 60) * math.pi / 180
		gauss = 1.3
		(reg, self.__scale) = self.__scales[gauss]'''


LSM9DS0()
