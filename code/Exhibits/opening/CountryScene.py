import pygame
from pygame.locals import *

from functools import partial
import math

from common.Scene import Scene
from common.Button import Button
from common.Log import Log 

from common.Utilities import Utilities

START_BUTTON_TEXT_COLOR = [0, 0, 0]

class CountryScene(Scene):
	def __init__(self, game, countryKey):
		super().__init__(game)

		self.countryKey = countryKey

		self.countryImage = pygame.image.load('assets/images/opening/map/' + countryKey + '-big.png')
		self.countryImagePos = (601 - self.countryImage.get_width() // 2, 548 - self.countryImage.get_height() // 2)
		self.dotImage = pygame.image.load('assets/images/opening/map/dot-normal.png')
		self.selectedDotImage = pygame.image.load('assets/images/opening/map/dot-selected.png')

		self.institutions = self.config.getInstitutions(self.countryKey)
		self.institutionIndex = None

		self.nextButton = Button(self.screen, pygame.Rect(1729, 314, 40, 26), 
				pygame.image.load('assets/images/opening/map/right-arrow.png'), pygame.image.load('assets/images/opening/map/right-arrow-tapped.png'), 
				None, None, None, None, self.onNextInstitutionClick, 4.0)
		self.nextButton.visible = False
		self.buttons.append(self.nextButton)

		self.prevButton = Button(self.screen, pygame.Rect(1041, 314, 20, 26), 
				pygame.image.load('assets/images/opening/map/left-arrow.png'), pygame.image.load('assets/images/opening/map/left-arrow-tapped.png'), 
				None, None, None, None, self.onPrevInstitutionClick, 4.0)
		self.prevButton.visible = False
		self.buttons.append(self.prevButton)

		image = pygame.image.load('assets/images/opening/map/play-video-normal.png')
		selectedImage = pygame.image.load('assets/images/opening/map/play-video-tapped.png')
		self.playVideoButton = Button(self.screen, pygame.Rect(1300, 914, image.get_width(), selectedImage.get_height()), 
				image, selectedImage, 
				self.config.getText("OS_MAP_PLAY_VIDEO_BUTTON_TEXT"), (0, 0, 0), (255, 255, 255), self.buttonFont, self.onPlayVideoClick)
		self.playVideoButton.visible = False
		self.buttons.append(self.playVideoButton)

		self.createTexts()

	def onNextInstitutionClick(self):
		self.clearResetTimer()
		self.institutionIndex = (self.institutionIndex + 1) % len(self.institutions)
		self.logInstitution('NEXT_INSTITUTION')
		self.loadInstitution()

	def onPrevInstitutionClick(self):
		self.clearResetTimer()
		self.institutionIndex = (self.institutionIndex - 1) % len(self.institutions)
		self.logInstitution('PREV_INSTITUTION')
		self.loadInstitution()

	def onCloseClick(self):
		pass

	def onPlayVideoClick(self):
		self.clearResetTimer()
		baseFile = 'assets/videos/opening/map/' + self.institutions[self.institutionIndex]['video'] + '-' + self.config.languagePrefix
		self.game.transition('INST_VIDEO', {'countryData': self.countryKey ,'file': baseFile + '.mp4', 'soundFile': baseFile + '.ogg', 'fps': self.institutions[self.institutionIndex]['fps']})

	def onLanguageChanged(self):
		super().onLanguageChanged()
		self.createTexts()
		self.loadInstitution()

	def createTexts(self):
		self.countryHeader = self.headerFont.render(self.config.getCountryName(self.countryKey), True, (249, 207, 71))
		self.tapInstructions = self.smallTextFont.render(self.config.getText("OS_MAP_SELECT_DOT_INSTRUCTIONS"), True, (255, 255, 255))
		self.playVideoButton.createText(self.config.getText("OS_MAP_PLAY_VIDEO_BUTTON_TEXT"), self.buttonFont)

	def onMouseDown(self, pos):
		super().onMouseDown(pos)
		self.tappedIndex = self.getClosestDotIndex(pos)

	def onMouseUp(self, pos):
		super().onMouseUp(pos)
		releaseIndex = self.getClosestDotIndex(pos)
		if self.tappedIndex is not None and self.tappedIndex == releaseIndex:
			self.selectIndex(self.tappedIndex)
		self.tappedIndex = None

	def getClosestDotIndex(self, pos):
		closestIndex = None
		closestDist = self.config.getMaxMapDotTapDistance()
		for i in range(len(self.institutions)):
			institution = self.institutions[i]
			dotCenterPosition = (self.countryImagePos[0] + institution['mapX'], self.countryImagePos[1] + institution['mapY'])
			dist = math.hypot(dotCenterPosition[0] - pos[0], dotCenterPosition[1] - pos[1])
			if dist < self.config.getMaxMapDotTapDistance():
				if dist < closestDist:
					closestIndex = i
					closestDist = dist

		return closestIndex

	def logInstitution(self, message):
		institution = self.institutions[self.institutionIndex]
		Log.info(message, self.countryKey, institution['nameKey'])

	def selectIndex(self, index):
		self.clearResetTimer()
		self.institutionIndex = index
		self.logInstitution('SELECT_INSTITUTION')
		self.loadInstitution()

	def loadInstitution(self):
		if self.institutionIndex is not None:
			institution = self.institutions[self.institutionIndex]
			self.institutionHeader = Utilities.renderTextList(self.config, self.subSubHeaderFont, institution['nameKey'], (255, 255, 255))
			self.institutionCity = Utilities.renderTextList(self.config, self.smallerTextFont, institution['cityKey'], (138, 138, 138))

			self.institutionDesc = None
			if institution.get('descriptionKey', None) is not None:
				self.institutionDesc = Utilities.renderTextList(self.config, self.almostExtraSmallTextFont, institution['descriptionKey'], (255, 255, 255))

			self.institutionImage = pygame.image.load('assets/images/opening/map/institutions/' + institution.get('image', 'default') + '.png')

			self.institutionHeaderY = 517
			self.institutionCityY = institution['cityY'] if institution.get('cityY', None) is not None else 565
			self.institutionDescY = institution['descY'] if institution.get('cityY', None) is not None else 622

			self.nextButton.visible = True
			self.prevButton.visible = True	

			self.playVideoButton.visible = institution.get('video', None) is not None

	def onHomeTapped(self):
		self.game.transition('MAP')

	def draw(self, dt):
		super().draw(dt)

		self.screen.blit(self.countryImage, self.countryImagePos)
		for i in range(0, len(self.institutions)):
			institution = self.institutions[i]
			dotCenterPosition = (self.countryImagePos[0] + institution['mapX'], self.countryImagePos[1] + institution['mapY'])
			if self.institutionIndex == i:
				self.screen.blit(self.selectedDotImage, (dotCenterPosition[0] - self.selectedDotImage.get_width() // 2, dotCenterPosition[1] - self.selectedDotImage.get_height() // 2))
			else:
				self.screen.blit(self.dotImage, (dotCenterPosition[0] - self.dotImage.get_width() // 2, dotCenterPosition[1] - self.dotImage.get_height() // 2))

		if self.institutionIndex is None:
			Utilities.drawTextOnCenterX(self.screen, self.countryHeader, (1098 + self.countryHeader.get_width() // 2, 402))
			Utilities.drawTextOnCenterX(self.screen, self.tapInstructions, (1098 + self.tapInstructions.get_width() // 2, 580))
		else:
			self.screen.blit(self.institutionImage, (1093, 157))

			if self.config.isRtl():
				Utilities.drawTextsOnRightX(self.screen, self.institutionHeader, (1693 ,self.institutionHeaderY), 40)
				Utilities.drawTextsOnRightX(self.screen, self.institutionCity, (1693 ,self.institutionCityY), 30)
			else:
				Utilities.drawTextsOnLeftX(self.screen, self.institutionHeader, (1093 ,self.institutionHeaderY), 40)
				Utilities.drawTextsOnLeftX(self.screen, self.institutionCity, (1093 ,self.institutionCityY), 30)

			if self.institutionDesc is not None:
				if self.config.isRtl():
					Utilities.drawTextsOnRightX(self.screen, self.institutionDesc, (1693 ,self.institutionDescY), 30)
				else:
					Utilities.drawTextsOnLeftX(self.screen, self.institutionDesc, (1093 ,self.institutionDescY), 30)