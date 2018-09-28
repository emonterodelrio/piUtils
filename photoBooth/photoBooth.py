#!/usr/bin/python
# a simple script for using the tactile buttons on the TFT
#* * * * * if [ -z $(ps aux | grep photoBooth.py  | grep -v grep | awk '{print $NF}') ]; then mkdir -p /home/pi/Desktop/scripts/logs/ && nohup /home/pi/Desktop/scripts/photoBooth/photoBooth.py >> /home/pi/logs/photoBooth.log; fi

import RPi.GPIO as GPIO
import time
import os

# Use Broadcom SOC Pin Numbers
# setup with internal pullups and pin in READ mode

GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(22, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(27, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(18, GPIO.IN, pull_up_down = GPIO.PUD_UP)

#  Main Loop

while 1:
  os.system("clear > /dev/tty1 && echo 'Menu:\n 1-TestCamera\n 2-Photo\n 3-Photo2Usb' > /dev/tty1")  
  time.sleep(.22)
  if ( GPIO.input(23) == False ):
    os.system("/home/pi/Desktop/scripts/photoBooth/takePhotoAndShow > /dev/tty1")
    time.sleep(1)
    os.system("clear > /dev/tty1")
  elif ( GPIO.input(22) == False ):
    os.system("clear > /dev/tty1 && echo 'Capturing, press 4444rd button to skip\n' > /dev/tty1")  
    os.system("for i in $(seq 7 -1 1); do sleep .7 && echo $i > /dev/tty1; done")
    count = 0
    while 1:
      count += 1
      #if ( count > 100 ):
      time.sleep(.1)
      #  os.system("echo '0' > /sys/class/backlight/soc\:backlight/brightness'")
      if ( ( count % 300 ) == 0) :
        print count  
        os.system("/home/pi/Desktop/scripts/photoBooth/takePhoto > /dev/tty1")  
        time.sleep(1)
      if ( GPIO.input(18) == False ):
        #os.system("echo '1' > /sys/class/backlight/soc\:backlight/brightness'")
        os.system("clear > /dev/tty1 && echo Quitting > /dev/tty1")
        time.sleep(.5)
        break
  elif ( GPIO.input(27) == False ):
    os.system("clear > /dev/tty1 && echo 'Copying files' > /dev/tty1")
    os.system("if [ ! -z $(lsblk | grep sda | head -n1 | awk '{print $1}') ]; then sudo mkdir -p /mnt/usb && sudo chmod 770 /mnt/usb && sudo mount /dev/sda1 /mnt/usb; mkdir -p /mnt/usb/camera && mv /home/pi/camera/*.jpg /mnt/usb/camera/ | pv 2> /dev/tty1; sudo umount /mnt/usb; else echo Usb not present > /dev/tty1; fi")
    os.system("echo > /dev/tty1 && echo 'All files copied' > /dev/tty1")
    time.sleep(3)
