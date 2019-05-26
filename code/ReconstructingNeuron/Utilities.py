import pygame
from pygame.locals import *

class Utilities:

	@staticmethod
	def drawTextOnCenter(screen, textBox, centerPoint):
		screen.blit(textBox, (centerPoint[0] - textBox.get_width() // 2, centerPoint[1] - textBox.get_height() // 2))

	@staticmethod
	def drawTextOnCenterX(screen, textBox, centerPoint):
		screen.blit(textBox, (centerPoint[0] - textBox.get_width() // 2, centerPoint[1] + textBox.get_height() // 2))


