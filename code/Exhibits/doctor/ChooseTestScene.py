import pygame
from pygame.locals import *

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

TEST_DATA = [{'normal': 'cognitive-test.png', 'selected': 'cognitive-test-selected.png', 'name-key': 'DFAM_COGNITIVE_TEST_NAME', 'desc-key': 'DFAM_COGNITIVE_TEST_DESC'}, 
	{'normal': 'pet-test.png', 'selected': 'pet-test-selected.png', 'name-key': 'DFAM_PET_TEST_NAME', 'desc-key': 'DFAM_PET_TEST_DESC'}, 
	{'normal': 'mri-test.png', 'selected': 'mri-test-selected.png', 'name-key': 'DFAM_MRI_TEST_NAME', 'desc-key': 'DFAM_MRI_TEST_DESC'}]

#TODO: Unite with choose neuron scene
class ChooseTestScene(Scene):
	def __init__(self, game):
		super().__init__(game)

		self.createTexts()

		self.neuronNames = []
		self.neuronDescs = []

		currImageButtonX = FIRST_TEST_IMAGE_X
		currSelectButtonX = FIRST_TEST_SELECT_BUTTON_X
		self.selectButtons = []
		for i in range(0, len(TEST_DATA)): #TODO: Move to config
			neuronImageSet = TEST_DATA[i]
			normalImage = pygame.image.load('assets/images/doctor/' + neuronImageSet['normal'])
			selectedImage = pygame.image.load('assets/images/doctor/' + neuronImageSet['selected'])
			self.buttons.append(Button(self.screen, pygame.Rect(currImageButtonX, FIRST_TEST_IMAGE_Y, normalImage.get_width(), normalImage.get_height()), 
				normalImage, selectedImage, None, None, None, None, partial(self.onNeuronClick, i)))

			normalButtonImage = pygame.image.load('assets/images/small-button-empty.png')
			selectButton = Button(self.screen, pygame.Rect(currSelectButtonX, FIRST_TEST_SELECT_BUTTON_Y, normalButtonImage.get_width(), normalButtonImage.get_height()), 
				normalButtonImage, pygame.image.load('assets/images/small-button-selected.png'), 
				self.config.getText('DFAM_CHOOSE_TEST_SELECT_BUTTON_TEXT'), [0, 0, 0], [0, 0, 0], self.buttonFont, partial(self.onNeuronClick, i))
			self.buttons.append(selectButton)
			self.selectButtons.append(selectButton)

			self.neuronNames.append(self.subHeaderFont.render(self.config.getText(neuronImageSet['name-key']), True, (255, 255, 255)))

			descTexts = Utilities.renderTextList(self.config, self.extraSmallTextFont, neuronImageSet['desc-key'])
			self.neuronDescs.append(descTexts)

			currImageButtonX += TEST_IMAGE_GAP
			currSelectButtonX += TEST_IMAGE_GAP

	def onLanguageChanged(self):
		super().onLanguageChanged()
		self.createTexts()

		for i in range(0, len(self.selectButtons)):
			self.selectButtons[i].createText(self.config.getText('DFAM_CHOOSE_TEST_SELECT_BUTTON_TEXT'), self.buttonFont)

	def createTexts(self):
		self.headerText = self.textFont.render(self.config.getText("DFAM_CHOOSE_TEST_INSTRUCTION"), True, (255, 255, 255))

	def onNeuronClick(self, index):
		self.game.transition('RUN_TEST', INDEX_TO_TEST_ID[index])

	def draw(self, dt):
		Utilities.drawTextOnCenterX(self.screen, self.headerText, (self.screen.get_width() // 2, 85))

		for i in range(len(self.neuronNames)):
			currX = FIRST_TEST_TEXT_MIDDLE + TEST_IMAGE_GAP * i
			Utilities.drawTextOnCenterX(self.screen, self.neuronNames[i], (currX, 543))
			Utilities.drawTextsOnCenterX(self.screen, self.neuronDescs[i], (currX, 615), SMALL_TEXT_LINE_SIZE)

		super().draw(dt)