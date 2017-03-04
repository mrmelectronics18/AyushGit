import pygame
import sys
import time
import os

gameDisp = pygame.display.set_mode((800,600))
pygame.display.set_caption('Test2')

gameExit = False
sur = pygame.Surface((100,100))
white = (255,255,255)
img = pygame.image.load(os.path.join('car_player.png'))
red = (255,0,0)
black = (0,0,0)

while not gameExit:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			gameExit = True


	gameDisp.fill(white)
	dev = pygame.transform.rotate(img,45)
	gameDisp.blit(dev,(50,50))
	pygame.display.update()
	print 1
	'''for i in range(0,45):
		time.sleep(0.1)
		#gameDisp.fill(white)
		#pygame.draw.line(sur,red,(0,0),(50,0))
		p = sur.get_rect()
		sur = pygame.transform.rotate(sur,i)
		rot = sur.get_rect(center=p.center)
		pygame.draw.rect(gameDisp,red,rot)
		#gameDisp.blit(s,(100,100))
		pygame.display.update()'''

pygame.quit()