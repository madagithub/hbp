import pygame
from pygame.locals import *

from functools import partial

from common.Scene import Scene
from common.Button import Button
from common.Utilities import Utilities
from common.Log import Log

FIRST_TEST_IMAGE_X = 140
FIRST_TEST_IMAGE_Y = 136
FIRST_TEST_SELECT_BUTTON_X = 154
FIRST_TEST_SELECT_BUTTON_Y = 534
FIRST_TEST_TEXT_MIDDLE = 244
TEST_IMAGE_GAP = 444

INDEX_TO_TEST_ID = ['COGNITIVE', 'MRI', 'PET']
TEST_ID_TO_INDEX = {
	'COGNITIVE': 0,
	'MRI': 1,
	'PET': 2,
}

TEST_DATA = [{'normal': 'cognitive-test.png', 'selected': 'cognitive-test-selected.png', 'healthy': 'results-cognitive-healthy.png', 'not-healthy': 'results-cognitive-not-healthy.png', 'name-key': 'DFAM_COGNITIVE_TEST_NAME', 'desc-key': 'DFAM_COGNITIVE_TEST_DESC'}, 
	{'normal': 'mri-test.png', 'selected': 'mri-test-selected.png', 'healthy': 'results-mri-healthy.png', 'not-healthy': 'results-mri-not-healthy.png', 'name-key': 'DFAM_MRI_TEST_NAME', 'desc-key': 'DFAM_MRI_TEST_DESC'},
	{'normal': 'pet-test.png', 'selected': 'pet-test-selected.png', 'healthy': 'results-pet-healthy.png', 'not-healthy': 'results-pet-not-healthy.png', 'name-key': 'DFAM_PET_TEST_NAME', 'desc-key': 'DFAM_PET_TEST_DESC'}]

#TODO: Unite with choose neuron scene
class ChooseTestScene(Scene):
	def __init__(self, game, isHealthy):
		super().__init__(game)

		self.isHealthy = isHealthy

		self.diagnoseQuestionOn = False

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
				self.config.getText('DFAM_CHOOSE_TEST_SELECT_BUTTON_TEXT'), [0, 0, 0], [0, 0, 0], self.extraSmallTextFont, partial(self.onTestClick, i))
			self.buttons.append(selectButton)
			self.selectButtons.append(selectButton)

			self.neuronNames.append(self.smallButtonTextFont.render(self.config.getText(neuronImageSet['name-key']), True, (255, 255, 255)))

			descTexts = Utilities.renderTextList(self.config, self.smallScreenExtraSmallTextFont, neuronImageSet['desc-key'])
			self.neuronDescs.append(descTexts)

			currImageButtonX += TEST_IMAGE_GAP
			currSelectButtonX += TEST_IMAGE_GAP

		normalImage = pygame.image.load('assets/images/doctor/diagnose-button-normal.png')
		selectedImage = pygame.image.load('assets/images/doctor/diagnose-button-selected.png')
		self.diagnoseButton = Button(self.screen, pygame.Rect(self.screen.get_width() // 2 - normalImage.get_width() // 2, 601, normalImage.get_width(), normalImage.get_height()), 
			normalImage, selectedImage, self.config.getText('DFAM_DIAGNOSE_BUTTON_TEXT'), [255, 255, 255], [255, 255, 255], self.smallButtonTextFont, self.onDiagnose)
		self.buttons.append(self.diagnoseButton)
		self.diagnoseButton.visible = False

		normalImage = pygame.image.load('assets/images/doctor/button-orange-small.png')
		selectedImage = pygame.image.load('assets/images/doctor/button-orange-small-selected.png')
		self.diagnoseYesButton = Button(self.screen, pygame.Rect(545, 601, normalImage.get_width(), normalImage.get_height()), 
			normalImage, selectedImage, self.config.getText('DFAM_DIAGNOSE_YES_BUTTON_TEXT'), [255, 255, 255], [255, 255, 255], self.smallButtonTextFont, partial(self.onDiagnoseResult, False))
		self.buttons.append(self.diagnoseYesButton)
		self.diagnoseYesButton.visible = False

		normalImage = pygame.image.load('assets/images/doctor/button-orange-small.png')
		selectedImage = pygame.image.load('assets/images/doctor/button-orange-small-selected.png')
		self.diagnoseNoButton = Button(self.screen, pygame.Rect(700, 601, normalImage.get_width(), normalImage.get_height()), 
			normalImage, selectedImage, self.config.getText('DFAM_DIAGNOSE_NO_BUTTON_TEXT'), [255, 255, 255], [255, 255, 255], self.smallButtonTextFont, partial(self.onDiagnoseResult, True))
		self.buttons.append(self.diagnoseNoButton)
		self.diagnoseNoButton.visible = False

		self.createTexts()

	def onLanguageChanged(self):
		super().onLanguageChanged()
		self.createTexts()

		for i in range(0, len(self.selectButtons)):
			self.selectButtons[i].createText(self.config.getText('DFAM_CHOOSE_TEST_SELECT_BUTTON_TEXT'), self.extraSmallTextFont)

	def createTexts(self):
		self.headerText = self.smallScreenSubSubHeaderFont.render(self.config.getText('DFAM_CHOOSE_TEST_INSTRUCTION'), True, (255, 255, 255))
		self.diagnoseQuestionText = self.smallScreenSubSubHeaderFont.render(self.config.getText('DFAM_DIAGNOSE_QUESTION_TEXT'), True, [255, 207, 0])

		for i in range(0, len(TEST_DATA)):
			neuronImageSet = TEST_DATA[i]
			selectButton = self.selectButtons[i]
			selectButton.createText(self.config.getText('DFAM_CHOOSE_TEST_DONE_SELECT_BUTTON_TEXT' if self.testsDone[i] else 'DFAM_CHOOSE_TEST_SELECT_BUTTON_TEXT'), self.extraSmallTextFont)

			self.neuronNames[i] = self.smallButtonTextFont.render(self.config.getText(neuronImageSet['name-key']), True, (255, 255, 255))
			self.neuronDescs[i] = Utilities.renderTextList(self.config, self.smallScreenExtraSmallTextFont, neuronImageSet['desc-key'])

		self.diagnoseButton.createText(self.config.getText('DFAM_DIAGNOSE_BUTTON_TEXT'), self.smallButtonTextFont)
		self.diagnoseYesButton.createText(self.config.getText('DFAM_DIAGNOSE_YES_BUTTON_TEXT'), self.smallButtonTextFont)
		self.diagnoseNoButton.createText(self.config.getText('DFAM_DIAGNOSE_NO_BUTTON_TEXT'), self.smallButtonTextFont)

	def onTestClick(self, index):
		if self.testsDone[index]:
			self.game.transition('TEST_RESULTS', {'test': INDEX_TO_TEST_ID[index], 'isHealthy': self.isHealthy})
		else:
			self.game.transition('RUN_TEST', {'test': INDEX_TO_TEST_ID[index], 'isHealthy': self.isHealthy})

	def onTestDone(self, test):
		self.clearResetTimer()

		testIndex = TEST_ID_TO_INDEX[test]
		self.testsDone[testIndex] = True

		button = self.selectButtons[testIndex]
		buttonCenterX = button.rect.x + button.image.get_width() // 2
		button.image = pygame.image.load('assets/images/doctor/done-test-button-normal.png')
		button.tappedImage = pygame.image.load('assets/images/doctor/done-test-button-selected.png')
		button.rect = Rect(buttonCenterX - button.image.get_width() // 2, button.rect.y, button.image.get_width(), button.image.get_height())
		button.color = button.selectedColor = [255, 255, 255]
		button.createText(self.config.getText('DFAM_CHOOSE_TEST_DONE_SELECT_BUTTON_TEXT'), self.extraSmallTextFont)

		imageButton = self.imageButtons[testIndex]
		conditionKey = 'healthy' if self.isHealthy else 'not-healthy'
		imageButton.image = pygame.image.load('assets/images/doctor/' + TEST_DATA[testIndex][conditionKey])
		imageButton.tappedImage = pygame.image.load('assets/images/doctor/' + TEST_DATA[testIndex][conditionKey])

		self.diagnoseButton.visible = not self.diagnoseQuestionOn

	def onDiagnose(self):
		Log.info('DIAGNOSE')
		self.clearResetTimer()
		
		self.diagnoseQuestionOn = True
		self.diagnoseButton.visible = False
		self.diagnoseYesButton.visible = True
		self.diagnoseNoButton.visible = True

		for button in self.selectButtons:
			button.rect.y -= 121
			button.updateTapRect()

	def onDiagnoseResult(self, isHealthy):
		self.game.transition('EVALUATE', {'condition': self.isHealthy, 'diagnosys': isHealthy})

	def draw(self, dt):
		Utilities.drawTextOnCenterX(self.screen, self.headerText, (self.screen.get_width() // 2, 49))

		for i in range(len(self.neuronNames)):
			currX = FIRST_TEST_TEXT_MIDDLE + TEST_IMAGE_GAP * i
			Utilities.drawTextOnCenterX(self.screen, self.neuronNames[i], (currX, 356))

			if not self.diagnoseQuestionOn:
				Utilities.drawTextsOnCenterX(self.screen, self.neuronDescs[i], (currX, 408), 21)

		if self.diagnoseQuestionOn:
			Utilities.drawTextOnCenterX(self.screen, self.diagnoseQuestionText, (self.screen.get_width() // 2, 534))

		super().draw(dt)