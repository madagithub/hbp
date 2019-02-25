import pygame
from pygame.locals import *
import cv2

from VideoPlayer import VideoPlayer

class Neuron:
	def __init__(self):
		self.playingVideos = []
		pass

	def start(self):
		pygame.init()
		self.screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)

		self.neuronVideo = VideoPlayer(self.screen, 'assets/videos/brainzoom.mov', 0, 0)
		self.playingVideos.append(self.neuronVideo)

		self.loop()

	def loop(self):
		isGameRunning = True

		while isGameRunning:

			self.screen.fill([0,0,0])

			self.playVideos();
			pygame.display.flip()

			for event in pygame.event.get():
				if event.type == KEYDOWN:
					isGameRunning = False

		pygame.quit()
		cv2.destroyAllWindows()

	def playVideos(self):
		self.playingVideos[:] = [video for video in self.playingVideos if video.draw()]


if __name__ == '__main__':
	Neuron().start()