import requests
import keyboard
import datetime

url = "http://localhost:7080/test/mo"

querystring = {"count": "1", "to": "bss", "text": "0651440", "from": "38765482530"}

payload = ""

def sendMessage():
	resp = requests.request("GET", url, data=payload, params=querystring)
	print(f'{datetime.datetime.now()} - {resp.text}')

keyboard.add_hotkey('ctrl+alt+m', sendMessage)
keyboard.wait()
