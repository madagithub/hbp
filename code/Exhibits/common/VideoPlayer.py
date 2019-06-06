import pygame
from pygame.locals import *
import cv2
import numpy as np
import time

class VideoPlayer:
	def __init__(self, screen, filename, x, y, loop=False):
		self.screen = screen
		self.video = cv2.VideoCapture(filename)
		self.x = x
		self.y = y
		self.loop = loop

	def draw(self):

		ret, frame = self.video.read()
		if ret:
			self.blitFrame(frame)
		else:
			if self.loop:
				self.video.set(cv2.CAP_PROP_POS_FRAMES, 0)
				ret, frame = self.video.read()
				self.blitFrame(frame)

		return ret

	def blitFrame(self, frame):
		frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
		frame = np.fliplr(frame)
		frame = np.rot90(frame)
		frame = pygame.surfarray.make_surface(frame)
		self.screen.blit(frame, (self.x, self.y))
