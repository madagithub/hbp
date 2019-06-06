import pygame
from pygame.locals import *

import math

from common.Scene import Scene
from common.Button import Button
from common.Utilities import Utilities
from common.Timer import Timer
from common.VideoPlayer import VideoPlayer

NEURON_BUTTON_WIDTH = 200
NEURON_BUTTON_HEIGHT = 400
NEURON_BUTTON_PADDING = 50

START_CIRCLE_POS = (165, 420)
CIRCLE_RADIUS = 10

MAX_DISTANCE_FROM_PATH = 30

TRACE_LINE_WIDTH = 3

TRACE_PATH_COLOR = (255,0,0)
DONE_PATH_COLOR = (0,180,0)

MAX_NON_DRAWING_TIME_UNTIL_RESET = 1.0

PATH_POINTS = [
	START_CIRCLE_POS,
	(167, 370),
	(167, 360),
	(167, 350),
	(167, 340),
	(167, 330),
	(167, 320),
	(167, 310),
	(157, 300),
	(147, 290),
	(137, 280),
	(127, 270),
	(117, 260),
	(107, 250),
	(97, 250),
	(87, 250)
]

PATH_POINTS = [
	START_CIRCLE_POS,
	(161, 415),
	(156, 410),
	(153, 405),
	(147, 398),
	(142, 393),
	(140, 387),
	(140, 379),
	(135, 375),
	(131, 370),
	(129, 365),
	(119, 355),
	(115, 351),
	(111, 347),
	(104, 341),
	(100, 336),
	(98, 330),
	(95, 325)
]

NEURON_TO_NAME_KEY = {
	'martinotti': "RN_CHOOSE_NEURON_MARTINOTTI_NAME",
	'basket': "RN_CHOOSE_NEURON_BASKET_NAME",
	'pyramidal': "RN_CHOOSE_NEURON_BASKET_NAME"
}

NEURON_IMAGE_Y = 196

DRAWING_STATE = 'drawing'
MODEL_STATE = '3d-model'
LIGHTNING_STATE = 'lightning'

class DrawNeuronScene(Scene):
	def __init__(self, game, neuronChosen):
		super().__init__(game)
		self.state = DRAWING_STATE

		self.neuronChosen = neuronChosen

		self.drawOnNeuron = pygame.image.load('assets/images/reconstruct-martinotti.png')

		self.drawingDone = False
		self.resetCirclePos()
		self.drawImagePos = (int(self.screen.get_width() / 2 - self.drawOnNeuron.get_width() / 2), NEURON_IMAGE_Y)
		self.lastUpTime = None

		self.timer = None

		self.createTexts()

		self.modelTextBalloon = pygame.image.load('assets/images/text-box-small.png')
		self.lightningTextBalloon = pygame.image.load('assets/images/text-box-large.png')
		
		self.modelPlayer = VideoPlayer(game.screen, 'assets/videos/neuron-blender-color.avi', self.screen.get_width() // 2 - 960 // 2, 200, True)
		self.lightningPlayer = VideoPlayer(game.screen, 'assets/videos/MC_full.avi', self.screen.get_width() // 2 - 600 // 2, 0, True)

		lightningButtonNormal = pygame.image.load('assets/images/button-electrify-normal.png')
		lightningButtonTapped = pygame.image.load('assets/images/button-electrify-tapped.png')
		self.lightningButton = Button(self.screen, pygame.Rect(920, 871, lightningButtonNormal.get_width(), lightningButtonNormal.get_height()), 
			lightningButtonNormal, lightningButtonTapped, None, None, None, None, self.onMoveToLightningState)
		self.lightningButton.visible = False
		self.buttons.append(self.lightningButton)

		self.nextButton = Button(self.screen, pygame.Rect(868, 872, 179, 56), 
			pygame.image.load('assets/images/button-small-normal.png'), pygame.image.load('assets/images/button-small-selected.png'), 
			self.config.getText("RN_DRAWING_SCREEN_CONTINUE_BUTTON_TEXT"), [0,0,0], [0,0,0], self.buttonFont, self.onNextClick)
		self.nextButton.visible = False
		self.buttons.append(self.nextButton)

	def onLanguageChanged(self):
		super().onLanguageChanged()
		self.createTexts()

	def createTexts(self):
		if self.state == DRAWING_STATE:
			self.headerText = self.subHeaderFont.render(self.config.getText(NEURON_TO_NAME_KEY[self.neuronChosen]), True, (255, 255, 255))
			self.instructionText = self.textFont.render(self.config.getText("RN_DRAWING_SCREEN_NEURON_INSTRUCTION"), True, (255, 255, 255))
		elif self.state == MODEL_STATE:
			self.instructionTexts = Utilities.renderTextList(self.config, self.textFont, "RN_DRAWING_SCREEN_LIGHTNING_INSTRUCTION")
			self.explanationTexts = Utilities.renderTextList(self.config, self.extraSmallTextFont, "RN_DRAWING_SCREEN_3D_MODEL_EXPLANATION")
		elif self.state == LIGHTNING_STATE:
			self.explanationTexts = Utilities.renderTextList(self.config, self.extraSmallTextFont, "RN_DRAWING_SCREEN_LIGHTNING_EXPLANATION")

	def draw(self, dt):
		if self.timer is not None:
			self.timer.tick(dt)

		if self.state == DRAWING_STATE:
			self.drawDrawingState()
		elif self.state == MODEL_STATE:
			self.draw3DModelState()
		elif self.state == LIGHTNING_STATE:
			self.drawLightningState()

		super().draw(dt)

	def drawDrawingState(self):
		if self.drawing and self.lastUpTime is not None and (pygame.time.get_ticks() - self.lastUpTime) / 1000 > MAX_NON_DRAWING_TIME_UNTIL_RESET:
			self.resetCirclePos()

		self.screen.blit(self.drawOnNeuron, self.drawImagePos)

		self.drawCurrPath()

		if not self.drawingDone:
			globalCirclePos = self.localNeuronPointToGlobalPoint(self.circlePos)
			pygame.draw.circle(self.screen, (255,0,0), globalCirclePos, CIRCLE_RADIUS)

		Utilities.drawTextOnCenterX(self.screen, self.headerText, (self.screen.get_width() // 2, 115))
		Utilities.drawTextOnCenterX(self.screen, self.instructionText, (self.screen.get_width() // 2, 820))

	def draw3DModelState(self):
		self.modelPlayer.draw()

		self.screen.blit(self.modelTextBalloon, (1326, 399))
		Utilities.drawTextsOnCenterX(self.screen, self.instructionTexts, (self.screen.get_width() // 2, 61), 40)
		Utilities.drawTextsOnCenterX(self.screen, self.explanationTexts, (1530, 429), 29)

	def drawLightningState(self):
		self.lightningPlayer.draw()

		self.screen.blit(self.lightningTextBalloon, (1327, 412))
		Utilities.drawTextsOnCenterX(self.screen, self.instructionTexts, (self.screen.get_width() // 2, 61), 40)
		Utilities.drawTextsOnCenterX(self.screen, self.explanationTexts, (1530, 442), 29)

	def onMouseDown(self, pos):
		super().onMouseDown(pos)

		if self.isInCircle(pos):
			self.drawing = True
			self.lastUpTime = None

	def onMouseUp(self, pos):
		super().onMouseUp(pos)

		if self.isInCircle(pos):
			self.lastUpTime = pygame.time.get_ticks()

	def onMouseMove(self, pos):
		super().onMouseMove(pos)

		if self.drawing and self.lastUpTime is None:
			newCirclePos = (pos[0] - int(self.screen.get_width() / 2 - self.drawOnNeuron.get_width() / 2), int(pos[1] - NEURON_IMAGE_Y))

			(distanceFromPath, pointIndex) = self.getDistanceFromPath(newCirclePos)
			if distanceFromPath >= MAX_DISTANCE_FROM_PATH:
				self.resetCirclePos()
			else:
				self.circlePos = newCirclePos
				self.currPointIndexReached = pointIndex

				if self.currPointIndexReached == len(PATH_POINTS) - 1:
					self.onDrawingDone()

	def onDrawingDone(self):
		#TODO: Move to next drawing...

		self.drawingDone = True
		self.timer = Timer(2.0, self.onMoveToModelState)

	def onMoveToModelState(self):
		self.timer = None
		self.state = MODEL_STATE
		self.createTexts()
		self.lightningButton.visible = True

	def onMoveToLightningState(self):
		self.state = LIGHTNING_STATE
		self.createTexts()
		self.lightningButton.visible = False
		self.nextButton.visible = True

	def onNextClick(self):
		self.game.transition('SUMMARY', self.neuronChosen)

	def drawCurrPath(self):
		for index in range(1, self.currPointIndexReached if not self.drawingDone else len(PATH_POINTS)):
			p1 = PATH_POINTS[index - 1]
			p2 = PATH_POINTS[index]
			pygame.draw.line(self.screen, TRACE_PATH_COLOR if not self.drawingDone else DONE_PATH_COLOR, self.localNeuronPointToGlobalPoint(p1), self.localNeuronPointToGlobalPoint(p2), TRACE_LINE_WIDTH)

	def localNeuronPointToGlobalPoint(self, p):
		return (p[0] + self.drawImagePos[0], p[1] + self.drawImagePos[1])

	def getDistanceFromPath(self, pos):
		minDist = self.screen.get_width()
		minIndex = 0
		index = 0
		for p in PATH_POINTS:
			dist = math.hypot(p[0] - pos[0], p[1] - pos[1])
			if dist < minDist:
				minDist = dist
				minIndex = index
			index = index + 1

		return (minDist, minIndex)

	def isInCircle(self, pos):
		x1 = pos[0]
		y1 = pos[1]
		globalCirclePos = self.localNeuronPointToGlobalPoint(self.circlePos)
		return math.hypot(x1 - globalCirclePos[0], y1 - globalCirclePos[1]) < CIRCLE_RADIUS

	def resetCirclePos(self):
		self.drawing = False
		self.circlePos = START_CIRCLE_POS
		self.currPointIndexReached = 0