class Timer:
	def __init__(self, time, callback):
		self.timeLeft = time
		self.callback = callback

	def tick(self, dt):
		self.timeLeft -= dt
		if self.timeLeft <= 0:
			self.callback()