import pygame
from pygame.locals import *
import cv2
import time

from OpeningScene import OpeningScene
from VideoScene import VideoScene
from ChooseNueronScene import ChooseNueronScene

class Neuron:
	def __init__(self):
		self.playingVideos = []

	def start(self):
		pygame.init()
		pygame.mouse.set_visible(False)
		self.screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)
		self.cursor = pygame.image.load('assets/images/cursor.png').convert_alpha()
		self.startVideoScene = VideoScene(self, self.screen, 'assets/videos/brainzoom-short.mov', 'CHOOSE')

		self.scene = OpeningScene(self, self.screen)

		self.loop()

	def transition(self, transitionId):
		if transitionId == 'START':
			self.scene = self.startVideoScene
		elif transitionId == 'CHOOSE':
			self.scene = ChooseNueronScene(self, self.screen)

	def loop(self):
		isGameRunning = True
		clock = pygame.time.Clock()

		while isGameRunning:

			start = time.time()

			for event in pygame.event.get():
				self.scene.processEvent(event)
				if event.type == KEYDOWN:
					isGameRunning = False

			self.screen.fill([0,0,0])
			self.scene.draw()
			self.screen.blit(self.cursor, (pygame.mouse.get_pos()))

			pygame.display.flip()

			end = time.time()

			clock.tick(30)

			end2 = time.time()

			#print("TIME 1: " + str(end - start))
			#print("TIME 2: " + str(end2 - start))

		pygame.quit()
		cv2.destroyAllWindows()


if __name__ == '__main__':
	Neuron().start()