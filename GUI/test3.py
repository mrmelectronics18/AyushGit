import pygame

pygame.init()

pygame.joystick.init()

joy = pygame.joystick.Joystick(0)

joy.init()

while True:
	for event in pygame.event.get():
		if event.type == pygame.JOYBUTTONDOWN :
			for i in range(joy.get_numbuttons()):
				if joy.get_button(i) == 1:
					print i
					