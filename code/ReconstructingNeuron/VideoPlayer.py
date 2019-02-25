import pygame
from pygame.locals import *
import cv2
import numpy as np

class VideoPlayer:
	def __init__(self, screen, filename, x, y):
		self.screen = screen
		self.video = cv2.VideoCapture(filename)
		self.x = x
		self.y = y

	def draw(self):
		ret, frame = self.video.read()

		if ret:
			frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
			frame = np.fliplr(frame)
			frame = np.rot90(frame)
			frame = pygame.surfarray.make_surface(frame)
			self.screen.blit(frame, (self.x, self.y))
		else:
			self.video.release()

		return ret
