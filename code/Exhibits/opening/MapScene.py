import pygame
from pygame.locals import *

from functools import partial

from common.Scene import Scene
from common.Button import Button

from common.Utilities import Utilities

START_BUTTON_TEXT_COLOR = [0, 0, 0]

COUNTRIES_DATA = [
	{'key': 'spain', 'image-name': 'spain-map-normal', 'selectedImage-name': 'spain-map-selected', 'x': 494, 'y': 638, 'nameImage': 'spain-name', 'nameX': 587, 'nameY': 681},
	{'key': 'portugal', 'image-name': 'portugal-map-normal', 'selectedImage-name': 'portugal-map-selected', 'x': 488, 'y': 678, 'nameImage': 'portugal-name', 'nameX': 499, 'nameY': 734},
	{'key': 'israel', 'image-name': 'israel-map-normal', 'selectedImage-name': 'israel-map-selected', 'x': 1321, 'y': 882, 'nameImage': 'israel-name', 'nameX': 1336, 'nameY': 888},
	{'key': 'turkey', 'image-name': 'turkey-map-normal', 'selectedImage-name': 'turkey-map-selected', 'x': 1144, 'y': 675, 'nameImage': 'turkey-name', 'nameX': 1276, 'nameY': 736},
	{'key': 'greece', 'image-name': 'greece-map-normal', 'selectedImage-name': 'greece-map-selected', 'x': 1029, 'y': 683, 'nameImage': 'greece-name', 'nameX': 1030, 'nameY': 729},
	{'key': 'italy', 'image-name': 'italy-map-normal', 'selectedImage-name': 'italy-map-selected', 'x': 780, 'y': 556, 'nameImage': 'italy-name', 'nameX': 808, 'nameY': 598},
	{'key': 'slovenia', 'image-name': 'slovenia-map-normal', 'selectedImage-name': 'slovenia-map-selected', 'x': 907, 'y': 564, 'nameImage': 'slovenia-name', 'nameX': 907, 'nameY': 574},
	{'key': 'hungary', 'image-name': 'hungary-map-normal', 'selectedImage-name': 'hungary-map-selected', 'x': 959, 'y': 519, 'nameImage': 'hungary-name', 'nameX': 963, 'nameY': 543},
	{'key': 'austria', 'image-name': 'austria-map-normal', 'selectedImage-name': 'austria-map-selected', 'x': 831, 'y': 508, 'nameImage': 'austria-name', 'nameX': 873, 'nameY': 528},
	{'key': 'switzerland', 'image-name': 'switzerland-map-normal', 'selectedImage-name': 'switzerland-map-selected', 'x': 764, 'y': 538, 'nameImage': 'switzerland-name', 'nameX': 772, 'nameY': 554},
	{'key': 'france', 'image-name': 'france-map-normal', 'selectedImage-name': 'france-map-selected', 'x': 578, 'y': 456, 'nameImage': 'france-name', 'nameX': 663, 'nameY': 523},
	{'key': 'germany', 'image-name': 'germany-map-normal', 'selectedImage-name': 'germany-map-selected', 'x': 760, 'y': 350, 'nameImage': 'germany-name', 'nameX': 799, 'nameY': 434},
	{'key': 'belgium', 'image-name': 'belgium-map-normal', 'selectedImage-name': 'belgium-map-selected', 'x': 710, 'y': 447, 'nameImage': 'belgium-name', 'nameX': 716, 'nameY': 449},
	{'key': 'netherlands', 'image-name': 'netherlands-map-normal', 'selectedImage-name': 'netherlands-map-selected', 'x': 717, 'y': 394, 'nameImage': 'netherlands-name', 'nameX': 734, 'nameY': 407},
	{'key': 'uk', 'image-name': 'uk-map-normal', 'selectedImage-name': 'uk-map-selected', 'x': 522, 'y': 175, 'nameImage': 'uk-name', 'nameX': 591, 'nameY': 403},
	{'key': 'denmark', 'image-name': 'denmark-map-normal', 'selectedImage-name': 'denmark-map-selected', 'x': 797, 'y': 271, 'nameImage': 'denmark-name', 'nameX': 803, 'nameY': 318},
	{'key': 'sweden', 'image-name': 'sweden-map-normal', 'selectedImage-name': 'sweden-map-selected', 'x': 848, 'y': 0, 'nameImage': 'sweden-name', 'nameX': 860, 'nameY': 221},
	{'key': 'finland', 'image-name': 'finland-map-normal', 'selectedImage-name': 'finland-map-selected', 'x': 1006, 'y': 0, 'nameImage': 'finland-name', 'nameX': 1027, 'nameY': 144},
	{'key': 'norway', 'image-name': 'norway-map-normal', 'selectedImage-name': 'norway-map-selected', 'x': 738, 'y': 0, 'nameImage': 'norway-name', 'nameX': 772, 'nameY': 181}
]

class MapScene(Scene):
	def __init__(self, game):
		super().__init__(game)

		self.titles = []
		self.selectedCountry = None

		self.background = pygame.image.load('assets/images/opening/map/map-background.png')

		for countryData in COUNTRIES_DATA:
			image = pygame.image.load('assets/images/opening/map/' + countryData['image-name'] + '.png')
			selectedImage = pygame.image.load('assets/images/opening/map/' + countryData['selectedImage-name'] + '.png')

			countryData['image'] = image
			countryData['selectedImage'] = selectedImage

			title = pygame.image.load('assets/images/opening/map/' + countryData['nameImage'] + '-' + self.config.languagePrefix + '.png')
			self.titles.append({'position': (countryData['nameX'], countryData['nameY']), 'image': title})

		self.createTexts()

	def onCountryClick(self, countryKey):
		self.game.transition('COUNTRY', countryKey)

	def onLanguageChanged(self):
		super().onLanguageChanged()
		self.createTexts()

	def createTexts(self):
		for i in range(len(COUNTRIES_DATA)):
			countryData = COUNTRIES_DATA[i]
			self.titles[i]['image'] = pygame.image.load('assets/images/opening/map/' + countryData['nameImage'] + '-' + self.config.languagePrefix + '.png')
			self.titles[i]['position'] = (countryData['nameX'] + ((-self.titles[i]['image'].get_width() + 20) if self.config.isRtl() else 0), countryData['nameY'])

	def getCountryAtPos(self, pos):
		for country in COUNTRIES_DATA:
			image = country['image']
			rect = Rect(country['x'], country['y'], image.get_width(), image.get_height())
			if rect.collidepoint(pos):
				alpha = image.get_at((pos[0] - country['x'], pos[1] - country['y'])).a
				if alpha > 0:
					return country

		return None

	def onMouseDown(self, pos):
		super().onMouseDown(pos)

		country = self.getCountryAtPos(pos)
		if country is not None:
			self.selectedCountry = country

	def onMouseUp(self, pos):
		super().onMouseUp(pos)

		if self.selectedCountry is not None:
			country = self.getCountryAtPos(pos)
			if country == self.selectedCountry:
				self.onCountryClick(country['key'])

		self.selectedCountry = None

	def draw(self, dt):
		self.screen.blit(self.background, (6,0))

		for countryData in COUNTRIES_DATA:
			if countryData == self.selectedCountry:
				self.screen.blit(countryData['selectedImage'], (countryData['x'], countryData['y']))
			else:
				self.screen.blit(countryData['image'], (countryData['x'], countryData['y']))

		for title in self.titles:
			self.screen.blit(title['image'], title['position'])

		super().draw(dt)