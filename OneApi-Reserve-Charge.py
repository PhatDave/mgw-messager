import datetime
import json
import re

import keyboard
import requests as req

url = "http://localhost:8181/mgw/oneapi/payment/"

headers = {
	"Content-Type": "application/json",
	"username": "ts",
	"password": "ts",
	"Accept": "application/json"
}

bodyReserve = {
	"endUserId": "38765485540",
	"paymentAmount": {
		"chargingInformation": {
			"amount": "10",
			"description": ["mteltest"]
		}},
	"transactionOperationStatus": "RESERVED"
}

bodyCharge = {
	"paymentAmount": {
		"chargingInformation": {
			"amount": "10",
			"description": ["mteltest"]
		}},
	"transactionOperationStatus": "CHARGED",
	"referenceCode": "672825310336213121"
}


def doReserve():
	res = req.post(url, json = bodyReserve, headers = headers)
	responseJson = json.loads(res.text)
	return responseJson['referenceCode']


def doCharge():
	try:
		for i in range(20):
			id = doReserve()
			bodyCharge['referenceCode'] = id
			res = req.post(url, json = bodyCharge, headers = headers)
			print(f'{datetime.datetime.now()} - {res.status_code}')
		# return res.status_code
	except:
		print("umro neki kurac")


keyboard.add_hotkey('ctrl+alt+c', doCharge)
keyboard.wait()
# print(f'doCharge() = {doCharge()}')
