import pygame
from pygame.locals import *

from Utilities import Utilities

class Button:
	def __init__(self, screen, rect, text, font, onClickCallback):
		self.screen = screen
		self.rect = rect
		self.text = text
		self.font = font
		self.onClickCallback = onClickCallback

	def draw(self):
		pygame.draw.rect(self.screen, [255,255,0], self.rect)
		Utilities.drawTextOnCenter(self.screen, self.text, self.rect, self.font)

	def onClick(self, position):
		if self.rect.collidepoint(position):
			self.onClickCallback()

