import pygame
from pygame.locals import *

class Utilities:

	@staticmethod
	def drawTextOnCenter(screen, text, centerPoint, font):
		textBox = font.render(text, True, (255, 255, 255))
		screen.blit(textBox, (centerPoint[0] - textBox.get_width() // 2, centerPoint[1] + textBox.get_height() // 2))


