import pygame
from pygame.locals import *

from common.Scene import Scene
from common.Button import Button

from common.Utilities import Utilities

START_BUTTON_TEXT_COLOR = [0, 0, 0]

class ExplanationScene(Scene):
	def __init__(self, game):
		super().__init__(game)

		self.nextButton = Button(self.screen, pygame.Rect(self.screen.get_width() // 2 - 245 // 2, 491, 245, 78), 
			pygame.image.load('assets/images/button-empty.png'), pygame.image.load('assets/images/button-selected.png'), 
			self.config.getText("DFAM_EXP_SCREEN_BUTTON_TEXT"), START_BUTTON_TEXT_COLOR, START_BUTTON_TEXT_COLOR, self.buttonFont, self.onStartClick)
		self.buttons.append(self.nextButton)

		self.createTexts()

	def onStartClick(self):
		self.game.transition('CHOOSE')

	def onLanguageChanged(self):
		super().onLanguageChanged()
		self.createTexts()
		self.nextButton.createText(self.config.getText("DFAM_EXP_SCREEN_BUTTON_TEXT"), self.buttonFont)

	def createTexts(self):
		self.headerTexts = Utilities.renderTextList(self.config, self.smallTextFont, "DFAM_EXP_SCREEN_HEADER_TEXT")
		self.infoTexts = Utilities.renderTextList(self.config, self.smallButtonTextFont, "DFAM_EXP_SCREEN_INFO_TEXT")

	def draw(self, dt):
		Utilities.drawTextsOnCenterX(self.screen, self.headerTexts, (self.screen.get_width() // 2, 186), 41)
		Utilities.drawTextsOnCenterX(self.screen, self.infoTexts, (self.screen.get_width() // 2, 321), 36)
		super().draw(dt)