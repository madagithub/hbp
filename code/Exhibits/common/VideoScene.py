import pygame
from pygame.locals import *

from common.Scene import Scene
from common.VideoPlayer import VideoPlayer
from common.Button import Button

class VideoScene(Scene):
	def __init__(self, game, filename, endScene, soundFile=None, hasBack=False):
		super().__init__(game)
		self.endScene = endScene
		self.blitCursor = False

		self.hasBack = hasBack
		if hasBack:
			image = pygame.image.load('assets/images/back-normal.png')
			tappedImage = pygame.image.load('assets/images/back-selected.png')
			self.backButton = Button(self.screen, pygame.Rect(1920 - image.get_width() - 1846, 1000, image.get_width(), image.get_height()),
				image, tappedImage, None, None, None, None,
				self.onBack)

		self.video = VideoPlayer(self.screen, filename, 0, 0, loop=False, soundFile=soundFile)
		self.video.play()

	def onBack(self):
		self.game.transition(self.endScene)

	def onMouseDown(self, pos):
		if self.hasBack:
			self.backButton.onMouseDown(pos)

	def onMouseUp(self, pos):
		if self.hasBack:
			self.backButton.onMouseUp(pos)

	def draw(self, dt):
		if self.video.draw(dt):
			self.game.transition(self.endScene)

		if self.hasBack:
			self.backButton.draw()

	def reset(self):
		self.video.reset()