import pygame
from pygame.locals import *
from pyfribidi import *
import sys
pygame.init()

s = u'عربية'
txt = log2vis(s)

screen = pygame.display.set_mode((640, 480))
screen.fill((255,255,255))
font = pygame.font.Font("TheSansArabic-Black.ttf", 35);
while True:
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
	surf = font.render(txt,False,(0, 0, 0))
	rect = surf.get_rect()
	rect.center = (300, 100)
	screen.blit(surf, rect)
	pygame.display.update()