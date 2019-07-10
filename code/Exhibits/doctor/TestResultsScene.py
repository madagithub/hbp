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
	'COGNITIVE': {'healthy': 'cognitive-healthy', 'not-healthy': 'cognitive-not-healthy', 'ideal-healthy': 'cognitive-ideal-healthy'},
	'PET': {'healthy': 'pet-healthy', 'not-healthy': 'pet-not-healthy', 'ideal-healthy': 'pet-ideal-healthy'},
	'MRI': {'healthy': 'mri-healthy', 'not-healthy': 'mri-not-healthy', 'ideal-healthy': 'mri-ideal-healthy'}	
}

class TestResultsScene(Scene):
	def __init__(self, game, testProperties):
		super().__init__(game)
		self.test = testProperties['test']
		self.game.getChooseTestScene().onTestDone(self.test)

		self.testImage = pygame.image.load('assets/images/doctor/' + TEST_ID_TO_RESULT_IMAGES[self.test]['healthy' if testProperties['isHealthy'] else 'not-healthy'] + '.png')
		self.healthyImage = pygame.image.load('assets/images/doctor/' + TEST_ID_TO_RESULT_IMAGES[self.test]['ideal-healthy'] + '.png')

		image = pygame.image.load('assets/images/button-empty.png')
		selectedImage = pygame.image.load('assets/images/button-selected.png')
		self.moreTestsButton = Button(self.screen, pygame.Rect(self.screen.get_width() // 2 - image.get_width() // 2, 599, image.get_width(), image.get_height()), 
			image, selectedImage, 
			self.config.getText("DFAM_TEST_RESULTS_MORE_TESTS_BUTTON_TEXT"), [0,0,0], [0,0,0], self.extraSmallTextFont, self.onMoreTestsClick)
		self.buttons.append(self.moreTestsButton)

		self.createTexts()

	def onMoreTestsClick(self):
		self.game.transition('CHOOSE')

	def onLanguageChanged(self):
		super().onLanguageChanged()
		self.createTexts()
		self.moreTestsButton.createText(self.config.getText("DFAM_TEST_RESULTS_MORE_TESTS_BUTTON_TEXT"), self.extraSmallTextFont)

	def createTexts(self):
		self.headerText = self.subHeaderFont.render(self.config.getText(TEST_ID_TO_RESULT_KEYS[self.test]['header']), True, (255, 255, 255))
		self.subHeaderTexts = Utilities.renderTextList(self.config, self.extraSmallTextFont, TEST_ID_TO_RESULT_KEYS[self.test]['subHeader'])
		self.testResultText = self.smallTextFont.render(self.config.getText('DFAM_TEST_RESULTS_RESULTS_HEADER'), True, (0, 0, 0))
		self.healthyResultText = self.smallTextFont.render(self.config.getText('DFAM_TEST_RESULTS_HEALTHY_HEADER'), True, (0, 0, 0))

	def draw(self, dt):
		self.screen.blit(self.testImage, (357 if self.test == 'COGNITIVE' else 201, 130))
		self.screen.blit(self.healthyImage, (724 if self.test == 'COGNITIVE' else 722, 130))
		Utilities.drawTextOnCenterX(self.screen, self.headerText, (self.screen.get_width() // 2, 44))
		Utilities.drawTextsOnCenterX(self.screen, self.subHeaderTexts, (self.screen.get_width() // 2, 482), 28)
		Utilities.drawTextOnCenterX(self.screen, self.testResultText, (591 if self.test == 'COGNITIVE' else 721, 570 if self.test == 'COGNITIVE' else 585))
		Utilities.drawTextOnCenterX(self.screen, self.healthyResultText, (1308 if self.test == 'COGNITIVE' else 1206, 570 if self.test == 'COGNITIVE' else 585))
		super().draw(dt)