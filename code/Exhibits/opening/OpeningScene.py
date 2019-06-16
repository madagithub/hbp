import pygame
from pygame.locals import *

from functools import partial

from common.Scene import Scene
from common.Button import Button

from common.Utilities import Utilities

START_BUTTON_TEXT_COLOR = [0, 0, 0]

class OpeningScene(Scene):
	def __init__(self, game):
		super().__init__(game)

		index = 0
		for video in self.config.getOpeningVideos():
			self.videoButton = Button(self.screen, pygame.Rect(video['x'], video['y'], 245, 78), 
				pygame.image.load('assets/images/button-empty.png'), pygame.image.load('assets/images/button-selected.png'), 
				"Video " + str(index), START_BUTTON_TEXT_COLOR, START_BUTTON_TEXT_COLOR, self.buttonFont, 
				partial(self.onVideoClick, video['file'], video.get('soundFile', None)))
			index += 1
			self.buttons.append(self.videoButton)

		self.mapButton = Button(self.screen, pygame.Rect(500, 500, 245, 78), 
				pygame.image.load('assets/images/button-empty.png'), pygame.image.load('assets/images/button-selected.png'), 
				"Map", START_BUTTON_TEXT_COLOR, START_BUTTON_TEXT_COLOR, self.buttonFont, self.onMapClick)
		self.buttons.append(self.mapButton)

		self.createTexts()

	def onMapClick(self):
		self.game.transition('MAP')

	def onVideoClick(self, file, soundFile):
		self.game.transition('VIDEO', {'file': file, 'soundFile': soundFile})

	def onLanguageChanged(self):
		super().onLanguageChanged()
		self.createTexts()

	def createTexts(self):
		pass

	def draw(self, dt):
		super().draw(dt)