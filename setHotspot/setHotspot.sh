#!/bin/bash
if [ $# -ne 0 ];then
  printf "\033[1;31m\n\n You have to pass nothing, like:\nsudo ./setHotspot.sh\033[0m\n"
  exit 1
fi	


if [ `whoami` = root ]; then



  if [ -z "$(cat /etc/apt/sources.list | grep "ftp.es.debian")" ];then
    printf "\033[1;32m\n\nAdd es repo\033[0m\n"
    echo "deb http://ftp.es.debian.org/debian sid main" >>/etc/apt/sources.list
  fi

  printf "\033[1;32m\n\nDelete dnsmasq if exists\033[0m\n"
  dpkg -s dnsmasq
  apt-get purge -y dns-root-data

  printf "\033[1;32m\n\napt-get update and upgrade\033[0m\n"
  apt-get update -y

  printf "\033[1;32m\n\nInstall hostapd\033[0m\n"
  apt-get install -y hostapd

  printf "\033[1;32m\n\nInstall dnsmasq\033[0m\n"
  apt-get install -y dnsmasq

  printf "\033[1;32m\n\nSystemctl daemon-reload\033[0m\n"
  systemctl daemon-reload

  printf "\033[1;32m\n\nDisable hostapd at boot\033[0m\n"
  systemctl disable hostapd

  printf "\033[1;32m\n\nDisable dnsmasq at boot\033[0m\n"
  systemctl disable dnsmasq

  printf "\033[1;32m\n\nConfigure myHotSpot.conf\033[0m\n"

  tee /etc/myHotSpot.conf <<EOF

  #2.4GHz setup wifi 80211 b,g,n
  interface=wlan0
  driver=nl80211
  ssid=meteopi
  hw_mode=g
  channel=8
  wmm_enabled=0
  macaddr_acl=0
  auth_algs=1
  ignore_broadcast_ssid=0
  wpa=2
  wpa_passphrase=1234567890
  wpa_key_mgmt=WPA-PSK
  wpa_pairwise=CCMP TKIP
  rsn_pairwise=CCMP

  #80211n - Change GB to your WiFi country code
  country_code=ES
  ieee80211n=1
  ieee80211d=1

EOF

else
  printf "\033[1;31m\n\nMust be run as:\nsudo ./setHotspot.sh\033[0m\n"
  exit 1
fi

