* * * * * bash -c "if [ ! "$(ps aux | grep leeTemperatura.py | grep -v grep)" ]; then cd /home/pi/Desktop/scripts && nohup  ./leeTemperatura.py >/home/pi/Desktop/scripts/leeTemperatura.log; fi"

