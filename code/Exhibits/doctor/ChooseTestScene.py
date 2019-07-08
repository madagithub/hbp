import pygame
from pygame.locals import *

import random

from functools import partial

from common.Scene import Scene
from common.Button import Button
from common.Utilities import Utilities

FIRST_TEST_IMAGE_X = 240
FIRST_TEST_IMAGE_Y = 179
FIRST_TEST_SELECT_BUTTON_X = 309
FIRST_TEST_SELECT_BUTTON_Y = 787
FIRST_TEST_TEXT_MIDDLE = 398
TEST_IMAGE_GAP = 565

SMALL_TEXT_LINE_SIZE = 26

INDEX_TO_TEST_ID = ['COGNITIVE', 'PET', 'MRI']
TEST_ID_TO_INDEX = {
	'COGNITIVE': 0,
	'PET': 1,
	'MRI': 2
}

TEST_DATA = [{'normal': 'cognitive-test.png', 'selected': 'cognitive-test-selected.png', 'healthy': 'results-cognitive-healthy.png', 'not-healthy': 'results-cognitive-not-healthy.png', 'name-key': 'DFAM_COGNITIVE_TEST_NAME', 'desc-key': 'DFAM_COGNITIVE_TEST_DESC'}, 
	{'normal': 'pet-test.png', 'selected': 'pet-test-selected.png', 'healthy': 'results-pet-healthy.png', 'not-healthy': 'results-pet-not-healthy.png', 'name-key': 'DFAM_PET_TEST_NAME', 'desc-key': 'DFAM_PET_TEST_DESC'}, 
	{'normal': 'mri-test.png', 'selected': 'mri-test-selected.png', 'healthy': 'results-mri-healthy.png', 'not-healthy': 'results-mri-not-healthy.png', 'name-key': 'DFAM_MRI_TEST_NAME', 'desc-key': 'DFAM_MRI_TEST_DESC'}]

#TODO: Unite with choose neuron scene
class ChooseTestScene(Scene):
	def __init__(self, game):
		super().__init__(game)

		self.diagnoseQuestionOn = False

		self.generateTestResults()

		self.createTexts()

		self.neuronNames = []
		self.neuronDescs = []
		self.imageButtons = []
		self.testsDone = [False] * len(TEST_DATA)

		currImageButtonX = FIRST_TEST_IMAGE_X
		currSelectButtonX = FIRST_TEST_SELECT_BUTTON_X
		self.selectButtons = []
		for i in range(0, len(TEST_DATA)): #TODO: Move to config
			neuronImageSet = TEST_DATA[i]
			normalImage = pygame.image.load('assets/images/doctor/' + neuronImageSet['normal'])
			selectedImage = pygame.image.load('assets/images/doctor/' + neuronImageSet['selected'])
			imageButton = Button(self.screen, pygame.Rect(currImageButtonX, FIRST_TEST_IMAGE_Y, normalImage.get_width(), normalImage.get_height()), 
				normalImage, selectedImage, None, None, None, None, partial(self.onTestClick, i))
			self.buttons.append(imageButton)
			self.imageButtons.append(imageButton)

			normalButtonImage = pygame.image.load('assets/images/small-button-empty.png')
			selectButton = Button(self.screen, pygame.Rect(currSelectButtonX, FIRST_TEST_SELECT_BUTTON_Y, normalButtonImage.get_width(), normalButtonImage.get_height()), 
				normalButtonImage, pygame.image.load('assets/images/small-button-selected.png'), 
				self.config.getText('DFAM_CHOOSE_TEST_SELECT_BUTTON_TEXT'), [0, 0, 0], [0, 0, 0], self.smallButtonTextFont, partial(self.onTestClick, i))
			self.buttons.append(selectButton)
			self.selectButtons.append(selectButton)

			self.neuronNames.append(self.subHeaderFont.render(self.config.getText(neuronImageSet['name-key']), True, (255, 255, 255)))

			descTexts = Utilities.renderTextList(self.config, self.extraSmallTextFont, neuronImageSet['desc-key'])
			self.neuronDescs.append(descTexts)

			currImageButtonX += TEST_IMAGE_GAP
			currSelectButtonX += TEST_IMAGE_GAP

		normalImage = pygame.image.load('assets/images/doctor/diagnose-button-normal.png')
		selectedImage = pygame.image.load('assets/images/doctor/diagnose-button-selected.png')
		self.diagnoseButton = Button(self.screen, pygame.Rect(847, 891, 232, 64), 
			normalImage, selectedImage, self.config.getText('DFAM_DIAGNOSE_BUTTON_TEXT'), [255, 255, 255], [255, 255, 255], self.buttonFont, self.onDiagnose)
		self.buttons.append(self.diagnoseButton)
		self.diagnoseButton.visible = False

		normalImage = pygame.image.load('assets/images/doctor/button-orange-small.png')
		selectedImage = pygame.image.load('assets/images/doctor/button-orange-small-selected.png')
		self.diagnoseYesButton = Button(self.screen, pygame.Rect(727, 891, normalImage.get_width(), normalImage.get_height()), 
			normalImage, selectedImage, self.config.getText('DFAM_DIAGNOSE_YES_BUTTON_TEXT'), [255, 255, 255], [255, 255, 255], self.buttonFont, partial(self.onDiagnoseResult, False))
		self.buttons.append(self.diagnoseYesButton)
		self.diagnoseYesButton.visible = False

		normalImage = pygame.image.load('assets/images/doctor/button-orange-small.png')
		selectedImage = pygame.image.load('assets/images/doctor/button-orange-small-selected.png')
		self.diagnoseNoButton = Button(self.screen, pygame.Rect(1013, 891, normalImage.get_width(), normalImage.get_height()), 
			normalImage, selectedImage, self.config.getText('DFAM_DIAGNOSE_NO_BUTTON_TEXT'), [255, 255, 255], [255, 255, 255], self.buttonFont, partial(self.onDiagnoseResult, True))
		self.buttons.append(self.diagnoseNoButton)
		self.diagnoseNoButton.visible = False

	def generateTestResults(self):
		self.isHealthy = True if random.random() > 0.5 else False

	def onLanguageChanged(self):
		super().onLanguageChanged()
		self.createTexts()

		for i in range(0, len(self.selectButtons)):
			self.selectButtons[i].createText(self.config.getText('DFAM_CHOOSE_TEST_SELECT_BUTTON_TEXT'), self.smallButtonTextFont)

	def createTexts(self):
		self.headerText = self.textFont.render(self.config.getText('DFAM_CHOOSE_TEST_INSTRUCTION'), True, (255, 255, 255))
		self.diagnoseQuestionText = self.subHeaderFont.render(self.config.getText('DFAM_DIAGNOSE_QUESTION_TEXT'), True, [255, 207, 0])

	def onTestClick(self, index):
		if self.testsDone[index]:
			self.game.transition('TEST_RESULTS', {'test': INDEX_TO_TEST_ID[index], 'isHealthy': self.isHealthy})
		else:
			self.game.transition('RUN_TEST', {'test': INDEX_TO_TEST_ID[index], 'isHealthy': self.isHealthy})

	def onTestDone(self, test):
		testIndex = TEST_ID_TO_INDEX[test]
		self.testsDone[testIndex] = True

		button = self.selectButtons[testIndex]
		buttonCenterX = button.rect.x + button.image.get_width() // 2
		button.image = pygame.image.load('assets/images/doctor/done-test-button-normal.png')
		button.tappedImage = pygame.image.load('assets/images/doctor/done-test-button-selected.png')
		button.rect = Rect(buttonCenterX - button.image.get_width() // 2, button.rect.y, button.image.get_width(), button.image.get_height())
		button.color = button.selectedColor = [255, 255, 255]
		button.createText(self.config.getText('DFAM_CHOOSE_TEST_DONE_SELECT_BUTTON_TEXT'), self.smallButtonTextFont)

		imageButton = self.imageButtons[testIndex]
		conditionKey = 'healthy' if self.isHealthy else 'not-healthy'
		imageButton.image = pygame.image.load('assets/images/doctor/' + TEST_DATA[testIndex][conditionKey])
		imageButton.tappedImage = pygame.image.load('assets/images/doctor/' + TEST_DATA[testIndex][conditionKey])

		self.diagnoseButton.visible = True

	def onDiagnose(self):
		self.diagnoseQuestionOn = True
		self.diagnoseButton.visible = False
		self.diagnoseYesButton.visible = True
		self.diagnoseNoButton.visible = True

		for button in self.selectButtons:
			button.rect.y -= 158

	def onDiagnoseResult(self, isHealthy):
		self.game.transition('EVALUATE', {'condition': self.isHealthy, 'diagnosys': isHealthy})

	def draw(self, dt):
		Utilities.drawTextOnCenterX(self.screen, self.headerText, (self.screen.get_width() // 2, 49))

		for i in range(len(self.neuronNames)):
			currX = FIRST_TEST_TEXT_MIDDLE + TEST_IMAGE_GAP * i
			Utilities.drawTextOnCenterX(self.screen, self.neuronNames[i], (currX, 543))

			if not self.diagnoseQuestionOn:
				Utilities.drawTextsOnCenterX(self.screen, self.neuronDescs[i], (currX, 615), SMALL_TEXT_LINE_SIZE)

		if self.diagnoseQuestionOn:
			Utilities.drawTextOnCenterX(self.screen, self.diagnoseQuestionText, (self.screen.get_width() // 2, 812))

		super().draw(dt)