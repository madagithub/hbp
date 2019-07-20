import pygame
from pygame.locals import *
from pygame import mixer

import cv2
import numpy as np
import time

from queue import Queue
from threading import Thread

class VideoPlayer:
	def __init__(self, screen, filename, x, y, loop=False, soundFile=None):
		self.screen = screen
		self.x = x
		self.y = y
		self.loop = loop

		self.video = cv2.VideoCapture(filename)
		self.fps = 23 #self.video.get(cv2.CAP_PROP_FPS)
		print("Loading video: " + filename)
		print("FPS: " + str(self.fps) + " ========")
		self.singleFrameTime = 1 / self.fps

		self.shouldPlayAudio = False
		if soundFile is not None:
			print('load sound file:', soundFile)
			mixer.music.load(soundFile)
			self.shouldPlayAudio = True

		self.reset()

	def reset(self):
		self.currFrame = None
		self.videoStopped = False
		self.canFinish = False
		self.framesQueue = Queue(maxsize = 200)
		self.currTime = 0
		self.video.set(cv2.CAP_PROP_POS_FRAMES, 0)
	
	def stop(self):
		self.videoStopped = True
		mixer.music.stop()

	def draw(self, dt):
		if self.videoStopped:
			return True

		self.currTime += dt

		if self.currTime < self.singleFrameTime:
			if self.currFrame is not None:
				self.blitFrame(self.currFrame)
			return False
		else:
			self.currTime -= self.singleFrameTime
			
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

			if self.videoStopped:
				return
 
			if not self.framesQueue.full():
				time.sleep(0.01)
				(grabbed, frame) = self.video.read()
 
				if not grabbed:
					if self.loop:
						self.video.set(cv2.CAP_PROP_POS_FRAMES, 0)
					else:
						self.canFinish = True
				else:
					self.framesQueue.put(self.processFrame(frame))

	def processFrame(self, frame):
		frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
		frame = np.fliplr(frame)
		frame = np.rot90(frame)
		return pygame.surfarray.make_surface(frame).convert()

	def blitFrame(self, frame):
		self.screen.blit(frame, (self.x, self.y))
