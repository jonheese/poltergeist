#!/bin/bash

# This will probably only work 100% properly on Ubuntu 14.04 (like what's installed on the VW-East RasPis)

cp apache-confs/* /etc/apache2/sites-available/
cp -r webdirs/* /var/www/

for site in $(ls apache-confs/*.conf | sed -i 's/\.conf//'); do
	a2ensite $site
done

service apache2 reload
