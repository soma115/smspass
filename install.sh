#!/usr/bin/env bash

yum -y install wget

# Dodaj EPEL repo aby zainstalowac Gnokii:
wget http://dl.fedoraproject.org/pub/epel/7/x86_64/e/epel-release-7-9.noarch.rpm
rpm -ivh epel-release-7-9.noarch.rpm

if yum -y install httpd gcc intltool spice-glib-devel gnokii
then
    echo "iptables -I INPUT -p tcp --dport 80 -j ACCEPT" >> /etc/rc.local
    iptables -I INPUT -p tcp --dport 80 -j ACCEPT
    chmod +x /etc/rc.d/rc.local

    mkdir -p /opt/bin/smspass
    cp ./smspass.py /opt/bin/smspass
    cp ./smspass.db /opt/bin/smspass
    echo "/opt/bin/smspass/smspass.py 2>/dev/null 1>>./log.txt &" >> /etc/rc.local
    sed -i 's/port = none/port = \/dev\/ttyUSB2/g' /etc/gnokiirc
    sed -i 's/model = fake/model = AT/g' /etc/gnokiirc
    sed -i 's/use_locking = yes/use_locking = no/g' /etc/gnokiirc
    sed -i 's/debug = on/debug = off/g' /etc/gnokiirc
    echo ">>> Wszystko poszlo dobrze <<<"
else
  echo ">>> Problem z instalacja <<<"
fi
