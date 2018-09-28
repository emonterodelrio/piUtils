#!/bin/bash
#This script setup crontabs if not exists

mkdir -p /home/pi/Desktop/scripts/leeTemperatura/
mkdir -p /home/pi/Desktop/scripts/who/

cp ./leeTemperatura/* /home/pi/Desktop/scripts/leeTemperatura/
cp ./who* /home/pi/Desktop/scripts/who/

grep 'leeTemperatura.py' /etc/crontab || echo '* * * * * bash -c "if [ ! "$(ps aux | grep leeTemperatura.py | grep -v grep)" ]; then cd /home/pi/Desktop/scripts/leeTemperatura/ && nohup  ./leeTemperatura.py &>> /home/pi/Desktop/scripts/leeTemperatura/leeTemperatura.log; fi"' >> /etc/crontab

grep 'who.sh' /etc/crontab || echo '* * * * * bash -c "if [ ! "$(ps aux | grep who.sh | grep -v grep)" ]; then cd /home/pi/Desktop/scripts/who/ && nohup  ./who.sh &>> /home/pi/Desktop/scripts/who/whoNohup.log; fi"' >> /etc/crontab

