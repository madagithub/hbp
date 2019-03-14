class Scene:
	def __init__(self, game, screen):
		self.game = game
		self.screen = screen

	def processEvent(self, event):
		raise NotImplemented

	def draw(self):
		raise NotImplemented