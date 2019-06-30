import pygame
from pygame.locals import *

from common.Scene import Scene
from common.VideoPlayer import VideoPlayer

class VideoScene(Scene):
	def __init__(self, game, filename, endScene, soundFile=None):
		super().__init__(game)
		self.endScene = endScene
		self.blitCursor = False

		self.video = VideoPlayer(self.screen, filename, 0, 0, loop=False, soundFile=soundFile)
		self.video.play()

	def draw(self, dt):
		self.video.draw(dt)
		#self.game.transition(self.endScene)

	def reset(self):
		self.video.reset()