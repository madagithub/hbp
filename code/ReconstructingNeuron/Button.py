import pygame
from pygame.locals import *

from Utilities import Utilities

REGULAR_COLOR = [127, 127, 127]
TAP_COLOR = [60, 60, 60]

class Button:
	def __init__(self, screen, rect, text, font, onClickCallback):
		self.screen = screen
		self.rect = rect
		self.text = text
		self.font = font
		self.onClickCallback = onClickCallback
		self.isMouseDownOnButton = False

	def draw(self):
		pygame.draw.rect(self.screen, TAP_COLOR if self.isMouseDownOnButton else REGULAR_COLOR, self.rect)
		Utilities.drawTextOnCenter(self.screen, self.text, self.rect, self.font)

	def onMouseDown(self, position):
		self.isMouseDownOnButton = self.rect.collidepoint(position)

	def onMouseUp(self, position):
		if self.rect.collidepoint(position) and self.isMouseDownOnButton:
			self.onClickCallback()

		self.isMouseDownOnButton = False

