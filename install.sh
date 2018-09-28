#!/bin/bash
#This script setup crontabs if not exists

if [ $# -ne 1 ];then
  printf "\033[1;31m\n\n You have to pass dht_22 GPIO pin, like:\nsudo ./install.sh 17\033[0m\n"
  exit 1
else
  PIN=$1
fi	


if [ `whoami` = root ]; then


  printf "\033[1;32m\n\n Updating apt-get\033[0m\n"

  apt-get update
  sleep 2
  echo
  printf "\033[1;32m\n\Install curl, vim, telnet....\033[0m\n"
  apt-get install vim curl telnet
  sleep 2

  printf "\033[1;32m\n\nInstall pip, setup tools and wheel\033[0m\n"
  apt-get install python-pip
  sleep 2
  python -m pip install --upgrade pip setuptools wheel

  printf "\033[1;32m\n\nInstall Adafruit _DHT22 required stuff\033[0m\n"
  pip install Adafruit_DHT

  printf "\033[1;32m\n\necho Creating folders\033[0m\n"
  mkdir -p /home/pi/Desktop/scripts/logs/
  mkdir -p /home/pi/Desktop/scripts/leeTemperatura/
  mkdir -p /home/pi/Desktop/scripts/logs/leeTemperatura/
  mkdir -p /home/pi/Desktop/scripts/who/
  mkdir -p /home/pi/Desktop/scripts/logs/who/

  printf "\033[1;32m\n\nCopying scripts\033[0m\n"
  cp ./leeTemperatura/* /home/pi/Desktop/scripts/leeTemperatura/
  cp ./who/* /home/pi/Desktop/scripts/who/

  printf "\033[1;32m\n\nSetting up crontabs\033[0m\n"
  if [ -z "$(crontab -l -u pi | grep leeTemperatura)" ];then
    echo "* * * * * bash -c 'if [ ! \"\$(ps aux | grep leeTemperatura.py | grep -v grep)\" ]; then cd /home/pi/Desktop/scripts/leeTemperatura/ && nohup  ./leeTemperatura.py &>> /home/pi/Desktop/scripts/logs/leeTemperatura/leeTemperatura.log; fi'" >> /var/spool/cron/crontabs/pi
  fi

  if [ -z "$(crontab -l -u pi | grep who)" ];then
    echo "* * * * * bash -c 'if [ ! \"\$(ps aux | grep who.sh | grep -v grep)\" ]; then cd /home/pi/Desktop/scripts/who/ && nohup  ./who.sh &>> /home/pi/Desktop/scripts/logs/who/who.log; fi'" >> /var/spool/cron/crontabs/pi
  fi
else
  printf "\033[1;31m\n\nMust be run as:\nsudo ./install.sh 17\033[0m\n"
  exit 1
fi


printf "\033[1;32m\n\necho Setting port at leeTemperatura.py\033[0m\n"
sed -i "/pin = /c\pin = ${PIN}" /home/pi/Desktop/scripts/leeTemperatura/leeTemperatura.py


printf "\033[1;32m\n\n#######################\nNow insert your thinkiverse api keys at:\nvi /home/pi/Desktop/scripts/leeTemperatura/leeTemperatura.py\033[0m\n"
