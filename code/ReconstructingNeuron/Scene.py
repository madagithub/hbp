import pygame
from pygame.locals import *

LANGUAGE_BUTTONS_X_PADDING = 100
LANGUAGE_BUTTONS_Y_PADDING = 100
LANGUAGE_BUTTONS_SIZE = 100

class Scene:
	def __init__(self, game, screen):
		self.game = game
		self.screen = screen
		self.font = pygame.font.SysFont(None, 48)
		self.blitCursor = True

		self.logo = pygame.image.load('assets/images/logo.png')

		self.buttons = []
		self.createStandardButtons()

	def processEvent(self, event):
		if event.type == MOUSEBUTTONDOWN:
			for button in self.buttons:
				button.onMouseDown(event.pos)
		elif event.type == MOUSEBUTTONUP:
			for button in self.buttons:
				button.onMouseUp(event.pos)

	def draw(self):
		self.screen.blit(self.logo, (23, 17))

		# Draw bottom bar
		self.screen.line(self.screen, [28, 28, 28], (999, 0), (999, 1920))

		for button in self.buttons:
			button.draw()

	def createStandardButtons(self):
		pass
		#self.buttons.append(Button(self.screen, pygame.Rect(self.screen.get_width() - LANGUAGE_BUTTONS_X_PADDING - LANGUAGE_BUTTONS_SIZE, self.screen.get_height() - LANGUAGE_BUTTONS_Y_PADDING - LANGUAGE_BUTTONS_SIZE, LANGUAGE_BUTTONS_SIZE, LANGUAGE_BUTTONS_SIZE), 'En', self.font, self.onLanguageClicked.bind(ENGLISH))