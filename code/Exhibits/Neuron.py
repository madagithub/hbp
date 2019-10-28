import pygame
from pygame.locals import *
import cv2
import time
import sys
import glob

from common.Exhibit import Exhibit
from common.VideoScene import VideoScene
from common.Log import Log
from common.VideoPlayer import VideoPlayer

from neuron.OpeningScene import OpeningScene
from neuron.ChooseNeuronScene import ChooseNeuronScene
from neuron.DrawNeuronScene import DrawNeuronScene
from neuron.SummaryScene import SummaryScene

EXTRA_CONFIG_FILENAME = 'assets/config/config-neuron.json'
LOG_FILE_PATH = 'neuron.log'

class Neuron(Exhibit):
	def __init__(self):
		Log.init(LOG_FILE_PATH)
		Log.info('INIT')

		super().__init__()

	def start(self, extraConfigFilename):
		super().start(extraConfigFilename)

		Log.info('PRELOAD_START')
		self.preloadVideos()
		Log.info('PRELOAD_DONE')
		
		self.scene = OpeningScene(self)

		self.drawingScenes = {}
		self.drawingScenes['martinotti'] = DrawNeuronScene(self, 'martinotti')
		self.drawingScenes['basket'] = DrawNeuronScene(self, 'basket')
		self.drawingScenes['pyramidal'] = DrawNeuronScene(self, 'pyramidal')

		self.loop()

	def preloadVideos(self):
		self.initialVideoFrames = {}

		videoFilenames = [f for f in glob.glob('assets/videos/neuron/*.mov', recursive=False)]

		for filename in videoFilenames:
			Log.info('PRELOADING_VIDEO_START,' + filename)
			self.initialVideoFrames[filename] = VideoPlayer.preloadInitialFrames(filename)
			Log.info('PRELOADING_VIDEO_DONE,' + filename)

	def gotoHome(self):
		self.scene = OpeningScene(self)

	def transition(self, transitionId, data=None):
		if transitionId == 'START':
			videoFilename = 'assets/videos/neuron/brainzoom-short.mov'
			self.scene = VideoScene(self, videoFilename, 'CHOOSE', initialFrames=self.initialVideoFrames[videoFilename])
		elif transitionId == 'CHOOSE':
			self.scene = ChooseNeuronScene(self)
		elif transitionId == 'DRAW':
			self.drawingScenes[data].reset()
			self.scene = self.drawingScenes[data]
		elif transitionId == 'SUMMARY':
			self.scene = SummaryScene(self, data)

if __name__ == '__main__':
	Neuron().start(None if len(sys.argv) == 2 and sys.argv[1] == '--mouse' else EXTRA_CONFIG_FILENAME)