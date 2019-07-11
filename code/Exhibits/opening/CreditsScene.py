import pygame
from pygame.locals import *

from functools import partial

from common.Scene import Scene
from common.Button import Button

class CreditsScene(Scene):
	def __init__(self, game):
		super().__init__(game)

		image = pygame.image.load('assets/images/back-normal.png')
		tappedImage = pygame.image.load('assets/images/back-selected.png')
		self.backButton = Button(self.screen, pygame.Rect(1920 - image.get_width() - 1846, 1000, image.get_width(), image.get_height()),
			image, tappedImage, None, None, None, None,
			self.onBack)

		self.createTexts()

	def onLanguageChanged(self):
		super().onLanguageChanged()
		self.createTexts()

	def createTexts(self):
		self.background = pygame.image.load('assets/images/opening/' + self.config.languagePrefix + '-credits.png')

	def onBack(self):
		self.game.transition('START')

	def draw(self, dt):
		self.screen.blit(self.background, (0,0))
		super().draw(dt)