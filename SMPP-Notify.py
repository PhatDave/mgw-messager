import random
import sched

import keyboard
import pygame
import pyperclip
import requests

url = "http://localhost:7080/test/mo"

fromNumber = 38765586767
numberSet = []
generateNRandomNumbers = 10000
querystring = {"count": "1", "to": "11111", "text": "bss", "from": "0"}

payload = ""
sch = sched.scheduler(pygame.time.get_ticks, pygame.time.wait)


def sendMessage(fromNumber):
	# fromNumber = '385' + str(random.randint(1000000, 9999999))

	while (len(numberSet) < generateNRandomNumbers):
		numberSet.append('385' + str(random.randint(1000000, 9999999)))
	fromNumber = random.choice(numberSet)

	print(f'{pygame.time.get_ticks()} - Sending message from number {fromNumber}')
	querystring["from"] = str(fromNumber)
	resp = requests.request("GET", url, data = payload, params = querystring)
	print(f'{pygame.time.get_ticks()} - {resp.text} - {fromNumber}\n')


def runSchedule(messagesNo, timeStep):
	global fromNumber
	# fromNumber = '385' + str(random.randint(1000000, 9999999))
	print(f'{pygame.time.get_ticks()} - Scheduling messages from number {fromNumber}')
	pyperclip.copy(str(fromNumber))
	for i in range(messagesNo):
		sch.enter(i * timeStep, int(1e10) - i, sendMessage, argument = (fromNumber,))
	sch.run()


keyboard.add_hotkey('ctrl+alt+m', runSchedule, args = (1, 10,))
# keyboard.add_hotkey('ctrl+alt+m', sendMessage, args=(fromNumber,))
keyboard.wait()
