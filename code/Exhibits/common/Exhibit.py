import pygame
from pygame.locals import *

import cv2
import time
import serial

import platform

if platform.system() == 'Linux':
	import evdev
	from evdev import InputDevice, categorize, ecodes

from common.Config import Config
from common.VideoScene import VideoScene
from common.TouchScreen import TouchScreen

from threading import Thread

import os 
os.environ['SDL_VIDEO_CENTERED'] = '1'

CONFIG_FILENAME = 'assets/config/config.json'

class Exhibit:
	def __init__(self):
		self.playingVideos = []

	def start(self, extraConfigFilename):
		self.config = Config(CONFIG_FILENAME, extraConfigFilename)

		self.serialPort = None
		self.openSerialPort()
		time.sleep(3)

		pygame.mixer.pre_init(44100, -16, 1, 512)
		pygame.init()
		pygame.mouse.set_visible(False)

		infoObject = pygame.display.Info()
		screenSize = (infoObject.current_w, infoObject.current_h)

		if self.config.getScreenWidth() is not None and self.config.getScreenHeight() is not None:
			screenSize = (self.config.getScreenWidth(), self.config.getScreenHeight())			

		self.screen = pygame.display.set_mode(screenSize, pygame.FULLSCREEN)
		self.cursor = pygame.image.load('assets/images/cursor.png').convert_alpha()

		if self.config.isTouch() and platform.system() == 'Linux':
			self.touchScreen = TouchScreen(self.config.getTouchDevicePartialName(), (self.config.getTouchScreenMaxX(), self.config.getTouchScreenMaxY()). screenSize)

			if not self.touchScreen.setup():
				self.config.setTouch(False)

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

			if self.config.isTouch() and platform.system() == 'Linux':
				event = self.touchScreen.readUpDownEvent()
				while event is not None:
					if event['type'] == TouchScreen.DOWN_EVENT:
						self.scene.onMouseDown(event['pos'])
					elif event['type'] == TouchScreen.UP_EVENT:
						self.scene.onMouseUp(event['pos'])
					event = self.touchScreen.readUpDownEvent()

				pos = self.touchScreen.getPosition()
				self.scene.onMouseMove(pos)				

			self.screen.fill(self.scene.backgroundColor)
			currTime = pygame.time.get_ticks()
			dt = currTime - lastTime
			lastTime = currTime
			self.scene.draw(dt / 1000)

			if not self.config.isTouch() and self.scene.blitCursor:
				self.screen.blit(self.cursor, (pygame.mouse.get_pos()))

			pygame.display.flip()
			clock.tick(60)

		pygame.quit()
		cv2.destroyAllWindows()
