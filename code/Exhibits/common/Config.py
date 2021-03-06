import json
import pyfribidi

class Config:

	def __init__(self, filename, extraFilename=None):
		with open(filename) as file:
			self.config = json.load(file)

		if extraFilename is not None:
			with open(extraFilename) as file:
				overrideConfig = json.load(file)

			self.config.update(overrideConfig)

		self.languagePrefix = self.config['defaultLanguage']
		self.languageIndex = next(index for index in range(len(self.config['languages'])) if self.config['languages'][index]['prefix'] == self.languagePrefix)

	def getText(self, key):
		text = self.config['texts'][self.languagePrefix][key]
		if self.getLanguage()['rtl']:
			text = pyfribidi.log2vis(text)
		return text

	def getTextList(self, key):
		lines = self.config['texts'][self.languagePrefix][key].split('\n')
		if self.getLanguage()['rtl']:
			lines = [pyfribidi.log2vis(s) for s in lines]
		return lines

	def getLanguages(self):
		return self.config['languages']

	def isRtl(self):
		return self.getLanguage()['rtl']

	def changeLanguage(self, index):
		self.languageIndex = index
		self.languagePrefix = self.getLanguages()[self.languageIndex]['prefix']

	def getLanguage(self):
		return self.config['languages'][self.languageIndex]

	def getDefaultLanguagePrefix(self):
		return self.config['defaultLanguage']

	def getScreenWidth(self):
		return self.config.get('screenWidth', None)

	def getScreenHeight(self):
		return self.config.get('screenHeight', None)

	def isTouch(self):
		return self.config['touch']

	def setTouch(self, value):
		self.config['touch'] = value

	def getTouchDevicePartialName(self):
		return self.config['touchDevicePartialName']

	def getTouchScreenMaxX(self):
		return self.config['touchMaxX']

	def getTouchScreenMaxY(self):
		return self.config['touchMaxY']

	def getOpeningVideos(self):
		return self.config['openingVideos']

	def getInstitutions(self, countryKey):
		return self.config['mapCountries'][countryKey]['institutions']

	def getInstitutionVideoFilenames(self):
		videoFilenames = []
		countriesMap = self.config['mapCountries']
		for countryKey in countriesMap.keys():
			institutions = countriesMap[countryKey]['institutions']
			for institution in institutions:
				if institution.get('video', None) is not None:
					videoFilenames.append(institution['video'])

		return videoFilenames

	def getMaxMapDotTapDistance(self):
		return self.config['maxMapDotTapDistance']

	def getCountryName(self, countryKey):
		return self.getText(self.config['mapCountries'][countryKey]['nameKey'])

	def getScreenSize(self):
		return (self.config['width'], self.config['height'])

	def shouldOpenSerial(self):
		return self.config['shouldOpenSerial']

	def getSerialPortCommandsByTime(self, command):
		resultMap = {}
		sourceMap = self.config[command + 'SerialCommands']
		for key in sourceMap:
			resultMap[key] = list(map(lambda command: bytes(command, 'utf-8'), sourceMap[key]))
		return resultMap

	def getTestRunTime(self, test):
		return self.config[test + 'RunTime']

	def getInitSerialPortCommands(self):
		return list(map(lambda command: bytes(command, 'utf-8'), self.config['initSerialCommands']))

	def getPETDoneSerialPortCommands(self):
		return list(map(lambda command: bytes(command, 'utf-8'), self.config['PETDoneSerialCommands']))

	def getAnimationPaths(self, neuron):
		return self.config['neuronPaths'][neuron]['animationPaths']

	def getDrawingPaths(self, neuron):
		return self.config['neuronPaths'][neuron]['tracePaths']

	def getSelectedPathsNumber(self, neuron):
		return self.config['neuronPaths'][neuron]['select']
