import pygame
from pygame.locals import *

from functools import partial

from common.Scene import Scene
from common.Button import Button
from common.Timer import Timer

from common.Utilities import Utilities

START_BUTTON_TEXT_COLOR = [0, 0, 0]

class OpeningScene(Scene):
	def __init__(self, game):
		super().__init__(game)

		self.videosTexts = []
		self.videos = self.config.getOpeningVideos()
		index = 0
		for video in self.videos:
			image = pygame.image.load('assets/images/opening/' + video['image'] + '.png')
			tappedImage = pygame.image.load('assets/images/opening/' + video['tappedImage'] + '.png')

			callbackFunc = None
			if video['type'] == 'VIDEO':
				callbackFunc = partial(self.onVideoClick, video['file'], video.get('soundFile', None), True)
			elif video['type'] == 'MAP':
				callbackFunc = self.onMapClick
			elif video['type'] == 'ABOUT':
				callbackFunc = self.onAboutClick
			elif video['type'] == 'CREDITS':
				callbackFunc = self.onCreditsClick

			self.videoButton = Button(self.screen, pygame.Rect(video['x'], video['y'], image.get_width(), image.get_height()),
				image, tappedImage, None, None, None, None,
				callbackFunc)
			index += 1
			self.buttons.append(self.videoButton)

			textBoxes = Utilities.renderTextList(self.config, self.subHeaderFont, video['textKey'], (0, 0, 0))
			self.videosTexts.append(textBoxes)

		self.textBackground = pygame.image.load('assets/images/opening/text-background.png')
		self.currTextIndex = 0

		self.createTexts()

		self.textsTimer = Timer(3, self.onShowNextText)

	def onShowNextText(self):
		self.currTextIndex = (self.currTextIndex + 1) % len(self.videos)
		self.textsTimer = Timer(3, self.onShowNextText)

	def onMapClick(self):
		self.game.transition('MAP')

	def onAboutClick(self):
		pass

	def onCreditsClick(self):
		pass

	def onVideoClick(self, file, soundFile, hasBack):
		self.game.transition('VIDEO', {'file': file[self.config.languagePrefix], 'soundFile': soundFile, 'hasBack': hasBack})

	def onLanguageChanged(self):
		super().onLanguageChanged()
		self.createTexts()

	def createTexts(self):
		pass

	def draw(self, dt):
		self.textsTimer.tick(dt)

		super().draw(dt)

		video = self.videos[self.currTextIndex]
		self.screen.blit(self.textBackground, (video['x'], video['y']))
		Utilities.drawTextsOnCenter(self.screen, self.videosTexts[self.currTextIndex], (video['x'] + 480 // 2, video['y'] + 500 // 2), 50)