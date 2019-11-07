import pygame
from pygame.locals import *
from pygame import mixer

import cv2
import numpy as np
import time

from queue import Queue
from threading import Thread

from common.Log import Log

QUEUE_MAX_SIZE = 25

class VideoPlayer:
	@staticmethod
	def preloadInitialFrames(filename):
		frames = []
		video = cv2.VideoCapture(filename)
		video.set(cv2.CAP_PROP_POS_FRAMES, 0)

		for i in range(QUEUE_MAX_SIZE // 2):
			(grabbed, frame) = video.read()
			frames.append(VideoPlayer.processFrame(frame))

		video.release()
		return frames

	@staticmethod
	def processFrame(frame):
		frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
		frame = np.fliplr(frame)
		frame = np.rot90(frame)
		return pygame.surfarray.make_surface(frame)

	def __init__(self, screen, filename, x, y, loop=False, soundFile=None, initialFrames=None, fps=None):
		self.screen = screen
		self.x = x
		self.y = y
		self.loop = loop
		self.initialFrames = initialFrames

		self.video = cv2.VideoCapture(filename)
		self.fps = fps if fps is not None else self.video.get(cv2.CAP_PROP_FPS)
		self.singleFrameTime = 1 / self.fps

		self.shouldPlayAudio = False
		if soundFile is not None:
			mixer.music.load(soundFile)
			self.shouldPlayAudio = True

		self.reset()

	def reset(self):
		self.currFrame = None
		self.videoStopped = False
		self.canFinish = False
		self.framesQueue = Queue(maxsize = QUEUE_MAX_SIZE)
		self.currTime = 0
		self.video.set(cv2.CAP_PROP_POS_FRAMES, 0)

		if self.initialFrames is not None:
			for frame in self.initialFrames:
				self.framesQueue.put(frame)
			self.video.set(cv2.CAP_PROP_POS_FRAMES, len(self.initialFrames))
		else:
			for i in range(QUEUE_MAX_SIZE):
				(grabbed, frame) = self.video.read()
				self.framesQueue.put(VideoPlayer.processFrame(frame))
	
	def stop(self):
		self.videoStopped = True
		mixer.music.stop()
		self.video.release()

	def draw(self, dt):
		if self.videoStopped:
			return True

		self.currTime += dt

		if self.currTime < self.singleFrameTime:
			if self.currFrame is not None:
				self.blitFrame(self.currFrame)
			return False
		else:
			frames = 0
			while self.currTime >= self.singleFrameTime:
				self.currTime -= self.singleFrameTime
				frames += 1
			if self.framesQueue.qsize() > 0:
				for i in range(frames):
					if self.framesQueue.qsize() > 0:
						self.currFrame = self.framesQueue.get()
				self.blitFrame(self.currFrame)
			elif self.canFinish:
				self.stop()
			
			return False

	def play(self):
		# Start a separate thread to read and process frames into a buffer, for performance
		self.readFramesThread = Thread(target=self.readFrames, args=())
		self.readFramesThread.daemon = True

		self.videoStopped = False
		self.readFramesThread.start()

		if self.shouldPlayAudio:
			mixer.music.play()

	def readFrames(self):
		while True:

			if self.canFinish:
				return

			if not self.framesQueue.full():
				(grabbed, frame) = self.video.read()
 
				if not grabbed:
					if self.loop:
						self.video.set(cv2.CAP_PROP_POS_FRAMES, 0)
					else:
						self.canFinish = True
				else:
					self.framesQueue.put(self.processFrame(frame))
			else:
				time.sleep(self.singleFrameTime / 2)

	def blitFrame(self, frame):
		self.screen.blit(frame, (self.x, self.y))
