import pygame
from pygame.locals import *
import cv2
import time
import sys

from common.Exhibit import Exhibit
from common.VideoScene import VideoScene

from doctor.OpeningScene import OpeningScene
from doctor.ExplanationScene import ExplanationScene
from doctor.ChooseTestScene import ChooseTestScene
from doctor.TestInProgressScene import TestInProgressScene
from doctor.TestResultsScene import TestResultsScene
from doctor.EvaluateScene import EvaluateScene
from doctor.LearnMoreScene import LearnMoreScene

EXTRA_CONFIG_FILENAME = 'assets/config/config-doctor.json'
EXTRA_CONFIG_MOUSE_FILENAME = 'assets/config/config-doctor-mouse.json'

class Doctor(Exhibit):
	def __init__(self):
		super().__init__()
		self.isHealthy = True

	def start(self, extraConfigFilename):
		super().start(extraConfigFilename)

		for command in self.config.getInitSerialPortCommands():
			self.sendToSerialPort(command)
			time.sleep(1)

		self.chooseTestScene = ChooseTestScene(self, self.isHealthy)
		self.scene = OpeningScene(self)

		self.loop()

	def gotoHome(self):
		self.chooseTestScene = ChooseTestScene(self, self.isHealthy)
		self.scene = OpeningScene(self)

	def getChooseTestScene(self):
		return self.chooseTestScene

	def transition(self, transitionId, data=None):
		if transitionId == 'EXPLANATION':
			self.scene = ExplanationScene(self)
		elif transitionId == 'OPENING_VIDEO':
			self.scene = VideoScene(self, 'assets/videos/doctor/patient-entering.mp4', 'EXPLANATION')
		elif transitionId == 'CHOOSE':
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