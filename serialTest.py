import serial

ser1 = serial.Serial('/dev/ttyUSB0',9600)
ser2 = serial.Serial('/dev/ttyAMA0',9600)

while(True):
	ser1.write('a')
	print ser2.read()
