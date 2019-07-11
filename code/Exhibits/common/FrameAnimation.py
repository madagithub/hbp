import pygame
from pygame.locals import *

class FrameAnimation:
	def __init__(self, filePrefix, framesNum, fps):
		self.frames = []
		for i in range(framesNum):
			self.frames.append(pygame.image.load(filePrefix + str(i + 1) + '.png').convert_alpha())

		self.timeUntilNextFrame = 1 / fps
		self.currTime = 0
		self.currFrameIndex = 0

	def getFrame(self, dt):
		self.currTime += dt
		if self.currTime > self.timeUntilNextFrame:
			self.currFrameIndex = (self.currFrameIndex + 1) % len(self.frames)
			self.currTime -= self.timeUntilNextFrame

		return self.frames[self.currFrameIndex]