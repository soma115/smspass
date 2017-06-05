#!/usr/bin/env bash

if yum -y install httpd wget gcc intltool spice-glib-devel
then
  echo ">>> Zainstalowałem: httpd wget gcc intltool spice-glib-devel <<<"
else
  echo ">>> Problem z instalacją: httpd wget gcc intltool spice-glib-devel <<<"
fi

if yum -y install gnokii
then
  echo ">>> Udało się <<<"
else
  echo ">>> Muszę skompilować gnokii. Poczekaj minutkę. <<<"
  yum -y install httpd wget gcc intltool spice-glib-devel ; cd
  wget https://www.gnokii.org/download/gnokii/0.6.x/gnokii-0.6.31.tar.gz
  tar -xzf ./gnokii-0.6.31.tar.gz ; cd gnokii-0.6.31 ; ./configure ; gmake ; gmake install
fi

echo "iptables -I INPUT -p tcp --dport 80 -j ACCEPT" >> /etc/rc.local
iptables -I INPUT -p tcp --dport 80 -j ACCEPT
chmod +x /etc/rc.d/rc.local

mkdir -p /opt/bin/smspass
cp ./* /opt/bin/smspass
echo `pwd`"/smspass.py &" >> /etc/rc.local
sed -i 's/port = none/port = \/dev\/ttyUSB0/g' /etc/gnokiirc
sed -i 's/model = fake/model = AT/g' /etc/gnokiirc
sed -i 's/use_locking = yes/use_locking = no/g' /etc/gnokiirc

