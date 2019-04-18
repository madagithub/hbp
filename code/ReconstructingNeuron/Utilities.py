import pygame
from pygame.locals import *

class Utilities:

	@staticmethod
	def drawTextOnCenter(screen, text, rect, font):
		textBox = font.render(text, True, (255, 255, 255))
		screen.blit(textBox, (rect.center[0] - textBox.get_width() // 2, rect.center[1] - textBox.get_height() //2))

