import pygame
from pygame.locals import *

from Scene import Scene
from Button import Button

NEURON_BUTTON_WIDTH = 200
NEURON_BUTTON_HEIGHT = 400
NEURON_BUTTON_PADDING = 50

class ChooseNeuronScene(Scene):
	def __init__(self, game, screen):
		super().__init__(game, screen)

		currX = self.screen.get_width() / 2 - NEURON_BUTTON_WIDTH * 3 / 2 - NEURON_BUTTON_PADDING
		for i in range(0, 3):
			self.buttons.append(Button(screen, pygame.Rect(currX, self.screen.get_height() / 2 - NEURON_BUTTON_HEIGHT / 2, NEURON_BUTTON_WIDTH, NEURON_BUTTON_HEIGHT), 'Neuron ' + str(i + 1), self.font, self.onNueronClick))
			currX += NEURON_BUTTON_PADDING + NEURON_BUTTON_WIDTH

		self.headerText = self.font.render('Choose a Neuron', True, (255, 255, 255))

	def onNueronClick(self):
		self.game.transition('DRAW')

	def draw(self):
		self.screen.blit(self.headerText, (self.screen.get_width() / 2 - self.headerText.get_width() / 2, 100))
		super().draw()