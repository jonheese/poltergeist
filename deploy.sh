#!/bin/bash

# This will probably only work 100% properly on Ubuntu 14.04 (like what's installed on the VW-East RasPis)

function do_cmd() {
	cmd=$*
	[ -n "$ssh" ] && $ssh "$cmd" || $cmd
}

function deploy() {
    dest=""
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
    do_cmd /root/poltergeist/misc_setup.sh

    echo ""
    echo "Installing speech script${onstring}..."
    do_cmd rm -f /root/speech.sh
    do_cmd ln -s /usr/bin/speech.sh /root/speech.sh
    do_cmd touch /var/log/speech.log
    do_cmd ln -s /usr/bin/play /usr/bin/play-unkillable 2>/dev/null
    do_cmd chown www-data:www-data /var/log/speech.log

    echo ""
    echo "Ensuring speech user is present${onstring}..."
    do_cmd id -u speech >/dev/null 2>&1
    [ $? -ne 0 ] && do_cmd useradd -s /bin/bash -m speech

    echo ""
    echo "Getting apache config${onstring}..."
    apachectl=$(do_cmd apachectl -S)

    echo ""
    echo "Copying poltercron to /etc/cron.d${onstring}..."
    rsync -av poltercron ${dest}/etc/cron.d/

    echo ""
    echo "Enabling sites${onstring}..."
    cd apache-confs
    for site in $(ls *.conf | sed 's/\.conf//g'); do
	    found=$(echo $apachectl | grep " $site\.")
    	[ -n "$found" ] && continue
	    echo " - ${site}"
    	do_cmd a2ensite $site >/dev/null 2>&1
	    [ $? -ne 0 ] && echo "Error enabling $site site!" && error=1
    done
    cd ..

    echo ""
    echo "Removing sites${onstring}..."
    if [ -s deletion_list.txt ] ; then
        for site in $(cat deletion_list.txt) ; do
            found=$(echo "$apachectl" | grep " $site\.")
            [ -z "$found" ] && continue
            echo " - ${site}"
            do_cmd a2dissite $site >/dev/null 2>&1
            [ $? -ne 0 ] && echo "Error disabling $site site!" && error=1
            do_cmd rm -rf /var/www/${site}
            [ $? -ne 0 ] && echo "Error removing $site content!" && error=1
            do_cmd rm -rf /etc/apache2/sites-available/${site}.conf
            [ $? -ne 0 ] && echo "Error removing $site config!" && error=1
        done
    fi

    echo "Disabling PHP safe_mode${onstring}..."
    rsync -av disable_php_safe_mode.sh ${dest}/root/
    do_cmd /root/disable_php_safe_mode.sh

    if [ $error -eq 0 ] ; then
    	do_cmd service apache2 reload
    	do_cmd systemctl daemon-reload
    	[ $? -ne 0 ] && echo "Error reloading apache2 service!" && return 1
    	echo "Sites successfully deployed${tostring}!"
    else
    	echo "Sites not deployed${tostring}!"
    fi
    echo ""
}

source config-local.conf
if [ "$LOCAL" -eq 1 ] ; then
    deploy
fi
for DEVICE in $DEVICES ; do
    deploy $DEVICE
done
