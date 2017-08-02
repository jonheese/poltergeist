#!/bin/bash

# This will probably only work 100% properly on Ubuntu 14.04 (like what's installed on the VW-East RasPis)

error=0

if [ -n "$1" ] ; then
	ssh="ssh $1"
	dest="${1}:"
fi

rsync -av apache-confs/* ${dest}/etc/apache2/sites-available/
rsync -av webdirs/* ${dest}/var/www/

cd apache-confs
for site in $(ls *.conf | sed 's/\.conf//g'); do
	$ssh a2ensite $site >/dev/null 2>&1
	[ $? -ne 0 ] && echo "Error enabling $site site!" && error=1
done
cd ..

if [ $error -eq 0 ] ; then
	$ssh service apache2 reload
	[ $? -ne 0 ] && echo "Error reloading apache2 service!" && exit 1
	echo "Sites successfully deployed!"
else
	echo "Sites not deployed!"
fi
