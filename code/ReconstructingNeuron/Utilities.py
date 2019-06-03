import pygame
from pygame.locals import *

class Utilities:

	@staticmethod
	def drawTextOnCenter(screen, textBox, centerPoint):
		screen.blit(textBox, (centerPoint[0] - textBox.get_width() // 2, centerPoint[1] - textBox.get_height() // 2))

	@staticmethod
	def drawTextOnCenterX(screen, textBox, centerPoint):
		screen.blit(textBox, (centerPoint[0] - textBox.get_width() // 2, centerPoint[1] + textBox.get_height() // 2))

	@staticmethod
	def drawTextsOnCenterX(screen, textBoxes, position, lineGap):
			for i in range(len(textBoxes)):
				textBox = textBoxes[i]
				Utilities.drawTextOnCenterX(screen, textBox, (position[0], position[1] + i * lineGap))

	@staticmethod
	def renderTextList(config, font, key):
		textBoxes = []
		for text in config.getTextList(key):
			textBoxes.append(font.render(text, True, (255, 255, 255)))

		return textBoxes


