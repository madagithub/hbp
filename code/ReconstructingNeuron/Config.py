import json
import pyfribidi

import arabic_reshaper
from bidi.algorithm import get_display

class Config:

	def __init__(self, filename):
		with open(filename) as file:
			self.config = json.load(file)
		self.languagePrefix = self.config['defaultLanguage']
		self.languageIndex = next(index for index in range(len(self.config['languages'])) if self.config['languages'][index]['prefix'] == self.languagePrefix)

	def getText(self, key):
		return pyfribidi.log2vis(self.config['texts'][self.languagePrefix][key])

	def getTextList(self, key):
		return [pyfribidi.log2vis(s) for s in self.config['texts'][self.languagePrefix][key].split('\n')]

	def getLanguages(self):
		return self.config['languages']

	def changeLanguage(self, index):
		self.languageIndex = index
		self.languagePrefix = self.getLanguages()[self.languageIndex].languagePrefix

	def getLanguage(self):
		return self.config['languages'][self.languageIndex]



