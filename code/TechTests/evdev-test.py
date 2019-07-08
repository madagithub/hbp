import evdev
from evdev import InputDevice, categorize, ecodes

device = evdev.InputDevice('/dev/input/event8')

print(device.capabilities(verbose=True))

currX = 0
currY = 0

coordinatesChanged = 0

isUp = False
isDown = False

for event in device.read_one():
	if event.type == ecodes.SYN_REPORT:
		if isUp:
			print('UP:', str(currX), '-', str(currY))
		elif isDown:
			print('DOWN: ', str(currX), '-', str(currY))
		else:
			print('MOVE: ', str(currX), '-', str(currY))

		isUp = False
		isDown = False

	if event.type == ecodes.EV_KEY:
		keyEvent = categorize(event)
		pass
		if keyEvent.keycode[0] == 'BTN_LEFT':
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