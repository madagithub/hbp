import pygame
from pygame.locals import *

from Scene import Scene
from Button import Button

from Utilities import Utilities

class OpeningScene(Scene):
	def __init__(self, game, screen):
		super().__init__(game, screen)

		self.headerText = self.font.render('Neuron Under Construction', True, (255, 255, 255))
		self.subHeaderText = self.font.render('You are invited to reconstruct your own neuron', True, (255, 255, 255))

		self.buttons.append(Button(screen, pygame.Rect(self.screen.get_width() / 2 - 300 / 2, self.screen.get_height() * 2 / 3, 300, 50), 'Start', self.font, self.onStartClick))

	def onStartClick(self):
		self.game.transition('START')		

	def draw(self):
		Utilities.drawTextOnCenter(self.screen, 'Neuron Under Construction', (self.screen.get_width() / 2, 353), self.font)
		Utilities.drawTextOnCenter(self.screen, 'You are invited to reconstruct your own neuron', (self.screen.get_width() / 2, 469), self.font)
		self.screen.blit(self.headerText, (self.screen.get_width() / 2 - self.headerText.get_width() / 2, 100))
		super().draw()