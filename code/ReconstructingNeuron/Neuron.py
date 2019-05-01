import pygame
from pygame.locals import *
import cv2

from OpeningScene import OpeningScene
from VideoScene import VideoScene
from ChooseNeuronScene import ChooseNeuronScene
from DrawNeuronScene import DrawNeuronScene

class Neuron:
	def __init__(self):
		self.playingVideos = []
		pass

	def start(self):
		pygame.init()
		self.screen = pygame.display.set_mode((1280, 800), pygame.FULLSCREEN)

		self.scene = OpeningScene(self, self.screen)

		self.loop()

	def transition(self, transitionId):
		if transitionId == 'START':
			self.scene = VideoScene(self, self.screen, 'assets/videos/brainzoom.mov', 'CHOOSE')
		elif transitionId == 'CHOOSE':
			self.scene = ChooseNeuronScene(self, self.screen)

	def loop(self):
		isGameRunning = True
		clock = pygame.time.Clock()

		while isGameRunning:

			for event in pygame.event.get():
				self.scene.processEvent(event)
				if event.type == KEYDOWN:
					isGameRunning = False

			self.screen.fill([0,0,0])
			self.scene.draw()

			pygame.display.flip()
			clock.tick(60)

		pygame.quit()
		cv2.destroyAllWindows()


if __name__ == '__main__':
	Neuron().start()