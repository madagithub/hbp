import pygame
from pygame.locals import *
import cv2
import time

from common.Exhibit import Exhibit
from common.VideoScene import VideoScene

from neuron.OpeningScene import OpeningScene
from neuron.ChooseNeuronScene import ChooseNeuronScene
from neuron.DrawNeuronScene import DrawNeuronScene
from neuron.SummaryScene import SummaryScene

class Neuron(Exhibit):
	def __init__(self):
		super().__init__()

	def start(self):
		super().start()
		
		self.startVideoScene = VideoScene(self, 'assets/videos/brainzoom-short.mov', 'CHOOSE')
		self.scene = DrawNeuronScene(self, 'martinotti') # OpeningScene(self)

		self.loop()

	def gotoHome(self):
		self.scene = OpeningScene(self)

	def transition(self, transitionId, data=None):
		if transitionId == 'START':
			self.scene = self.startVideoScene
		elif transitionId == 'CHOOSE':
			self.scene = ChooseNeuronScene(self)
		elif transitionId == 'DRAW':
			self.scene = DrawNeuronScene(self, data)
		elif transitionId == 'SUMMARY':
			self.scene = SummaryScene(self, data)

if __name__ == '__main__':
	Neuron().start()