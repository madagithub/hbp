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
		
		self.scene = OpeningScene(self)

		self.drawingScenes = {}
		self.drawingScenes['martinotti'] = DrawNeuronScene(self, 'martinotti')
		self.drawingScenes['basket'] = DrawNeuronScene(self, 'basket')
		self.drawingScenes['pyramidal'] = DrawNeuronScene(self, 'pyramidal')

		self.loop()

	def gotoHome(self):
		self.scene = OpeningScene(self)

	def transition(self, transitionId, data=None):
		if transitionId == 'START':
			self.scene = VideoScene(self, 'assets/videos/neuron/brainzoom-short.mov', 'CHOOSE')
		elif transitionId == 'CHOOSE':
			self.scene = ChooseNeuronScene(self)
		elif transitionId == 'DRAW':
			self.scene = self.drawingScenes[data]
			self.scene.reset()
		elif transitionId == 'SUMMARY':
			self.scene = SummaryScene(self, data)

if __name__ == '__main__':
	Neuron().start()