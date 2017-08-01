#!/bin/bash

# This will probably only work 100% properly on Ubuntu 14.04 (like what's installed on the VW-East RasPis)

error=0

cp apache-confs/* /etc/apache2/sites-available/
cp -r webdirs/* /var/www/

cd apache-confs
for site in $(ls *.conf | sed 's/\.conf//g'); do
	a2ensite $site >/dev/null 2>&1
	[ $? -ne 0 ] && echo "Error enabling $site site!" && error=1
done
cd ..

if [ $error -eq 0 ] ; then
	service apache2 reload
	echo "Sites successfully deployed!"
else
	echo "Sites not deployed!"
fi
