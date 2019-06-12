import pygame
from pygame.locals import *
import cv2
import time

from common.Exhibit import Exhibit
from common.VideoScene import VideoScene

from doctor.OpeningScene import OpeningScene
from doctor.ExplanationScene import ExplanationScene

class Doctor(Exhibit):
	def __init__(self):
		super().__init__()

	def start(self):
		super().start()
		
		#self.startVideoScene = VideoScene(self, 'assets/videos/brainzoom-short.mov', 'CHOOSE')
		self.scene = OpeningScene(self)

		self.loop()

	def gotoHome(self):
		self.scene = OpeningScene(self)

	def transition(self, transitionId, data=None):
		if transitionId == 'EXPLANATION':
			self.scene = ExplanationScene(self)
		elif transitionId == 'CHOOSE':
			pass
			#self.scene = self.startVideoScene

if __name__ == '__main__':
	Doctor().start()