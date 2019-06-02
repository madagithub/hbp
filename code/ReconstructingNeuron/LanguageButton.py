import pygame
from pygame.locals import *

from Utilities import Utilities
from Button import Button

class LanguageButton(Button):
	def __init__(self, screen, rect, image, tappedImage, notVisibleImage, text, color, selectedColor, font, onClickCallback):
		super().__init__(screen, rect, image, tappedImage, text, color, selectedColor, font, onClickCallback)

		self.notVisibleImage = notVisibleImage

	def draw(self):
		super().draw()

		if not self.visible:
			self.screen.blit(self.notVisibleImage, (self.rect.left, self.rect.top))
			if self.textBox is not None:
				Utilities.drawTextOnCenter(self.screen, self.textBox, self.rect.center)

