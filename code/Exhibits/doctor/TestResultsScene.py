import pygame
from pygame.locals import *

from common.Scene import Scene
from common.Button import Button

from common.Utilities import Utilities

TEST_ID_TO_RESULT_KEYS = {
	'COGNITIVE': {'header': 'DFAM_TEST_RESULTS_HEADER_COGNITIVE', 'subHeader': 'DFAM_TEST_RESULTS_DESC_COGNITIVE'},
	'PET': {'header': 'DFAM_TEST_RESULTS_HEADER_PET', 'subHeader': 'DFAM_TEST_RESULTS_DESC_PET'},
	'MRI': {'header': 'DFAM_TEST_RESULTS_HEADER_MRI', 'subHeader': 'DFAM_TEST_RESULTS_DESC_MRI'}
}

TEST_ID_TO_RESULT_IMAGES = {
	'COGNITIVE': {'healthy': 'cognitive-healthy', 'ill': 'cognitive-ill'},
	'PET': {'healthy': 'pet-healthy', 'ill': 'pet-ill'},
	'MRI': {'healthy': 'mri-healthy', 'ill': 'mri-ill'}	
}

#			"DFAM_TEST_RESULTS_HEALTHY_HEADER": "Healthy patient",
#			"DFAM_TEST_RESULTS_RESULTS_HEADER": "Test result"

#TODO: Unite with neuron opening screen
class TestResultsScene(Scene):
	def __init__(self, game, test):
		super().__init__(game)
		self.test = test
		self.game.getChooseTestScene().onTestDone(self.test)

		self.testImage = pygame.image.load('assets/images/doctor/' + TEST_ID_TO_RESULT_IMAGES[self.test]['ill'] + '.png')
		self.healthyImage = pygame.image.load('assets/images/doctor/' + TEST_ID_TO_RESULT_IMAGES[self.test]['healthy'] + '.png')

		self.testCaptionBackground = pygame.image.load('assets/images/doctor/test-caption-background.png')

		self.moreTestsButton = Button(self.screen, pygame.Rect(self.screen.get_width() // 2 - 245 // 2, 869, 245, 78), 
			pygame.image.load('assets/images/button-empty.png'), pygame.image.load('assets/images/button-selected.png'), 
			self.config.getText("DFAM_TEST_RESULTS_MORE_TESTS_BUTTON_TEXT"), [0,0,0], [0,0,0], self.buttonFont, self.onMoreTestsClick)
		self.buttons.append(self.moreTestsButton)

		self.createTexts()

	def onMoreTestsClick(self):
		self.game.transition('CHOOSE')

	def onLanguageChanged(self):
		super().onLanguageChanged()
		self.createTexts()
		self.moreTestsButton.createText(self.config.getText("DFAM_TEST_RESULTS_MORE_TESTS_BUTTON_TEXT"), self.buttonFont)

	def createTexts(self):
		self.headerText = self.subHeaderFont.render(self.config.getText(TEST_ID_TO_RESULT_KEYS[self.test]['header']), True, (255, 255, 255))
		self.subHeaderTexts = Utilities.renderTextList(self.config, self.textFont, TEST_ID_TO_RESULT_KEYS[self.test]['subHeader'])

	def draw(self, dt):
		self.screen.blit(self.testImage, (531, 200))
		self.screen.blit(self.healthyImage, (1020, 200))
		self.screen.blit(self.testCaptionBackground, (531, 576))
		self.screen.blit(self.testCaptionBackground, (1020, 576))
		Utilities.drawTextOnCenterX(self.screen, self.headerText, (self.screen.get_width() // 2, 69))
		Utilities.drawTextsOnCenterX(self.screen, self.subHeaderTexts, (self.screen.get_width() // 2, 692), 40)
		super().draw(dt)