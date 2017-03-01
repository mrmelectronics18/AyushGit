import pygame
import sys
import time
import os

gameDisp = pygame.display.set_mode((800,600))
pygame.display.set_caption('Test2')

gameExit = False
sur = pygame.Surface((100,100))
white = (255,255,255)
red = (255,0,0)
black = (0,0,0)

while not gameExit:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			gameExit = True


	gameDisp.fill(white)
	sur.fill(black)
	pygame.draw.line(sur,red,(0,0),(0,50))
	
	
	gameDisp.blit(sur,(100,100))
	pygame.display.update()
	print 1
	'''for i in range(0,45):
		time.sleep(0.1)
		gameDisp.fill(white)
		pygame.draw.line(sur,red,(0,0),(50,0))
		s = pygame.transform.rotate(sur,i)
		gameDisp.blit(s,(100,100))
		pygame.display.update()'''

pygame.quit()