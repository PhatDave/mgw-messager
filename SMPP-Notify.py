import random
import sched

import keyboard
import pygame
import pyperclip
import requests

URL = "http://localhost:7080/test/mo"

FROM_NUMBER = 38765586767
NUMBER_SET = []
GENERATE_N_NUMBERS = 10000
QUERY_STRING = {"count": "1", "to": "11111", "text": "bss", "from": "0"}

RANDOMIZE_NUMBER_PER_BATCH = False
RANDOMIZE_NUMBER_PER_MESSAGE = False
RANDOMIZE_NUMBER_FROM_SET = False

sch = sched.scheduler(pygame.time.get_ticks, pygame.time.wait)


def sendMessage(fromNumber):
	if RANDOMIZE_NUMBER_PER_MESSAGE:
		fromNumber = '385' + str(random.randint(1000000, 9999999))

	if RANDOMIZE_NUMBER_FROM_SET:
		while len(NUMBER_SET) < GENERATE_N_NUMBERS:
			NUMBER_SET.append('385' + str(random.randint(1000000, 9999999)))
		fromNumber = random.choice(NUMBER_SET)

	print(f'{pygame.time.get_ticks()} - Sending message from number {fromNumber}')
	QUERY_STRING["from"] = str(fromNumber)
	resp = requests.request("GET", URL, data = "", params = QUERY_STRING)
	print(f'{pygame.time.get_ticks()} - {resp.text} - {fromNumber}\n')


def runSchedule(messagesNo, timeStep):
	global FROM_NUMBER
	fromNumber = FROM_NUMBER

	if RANDOMIZE_NUMBER_PER_BATCH:
		fromNumber = '385' + str(random.randint(1000000, 9999999))

	print(f'{pygame.time.get_ticks()} - Scheduling messages from number {fromNumber}')
	pyperclip.copy(str(fromNumber))
	for i in range(messagesNo):
		sch.enter(i * timeStep, int(1e10) - i, sendMessage, argument = (fromNumber,))
	sch.run()


keyboard.add_hotkey('ctrl+alt+m', runSchedule, args = (1, 10,))
keyboard.wait()
