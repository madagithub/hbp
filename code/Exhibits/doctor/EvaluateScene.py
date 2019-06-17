import pygame
from pygame.locals import *

from common.Scene import Scene
from common.Button import Button

from common.Utilities import Utilities

START_BUTTON_TEXT_COLOR = [0, 0, 0]

#TODO: Unite with neuron opening screen
class EvaluateScene(Scene):
	def __init__(self, game, evaluation):
		super().__init__(game)

		self.evaluation = evaluation
		self.isCorrect = evaluation['diagnosys'] == evaluation['condition']
		self.isHealthy = evaluation['condition']

		self.evaluationImage = pygame.image.load('assets/images/doctor/' + ('correct' if self.isCorrect else 'incorrect') + '.png')

		self.anotherPatientButton = Button(self.screen, pygame.Rect(915, 629, 386, 56), 
			pygame.image.load('assets/images/button-long-normal.png'), pygame.image.load('assets/images/button-long-selected.png'), 
			self.config.getText("DFAM_EVALUATION_ANOTHER_PATIENT_TEXT"), START_BUTTON_TEXT_COLOR, START_BUTTON_TEXT_COLOR, self.smallButtonTextFont, self.onAnotherPatient)
		self.buttons.append(self.anotherPatientButton)

		self.learnMoreButton = Button(self.screen, pygame.Rect(656, 629, 179, 56), 
			pygame.image.load('assets/images/doctor/learn-more-button-normal.png'), pygame.image.load('assets/images/doctor/learn-more-button-selected.png'), 
			self.config.getText("DFAM_EVALUATION_LEARN_MORE_TEXT"), START_BUTTON_TEXT_COLOR, [255,255,255], self.smallButtonTextFont, self.onLearnMore)
		self.buttons.append(self.learnMoreButton)

		self.createTexts()

	def onAnotherPatient(self):
		self.game.transition('RESET')

	def onLearnMore(self):
		self.game.transition('LEARN_MORE', self.evaluation)

	def onLanguageChanged(self):
		super().onLanguageChanged()
		self.createTexts()
		self.anotherPatientButton.createText(self.config.getText("DFAM_EVALUATION_ANOTHER_PATIENT_TEXT"), self.smallButtonTextFont)

	def createTexts(self):
		self.headerText = self.subHeaderFont.render(self.config.getText('DFAM_EVALUATION_SCREEN_CORRECT_HEADER' if self.isCorrect else 'DFAM_EVALUATION_SCREEN_INCORRECT_HEADER'), True, [249, 207, 71])
		self.subHeaderText = self.textFont.render(self.config.getText('DFAM_EVALUATION_SCREEN_HEALTHY_HEADER' if self.isHealthy else 'DFAM_EVALUATION_SCREEN_NOT_HEALTHY_HEADER'), True, [255, 255, 255])

	def draw(self, dt):
		self.screen.blit(self.evaluationImage, (self.screen.get_width() // 2 - self.evaluationImage.get_width() // 2, 229))
		Utilities.drawTextOnCenterX(self.screen, self.headerText, (self.screen.get_width() // 2, 467))
		Utilities.drawTextOnCenterX(self.screen, self.subHeaderText, (self.screen.get_width() // 2, 551))
		super().draw(dt)