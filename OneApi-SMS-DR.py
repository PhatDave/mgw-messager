import json
import sched

import keyboard
import pygame
import requests as req

ADDRESS = 38630400382
SENDER_ADDRESS = 'OneApi'
AUTH_USER = 'oaob123'
AUTH_PW = 'oaob123'
MESSAGE = 'SNT Test DR'

sch = sched.scheduler(pygame.time.get_ticks, pygame.time.wait)

URL = f"http://localhost:8181/mgw/oneapi/messaging/v1/outbound/{SENDER_ADDRESS}/requests"

HEADERS = {
	'Content-Type': 'application/json',
	'username': AUTH_USER,
	'password': AUTH_PW,
	'senderAddress': SENDER_ADDRESS,
	'Accept': 'application/json'
}

MESSAGE_BODY = {
	"address": [f"{38630400382}"],
	"senderAddress": SENDER_ADDRESS,
	"outboundSMSTextMessage": {
		"message": MESSAGE
	}
}


def do_send():
	response = req.post(URL, json=MESSAGE_BODY, headers=HEADERS)
	vas_ref_id = get_and_split_response(response)
	print(f'{pygame.time.get_ticks()} - Sending message from number {ADDRESS}\n{pygame.time.get_ticks()} - VAS REF: {vas_ref_id}\n')


def run_schedule(messages_no, time_step):
	print(f'{pygame.time.get_ticks()} - Scheduling messages from number {ADDRESS}')
	for i in range(messages_no):
		sch.enter(i * time_step, int(1e10) - i, do_send)
	sch.run()


def get_and_split_response(response):
	responseJson = json.loads(response.text)
	resourceUrl = responseJson["resourceURL"]
	return resourceUrl.rsplit('/', 1)[-1]


keyboard.add_hotkey('ctrl+alt+o', run_schedule, args=(1, 10,))
keyboard.wait()
