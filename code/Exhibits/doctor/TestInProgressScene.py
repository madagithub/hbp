import pygame
from pygame.locals import *

from common.Scene import Scene
from common.Button import Button

from common.Utilities import Utilities
from common.Timer import Timer
from common.FrameAnimation import FrameAnimation

TEST_ID_TO_KEYS = {
	'PET': {'header': 'DFAM_TEST_IN_PROGRESS_HEADER_PET', 'subHeader': 'DFAM_TEST_IN_PROGRESS_SUB_HEADER_PET'},
	'MRI': {'header': 'DFAM_TEST_IN_PROGRESS_HEADER_MRI', 'subHeader': 'DFAM_TEST_IN_PROGRESS_SUB_HEADER_MRI'}
}

class TestInProgressScene(Scene):
	def __init__(self, game, test):
		super().__init__(game)
		self.test = test
		self.timer = Timer(5.0, self.onTestDone)
		self.progressBarAnimation = FrameAnimation('assets/images/doctor/loading/yellow fading_line', 18, 25)

		self.createTexts()

	def onTestDone(self):
		self.game.transition('TEST_RESULTS', self.test)

	def onLanguageChanged(self):
		super().onLanguageChanged()
		self.createTexts()

	def createTexts(self):
		self.headerText = self.headerFont.render(self.config.getText(TEST_ID_TO_KEYS[self.test]['header']), True, (255, 255, 255))
		self.subHeaderTexts = Utilities.renderTextList(self.config, self.textFont, TEST_ID_TO_KEYS[self.test]['subHeader'])

	def draw(self, dt):
		self.timer.tick(dt)
		self.screen.blit(self.progressBarAnimation.getFrame(dt), (892, 572))
		Utilities.drawTextOnCenter(self.screen, self.headerText, (self.screen.get_width() // 2, 320))
		Utilities.drawTextsOnCenterX(self.screen, self.subHeaderTexts, (self.screen.get_width() // 2, 419), 40)
		super().draw(dt)