#!/usr/bin/env python
import serial
ser = serial.Serial('/dev/rfcomm0', 9600, timeout=3)  # open serial port
print(ser.name)         # check which port was really used
line = ser.readline()
print line
ser.close()             # close port
