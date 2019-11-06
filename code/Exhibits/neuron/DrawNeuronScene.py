import pygame
from pygame.locals import *

import math
import random

from common.Scene import Scene
from common.Button import Button
from common.Utilities import Utilities
from common.Timer import Timer
from common.VideoPlayer import VideoPlayer
from common.FrameAnimation import FrameAnimation
from common.Log import Log

from queue import Queue

NEURON_BUTTON_WIDTH = 200
NEURON_BUTTON_HEIGHT = 400
NEURON_BUTTON_PADDING = 50

CIRCLE_RADIUS = 10
CIRCLE_DOT_RADIUS = 2

MAX_DISTANCE_FROM_PATH = 30

TRACE_LINE_WIDTH = 3

ANIMATION_PATH_COLOR = (56,143,254)
ANIMATION_TRACE_COLOR = (255,121,36)
TRACE_PATH_COLOR = (26,54,163)
DONE_PATH_COLOR = (231,6,230)

MAX_NON_DRAWING_TIME_UNTIL_RESET = 1.0

DOTTED_SEGMENT_SIZE = 2

NEURON_TO_NAME_KEY = {
	'martinotti': "RN_CHOOSE_NEURON_MARTINOTTI_NAME",
	'basket': "RN_CHOOSE_NEURON_BASKET_NAME",
	'pyramidal': "RN_CHOOSE_NEURON_PYRAMIDAL_NAME"
}

NEURON_IMAGE_Y = 196

DRAWING_STATE = 'drawing'
MODEL_STATE = '3d-model'
LIGHTNING_STATE = 'lightning'

OFFSET_X_FIX = 5
OFFSET_Y_FIX = 5

class DrawNeuronScene(Scene):
	def __init__(self, game, neuronChosen):
		super().__init__(game)

		self.neuronChosen = neuronChosen

		self.spinningAnimation = FrameAnimation('assets/videos/neuron/animations/' + self.neuronChosen + '-big/animation-', 60, 24)
		self.electricAnimation = FrameAnimation('assets/videos/neuron/animations/' + self.neuronChosen + '-electric-big/animation-', 46, 48)

		self.originalAnimationPaths = self.config.getAnimationPaths(self.neuronChosen)
		self.animationPaths = self.originalAnimationPaths.copy()
		self.drawingPaths = self.getDrawingPaths([], self.animationPaths, False)

		self.circleImage = pygame.image.load('assets/images/neuron/draw-handle.png').convert_alpha()

		self.drawOnNeuron = pygame.image.load('assets/images/neuron/' + self.neuronChosen + '-big.png')
		self.videoMask = pygame.image.load('assets/images/video-mask.png')

		self.modelTextBalloon = pygame.image.load('assets/images/text-box-large.png')
		self.lightningTextBalloon = pygame.image.load('assets/images/text-box-small.png')

		lightningButtonNormal = pygame.image.load('assets/images/button-electrify-normal.png')
		lightningButtonTapped = pygame.image.load('assets/images/button-electrify-tapped.png')
		
		self.lightningButton = Button(self.screen, pygame.Rect(920, 871, lightningButtonNormal.get_width(), lightningButtonNormal.get_height()), 
			lightningButtonNormal, lightningButtonTapped, None, None, None, None, self.onMoveToLightningState)
		self.buttons.append(self.lightningButton)

		self.nextButton = Button(self.screen, pygame.Rect(868, 872, 179, 56), 
			pygame.image.load('assets/images/button-small-normal.png'), pygame.image.load('assets/images/button-small-selected.png'), 
			self.config.getText("RN_DRAWING_SCREEN_CONTINUE_BUTTON_TEXT"), [0,0,0], [0,0,0], self.buttonFont, self.onNextClick)
		self.buttons.append(self.nextButton)

	def reset(self):
		self.state = DRAWING_STATE

		self.loadFonts()
		self.onLanguageChanged()

		self.nextButton.visible = False
		self.lightningButton.visible = False

		self.animationPaths = self.originalAnimationPaths.copy()

		random.shuffle(self.drawingPaths)
		self.selectedPaths = self.drawingPaths[:self.config.getSelectedPathsNumber(self.neuronChosen)]

		q = Queue()

		for path in self.animationPaths:
			q.put(path)

		while not q.empty():
			currPath = q.get()
			isSelected = False
			for selectedPath in self.selectedPaths:
				if set(self.pathToList(currPath['path'])).issubset(set(self.pathToList(selectedPath))):
					isSelected = True
			currPath['type'] = 'regular' if not isSelected else 'dotted'
			subPaths = currPath.get('nextPaths', [])
			for path in subPaths:
				q.put(path)

		self.animationIndex = 0
		self.animationTime = None
		self.animationDone = False
		self.selectedPathIndex = 0

		for path in self.animationPaths:
			path['done'] = False
			path['startAnimationIndex'] = 0

		self.drawingDone = False
		self.resetCirclePos()
		self.drawImagePos = (int(self.screen.get_width() / 2 - self.drawOnNeuron.get_width() / 2), NEURON_IMAGE_Y)
		self.lastUpTime = None

		self.timer = None

		self.createTexts()

	def pathToList(self, path):
		resultList = []
		for p in path:
			resultList.append(p['x'])
			resultList.append(p['y'])
		return resultList

	def getDrawingPaths(self, currPath, subPaths, justOne):
		drawingPaths = []

		dottedSubPaths = list(filter(lambda path: path['type'] == 'dotted', subPaths))
		nonDottedSubPaths = list(filter(lambda path: path['type'] == 'regular', subPaths))

		dottedPathsToCheck = []
		if justOne and len(dottedSubPaths) > 0:
			random.shuffle(dottedSubPaths)
			dottedPathsToCheck.append(dottedSubPaths[0])
		else:
			dottedPathsToCheck = dottedSubPaths

		for subPath in dottedPathsToCheck:
			if subPath.get('nextPaths', None) is None:
				drawingPaths.append(currPath + subPath['path'])
			else:
				drawingPaths += self.getDrawingPaths(currPath + subPath['path'], subPath.get('nextPaths'), True)

		for subPath in nonDottedSubPaths:
			if subPath.get('nextPaths', None) is not None:
				drawingPaths += self.getDrawingPaths([], subPath['nextPaths'], True)

		return drawingPaths


	def onLanguageChanged(self):
		super().onLanguageChanged()
		self.createTexts()

	def getCurrPath(self):
		return self.selectedPaths[self.selectedPathIndex]

	def createTexts(self):
		if self.state == DRAWING_STATE:
			self.headerText = self.subHeaderFont.render(self.config.getText(NEURON_TO_NAME_KEY[self.neuronChosen]), True, (255, 255, 255))
			self.instructionText = self.textFont.render(self.config.getText("RN_DRAWING_SCREEN_NEURON_INSTRUCTION"), True, (255, 255, 255))
		elif self.state == MODEL_STATE:
			self.instructionTexts = Utilities.renderTextList(self.config, self.textFont, "RN_DRAWING_SCREEN_LIGHTNING_INSTRUCTION")
			self.explanationTexts = Utilities.renderTextList(self.config, self.extraSmallTextFont, "RN_DRAWING_SCREEN_3D_MODEL_EXPLANATION")
		elif self.state == LIGHTNING_STATE:
			self.explanationTexts = Utilities.renderTextList(self.config, self.extraSmallTextFont, "RN_DRAWING_SCREEN_LIGHTNING_EXPLANATION")
			self.nextButton.createText(self.config.getText("RN_DRAWING_SCREEN_CONTINUE_BUTTON_TEXT"), self.buttonFont)

	def draw(self, dt):
		if self.timer is not None:
			self.timer.tick(dt)

		if self.state == DRAWING_STATE:
			self.drawDrawingState(dt)
		elif self.state == MODEL_STATE:
			self.draw3DModelState(dt)
		elif self.state == LIGHTNING_STATE:
			self.drawLightningState(dt)

		super().draw(dt)

	def drawDrawingState(self, dt):
		self.screen.blit(self.drawOnNeuron, self.drawImagePos)

		Utilities.drawTextOnCenterX(self.screen, self.headerText, (self.screen.get_width() // 2, 115))
		Utilities.drawTextOnCenterX(self.screen, self.instructionText, (self.screen.get_width() // 2, 820))

		if (self.animationTime is None):
			Log.info('DRAW_ANIMATION_START')
			self.animationTime = 0

		self.animationTime += dt
		self.animationIndex = int(self.animationTime / 0.05)
		self.drawAnimationPaths()

		if not self.animationDone and len(self.animationPaths) == len(list(filter(lambda path: path['done'], self.animationPaths))):
			self.animationDone = True
			Log.info('DRAW_ANIMATION_DONE')

		self.drawCurrPaths()

		if not self.drawingDone:
			if self.drawing and self.lastUpTime is not None and (pygame.time.get_ticks() - self.lastUpTime) / 1000 > MAX_NON_DRAWING_TIME_UNTIL_RESET:
				Log.info('DRAW_WRONG', 'NO_DRAW')
				self.resetCirclePos()

			globalCirclePos = self.localNeuronPointToGlobalPoint(self.circlePos)

			self.screen.blit(self.circleImage, (globalCirclePos[0] - self.circleImage.get_width() // 2, globalCirclePos[1] - self.circleImage.get_height() // 2))

	def draw3DModelState(self, dt):
		self.screen.blit(self.spinningAnimation.getFrame(dt), (self.screen.get_width() // 2 - 600 // 2, 240))
		self.screen.blit(self.videoMask, (0, 0))

		self.screen.blit(self.modelTextBalloon, (1314, 399))
		Utilities.drawTextsOnCenterX(self.screen, self.instructionTexts, (self.screen.get_width() // 2, 61), 40)

		if self.config.isRtl():
			Utilities.drawTextsOnRightX(self.screen, self.explanationTexts, (1692, 429), 29)
		else:
			Utilities.drawTextsOnLeftX(self.screen, self.explanationTexts, (1349, 429), 29)

	def drawLightningState(self, dt):
		self.screen.blit(self.electricAnimation.getFrame(dt), (self.screen.get_width() // 2 - 600 // 2, 0))
		self.screen.blit(self.videoMask, (0, 0))

		self.screen.blit(self.lightningTextBalloon, (1314, 412))
		Utilities.drawTextsOnCenterX(self.screen, self.instructionTexts, (self.screen.get_width() // 2, 61), 40)

		if self.config.isRtl():
			Utilities.drawTextsOnRightX(self.screen, self.explanationTexts, (1692, 442), 29)
		else:
			Utilities.drawTextsOnLeftX(self.screen, self.explanationTexts, (1349, 442), 29)		

	def onMouseDown(self, pos):
		super().onMouseDown(pos)

		if self.isInCircle(pos):
			Log.info('DRAW_START')
			self.clearResetTimer()
			self.drawing = True
			self.lastUpTime = None

	def onMouseUp(self, pos):
		super().onMouseUp(pos)

		if self.isInCircle(pos):
			self.clearResetTimer()
			self.lastUpTime = pygame.time.get_ticks()

	def onMouseMove(self, pos):
		super().onMouseMove(pos)

		if not self.drawingDone:
			if self.drawing and self.lastUpTime is None:
				self.clearResetTimer()

				newCirclePos = (pos[0] - int(self.screen.get_width() / 2 - self.drawOnNeuron.get_width() / 2), int(pos[1] - NEURON_IMAGE_Y))

				(distanceFromPath, pointIndex) = self.getDistanceFromPath(newCirclePos)
				if distanceFromPath >= MAX_DISTANCE_FROM_PATH:
					Log.info('DRAW_WRONG', 'DIST')
					self.resetCirclePos()
				else:
					self.circlePos = newCirclePos
					self.currPointIndexReached = pointIndex

					if self.currPointIndexReached == len(self.getCurrPath()) - 1:
						self.onDrawingDone()

	def onDrawingDone(self):
		self.clearResetTimer()
		self.selectedPathIndex += 1
		Log.info('DRAW_CORRECT', str(self.selectedPathIndex))
		if self.selectedPathIndex >= len(self.selectedPaths):
			self.drawingDone = True
			self.timer = Timer(2.0, self.onMoveToModelState)
		else:
			self.resetCirclePos()

	def onMoveToModelState(self):
		Log.info('MODEL')
		self.clearResetTimer()
		self.timer = None
		self.state = MODEL_STATE
		self.createTexts()
		self.lightningButton.visible = True

	def onMoveToLightningState(self):
		Log.info('LIGHTNING')
		self.clearResetTimer()
		self.state = LIGHTNING_STATE
		self.createTexts()
		self.lightningButton.visible = False
		self.nextButton.visible = True

	def onNextClick(self):
		self.game.transition('SUMMARY', self.neuronChosen)

	def drawCurrPaths(self):
		for i in range(min(len(self.selectedPaths), self.selectedPathIndex + 1)):
			path = self.selectedPaths[i]

			for index in range(1, self.currPointIndexReached if i == self.selectedPathIndex else len(path)):
				p1 = path[index - 1]
				p2 = path[index]
				pygame.draw.line(self.screen, TRACE_PATH_COLOR if i == self.selectedPathIndex else DONE_PATH_COLOR, self.localNeuronPointToGlobalPoint((p1['x'] + OFFSET_X_FIX, p1['y'] + OFFSET_Y_FIX)), self.localNeuronPointToGlobalPoint((p2['x'] + OFFSET_X_FIX, p2['y'] + OFFSET_Y_FIX)), TRACE_LINE_WIDTH)

	def drawAnimationPaths(self):
		newPaths = []

		for path in self.animationPaths:
			pathDefinition = path['path']

			isDrawing = True
			if path['type'] == 'dotted':
				dottedCounter = DOTTED_SEGMENT_SIZE

			for i in range(1, min(len(pathDefinition), self.animationIndex - path['startAnimationIndex'])):
				if isDrawing:
					if path['type'] == 'dotted':
						pygame.draw.circle(self.screen, ANIMATION_TRACE_COLOR, self.localNeuronPointToGlobalPoint((pathDefinition[i]['x'] + OFFSET_X_FIX, pathDefinition[i]['y'] + OFFSET_Y_FIX)), CIRCLE_DOT_RADIUS)
						isDrawing = False
					else:
						pygame.draw.line(self.screen, ANIMATION_PATH_COLOR if path['type'] == 'regular' else ANIMATION_TRACE_COLOR, self.localNeuronPointToGlobalPoint((pathDefinition[i-1]['x'] + OFFSET_X_FIX, pathDefinition[i-1]['y'] + OFFSET_Y_FIX)), self.localNeuronPointToGlobalPoint((pathDefinition[i]['x'] + OFFSET_X_FIX, pathDefinition[i]['y'] + OFFSET_Y_FIX)), TRACE_LINE_WIDTH)

				if path['type'] == 'dotted':
					dottedCounter -= 1
					if dottedCounter == 0:
						isDrawing = not isDrawing
						dottedCounter = DOTTED_SEGMENT_SIZE

			if not path['done'] and self.animationIndex >= len(pathDefinition) + path['startAnimationIndex']:
				path['done'] = True
				for newPath in path.get('nextPaths', []):
					newPath['done'] = False
					newPath['startAnimationIndex'] = len(pathDefinition) + path['startAnimationIndex']
					newPaths.append(newPath)

		for path in newPaths:
			self.animationPaths.append(path)


	def localNeuronPointToGlobalPoint(self, p):
		return (p[0] + self.drawImagePos[0], p[1] + self.drawImagePos[1])

	def getDistanceFromPath(self, pos):
		minDist = self.screen.get_width()
		minIndex = 0
		index = 0
		for p in self.getCurrPath():
			dist = math.hypot(p['x'] - pos[0], p['y'] - pos[1])
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
		self.clearResetTimer()
		self.drawing = False
		self.circlePos = (self.getCurrPath()[0]['x'] + OFFSET_X_FIX, self.getCurrPath()[0]['y'] + OFFSET_Y_FIX)
		self.currPointIndexReached = 0