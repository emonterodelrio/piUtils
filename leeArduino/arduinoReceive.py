#! /usr/bin/python
import serial

ser = serial.Serial('/dev/rfcomm0', 9600)

while True:
  result = ser.read()
  print result
