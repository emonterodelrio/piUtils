#!/usr/bin/env python
# -*- coding: utf-8 -*-
#* * * * * bash -c "if [ ! "$(ps aux | grep leeTemperatura.py | grep -v grep)" ]; then cd /home/pi/Desktop/scripts && nohup  ./leeTemperatura.py &>> /home/pi/Desktop/scripts/leeTemperatura.log; fi"

import sys
import os
from time import sleep
import Adafruit_DHT
import requests
from Adafruit_BMP085 import BMP085

api_keys = ["", "", "", ""]

myDelay = 900 #how many seconds between posting data

#Sensors
#sensor = Adafruit_DHT.DHT11
sensor = Adafruit_DHT.DHT22
pin = 23

# Initialise the BMP085 and use STANDARD mode (default value)
# bmp = BMP085(0x77, debug=True)
bmp = BMP085(0x77)


def readTempHumHPa():
  try:
    print "Reading"

    temp2 = bmp.readTemperature()
    sleep(1)
    # Read the current barometric pressure level
    prs = bmp.readPressure()
    sleep(1)
    # To calculate altitude based on an estimated mean sea level pressure
    # (1013.25 hPa) call the function as follows, but this won't be very accurate
    alt = bmp.readAltitude()
    sleep(1)

    hum ,temp = Adafruit_DHT.read_retry(sensor, pin)
    sleep(1)
  except Exception:
    print "Error gettin info from sensor"  

  print "Hum " + str(hum)
  print "Temp " + str(temp)
  print "Temp2 %.2f C" % temp2
  print "hPa %.2f hPa" % (prs/100.0)
  print "Alt %.2f" % alt
  if temp is not None and hum is not None:
    temp = round( temp,2 )
    hum = round( hum, 2 )
    temp2 = round( temp2, 2 )
    prs = round( (prs/100.0), 2 )
    alt = round( alt, 2 )
    return (float(hum), temp, temp2, prs, alt)
  else:
    return (10,10,10,10,10)

def main():
    global hum, temp, temp2, prs, alt
    print "--- Init ---"
    hum, temp, temp2, prs, alt = readTempHumHPa()
    print "------------"
    while True:
      print
      hum, temp, temp2, prs, alt = readTempHumHPa()
      print "Sending\t\t\t\t\tt = " + str(temp)+ "ºC \t\th =  " + str(hum) + " %\t\t" + str(temp2) + " ºC\t\t" + str(prs) + " hPa\t\t" + str(alt) + " m"
      for key in range(len(api_keys)):
        print "url = \"https://api.thingspeak.com/update?api_key=" + api_keys[key] + "&field1=" + str(hum) + "&field2=" + str(temp) + "&field3=" + str(temp2) + "&field4=" + str(prs) + "&field5=" + str(alt)
        url = "https://api.thingspeak.com/update?api_key=" + api_keys[key] + "&field1=" + str(hum) + "&field2=" + str(temp) + "&field3=" + str(temp2) + "&field4=" + str(prs) + "&field5=" + str(alt)
        r = requests.get(url)
        r.json()
        # Update Avg
      print "Goin to sleep " +  str (myDelay) + " seconds"
      sleep(int(myDelay))

if __name__ == '__main__':
  main()
