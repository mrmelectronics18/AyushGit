import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setup(12,GPIO.OUT)
my_pwm = GPIO.PWM(12,100000)
my_pwm.start(0)
try:
	while(True):
		for i in range(100):
			my_pwm.ChangeDutyCycle(i)	
			time.sleep(0.02)
		for i in range(100):
			my_pwm.ChangeDutyCycle(100-i)
			time.sleep(0.02)

except KeyboardException:
	my_pwm.stop()	
	GPIO.cleanup()
