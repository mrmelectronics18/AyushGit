import sys
import pygame

print('Pyagme init : '+str(pygame.init()))


gameDisp = pygame.display.set_mode((800,600))
pygame.display.set_caption('Demo')

white = (255,255,255)
black = (0,0,0)

gameExit = False
lead_x = 300
lead_y= 300
lead_x_change = 0

clock = pygame.time.Clock()

while not gameExit:
	for event in pygame.event.get():
		print(event)
		if event.type == pygame.QUIT:
			gameExit = True		
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LEFT:
				lead_x_change = -10
			if event.key == pygame.K_RIGHT:
				lead_x_change = 10
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_LEFT:
				lead_x_change = 0
			if event.key == pygame.K_RIGHT:
				lead_x_change = 0

	lead_x += lead_x_change
	gameDisp.fill(white)
	pygame.draw.rect(gameDisp,black,[lead_x,lead_y,10,10])

	pygame.display.update()
	clock.tick(30)

pygame.quit()

