#!/usr/bin/env python
import sys
import os
from time import sleep
import Adafruit_DHT
import requests

api_keys = ["X", "X", "X", "X"]

myDelay = 300 #how many seconds between posting data

#Sensors
#sensor = Adafruit_DHT.DHT11
sensor = Adafruit_DHT.DHT22
pin = 23

def readTempHum():
  try:
    print "Leo"
    hum ,temp = Adafruit_DHT.read_retry(sensor, pin)
  except Exception:
    print "Error gettin info from sensor"  

  print "Hum " + str(hum)
  print "Temp " + str(temp)
  if temp is not None and hum is not None:
    temp = round( temp,2 )
    hum = round( hum, 2 )
    return (float(hum), temp)
  else:
    return (10,10)

def main():
    global hum, temp
    print "Init"
    hum, temp = readTempHum()

    while True:
      print "Leo"
      hum, temp = readTempHum()
      print "Envio!" + str(hum)+ " " + str(temp)
      for key in range(len(api_keys)):
        url = "https://api.thingspeak.com/update?api_key=" + api_keys[key] + "&field1=" + str(hum) + "&field2=" + str(temp)
        r = requests.get(url)
        r.json()
        # Update Avg
      sleep(int(myDelay))

if __name__ == '__main__':
  main()

