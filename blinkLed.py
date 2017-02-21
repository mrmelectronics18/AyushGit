import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setup(3,GPIO.OUT)

while(True):
	GPIO.output(3,True)
	for i in range(10**6):
		time.sleep(0.000001)
	GPIO.output(3,False)
	for i in range(10**6):
                time.sleep(0.000001)
	
GPIO.cleanup()
