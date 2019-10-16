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

    echo -n "Copying files${tostring}... "
    rsync -av apache-confs/* ${dest}/etc/apache2/sites-available/ 2>&1 >/dev/null
    rsync -av webdirs/* ${dest}/var/www/ 2>&1 >/dev/null
    rsync -av speech.sh ${dest}/usr/bin/ 2>&1 >/dev/null
    rsync -av $POLTERGEIST_DIR/client/client.py  ${dest}/root/poltergeist/client/ 2>&1 >/dev/null
    do_cmd /root/poltergeist/misc_setup.sh
    echo "Done"

    echo -n "Installing speech script${onstring}... "
    do_cmd rm -f /root/speech.sh
    do_cmd ln -s /usr/bin/speech.sh /root/speech.sh
    do_cmd touch /var/log/speech.log
    do_cmd ln -s /usr/bin/play /usr/bin/play-unkillable 2>/dev/null
    do_cmd chown www-data:www-data /var/log/speech.log
    echo "Done"

    echo -n "Ensuring speech user is present${onstring}... "
    do_cmd id -u speech >/dev/null 2>&1
    [ $? -ne 0 ] && do_cmd useradd -s /bin/bash -m speech
    echo "Done"

    echo -n "Getting apache config${onstring}... "
    apachectl=$(do_cmd apachectl -S)
    echo "Done"

    echo -n "Copying poltercron to /etc/cron.d${onstring}... "
    rsync -av poltercron ${dest}/etc/cron.d/ 2>&1 >/dev/null
    echo "Done"

    if [ $FULL -eq 1 ] ; then
        echo -n "Enabling sites${onstring}... "
        cd apache-confs
        for site in $(ls *.conf | sed 's/\.conf//g'); do
            found=$(echo $apachectl | grep " $site\.")
    	    [ -n "$found" ] && continue
            echo " - ${site}"
    	    do_cmd a2ensite $site >/dev/null 2>&1
            [ $? -ne 0 ] && echo "Error enabling $site site!" && error=1
        done
        cd ..
        echo "Done"

        echo -n "Removing sites${onstring}..."
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
        echo "Done"
    fi

    echo -n "(Re)starting Poltergeist Client service${onstring}... "
    if [ $error -eq 0 ] ; then
    	do_cmd systemctl daemon-reload
    	do_cmd systemctl restart poltergeist-client
    	[ $? -ne 0 ] && echo "Error reloading poltergeist-client service!" && return 1
    	echo "Poltergeist client successfully deployed${tostring}!"
    else
    	echo "Poltergeist client not deployed${tostring}!"
    fi
}

FULL=0
if [ -n "$1" ] ; then
    FULL=1
fi

source config-local.conf
if [ "$LOCAL" -eq 1 ] ; then
    deploy
fi
for DEVICE in $DEVICES ; do
    deploy $DEVICE
done
