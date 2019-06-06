import pygame
from pygame.locals import *
import cv2
import time

from common.Exhibit import Exhibit
from common.VideoScene import VideoScene

from opening.OpeningScene import OpeningScene

class Opening(Exhibit):
	def __init__(self):
		super().__init__()

	def start(self):
		super().start()

		self.scene = OpeningScene(self)

		self.loop()

	def transition(self, transitionId, data=None):
		if transitionId == 'VIDEO':
			self.scene = VideoScene(self, data, 'START')
		elif transitionId == 'START':
			self.scene = OpeningScene(self)

if __name__ == '__main__':
	Opening().start()