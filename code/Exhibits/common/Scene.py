import pygame
from pygame.locals import *

from functools import partial

from common.Button import Button
from common.LanguageButton import LanguageButton
from common.Log import Log

from pyfribidi import *

LANGUAGE_BUTTONS_X_PADDING = 100
LANGUAGE_BUTTONS_Y_PADDING = 100
LANGUAGE_BUTTONS_SIZE = 100

BACKGROUND_COLOR = [51, 51, 51]
LANGUAGE_TEXT_COLOR = [187, 187, 187]
LANGUAGE_SELECTED_TEXT_COLOR = [249, 207, 71]

BOTTOM_BAR_Y_OFFSET = 81

TIME_TO_RESET = 5 * 60

class Scene:
	def __init__(self, game, isSmallScreen=False):
		self.game = game
		self.screen = game.screen
		self.config = game.config
		self.isSmallScreen = isSmallScreen

		self.blitCursor = True

		self.logo = pygame.image.load('assets/images/logo-small.png' if self.isSmallScreen else 'assets/images/logo.png')
		self.bottomBar = pygame.image.load('assets/images/bottom-bar.png')
		self.bottomBarSeparator = pygame.image.load('assets/images/bottom-bar-separator.png')

		self.buttons = []
		self.languageButtons = []

		self.backgroundColor = BACKGROUND_COLOR

		self.loadFonts()
		self.createBottomBarButtons()
		self.clearResetTimer()

	def createBottomBarButtons(self):
		homeNormal = pygame.image.load('assets/images/button-home-normal.png')
		homeTapped = pygame.image.load('assets/images/button-home-tapped.png')
		self.buttons.append(Button(self.screen, pygame.Rect(0, self.screen.get_height() - BOTTOM_BAR_Y_OFFSET, homeNormal.get_width(), homeNormal.get_height()), 
			homeNormal, homeTapped, None, None, None, None, self.onHomeTapped))

		languagesNum = len(self.config.getLanguages())
		for i in range(languagesNum):
			languageData = self.config.getLanguages()[i]

			languageNormal = pygame.image.load('assets/images/language-button-normal.png')
			languageTapped = pygame.image.load('assets/images/language-button-tapped.png')
			languageSelected = pygame.image.load('assets/images/language-button-selected.png')
			font = pygame.font.Font(languageData['fonts']['textFont']['filename'], languageData['fonts']['textFont']['size'])
			
			languageButton = LanguageButton(self.screen, pygame.Rect(self.screen.get_width() - (languagesNum - i) * languageNormal.get_width(), self.screen.get_height() - BOTTOM_BAR_Y_OFFSET, 
				languageNormal.get_width(), languageNormal.get_height()), languageNormal, languageTapped, languageSelected, log2vis(languageData['buttonText']), 
				LANGUAGE_TEXT_COLOR, LANGUAGE_SELECTED_TEXT_COLOR, font, partial(self.onLanguageTapped, i))
			if languageData['prefix'] == self.config.languagePrefix:
				languageButton.visible = False

			self.buttons.append(languageButton)
			self.languageButtons.append(languageButton)

	def onHomeTapped(self):
		Log.info('HOME')
		self.clearResetTimer() # For the current scene if it should return
		self.game.gotoHome()

	def onLanguageTapped(self, index):
		lastLanguagePrefix = self.config.languagePrefix
		self.config.changeLanguage(index)
		Log.info('LANGUAGE', lastLanguagePrefix, self.config.languagePrefix)
		self.loadFonts()
		self.onLanguageChanged()
		self.clearResetTimer()

	def loadFonts(self):
		languageData = self.config.getLanguage()
		self.bigHeaderFont = pygame.font.Font(languageData['fonts']['bigHeaderFont']['filename'], languageData['fonts']['bigHeaderFont']['size'])
		self.headerFont = pygame.font.Font(languageData['fonts']['headerFont']['filename'], languageData['fonts']['headerFont']['size'])
		self.smallScreenHeaderFont = pygame.font.Font(languageData['fonts']['smallScreenHeaderFont']['filename'], languageData['fonts']['smallScreenHeaderFont']['size'])
		self.subHeaderFont = pygame.font.Font(languageData['fonts']['subHeaderFont']['filename'], languageData['fonts']['subHeaderFont']['size'])
		self.subSubHeaderFont = pygame.font.Font(languageData['fonts']['subSubHeaderFont']['filename'], languageData['fonts']['subSubHeaderFont']['size'])
		self.smallScreenSubSubHeaderFont = pygame.font.Font(languageData['fonts']['smallScreenSubSubHeaderFont']['filename'], languageData['fonts']['smallScreenSubSubHeaderFont']['size'])
		self.textFont = pygame.font.Font(languageData['fonts']['textFont']['filename'], languageData['fonts']['textFont']['size'])
		self.smallTextFont = pygame.font.Font(languageData['fonts']['smallTextFont']['filename'], languageData['fonts']['smallTextFont']['size'])
		self.smallerTextFont = pygame.font.Font(languageData['fonts']['smallerTextFont']['filename'], languageData['fonts']['smallerTextFont']['size'])
		self.almostExtraSmallTextFont = pygame.font.Font(languageData['fonts']['almostExtraSmallTextFont']['filename'], languageData['fonts']['almostExtraSmallTextFont']['size'])
		self.extraSmallTextFont = pygame.font.Font(languageData['fonts']['extraSmallTextFont']['filename'], languageData['fonts']['extraSmallTextFont']['size'])
		self.smallScreenExtraSmallTextFont = pygame.font.Font(languageData['fonts']['smallScreenExtraSmallTextFont']['filename'], languageData['fonts']['smallScreenExtraSmallTextFont']['size'])
		self.buttonFont = self.smallTextFont
		self.smallButtonTextFont = pygame.font.Font(languageData['fonts']['smallButtonTextFont']['filename'], languageData['fonts']['smallButtonTextFont']['size'])

	def onLanguageChanged(self):
		languages = self.config.getLanguages()
		for i in range(len(languages)):
			if i == self.config.languageIndex:
				self.languageButtons[i].visible = False
			else:
				self.languageButtons[i].visible = True

	def onMouseDown(self, pos):
		for button in self.buttons:
			button.onMouseDown(pos)

	def onMouseUp(self, pos):
		for button in self.buttons:
			button.onMouseUp(pos)

	def onMouseMove(self, pos):
		pass

	def clearResetTimer(self):
		self.timeToReset = TIME_TO_RESET

	def draw(self, dt):
		self.timeToReset -= dt
		if self.timeToReset <= 0:
			Log.info('TIME_RESET', str(TIME_TO_RESET))
			self.onHomeTapped()

		self.screen.blit(self.logo, (24, 24))

		# Draw bottom bar
		self.screen.blit(self.bottomBar, (0, self.screen.get_height() - 81))

		# Draw current language image

		for button in self.buttons:
			button.draw()

		# Draw bottom bar separator
		self.screen.blit(self.bottomBarSeparator, (0, self.screen.get_height() - 81))