import pygame
from pygame.locals import *

from Scene import Scene
from Button import Button

NEURON_BUTTON_WIDTH = 200
NEURON_BUTTON_HEIGHT = 400
NEURON_BUTTON_PADDING = 50

START_CIRCLE_POS = (167, 380)
CIRCLE_RADIUS = 10

class DrawNeuronScene(Scene):
	def __init__(self, game, screen):
		super().__init__(game, screen)

		self.prototypeNeuron = pygame.image.load('assets/images/pyramidal_neuron_small.png')
		self.drawOnNeuron = pygame.image.load('assets/images/pyramidal_neuron_small.png')

		self.circlePos = START_CIRCLE_POS

	def processEvent(self, event):
		if event.type == MOUSEBUTTONDOWN:
			pass

	def draw(self):
		self.screen.blit(pygame.transform.scale(self.prototypeNeuron, (int(self.prototypeNeuron.get_width() * 0.8), int(self.prototypeNeuron.get_height() * 0.8))), (100, 100))
		self.screen.blit(self.drawOnNeuron, (self.screen.get_width() / 2 - self.drawOnNeuron.get_width() / 2, 100))
		circlePos = (int(self.screen.get_width() / 2 - self.drawOnNeuron.get_width() / 2 + self.circlePos[0]), int(100 + self.circlePos[1]))
		pygame.draw.circle(self.screen, (255,0,0), circlePos, CIRCLE_RADIUS)