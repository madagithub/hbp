import pygame
from pygame.locals import *

from Scene import Scene
from Button import Button

from Utilities import Utilities

START_BUTTON_TEXT_COLOR = [0, 0, 0]

class OpeningScene(Scene):
	def __init__(self, game):
		super().__init__(game)

		self.background = pygame.image.load('assets/images/background.png')

		self.headerText = self.headerFont.render(self.config.getText("RN_OPENING_SCREEN_HEADER"), True, (255, 255, 255))
		self.subHeaderText = self.subHeaderFont.render(self.config.getText("RN_OPENING_SCREEN_SUB_HEADER"), True, (255, 255, 255))

		self.buttons.append(Button(self.screen, pygame.Rect(self.screen.get_width() // 2 - 245 // 2, 649, 245, 78), 
			pygame.image.load('assets/images/button-empty.png'), pygame.image.load('assets/images/button-selected.png'), 
			self.config.getText("RN_OPENING_SCREEN_BUTTON_TEXT"), START_BUTTON_TEXT_COLOR, self.buttonFont, self.onStartClick))

	def onStartClick(self):
		self.game.transition('START')		

	def draw(self):
		self.screen.blit(self.background, (0, 0))
		Utilities.drawTextOnCenter(self.screen, self.headerText, (self.screen.get_width() // 2, 411))
		Utilities.drawTextOnCenter(self.screen, self.subHeaderText, (self.screen.get_width() // 2, 494))
		super().draw()