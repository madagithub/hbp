import pygame
from pygame.locals import *

from functools import partial

from common.Scene import Scene
from common.Button import Button
from common.Utilities import Utilities

FIRST_NEURON_IMAGE_X = 236
FIRST_NEURON_IMAGE_Y = 236
FIRST_NEURON_SELECT_BUTTON_X = 284
FIRST_NEURON_SELECT_BUTTON_Y = 739
FIRST_NEURON_TEXT_MIDDLE = 374
NEURON_IMAGE_GAP = 584

SMALL_TEXT_LINE_SIZE = 26

NEURON_DATA = [{'id': 'pyramidal', 'normal': 'select-pyramidal-neuron-normal.png', 'selected': 'select-pyramidal-neuron-selected.png', 'name-key': 'RN_CHOOSE_NEURON_PYRAMIDAL_NAME', 'desc-key': 'RN_CHOOSE_NEURON_PYRAMIDAL_DESC'}, 
	{'id': 'basket', 'normal': 'select-basket-neuron-normal.png', 'selected': 'select-basket-neuron-selected.png', 'name-key': 'RN_CHOOSE_NEURON_BASKET_NAME', 'desc-key': 'RN_CHOOSE_NEURON_BASKET_DESC'}, 
	{'id': 'martinotti', 'normal': 'select-martinotti-neuron-normal.png', 'selected': 'select-martinotti-neuron-selected.png', 'name-key': 'RN_CHOOSE_NEURON_MARTINOTTI_NAME', 'desc-key': 'RN_CHOOSE_NEURON_MARTINOTTI_DESC'}]

class ChooseNeuronScene(Scene):
	def __init__(self, game):
		super().__init__(game)

		self.neuronNames = []
		self.neuronDescs = []

		currImageButtonX = FIRST_NEURON_IMAGE_X
		currSelectButtonX = FIRST_NEURON_SELECT_BUTTON_X
		self.neuronImages = []
		self.selectButtons = []
		self.indexToId = []
		for i in range(0, len(NEURON_DATA)): #TODO: Move to config
			neuronImageSet = NEURON_DATA[i]
			normalImage = pygame.image.load('assets/images/' + neuronImageSet['normal'])
			selectedImage = pygame.image.load('assets/images/' + neuronImageSet['selected'])
			self.buttons.append(Button(self.screen, pygame.Rect(currImageButtonX, FIRST_NEURON_IMAGE_Y, normalImage.get_width(), normalImage.get_height()), 
				normalImage, selectedImage, None, None, None, None, partial(self.onNeuronClick, i)))
			normalButtonImage = pygame.image.load('assets/images/small-button-empty.png')

			selectButton = Button(self.screen, pygame.Rect(currSelectButtonX, FIRST_NEURON_SELECT_BUTTON_Y, normalButtonImage.get_width(), normalButtonImage.get_height()), 
				normalButtonImage, pygame.image.load('assets/images/small-button-selected.png'), 
				self.config.getText('RN_CHOOSE_NEURON_SELECT_BUTTON_TEXT'), [0, 0, 0], [0, 0, 0], self.buttonFont, partial(self.onNeuronClick, i))
			self.buttons.append(selectButton)
			self.selectButtons.append(selectButton)

			self.neuronNames.append(self.subHeaderFont.render(self.config.getText(neuronImageSet['name-key']), True, (255, 255, 255)))

			descTexts = Utilities.renderTextList(self.config, self.extraSmallTextFont, neuronImageSet['desc-key'])
			self.neuronDescs.append(descTexts)

			self.indexToId.append(neuronImageSet['id'])

			currImageButtonX += NEURON_IMAGE_GAP
			currSelectButtonX += NEURON_IMAGE_GAP

		self.createTexts()

	def onLanguageChanged(self):
		super().onLanguageChanged()
		self.createTexts()

		for i in range(0, len(self.selectButtons)):
			self.selectButtons[i].createText(self.config.getText('RN_CHOOSE_NEURON_SELECT_BUTTON_TEXT'), self.buttonFont)

	def createTexts(self):
		self.headerText = self.textFont.render(self.config.getText("RN_CHOOSE_NEURON_INSTRUCTION"), True, (255, 255, 255))

		for i in range(0, len(NEURON_DATA)):
			neuronImageSet = NEURON_DATA[i]

			self.selectButtons[i].createText(self.config.getText('RN_CHOOSE_NEURON_SELECT_BUTTON_TEXT'), self.buttonFont)
			self.neuronNames[i] = self.subHeaderFont.render(self.config.getText(neuronImageSet['name-key']), True, (255, 255, 255))
			self.neuronDescs[i] = Utilities.renderTextList(self.config, self.extraSmallTextFont, neuronImageSet['desc-key'])

	def onNeuronClick(self, index):
		self.game.transition('DRAW', self.indexToId[index])

	def draw(self, dt):
		Utilities.drawTextOnCenterX(self.screen, self.headerText, (self.screen.get_width() // 2, 61))

		for i in range(len(self.neuronNames)):
			currX = FIRST_NEURON_TEXT_MIDDLE + NEURON_IMAGE_GAP * i
			Utilities.drawTextOnCenterX(self.screen, self.neuronNames[i], (currX, 556))
			Utilities.drawTextsOnCenterX(self.screen, self.neuronDescs[i], (currX, 620), SMALL_TEXT_LINE_SIZE)

		super().draw(dt)