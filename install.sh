#!/usr/bin/env bash

# Dodaj EPEL repo aby zainstalowac Gnokii:
wget http://dl.fedoraproject.org/pub/epel/7/x86_64/e/epel-release-7-9.noarch.rpm
rpm -ivh epel-release-7-9.noarch.rpm

if yum -y install httpd wget gcc intltool spice-glib-devel gnokii
then
  echo ">>> Zainstalowałem: httpd wget gcc intltool spice-glib-devel gnokii <<<"
else
  echo ">>> Problem z instalacją: httpd wget gcc intltool spice-glib-devel gnokii <<<"
fi

echo "iptables -I INPUT -p tcp --dport 80 -j ACCEPT" >> /etc/rc.local
iptables -I INPUT -p tcp --dport 80 -j ACCEPT
chmod +x /etc/rc.d/rc.local

mkdir -p /opt/bin/smspass
cp ./smspass.py /opt/bin/smspass
cp ./smspass.db /opt/bin/smspass
echo `pwd`"/smspass.py &" >> /etc/rc.local
sed -i 's/port = none/port = \/dev\/ttyUSB0/g' /etc/gnokiirc
sed -i 's/model = fake/model = AT/g' /etc/gnokiirc
sed -i 's/use_locking = yes/use_locking = no/g' /etc/gnokiirc

