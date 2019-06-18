import pygame
from pygame.locals import *

from common.Scene import Scene
from common.Button import Button

from common.Utilities import Utilities
from common.Timer import Timer
from common.FrameAnimation import FrameAnimation
from common.VideoPlayer import VideoPlayer

TEST_ID_TO_KEYS = {
	'PET': {'header': 'DFAM_TEST_IN_PROGRESS_HEADER_PET', 'subHeader': 'DFAM_TEST_IN_PROGRESS_SUB_HEADER_PET'},
	'MRI': {'header': 'DFAM_TEST_IN_PROGRESS_HEADER_MRI', 'subHeader': 'DFAM_TEST_IN_PROGRESS_SUB_HEADER_MRI'},
	'COGNITIVE': {'header': 'DFAM_TEST_IN_PROGRESS_HEADER_COGNITIVE'}
}

class TestInProgressScene(Scene):
	def __init__(self, game, testProperties):
		super().__init__(game)
		self.testProperties = testProperties
		self.test = testProperties['test']

		if self.test != 'COGNITIVE':
			self.timer = Timer(5.0, self.onTestDone)
			self.progressBarAnimation = FrameAnimation('assets/images/doctor/loading/loading_', 18, 25)
		else:
			self.cognitiveVideo = VideoPlayer(self.screen, 
				'assets/videos/doctor/cognitive-test-healthy.mp4' if self.testProperties['isHealthy'] else 'assets/videos/doctor/cognitive-test-not-healthy.mp4', 
				386, 207, loop=False)

		self.createTexts()

	def onTestDone(self):
		self.game.transition('TEST_RESULTS', self.testProperties)

	def onLanguageChanged(self):
		super().onLanguageChanged()
		self.createTexts()

	def createTexts(self):
		self.headerText = self.headerFont.render(self.config.getText(TEST_ID_TO_KEYS[self.test]['header']), True, (255, 255, 255))
		if self.test != 'COGNITIVE':
			self.subHeaderTexts = Utilities.renderTextList(self.config, self.smallTextFont, TEST_ID_TO_KEYS[self.test]['subHeader'])

	def draw(self, dt):
		Utilities.drawTextOnCenter(self.screen, self.headerText, (self.screen.get_width() // 2, 320 if self.test != 'COGNITIVE' else 58))

		if self.test != 'COGNITIVE':
			self.timer.tick(dt)
			self.screen.blit(self.progressBarAnimation.getFrame(dt), (892, 572))
			Utilities.drawTextsOnCenterX(self.screen, self.subHeaderTexts, (self.screen.get_width() // 2, 419), 40)
		else:
			if not self.cognitiveVideo.draw(dt):
				self.onTestDone()

		super().draw(dt)