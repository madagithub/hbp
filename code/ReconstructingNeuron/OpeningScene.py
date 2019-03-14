import pygame
from pygame.locals import *

from Scene import Scene

class OpeningScene(Scene):
	def __init__(self, game, screen):
		super().__init__(game, screen)

		font = pygame.font.SysFont(None, 48)
		self.headerText = font.render('Reconstructing Neuron', True, (255, 255, 255))

		self.startButton = pygame.Rect(self.screen.get_width() / 2 - 300 / 2, self.screen.get_height() * 2 / 3, 300, 50)

	def processEvent(self, event):
		if event.type == MOUSEBUTTONDOWN:
			if self.startButton.collidepoint(event.pos):
				self.game.transition('START')

	def draw(self):
		pygame.draw.rect(self.screen, [255, 0, 0], self.startButton)
		self.screen.blit(self.headerText, (self.screen.get_width() / 2 - self.headerText.get_width() / 2, 100))