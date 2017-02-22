import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setup(3,GPIO.OUT)
my_pwm = GPIO.(3,100)
my_pwm.start(0)

while(True):
	my_pwm.ChangeDutyCycle(100)
	time.sleep(1)
	my_pwm.ChangeDutyCycle(100)
	time.sleep(1)
	
GPIO.cleanup()