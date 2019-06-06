import pygame
from pygame.locals import *
import cv2
import time

from OpeningScene import OpeningScene
from VideoScene import VideoScene
from ChooseNeuronScene import ChooseNeuronScene
from DrawNeuronScene import DrawNeuronScene
from SummaryScene import SummaryScene
from Config import Config

from functools import partial

import os 
os.environ['SDL_VIDEO_CENTERED'] = '1'

CONFIG_FILENAME = 'assets/config/config.json'

from ft5406 import Touchscreen, TS_PRESS, TS_RELEASE, TS_MOVE

class Neuron:
	def __init__(self):
		self.playingVideos = []

	def start(self):
		self.config = Config(CONFIG_FILENAME)

		pygame.init()
		pygame.mouse.set_visible(False)

		self.screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)
		self.cursor = pygame.image.load('assets/images/cursor.png').convert_alpha()
		self.startVideoScene = VideoScene(self, 'assets/videos/brainzoom-short.mov', 'CHOOSE')

		self.scene = DrawNeuronScene(self, 'martinotti') #OpeningScene(self)

		if self.config.isTouch():
			self.ts = Touchscreen(self.config.getTouchDevice())

			for touch in self.ts.touches:
			    touch.on_press = self.onMouseDown
			    touch.on_release = self.onMouseUp
			    touch.on_move = self.onMouseMove

			self.ts.run()

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

	def onMouseDown(self, event, touch):
		self.scene.onMouseDown((touch.x * 1920 / 4095, touch.y * 1080 / 4095))

	def onMouseUp(self, event, touch):
		self.scene.onMouseUp((touch.x * 1920 / 4095, touch.y * 1080 / 4095))

	def onMouseMove(self, event, touch):
		self.scene.onMouseMove((touch.x * 1920 / 4095, touch.y * 1080 / 4095))

	def loop(self):
		isGameRunning = True
		clock = pygame.time.Clock()
		lastTime = pygame.time.get_ticks()

		while isGameRunning:

			for event in pygame.event.get():
				if event.type == MOUSEBUTTONDOWN:
					if not self.config.isTouch():
						self.scene.onMouseDown(event.pos)
				elif event.type == MOUSEBUTTONUP:
					if not self.config.isTouch():
						self.scene.onMouseUp(event.pos)
				elif event.type == MOUSEMOTION:
					if not self.config.isTouch():
						self.scene.onMouseMove(event.pos)
				elif event.type == KEYDOWN:
					if event.key == K_ESCAPE:
						isGameRunning = False

			self.screen.fill(self.scene.backgroundColor)
			currTime = pygame.time.get_ticks()
			dt = currTime - lastTime
			lastTime = currTime
			self.scene.draw(dt / 1000)
			if not self.config.isTouch() and self.scene.blitCursor:
				self.screen.blit(self.cursor, (pygame.mouse.get_pos()))

			pygame.display.flip()
			clock.tick(30)

		pygame.quit()
		cv2.destroyAllWindows()

		if self.config.isTouch():
			self.ts.stop()


if __name__ == '__main__':
	Neuron().start()