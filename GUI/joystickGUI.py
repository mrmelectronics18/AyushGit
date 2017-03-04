import pygame
import time
import os
import math

class BigController():

	white = (255,255,255)
	black = (0,0,0)
	red = (255,0,0)
	green = (0,255,0)
	blue = (0,0,255)
	height = 590
	width = 590

	def __init__(self):
		global joystick
		global ser
		pygame.init()
		pygame.joystick.init()
		if pygame.joystick.get_init() == 1:
			print("Module initialized")
		joystickinit = pygame.joystick.Joystick(0)
		print "Joystick's name : "+joystickinit.get_name() + " id : "+str(joystickinit.get_id())
		joystickinit.init()
		joystick = joystickinit
		#ser = serial.Serial('/dev/ttyUSB0',9600)	
		#print(ser.name+" is initialized.")
		self.mainDisp = pygame.display.set_mode(((self.width+10)*2,self.height+10))
		pygame.display.set_caption('MotorCode')
		self.roverDisp = pygame.Surface((590,590))
		pygame.draw.circle(self.roverDisp,self.white,(295,295),295)
		#pygame.draw.rect(self.roverDisp,self.white,[0,0,self.width,self.height])
		self.mainDisp.blit(self.roverDisp,(5,5))
		self.font = pygame.font.SysFont(None,35)
		pygame.display.update()
		self.main()

	def mapVal(self,a,b,c,d,e):
		return (a-b)*(e-d)/(c-b) + d

	def getCoordinates(self,angle,distance):
		x = math.cos(math.radians(angle)) * distance
		y = math.sin(math.radians(angle)) * distance
		return (int(x),int(y))

	def hairPin(self,centerBuff):
		hairpin_len = int(self.mapVal(centerBuff*2,0,1023,0,self.width))
		pygame.draw.line(self.roverDisp,self.black,(self.width/2 - hairpin_len/2,self.height/2),(self.width/2 + hairpin_len/2,self.height/2),1)
		pygame.draw.line(self.roverDisp,self.black,(self.width/2,self.height/2 - hairpin_len/2),(self.width/2,self.height/2 + hairpin_len/2),1)
		self.buttonDisp = pygame.Surface((590,590/2-2.5))
		self.sensorDisp = pygame.Surface((590,590/2+2.5))
		self.buttonDisp.fill(self.white)
		self.sensorDisp.fill(self.white)
		#pygame.draw.rect(self.gameDisp,self.white,[600,5,self.width,self.height/2])
		#pygame.draw.rect(self.gameDisp,self.white,[600,self.height/2 +10,self.width,self.height/2 - 5])

	def processBut(self):
		buttonSurfaces = []
		for i in range(13):
			if i in range(8,13):
				t = pygame.Surface((116,90))
			else:
				t = pygame.Surface((145,90))
			buttonSurfaces.append(t)
			buttonSurfaces[i].fill(self.white)

		print buttonSurfaces[4]
		

		for i in range(8):
			pygame.draw.circle(buttonSurfaces[i],self.black,(40,45),10)
			pygame.draw.circle(buttonSurfaces[i],self.white,(40,45),8)
			if self.buttons[i] == 1:
				pygame.draw.circle(buttonSurfaces[i],self.black,(40,45),8)
			text = self.font.render(str(i),True,self.black)
			buttonSurfaces[i].blit(text,(60,30))
			if i in range(0,4):
				self.buttonDisp.blit(buttonSurfaces[i],(i*145+3,0))
			else:
				print i
				self.buttonDisp.blit(buttonSurfaces[i],((i-4)*145+3,100))

		for i in range(8,13):
			pygame.draw.circle(buttonSurfaces[i],self.black,(40,45),10)
			pygame.draw.circle(buttonSurfaces[i],self.white,(40,45),8)
			if self.buttons[i] == 1:
				pygame.draw.circle(buttonSurfaces[i],self.black,(40,45),8)
			text = self.font.render(str(i),True,self.black)
			buttonSurfaces[i].blit(text,(60,30))
			self.buttonDisp.blit(buttonSurfaces[i],((i-8)*116,200))

		'''
		pygame.draw.circle(buttonSurfaces[0],self.red,(40,45),10)
		pygame.draw.circle(buttonSurfaces[12],self.red,(40,45),10)

		button_no1 = self.font.render('0',True,self.red)
		button_no2 = self.font.render('12',True,self.red)

		pygame.draw.circle(buttonSurfaces[0],self.black,(40,45),8)
		pygame.draw.circle(buttonSurfaces[12],self.black,(40,45),8)

		buttonSurfaces[0].blit(button_no1,(60,30))
		buttonSurfaces[12].blit(button_no2,(60,30))

		self.buttonDisp.blit(buttonSurfaces[12],(0,180))
		self.buttonDisp.blit(buttonSurfaces[0],(0,0))'''



	def getAngle(self,x,y):
		if(x==512):
		    if(y>=512):
		    	tangle = 270
		    else:
		    	tangle = 90
		else:
			m1 = (y-512.0)/(x-512.0)
			m2 = (512.0-512.0)/(1023.0-0.0)
			tangle =int(math.atan((m2-m1)/(1.0+m1*m2))*57.3)
			if(x < 512):
				tangle+=180
			elif(y>512):
				tangle+=360
			if(tangle==360):
				tangle = 0
			if(x==512 and y==512):
				tangle = 0
		return tangle



	def main(self):
		clock = pygame.time.Clock()
		global joystick 
		global ser
		print joystick.get_name()

		leftr = leftf = rightr = rightf = x = y = pressed = throttle = rot = 0
		buffVal = 50
		centerBuff = 50
		prevx = prevy = 512
		prevRotVal = 0
		bufferRotVal = 20
		gameExit = False
		rotVal = 0
		self.tangle = 0
		self.buttons = [0,0,0,0,0,0,0,0,0,0,0,0,0]


		while not gameExit:
			for event in pygame.event.get():
				if event.type == pygame.QUIT :
					gameExit = True
				elif event.type == pygame.JOYAXISMOTION :
					pass
				elif event.type == pygame.JOYBUTTONDOWN:
					for i in range(len(self.buttons)):
						if joystick.get_button(i) == 1:
							self.buttons[i] = 1
				elif event.type == pygame.JOYBUTTONUP:
					for i in range(len(self.buttons)):
						if joystick.get_button(i) == 0:
							self.buttons[i] = 0

			x = joystick.get_axis(0)*512.0+512
			y = joystick.get_axis(1)*512.0+512	
			throttle = joystick.get_axis(3)*100.0+100
			rotVal = joystick.get_axis(2)*100.0 
					
			if rotVal - prevRotVal >=bufferRotVal:
				rotVal = prevRotVal + bufferRotVal
			elif rotVal - prevRotVal <=-bufferRotVal:
				rotVal = prevRotVal - bufferRotVal
			elif rotVal - prevRotVal <=-bufferRotVal:
				rotVal = prevRotVal - bufferRotVal
			elif rotVal - prevRotVal >= bufferRotVal:
				rotVal = prevRotVal + bufferRotVal

			top = self.mapVal(throttle,0,200,0,255)

			if(x>1023): 
				x = 1023
			if(y>1023): 
				y = 1023
			if(x-prevx>buffVal):
				x = prevx + buffVal
			elif(x-prevx<-buffVal):
				x = prevx - buffVal
			if(y-prevy>buffVal):
				y = prevy + buffVal
			elif(y-prevy<-buffVal):
				y = prevy - buffVal
			if(x<=512+centerBuff and x>=512-centerBuff and y<=512+centerBuff and y>=512-centerBuff):
				leftf = leftr = rightf = rightr = 0
			elif(x<=512+centerBuff and x>=512-centerBuff):
				if(y>=512+centerBuff):
						rightf = self.mapVal(y,512+centerBuff,1023,0,top)
						rightr = 0
						leftr = self.mapVal(y,512+centerBuff,1023,0,top)
						leftf = 0
				elif(y<=512-centerBuff):
						rightr = self.mapVal(y,0,512-centerBuff,top,0)
						rightf = 0
						leftf = self.mapVal(y,0,512-centerBuff,top,0)
						leftr = 0
			elif(y<=512+centerBuff and y>=512-centerBuff):
				if(x>=512+centerBuff):
					leftf = self.mapVal(x,512+centerBuff,1023,0,top)
					leftr = 0
					rightf = 0
					rightr = 0
				elif(x<512-centerBuff):
					leftr = 0
					leftf = 0
					rightf = 0
					rightr = self.mapVal(x,0,512-centerBuff,top,0)
			else:
				refx = refy = 0
				if(y<512):
					if(x>512):
						refy = y
						refx = 1023 - refy
						if(x<=refx):
							leftr = 0
							leftf = self.mapVal(y,0,511,top,0)
							rightf = 0
							rightr = self.mapVal(x,512,refx,top,top/2.0)
		
						else:
							refx = x
							refy = 1023 - refx
							leftr = 0
							leftf = self.mapVal(x,512,1023,0,top)
				  			rightf = 0
							rightr = self.mapVal(y,refy,511,top/2.0,0)

					else:
						refy = refx = y
						if(x>=refx):
							rightf = 0
							rightr = self.mapVal(y,0,511,top,0)
							leftr = 0
							leftf = self.mapVal(x,refx,511,top/2.0,top)

						else:
							refx = refy = x
							rightf = 0
							rightr = self.mapVal(x,0,511,top,0)
							leftr = 0
							leftf = self.mapVal(y,refy,511,top/2.0,0)

				else:
					if(x<512):
						refy = y
						refx = 1023 - refy
						if(x>=refx):
							rightr = 0
							rightf = self.mapVal(y,512,1023,0,top)
							leftr = self.mapVal(x,refx,511,0,top)
							leftf = 0
								#else:
								#	refx = x
								#	refy = 1023 - refx
								#	leftf = 0
								#	leftr = self.mapVal(y,512,1023,0,top)
								#	rightr = 0
								#	rightf = self.mapVal(x,refx,511,0,top)

					else:
						refx = refy = y
							#if(x>refx):
								#	refx = refy = x
								#	rightr = 0
								#	rightf = self.mapVal(x,512,1023,0,top)
								#	leftr = 0
								#	leftf = self.mapVal(y,512,refy,top,0)

						if(x<=refx):
							refx = refy = y
							leftf = 0
							leftr = self.mapVal(y,512,1023,0,top)
							rightr = 0
							rightf = self.mapVal(x,512,refx,top,0)

			prevx = x
			prevy = y

			if rotVal!=0 and x<=512+centerBuff and x>=512-centerBuff and y<=512+centerBuff and y>=512-centerBuff:
						
				if(rotVal<-centerBuff):
					leftf = 0
					leftr = self.mapVal(rotVal,0,-100,0,top)
					rightf = 0
					rightr = self.mapVal(rotVal,0,-100,0,top)
				elif(rotVal>centerBuff):
					leftr = 0
					leftf = self.mapVal(rotVal,0,100,0,top)
					rightr = 0
					rightf = self.mapVal(rotVal,0,100,0,top)
				prevRotVal = rotVal

			if rotVal == 0:
				prevRotVal = 0

			leftf = int(leftf)
			leftr = int(leftr)
			rightf = int(rightf)
			rightr = int(rightr)
			
			print ("x : "+str(x)+" y : "+str(y))
			print("leftf : "+str(leftf)+" rightf : "+str(rightf))
			print("leftr : "+str(leftr)+" rightr : "+str(rightr))
			print("Throttle : "+str(throttle))
			print("Rotation Value: "+str(rotVal))
			clock.tick(30)
			'''ser.write('0'+str(leftf)+'$')
			ser.write('1'+str(leftr)+'$')
			ser.write('2'+str(rightf)+'$')
			ser.write('3'+str(rightr)+'$')
			#print('aafaduf gakdugfikasd'+str(ser.read()))
			if pressed == 2:
				break'''

			leftPoint = (295-20,295)
			rightPoint = (295+20,295)
			point = (295,295)

			if rotVal != 0:
				if rotVal > 0:
					if rotVal <= 50:
						tx = int(295-(self.mapVal(rotVal,0,50,0,20)))
						ty = int(math.sqrt(400-(tx-295)**2) + 295)
						ty = 295 - (ty - 295)
						leftPoint = (ty,tx)
						print leftPoint
						tx = int(295+(self.mapVal(rotVal,0,50,0,20)))
						ty = int(math.sqrt(400-(tx-295)**2) + 295)
						#ty = 295 - (ty - 295)
						rightPoint = (ty,tx)
						print rightPoint
					elif rotVal <= 100:
						tx = int(295+(self.mapVal(rotVal,50,100,0,20)))
						ty = int(math.sqrt(400-(tx-295)**2) + 295)
						ty = 295 - (ty - 295)
						leftPoint = (tx,ty)
						print leftPoint
						tx = int(295-(self.mapVal(rotVal,50,100,0,20)))
						ty = int(math.sqrt(400-(tx-295)**2) + 295)
						#ty = 295 - (ty - 295)
						rightPoint = (tx,ty)
						print rightPoint
				elif rotVal < 0:
					if rotVal >= -50:
						tx = int(295-(self.mapVal(rotVal,0,-50,0,20)))
						ty = int(math.sqrt(400-(tx-295)**2) + 295)
						#ty = 295 - (ty - 295)
						leftPoint = (ty,tx)
						print leftPoint
						tx = int(295+(self.mapVal(rotVal,0,-50,0,20)))
						ty = int(math.sqrt(400-(tx-295)**2) + 295)
						ty = 295 - (ty - 295)
						rightPoint = (ty,tx)
						print rightPoint
					elif rotVal >= -100:
						tx = int(295+(self.mapVal(rotVal,-50,-100,0,20)))
						ty = int(math.sqrt(400-(tx-295)**2) + 295)
						#ty = 295 - (ty - 295)
						leftPoint = (tx,ty)
						print leftPoint
						tx = int(295-(self.mapVal(rotVal,-50,-100,0,20)))
						ty = int(math.sqrt(400-(tx-295)**2) + 295)
						ty = 295 - (ty - 295)
						rightPoint = (tx,ty)
						print rightPoint



			#outside for events
			#if(x<=512+centerBuff and x>=512-centerBuff and y<=512+centerBuff and y>=512-centerBuff):
			self.mainDisp.fill(self.black)
			pygame.draw.circle(self.roverDisp,self.white,(295,295),295)
			pygame.draw.line(self.roverDisp,self.black,(0,0),(590,590),1)
			pygame.draw.line(self.roverDisp,self.black,(0,295),(590,295),1)
			pygame.draw.line(self.roverDisp,self.black,(295,0),(295,590),1)
			pygame.draw.line(self.roverDisp,self.black,(0,590),(590,0),1)
			pygame.draw.circle(self.roverDisp,self.blue,leftPoint,5)
			pygame.draw.circle(self.roverDisp,self.green,rightPoint,5)
			pygame.draw.circle(self.roverDisp,self.red,point,5)

			#point = (int(self.mapVal(x,0,1023,0,self.width)),int(self.mapVal(y,0,1023,0,self.height)))
			angle=0
			diffAngle = 0
			dist = 0
			#if x!=512 and y!=512:
			angle = self.getAngle(x,y)
			print angle

			if rotVal==0:
				if angle <= 90 and angle >=1 and leftf >= rightr :
					diffAngle = 90 - self.mapVal(leftf - rightr,0,255,0,45)
					print "Leftf :"+str(leftf)+"Rightr : "+str(rightr)
					dist = self.mapVal(leftf,0,255,0,295)
					point = self.getCoordinates(diffAngle,dist)
					point = (295+point[0],295-point[1])
					pygame.draw.circle(self.roverDisp,self.red,point,5)
					leftPoint = self.getCoordinates(diffAngle+90,20)
					print leftPoint
					leftPoint = (point[0]+leftPoint[0],point[1]-leftPoint[1])
					rightPoint = self.getCoordinates(-(90-diffAngle),20)
					print rightPoint
					rightPoint = (point[0]+rightPoint[0],point[1]-rightPoint[1])
					pygame.draw.circle(self.roverDisp,self.blue,leftPoint,5)
					pygame.draw.circle(self.roverDisp,self.green,rightPoint,5)
					print "diff angle :"+str(diffAngle)
					print "distance : "+str(dist)

				elif angle <= 180 and angle >=91 and rightr >= leftf:
					diffAngle = 90 + self.mapVal(rightr - leftf,0,255,0,45)
					print "Leftf :"+str(leftf)+"Rightr : "+str(rightr)
					dist = self.mapVal(rightr,0,255,0,295)
					point = self.getCoordinates(diffAngle,dist)
					point = (295+point[0],295-point[1])
					pygame.draw.circle(self.roverDisp,self.red,point,5)
					leftPoint = self.getCoordinates(diffAngle+90,20)
					print leftPoint
					leftPoint = (point[0]+leftPoint[0],point[1]-leftPoint[1])
					rightPoint = self.getCoordinates(-(90-diffAngle),20)
					print rightPoint
					rightPoint = (point[0]+rightPoint[0],point[1]-rightPoint[1])
					pygame.draw.circle(self.roverDisp,self.blue,leftPoint,5)
					pygame.draw.circle(self.roverDisp,self.green,rightPoint,5)
					print "diff angle :"+str(diffAngle)
					print "distance : "+str(dist)

				elif angle <= 270 and angle >=181 and rightf >= leftr:
					diffAngle = 180 + 90 - self.mapVal(rightf - leftr,0,255,0,45)
					print "Leftr :"+str(leftr)+"Rightf : "+str(rightf)
					dist = self.mapVal(rightf,0,255,0,295)
					point = self.getCoordinates(diffAngle,dist)
					point = (295+point[0],295-point[1])
					pygame.draw.circle(self.roverDisp,self.red,point,5)
					leftPoint = self.getCoordinates(diffAngle+90,20)
					print leftPoint
					leftPoint = (point[0]+leftPoint[0],point[1]-leftPoint[1])
					rightPoint = self.getCoordinates(-(90-diffAngle),20)
					print rightPoint
					rightPoint = (point[0]+rightPoint[0],point[1]-rightPoint[1])
					pygame.draw.circle(self.roverDisp,self.blue,leftPoint,5)
					pygame.draw.circle(self.roverDisp,self.green,rightPoint,5)
					print "diff angle :"+str(diffAngle)
					print "distance : "+str(dist)

				elif angle <= 360 and angle >=271 and leftr >= rightf:
					diffAngle = 270 + self.mapVal(leftr - rightf,0,255,0,45)
					print "Leftr :"+str(leftr)+"Rightf : "+str(rightf)
					dist = self.mapVal(leftr,0,255,0,295)
					point = self.getCoordinates(diffAngle,dist)
					point = (295+point[0],295-point[1])
					pygame.draw.circle(self.roverDisp,self.red,point,5)
					leftPoint = self.getCoordinates(diffAngle+90,20)
					print leftPoint
					leftPoint = (point[0]+leftPoint[0],point[1]-leftPoint[1])
					rightPoint = self.getCoordinates(-(90-diffAngle),20)
					print rightPoint
					rightPoint = (point[0]+rightPoint[0],point[1]-rightPoint[1])
					pygame.draw.circle(self.roverDisp,self.blue,leftPoint,5)
					pygame.draw.circle(self.roverDisp,self.green,rightPoint,5)
					print "diff angle :"+str(diffAngle)
					print "distance : "+str(dist)


			
				

			'''if(angle<=90 and rotVal==0):
				t = leftf - rightr
				angle = self.mapVal(t,0,255,0,45) '''

			self.hairPin(centerBuff)
			self.processBut()
			self.mainDisp.blit(self.roverDisp,(5,5))
			self.mainDisp.blit(self.buttonDisp,(600,5))
			self.mainDisp.blit(self.sensorDisp,(600,300))
			pygame.display.update()





BigController()