import datetime
import json
import random
import sched

import keyboard
import pygame
import pyperclip
import requests as req

FROM_NUMBER = 38765586767
NUMBER_SET = []
GENERATE_N_NUMBERS = 10000

RANDOMIZE_NUMBER_PER_BATCH = False
RANDOMIZE_NUMBER_PER_MESSAGE = False
RANDOMIZE_NUMBER_FROM_SET = False

AUTH_USER = 'ts'
AUTH_PW = 'ts'

sch = sched.scheduler(pygame.time.get_ticks, pygame.time.wait)

URL = "http://localhost:8181/mgw/oneapi/payment/"

HEADERS = {
	'Content-Type': 'application/json',
	'username': AUTH_USER,
	'password': AUTH_PW,
	'Accept': 'application/json'
}

RESERVE_BODY = {
	"endUserId": "38765485540",
	"paymentAmount": {
		"chargingInformation": {
			"amount": "10",
			"description": ["mteltest"]
		}},
	"transactionOperationStatus": "RESERVED"
}

CHARGE_BODY = {
	"paymentAmount": {
		"chargingInformation": {
			"amount": "10",
			"description": ["mteltest"]
		}},
	"transactionOperationStatus": "CHARGED",
	"referenceCode": "672825310336213121"
}


def doReserve(fromNumber):
	RESERVE_BODY['endUserId'] = fromNumber
	res = req.post(URL, json = RESERVE_BODY, headers = HEADERS)
	responseJson = json.loads(res.text)
	return responseJson['referenceCode']


def doCharge(id):
	CHARGE_BODY['referenceCode'] = id
	res = req.post(URL, json = CHARGE_BODY, headers = HEADERS)
	return res


def doTransaction(fromNumber):
	if RANDOMIZE_NUMBER_PER_MESSAGE:
		fromNumber = '385' + str(random.randint(1000000, 9999999))

	if RANDOMIZE_NUMBER_FROM_SET:
		while len(NUMBER_SET) < GENERATE_N_NUMBERS:
			NUMBER_SET.append('385' + str(random.randint(1000000, 9999999)))
		fromNumber = random.choice(NUMBER_SET)

	print(f'{pygame.time.get_ticks()} - Sending message from number {fromNumber}')
	id = doReserve(fromNumber)
	res = doCharge(id)
	print(f'{pygame.time.get_ticks()} - {res.status_code} - {fromNumber}\n')


def runSchedule(messagesNo, timeStep):
	global FROM_NUMBER
	fromNumber = FROM_NUMBER

	if RANDOMIZE_NUMBER_PER_BATCH:
		fromNumber = '385' + str(random.randint(1000000, 9999999))

	print(f'{pygame.time.get_ticks()} - Scheduling messages from number {fromNumber}')
	pyperclip.copy(str(fromNumber))
	for i in range(messagesNo):
		sch.enter(i * timeStep, int(1e10) - i, doTransaction, argument = (fromNumber,))
	sch.run()


keyboard.add_hotkey('ctrl+alt+c', runSchedule, args = (1, 10,))
keyboard.wait()
