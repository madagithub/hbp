import pygame
from pygame.locals import *
import cv2
import time
import sys
import glob

from common.Exhibit import Exhibit
from common.VideoScene import VideoScene
from common.Log import Log
from common.VideoPlayer import VideoPlayer

from doctor.OpeningScene import OpeningScene
from doctor.ExplanationScene import ExplanationScene
from doctor.ChooseTestScene import ChooseTestScene
from doctor.TestInProgressScene import TestInProgressScene
from doctor.TestResultsScene import TestResultsScene
from doctor.EvaluateScene import EvaluateScene
from doctor.LearnMoreScene import LearnMoreScene

EXTRA_CONFIG_FILENAME = 'assets/config/config-doctor.json'
EXTRA_CONFIG_MOUSE_FILENAME = 'assets/config/config-doctor-mouse.json'
LOG_FILE_PATH = 'doctor.log'

class Doctor(Exhibit):
	def __init__(self):
		Log.init(LOG_FILE_PATH)
		Log.info('INIT')

		super().__init__()
		self.isHealthy = False

	def start(self, extraConfigFilename):
		super().start(extraConfigFilename)

		for command in self.config.getInitSerialPortCommands():
			self.sendToSerialPort(command)
			time.sleep(1)

		Log.info('PRELOAD_START')
		self.preloadVideos()
		Log.info('PRELOAD_DONE')

		self.chooseTestScene = ChooseTestScene(self, self.isHealthy)
		self.scene = OpeningScene(self)

		self.loop()

	def preloadVideos(self):
		self.initialVideoFrames = {}

		videoFilenames = [f for f in glob.glob('assets/videos/doctor/*.mp4', recursive=False)]

		for filename in videoFilenames:
			Log.info('PRELOADING_VIDEO_START,' + filename)
			self.initialVideoFrames[filename] = VideoPlayer.preloadInitialFrames(filename)
			Log.info('PRELOADING_VIDEO_DONE,' + filename)

	def gotoHome(self):
		self.chooseTestScene = ChooseTestScene(self, self.isHealthy)
		self.scene = OpeningScene(self)

	def getChooseTestScene(self):
		return self.chooseTestScene

	def transition(self, transitionId, data=None):
		if transitionId == 'EXPLANATION':
			self.scene = ExplanationScene(self)
		elif transitionId == 'OPENING_VIDEO':
			videoFilename = 'assets/videos/doctor/patient-entering.mp4'
			self.scene = VideoScene(self, videoFilename, 'EXPLANATION', initialFrames=self.initialVideoFrames[videoFilename])
		elif transitionId == 'CHOOSE':
			self.chooseTestScene.onLanguageTapped(self.config.languageIndex)
			self.scene = self.chooseTestScene
		elif transitionId == 'RUN_TEST':
			self.scene = TestInProgressScene(self, data)
		elif transitionId == 'TEST_RESULTS':
			self.scene = TestResultsScene(self, data)
		elif transitionId == 'EVALUATE':
			self.scene = EvaluateScene(self, data)
		elif transitionId == 'LEARN_MORE':
			self.scene = LearnMoreScene(self, data)
		elif transitionId == 'RESET':
			self.isHealthy = not self.isHealthy
			self.chooseTestScene = ChooseTestScene(self, self.isHealthy)
			self.scene = OpeningScene(self)

if __name__ == '__main__':
	Doctor().start(EXTRA_CONFIG_MOUSE_FILENAME if len(sys.argv) == 2 and sys.argv[1] == '--mouse' else EXTRA_CONFIG_FILENAME)