import pygame
from pygame.locals import *
from pygame import mixer

import cv2
import numpy as np
import time

class VideoPlayer:
	def __init__(self, screen, filename, x, y, loop=False, soundFile=None):
		self.screen = screen
		self.video = cv2.VideoCapture(filename)
		self.fps = self.video.get(cv2.CAP_PROP_FPS)
		print("FPS: " + str(self.fps) + " ========")
		self.currTime = 0
		self.fps = 23
		self.singleFrameTime = 1 / self.fps

		self.isAudioPlaying = True
		if soundFile is not None:
			print('load sound file:', soundFile)
			mixer.music.load(soundFile)
			self.isAudioPlaying = False

		self.x = x
		self.y = y
		self.loop = loop

		ret, frame = self.video.read()
		self.processFrame(frame)

	def draw(self, dt):
		self.currTime += dt

		if not self.isAudioPlaying:
			print('playing!')
			mixer.music.play()
			self.isAudioPlaying = True

		if self.currTime < self.singleFrameTime:
			self.blitFrame(self.currFrame)
			return True
		else:
			self.currTime -= self.singleFrameTime
			ret, frame = self.video.read()
			if ret:
				self.processFrame(frame)
				self.blitFrame(frame)
			else:
				if self.loop:
					self.video.set(cv2.CAP_PROP_POS_FRAMES, 0)
					ret, frame = self.video.read()
					self.processFrame(frame)
					self.blitFrame(frame)

			return ret

	def processFrame(self, frame):
		frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
		frame = np.fliplr(frame)
		frame = np.rot90(frame)
		self.currFrame = pygame.surfarray.make_surface(frame)

	def blitFrame(self, frame):
		self.screen.blit(self.currFrame, (self.x, self.y))
