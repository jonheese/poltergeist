#!/bin/bash

# This will probably only work 100% properly on Ubuntu 14.04 (like what's installed on the VW-East RasPis)

error=0

if [ -n "$1" ] ; then
	ssh="ssh $1"
	dest="${1}:"
	tostring=" to $1"
	onstring=" on $1"
fi

echo "Coping files${tostring}..."
rsync -av apache-confs/* ${dest}/etc/apache2/sites-available/
rsync -av webdirs/* ${dest}/var/www/
rsync -av speech.sh ${dest}/usr/bin/

echo ""
echo "Installing speech script${onstring}..."
$ssh "rm -f /root/speech.sh; ln -s /usr/bin/speech.sh /root/speech.sh; touch /var/log/speech.log; chown www-data:www-data /var/log/speech.log"

echo ""
echo "Ensuring speech user is present${onstring}..."
$ssh "id -u speech >/dev/null 2>&1; [ \$? -ne 0 ] && useradd -s /bin/bash -m speech"

echo ""
echo "Enabling sites${onstring}..."
cd apache-confs
for site in $(ls *.conf | sed 's/\.conf//g'); do
	echo " - ${site}"
	$ssh a2ensite $site >/dev/null 2>&1
	[ $? -ne 0 ] && echo "Error enabling $site site!" && error=1
done
cd ..

if [ $error -eq 0 ] ; then
	$ssh service apache2 reload
	[ $? -ne 0 ] && echo "Error reloading apache2 service!" && exit 1
	echo "Sites successfully deployed${tostring}!"
else
	echo "Sites not deployed${tostring}!"
fi
echo ""
