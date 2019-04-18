import pygame
from pygame.locals import *

from Scene import Scene
from Button import Button

class OpeningScene(Scene):
	def __init__(self, game, screen):
		super().__init__(game, screen)

		font = pygame.font.SysFont(None, 48)
		self.headerText = font.render('Reconstructing Neuron', True, (255, 255, 255))

		self.startButton = Button(screen, pygame.Rect(self.screen.get_width() / 2 - 300 / 2, self.screen.get_height() * 2 / 3, 300, 50), 'Start', font, self.onStartClick)

	def processEvent(self, event):
		if event.type == MOUSEBUTTONDOWN:
			self.startButton.onClick(event.pos)

	def onStartClick(self):
		self.game.transition('START')		

	def draw(self):
		self.screen.blit(self.headerText, (self.screen.get_width() / 2 - self.headerText.get_width() / 2, 100))
		self.startButton.draw()