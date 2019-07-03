import pygame
from pygame.locals import *

import cv2
import time

from common.Exhibit import Exhibit
from common.VideoScene import VideoScene

from opening.OpeningScene import OpeningScene
from opening.MapScene import MapScene
from opening.CountryScene import CountryScene

class Opening(Exhibit):
	def __init__(self):
		super().__init__()

	def start(self):
		super().start()

		self.scene = OpeningScene(self)

		self.loop()

	def gotoHome(self):
		self.scene = OpeningScene(self)

	def transition(self, transitionId, data=None):
		if transitionId == 'VIDEO':
			self.scene = VideoScene(self, data['file'], 'START', data['soundFile'])
		elif transitionId == 'START':
			self.scene = OpeningScene(self)
		elif transitionId == 'MAP':
			self.scene = MapScene(self)
		elif transitionId == 'COUNTRY':
			self.scene = CountryScene(self, data)

if __name__ == '__main__':
	Opening().start()