import pygame
from pygame.locals import *

from common.Scene import Scene
from common.Button import Button

from common.Utilities import Utilities
from common.VideoPlayer import VideoPlayer
from common.FrameAnimation import FrameAnimation

START_BUTTON_TEXT_COLOR = [0, 0, 0]

class SummaryScene(Scene):
	def __init__(self, game, neuronChosen):
		super().__init__(game)

		self.neuronChosen = neuronChosen

		self.summaryTextBackground = pygame.image.load('assets/images/summary-text-background.png')

		self.neuronImage = pygame.image.load('assets/images/reconstruct-' + self.neuronChosen + '-small.png')
		self.spinningAnimationSmall = FrameAnimation('assets/videos/neuron/animations/' + self.neuronChosen + '-small/animation-', 60, 24)
		self.electricAnimationSmall = FrameAnimation('assets/videos/neuron/animations/' + self.neuronChosen + '-electric-small/animation-', 77, 24)
		self.videoMask = pygame.image.load('assets/images/neuron/small-video-mask.png')

		self.anotherNeuronButton = Button(self.screen, pygame.Rect(771, 620, 386, 56), 
			pygame.image.load('assets/images/button-long-normal.png'), pygame.image.load('assets/images/button-long-selected.png'), 
			self.config.getText("RN_SUMMARY_SCREEN_ANOTHER_NEURON_BUTTON_TEXT"), START_BUTTON_TEXT_COLOR, START_BUTTON_TEXT_COLOR, self.buttonFont, self.onAnotherNeuronClick)
		self.buttons.append(self.anotherNeuronButton)

		self.createTexts()

	def onLanguageChanged(self):
		super().onLanguageChanged()
		self.createTexts()

	def onAnotherNeuronClick(self):
		self.game.transition('CHOOSE')

	def createTexts(self):
		self.headerText = self.subHeaderFont.render(self.config.getText("RN_SUMMARY_SCREEN_HEADER"), True, (249, 207, 71))
		self.subHeaderText = self.textFont.render(self.config.getText("RN_SUMMARY_SCREEN_SUB_HEADER"), True, (255, 255, 255))
		self.summaryHeaderText = self.textFont.render(self.config.getText("RN_SUMMARY_SCREEN_SUMMARY_HEADER"), True, (255, 255, 255))
		self.summaryTexts = Utilities.renderTextList(self.config, self.almostExtraSmallTextFont, "RN_SUMMARY_SCREEN_SUMMARY_TEXT")

		self.drawingHeaderText = self.subHeaderFont.render(self.config.getText("RN_SUMMARY_SCREEN_DRAWING_TEXT"), True, [255, 255, 255])
		self.modelingHeaderText = self.subHeaderFont.render(self.config.getText("RN_SUMMARY_SCREEN_MODELING_TEXT"), True, [255, 255, 255])
		self.activateHeaderText = self.subHeaderFont.render(self.config.getText("RN_SUMMARY_SCREEN_ELECTRIFY_TEXT"), True, [255, 255, 255])

		self.anotherNeuronButton.createText(self.config.getText("RN_SUMMARY_SCREEN_ANOTHER_NEURON_BUTTON_TEXT"), self.buttonFont)

	def draw(self, dt):
		self.screen.blit(self.summaryTextBackground, (0, 726))
		self.screen.blit(self.neuronImage, (201, 203))
		self.screen.blit(self.spinningAnimationSmall.getFrame(dt), (818, 203))
		self.screen.blit(self.electricAnimationSmall.getFrame(dt), (1434, 103))
		self.screen.blit(self.videoMask, (818 - 24 // 2, 0 - 24 // 2))
		self.screen.blit(self.videoMask, (1434 - 24 // 2, 3 - 24 // 2))

		Utilities.drawTextOnCenterX(self.screen, self.headerText, (self.screen.get_width() // 2, 60))
		Utilities.drawTextOnCenterX(self.screen, self.subHeaderText, (self.screen.get_width() // 2, 113))
		Utilities.drawTextOnCenterX(self.screen, self.summaryHeaderText, (self.screen.get_width() // 2, 749))
		Utilities.drawTextsOnCenterX(self.screen, self.summaryTexts, (self.screen.get_width() // 2, 837), 29)

		Utilities.drawTextOnCenterX(self.screen, self.drawingHeaderText, (350, 521))
		Utilities.drawTextOnCenterX(self.screen, self.modelingHeaderText, (973, 521))
		Utilities.drawTextOnCenterX(self.screen, self.activateHeaderText, (1577, 521))

		super().draw(dt)