import pygame
from pygame.locals import *

import sys

OUTPUT_PREFIX = 'path-'

if len(sys.argv) != 2:
	print("Usage: python3 create-paths.py [ImageFileWithoutExtension]")
else:
	pygame.init()

	screen = pygame.display.set_mode((1920, 1080), FULLSCREEN)
	image = pygame.transform.scale(pygame.image.load('assets/images/neuron/' + sys.argv[1] + '.png'), (1200, 1200))
	cursor = pygame.image.load('assets/images/cursor.png').convert_alpha()

	isGameRunning = True
	clock = pygame.time.Clock()
	lastTime = pygame.time.get_ticks()

	pygame.mouse.set_visible(False)

	currPathIndex = 1
	currPath = []

	while isGameRunning:

		for event in pygame.event.get():
			if event.type == MOUSEBUTTONDOWN:
				currPath.append((event.pos[0] + 7, event.pos[1] + 3))
			elif event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					isGameRunning = False
				elif event.key == K_s:
					with open(OUTPUT_PREFIX + str(currPathIndex) + '.txt', 'w') as f:
						f.write('[\n')
						for i in range(len(currPath)):
							p = currPath[i]
							f.write('\t{"x": ' + str(p[0] // 2) + ', "y": ' + str(p[1] // 2) + "}")
							if i == len(currPath) - 1:
								f.write("\n]\n")
							else:
								f.write(",\n")

					currPathIndex += 1
					currPath = []

		screen.fill([0,0,0])
		screen.blit(image, (0,0))
		screen.blit(cursor, (pygame.mouse.get_pos()))

		pygame.display.flip()
		clock.tick(60)

	pygame.quit()

