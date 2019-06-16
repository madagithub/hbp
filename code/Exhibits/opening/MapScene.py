import pygame
from pygame.locals import *

from functools import partial

from common.Scene import Scene
from common.Button import Button

from common.Utilities import Utilities

START_BUTTON_TEXT_COLOR = [0, 0, 0]

COUNTRIES_DATA = [
	{'key': 'spain', 'image': 'spain-map-normal', 'selectedImage': 'spain-map-selected', 'x': 494, 'y': 638, 'nameImage': 'spain-name', 'nameX': 587, 'nameY': 681},
]

class MapScene(Scene):
	def __init__(self, game):
		super().__init__(game)

		self.titles = []

		self.background = pygame.image.load('assets/images/opening/map/map-background.png')

		for countryData in COUNTRIES_DATA:
			image = pygame.image.load('assets/images/opening/map/' + countryData['image'] + '.png')
			selectedImage = pygame.image.load('assets/images/opening/map/' + countryData['selectedImage'] + '.png')
			mapButton = Button(self.screen, pygame.Rect(countryData['x'], countryData['y'], image.get_width(), image.get_height()), 
					image, selectedImage, None, None, None, None, partial(self.onCountryClick, countryData['key']))

			self.buttons.append(mapButton)

			title = pygame.image.load('assets/images/opening/map/' + countryData['nameImage'] + '-' + self.config.languagePrefix + '.png')
			self.titles.append({'position': (countryData['nameX'], countryData['nameY']), 'image': title})

		self.createTexts()

	def onCountryClick(self, countryKey):
		self.game.transition('COUNTRY', countryKey)

	def onLanguageChanged(self):
		super().onLanguageChanged()
		self.createTexts()

	def createTexts(self):
		pass

	def draw(self, dt):
		self.screen.blit(self.background, (0,0))
		for title in self.titles:
			self.screen.blit(title['image'], title['position'])
		super().draw(dt)