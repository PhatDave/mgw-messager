import datetime

import requests as req
import re
import keyboard

url = r'http://localhost:8181/mgw/oneapi/payment/'
header = {
	"username": "ts",
	"password": "ts",
	"Accept": "application/xml",
	"Content-Type": "application/xml"
}
bodyReserve = r'''<?xml version="1.0" encoding="UTF-8"?>
<payment:amountReservationTransaction xmlns:payment="urn:oma:xml:rest:netapi:payment:1">
	<endUserId>321312312312</endUserId>
	<paymentAmount>
		<chargingInformation>
			<description>oneapicharging</description>
			<amount>7</amount>
		</chargingInformation>
	</paymentAmount>
	<transactionOperationStatus>Reserved</transactionOperationStatus>
</payment:amountReservationTransaction>'''
bodyCharge = r'''<?xml version="1.0" encoding="UTF-8"?>
<payment:amountReservationTransaction xmlns:payment="urn:oma:xml:rest:netapi:payment:1">
	<endUserId>321312312312</endUserId>
	<paymentAmount>
		<chargingInformation>
			<description>oneapicharging</description>
			<amount>4</amount>
		</chargingInformation>
	</paymentAmount>
	<transactionOperationStatus>Charged</transactionOperationStatus>
	<referenceCode>662466831337355500</referenceCode>
</payment:amountReservationTransaction>'''


def doReserve():
	res = req.post(url, data=bodyReserve, headers=header)
	try:
		return re.match(r'.*<referenceCode>(.*)</referenceCode>.*', res.text).group(1)
	except AttributeError:
		print("Error")
		print(res.content)
		return 0


def doCharge():
	id = doReserve()
	tempBody = bodyCharge.replace('662466831337355500', id)
	res = req.post(url, data=tempBody, headers=header)
	print(f'{datetime.datetime.now()} - {res.status_code}')
	return res.status_code


keyboard.add_hotkey('ctrl+alt+c', doCharge)
keyboard.wait()
# print(f'doCharge() = {doCharge()}')
