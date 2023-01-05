import random

import keyboard
import pyperclip


def generateFloatToClipboard():
	randVal = random.random() * 100
	randStr = str(randVal)
	while len(randStr) > 8:
		randStr = randStr[:-1]
	pyperclip.copy(randStr)


keyboard.add_hotkey('ctrl+v', generateFloatToClipboard)
keyboard.wait()
