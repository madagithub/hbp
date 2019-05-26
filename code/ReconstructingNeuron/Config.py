import json

class Config:

	def __init__(self, filename):
		with open(filename) as file:
			self.config = json.load(file)
		self.language = self.config['defaultLanguage']

	def getText(self, key):
		return self.config['texts'][self.language][key]

	def getTextList(self, key):
		return self.config['texts'][self.language][key].split('\n')

	def getLanguages(self):
		return self.config['languages']

	def changeLanguage(self, language):
		self.language = language



