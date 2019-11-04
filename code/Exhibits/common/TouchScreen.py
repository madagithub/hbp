import platform
import sys
import traceback
from queue import Queue
from threading import Thread

if platform.system() == 'Linux':
	import evdev
	from evdev import InputDevice, categorize, ecodes

class TouchScreen:
	DOWN_EVENT = 'down'
	UP_EVENT = 'up'

	def __init__(self, name, bounds, resolution):
		self.touchPartialName = name
		self.touchScreenBounds = bounds
		self.screenResolution = resolution
		self.touchPos = None
		self.eventQueue = Queue()
		self.device = None
		self.readTouchThread = None

	def setup(self):
		print(platform.system())
		if platform.system() != 'Linux':
			return False

		devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
		devicePath = None
		for device in devices:
			if self.touchPartialName in device.name:
				print (device.name)
				devicePath = device.path
				break

		if devicePath is not None:
			print("Path: ", devicePath)
			self.device = evdev.InputDevice(devicePath)
			self.readTouchThread = Thread(target=self.readTouch, args=())
			self.readTouchThread.daemon = True
			self.readTouchThread.start()
			return True

		return False

	def getPosition(self):
		position = self.touchPos
		return position

	def readUpDownEvent(self):
		if self.eventQueue.empty():
			return None

		return self.eventQueue.get()

	def readTouch(self):
		try:
			currX = 0
			currY = 0

			coordinatesChanged = 0

			isUp = False
			isDown = False

			# TODO: Change to read_one and alow thread to exit when marked
			for event in self.device.read_loop():
				if event.type == ecodes.SYN_REPORT:
					pos = (int(currX * self.screenResolution[0] / self.touchScreenBounds[0]), int(currY * self.screenResolution[1] / self.touchScreenBounds[1]))
					if isUp:
						self.eventQueue.put({'type': self.UP_EVENT, 'pos': pos})
					elif isDown:
						self.eventQueue.put({'type': self.DOWN_EVENT, 'pos': pos})
					else:
						self.touchPos = pos

					isUp = False
					isDown = False

				if event.type == ecodes.EV_KEY:
					keyEvent = categorize(event)
					if keyEvent.keycode[0] == 'BTN_LEFT' or keyEvent.keycode == 'BTN_TOUCH':
						if keyEvent.keystate == keyEvent.key_up:
							isUp = True
						elif keyEvent.keystate == keyEvent.key_down:
							isDown = True
				elif event.type == ecodes.EV_ABS:
					absEvent = categorize(event)

					if absEvent.event.code == 0:
						currX = absEvent.event.value
					elif absEvent.event.code == 1:
						currY = absEvent.event.value
		except:
			excType, excValue, excTraceback = sys.exc_info()
			lines = traceback.format_exception(excType, excValue, excTraceback)
			Log.error(lines.join('\n'))