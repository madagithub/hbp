import pygame
from pygame.locals import *

from common.Scene import Scene
from common.Button import Button

from common.Utilities import Utilities

START_BUTTON_TEXT_COLOR = [0, 0, 0]

class OpeningScene(Scene):
	def __init__(self, game):
		super().__init__(game)

		self.background = pygame.image.load('assets/images/background.png').convert()

		self.startButton = Button(self.screen, pygame.Rect(self.screen.get_width() // 2 - 245 // 2, 649, 245, 78), 
			pygame.image.load('assets/images/button-empty.png'), pygame.image.load('assets/images/button-selected.png'), 
			self.config.getText("RN_OPENING_SCREEN_BUTTON_TEXT"), START_BUTTON_TEXT_COLOR, START_BUTTON_TEXT_COLOR, self.buttonFont, self.onStartClick)
		self.buttons.append(self.startButton)

		self.createTexts()

	def onStartClick(self):
		self.game.transition('START')

	def onLanguageChanged(self):
		super().onLanguageChanged()
		self.createTexts()
		self.startButton.createText(self.config.getText("RN_OPENING_SCREEN_BUTTON_TEXT"), self.buttonFont)

	def createTexts(self):
		self.headerText = self.headerFont.render(self.config.getText("RN_OPENING_SCREEN_HEADER"), True, (255, 255, 255))
		self.subHeaderText = self.subHeaderFont.render(self.config.getText("RN_OPENING_SCREEN_SUB_HEADER"), True, (255, 255, 255))

	def draw(self, dt):
		self.screen.blit(self.background, (0, 0))
		Utilities.drawTextOnCenter(self.screen, self.headerText, (self.screen.get_width() // 2, 411))
		Utilities.drawTextOnCenter(self.screen, self.subHeaderText, (self.screen.get_width() // 2, 494))
		super().draw(dt)