#!/usr/bin/env python3

import time
# import json
from dronekit import Hangar
import httplib2
http = httplib2.Http()

hangar = Hangar()
for i in range(10):
    hangar.lights_on()
    hangar.open()
    time.sleep(1)
    hangar.lights_off()
    hangar.stop()
    time.sleep(10)
    hangar.lights_on()
    hangar.close()
    time.sleep(1)
    hangar.lights_off()
    hangar.stop()
    time.sleep(10)

# Para enviar ddados
#PATH = data = 'lights_off'
#PATH = '80'
#IP = '192.168.1.21'  # Standard loopback interface address (localhost)
#url = "http://" + IP + '/' + PATH
#print(url)

#response, content = http.request(url, "PUT", body=data)
#print(response)
#time.sleep(200)
#print("Activating LED")

# PATH = 'stop'
# url = "http://" + IP + '/' + PATH
# data = 'stop'
# print(url)
#
# response, content = http.request(url, "PUT", body=data)
# print(response)
# print("Stopping")
