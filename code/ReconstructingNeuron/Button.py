import pygame
from pygame.locals import *

from Utilities import Utilities

class Button:
	def __init__(self, screen, rect, image, tappedImage, text, color, selectedColor, font, onClickCallback):
		self.screen = screen
		self.rect = rect
		self.image = image
		self.tappedImage = tappedImage

		if text is not None:
			self.textBox = font.render(text, True, color)
			self.selectedTextBox = font.render(text, True, selectedColor)
		else:
			self.textBox = None

		#self.selectedTextBox = self.font.render(text, True, selectedColor)
		self.onClickCallback = onClickCallback
		self.isMouseDownOnButton = False

	def draw(self):
		self.screen.blit(self.tappedImage if self.isMouseDownOnButton else self.image, (self.rect.left, self.rect.top))

		if self.textBox is not None:
			Utilities.drawTextOnCenter(self.screen, self.selectedTextBox if self.isMouseDownOnButton else self.textBox, self.rect.center)

	def onMouseDown(self, position):
		self.isMouseDownOnButton = self.rect.collidepoint(position)

	def onMouseUp(self, position):
		if self.rect.collidepoint(position) and self.isMouseDownOnButton:
			self.onClickCallback()

		self.isMouseDownOnButton = False

