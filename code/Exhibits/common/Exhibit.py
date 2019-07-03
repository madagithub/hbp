import pygame
from pygame.locals import *

import cv2
import time
import serial

from common.Config import Config
from common.VideoScene import VideoScene

import os 
os.environ['SDL_VIDEO_CENTERED'] = '1'

CONFIG_FILENAME = 'assets/config/config.json'

from ft5406 import Touchscreen, TS_PRESS, TS_RELEASE, TS_MOVE

class Exhibit:
	def __init__(self):
		self.playingVideos = []

	def start(self):
		self.config = Config(CONFIG_FILENAME)

		self.serialPort = None
		self.openSerialPort()
		time.sleep(3)	

		self.touchScreenBounds = (self.config.getTouchScreenMaxX(), self.config.getTouchScreenMaxY())

		pygame.mixer.pre_init(44100, -16, 1, 512)
		pygame.init()
		pygame.mouse.set_visible(False)

		self.screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)
		self.cursor = pygame.image.load('assets/images/cursor.png').convert_alpha()

		if self.config.isTouch():
			print("Loading touch screen...")
			self.ts = Touchscreen(self.config.getTouchDevice())

			for touch in self.ts.touches:
			    touch.on_press = self.onMouseDown
			    touch.on_release = self.onMouseUp
			    touch.on_move = self.onMouseMove

			self.ts.run()

	def openSerialPort(self):
		if self.config.shouldOpenSerial():
			if self.serialPort is None:
				try:
					self.serialPort = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
				except Exception as e:
					print(str(e))
					self.serialPort = None

	# Try to send to serial, and if an error occurs, open serial port again for X retries
	def sendToSerialPort(self, originalCommand):
		print("Attempting sending " + str(originalCommand) + "...")
		command = originalCommand + b'\n'
		commandSent = False

		if self.config.shouldOpenSerial():
			retriesNum = 0

			self.openSerialPort()

			if self.serialPort is None:
				print("Failed to open serial port, returning...")
				return False

			while (not commandSent):
				try:
					self.serialPort.write(command)
					print("Send Successful!")
					commandSent = True
				except Exception as e:
					print(str(e))
					if retriesNum == 1:
						print("Failed to write on retrying, returning...")
						break

					try:
						self.serialPort = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
						retriesNum += 1
					except Exception as e:
						print(str(e))
						self.serialPort = None
						print("Failed to open serial port, returning...")
						break

		return commandSent

	def gotoHome(self):
		self.scene = OpeningScene(self)

	def transition(self, transitionId, data=None):
		pass

	def onMouseDown(self, event, touch):
		print("Down event!", touch.x, touch.y)
		try:
			self.scene.onMouseDown((int(touch.x * 1920 / self.touchScreenBounds[0]), int(touch.y * 1080 / self.touchScreenBounds[1])))
		except Exception as e:
			print(str(e))

	def onMouseUp(self, event, touch):
		print("Up event!", touch.x, touch.y)
		try:
			self.scene.onMouseUp((int(touch.x * 1920 / self.touchScreenBounds[0]), int(touch.y * 1080 / self.touchScreenBounds[1])))
		except Exception as e:
			print(str(e))

	def onMouseMove(self, event, touch):
		print("Move event!", touch.x, touch.y)
		try:
			self.scene.onMouseMove((int(touch.x * 1920 / self.touchScreenBounds[0]), int(touch.y * 1080 / self.touchScreenBounds[1])))
		except Exception as e:
			print(str(e))

	def loop(self):
		isGameRunning = True
		clock = pygame.time.Clock()
		lastTime = pygame.time.get_ticks()

		while isGameRunning:

			#ry:
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
				clock.tick(60)
			#except Exception as e:
			#	print(str(e))

		pygame.quit()
		cv2.destroyAllWindows()

		if self.config.isTouch():
			self.ts.stop()
