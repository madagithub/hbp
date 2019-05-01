import pygame
from pygame.locals import *
import cv2
import numpy as np
import time

class VideoPlayer:
	def __init__(self, screen, filename, x, y):
		self.screen = screen
		self.video = cv2.VideoCapture(filename)
		self.x = x
		self.y = y

		self.frames = []
		ret, frame = self.video.read()
		framesNum = 0
		while ret:
			frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
			frame = np.fliplr(frame)
			frame = np.rot90(frame)
			frame = pygame.surfarray.make_surface(frame)
			self.frames.append(frame)
			ret, frame = self.video.read()
			framesNum = framesNum + 1

		self.framesNum = framesNum
		self.currFrameIndex = 0

	def draw(self):

		if self.currFrameIndex < self.framesNum:
			frame = self.frames[self.currFrameIndex]
			self.screen.blit(frame, (self.x, self.y))
			self.currFrameIndex = self.currFrameIndex + 1
		else:
			self.video.release()

		return self.currFrameIndex < self.framesNum
