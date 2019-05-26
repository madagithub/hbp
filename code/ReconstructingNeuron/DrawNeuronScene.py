import pygame
from pygame.locals import *

import math

from Scene import Scene
from Button import Button

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

class DrawNeuronScene(Scene):
	def __init__(self, game):
		super().__init__(game)

		self.prototypeNeuron = pygame.image.load('assets/images/pyramidal_neuron_small.png')
		self.drawOnNeuron = pygame.image.load('assets/images/pyramidal_neuron_small.png')

		self.drawingDone = False
		self.resetCirclePos()
		self.drawImagePos = (int(self.screen.get_width() / 2 - self.drawOnNeuron.get_width() / 2), 100)
		self.lastUpTime = None

	def processEvent(self, event):
		if event.type == MOUSEBUTTONDOWN:
			if self.isInCircle(event.pos):
				self.drawing = True
				self.lastUpTime = None
		elif event.type == MOUSEBUTTONUP:
			if self.isInCircle(event.pos):
				self.lastUpTime = pygame.time.get_ticks()
		elif event.type == MOUSEMOTION:
			self.onMouseMove(event.pos)

	def onMouseMove(self, pos):
		if self.drawing and self.lastUpTime is None:
			newCirclePos = (pos[0] - int(self.screen.get_width() / 2 - self.drawOnNeuron.get_width() / 2), int(pos[1] - 100))

			(distanceFromPath, pointIndex) = self.getDistanceFromPath(newCirclePos)
			if distanceFromPath >= MAX_DISTANCE_FROM_PATH:
				self.resetCirclePos()
			else:
				self.circlePos = newCirclePos
				self.currPointIndexReached = pointIndex

				if self.currPointIndexReached == len(PATH_POINTS) - 1:
					self.drawingDone = True

	def draw(self):
		if self.drawing and self.lastUpTime is not None and (pygame.time.get_ticks() - self.lastUpTime) / 1000 > MAX_NON_DRAWING_TIME_UNTIL_RESET:
			self.resetCirclePos()

		self.screen.blit(pygame.transform.scale(self.prototypeNeuron, (int(self.prototypeNeuron.get_width() * 0.8), int(self.prototypeNeuron.get_height() * 0.8))), (100, 100))
		self.screen.blit(self.drawOnNeuron, (self.screen.get_width() / 2 - self.drawOnNeuron.get_width() / 2, 100))

		self.drawCurrPath()

		if not self.drawingDone:
			globalCirclePos = self.localNeuronPointToGlobalPoint(self.circlePos)
			pygame.draw.circle(self.screen, (255,0,0), globalCirclePos, CIRCLE_RADIUS)

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