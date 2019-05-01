import pygame
from pygame.locals import *

from Scene import Scene
from VideoPlayer import VideoPlayer

class VideoScene(Scene):
	def __init__(self, game, screen, filename, endScene):
		super().__init__(game, screen)
		self.endScene = endScene
		self.blitCursor = False
		self.video = VideoPlayer(self.screen, filename, 0, 0)

	def processEvent(self, event):
		pass

	def draw(self):
		if not self.video.draw():
			self.game.transition(self.endScene)