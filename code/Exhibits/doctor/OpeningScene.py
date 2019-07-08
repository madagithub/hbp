import pygame
from pygame.locals import *

import time

from common.Scene import Scene
from common.Button import Button

from common.Utilities import Utilities

START_BUTTON_TEXT_COLOR = [0, 0, 0]

#TODO: Unite with neuron opening screen
class OpeningScene(Scene):
	def __init__(self, game):
		super().__init__(game)

		for command in self.config.getPETDoneSerialPortCommands():
			game.sendToSerialPort(command)
			time.sleep(0.02)

		self.background = pygame.image.load('assets/images/doctor/background.png')

		self.startButton = Button(self.screen, pygame.Rect(self.screen.get_width() // 2 - 245 // 2, 650, 245, 78), 
			pygame.image.load('assets/images/button-empty.png'), pygame.image.load('assets/images/button-selected.png'), 
			self.config.getText("DFAM_OPENING_SCREEN_BUTTON_TEXT"), START_BUTTON_TEXT_COLOR, START_BUTTON_TEXT_COLOR, self.buttonFont, self.onStartClick)
		self.buttons.append(self.startButton)

		self.createTexts()

	def onStartClick(self):
		self.game.transition('OPENING_VIDEO')

	def onLanguageChanged(self):
		super().onLanguageChanged()
		self.createTexts()
		self.startButton.createText(self.config.getText("DFAM_OPENING_SCREEN_BUTTON_TEXT"), self.buttonFont)

	def createTexts(self):
		self.headerText = self.headerFont.render(self.config.getText("DFAM_OPENING_SCREEN_HEADER"), True, (255, 255, 255))
		self.subHeaderTexts = Utilities.renderTextList(self.config, self.textFont, "DFAM_OPENING_SCREEN_SUB_HEADER")

	def draw(self, dt):
		self.screen.blit(self.background, (0, 0))
		Utilities.drawTextOnCenterX(self.screen, self.headerText, (self.screen.get_width() // 2, 367))
		Utilities.drawTextsOnCenterX(self.screen, self.subHeaderTexts, (self.screen.get_width() // 2, 491), 40)
		super().draw(dt)