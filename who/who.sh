#!/bin/bash
while true; do
  date >> /home/pi/Desktop/who.log
  who >> /home/pi/Desktop/who.log
  sleep 10;
done
