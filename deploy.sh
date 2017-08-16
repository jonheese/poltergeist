#!/bin/bash

# This will probably only work 100% properly on Ubuntu 14.04 (like what's installed on the VW-East RasPis)

function do_cmd() {
	cmd=$*
	[ -n "$ssh" ] && $ssh "$cmd" || $cmd
}

error=0

if [ -n "$1" ] ; then
	ssh="ssh $1"
	dest="${1}:"
	tostring=" to $1"
	onstring=" on $1"
fi

echo "Copying files${tostring}..."
rsync -av apache-confs/* ${dest}/etc/apache2/sites-available/
rsync -av webdirs/* ${dest}/var/www/
rsync -av speech.sh ${dest}/usr/bin/

echo ""
echo "Installing speech script${onstring}..."
do_cmd rm -f /root/speech.sh
do_cmd ln -s /usr/bin/speech.sh /root/speech.sh
do_cmd touch /var/log/speech.log
do_cmd chown www-data:www-data /var/log/speech.log

echo ""
echo "Ensuring speech user is present${onstring}..."
do_cmd id -u speech >/dev/null 2>&1
[ $? -ne 0 ] && do_cmd useradd -s /bin/bash -m speech

echo ""
echo "Enabling sites${onstring}..."
cd apache-confs
for site in $(ls *.conf | sed 's/\.conf//g'); do
	echo " - ${site}"
	do_cmd a2ensite $site >/dev/null 2>&1
	[ $? -ne 0 ] && echo "Error enabling $site site!" && error=1
done
cd ..

if [ $error -eq 0 ] ; then
	do_cmd service apache2 reload
	[ $? -ne 0 ] && echo "Error reloading apache2 service!" && exit 1
	echo "Sites successfully deployed${tostring}!"
else
	echo "Sites not deployed${tostring}!"
fi
echo ""
