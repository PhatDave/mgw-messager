import base64
import random
import re
import sched

import keyboard
import pygame
import pyperclip
import requests

FROM_NUMBER = 38765586767
NUMBER_SET = []
GENERATE_N_NUMBERS = 10000

RANDOMIZE_NUMBER_PER_BATCH = False
RANDOMIZE_NUMBER_PER_MESSAGE = False
RANDOMIZE_NUMBER_FROM_SET = False

AUTH_USER = '1234'
AUTH_PW = '1234'

sch = sched.scheduler(pygame.time.get_ticks, pygame.time.wait)

URL = "http://localhost:8184/parlay-server/services/ReserveAmountChargingPort"
HEADERS = {
	'Authorization': f'Basic {base64.b64encode(f"{AUTH_USER}:{AUTH_PW}".encode()).decode()}',
	'Accept-Encoding': 'gzip,deflate',
	'Content-Type': 'text/xml;charset=UTF-8',
	'SOAPAction': '',
}

# Yes, it is backwards; no, I don't know why
RESERVE_SOAP_ACTION = 'ReserveAmountCharging#chargeReservation'
CHARGE_SOAP_ACTION = 'ReserveAmountCharging#reserveAmount'

RESERVE_BODY = """<soapenv:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:pay="http://www.csapi.org/wsdl/parlayx/payment">
   <soapenv:Header/>
   <soapenv:Body>
      <pay:reserveAmount soapenv:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
         <endUserIdentifier xsi:type="v1:EndUserIdentifier" xmlns:v1="http://www.csapi.org/schema/parlayx/common/v1_0">
            <value xsi:type="xsd:anyURI">to:38766328418</value>
         </endUserIdentifier>
         <amount xsi:type="xsd:decimal">2</amount>
         <billingText xsi:type="xsd:string">oa</billingText>
      </pay:reserveAmount>
   </soapenv:Body>
</soapenv:Envelope>"""

CHARGE_BODY = """<soapenv:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:pay="http://www.csapi.org/wsdl/parlayx/payment">
   <soapenv:Header/>
   <soapenv:Body>
      <pay:chargeReservation soapenv:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
         <reservationIdentifier xsi:type="xsd:string">672906749020369368</reservationIdentifier>
         <amount xsi:type="xsd:decimal">2</amount>
         <billingText xsi:type="xsd:string">oa</billingText>
         <referenceCode xsi:type="xsd:string">672907305196303896</referenceCode>
      </pay:chargeReservation>
   </soapenv:Body>
</soapenv:Envelope>"""


def doReserve(fromNumber):
	global RESERVE_BODY, HEADERS
	reserveHeaders = HEADERS
	reserveHeaders['SOAPAction'] = RESERVE_SOAP_ACTION
	RESERVE_BODY = re.sub(r'to:([0-9a-zA-Z]+)</value', f'to:{fromNumber}</value', RESERVE_BODY)
	res = requests.post(URL, data = RESERVE_BODY, headers = reserveHeaders)
	if (res.status_code != 200):
		print(f"Reserve got response code {res.status_code}")
		return 0
	id = re.findall(r'([0-9a-zA-Z]+)</result', res.text)[0]
	print(f"Reserve got response with transaction id {id}")
	return id


def doCharge(id):
	global CHARGE_BODY, HEADERS
	chargeHeaders = HEADERS
	chargeHeaders['SOAPAction'] = CHARGE_SOAP_ACTION
	CHARGE_BODY = re.sub(r'([0-9a-zA-Z]+)</referenceCode', f'{id}</referenceCode', CHARGE_BODY)
	CHARGE_BODY = re.sub(r'([0-9a-zA-Z]+)</reservationIdentifier', f'{id}</reservationIdentifier', CHARGE_BODY)
	res = requests.post(URL, data = CHARGE_BODY, headers = chargeHeaders)
	return res


def doTransaction(fromNumber):
	if RANDOMIZE_NUMBER_PER_MESSAGE:
		fromNumber = '385' + str(random.randint(1000000, 9999999))

	if RANDOMIZE_NUMBER_FROM_SET:
		while (len(NUMBER_SET) < GENERATE_N_NUMBERS):
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


keyboard.add_hotkey('ctrl+alt+p', runSchedule, args = (1, 10,))
keyboard.wait()
