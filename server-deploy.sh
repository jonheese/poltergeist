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

    echo "Deleting/re-creating directories${onstring}..."
    do_cmd rm -rf /var/www/poltergeist/static
    do_cmd rm -rf /var/www/poltergeist/templates
    do_cmd rm -rf /opt/poltergeist
    do_cmd mkdir -p /var/www/poltergeist/static
    do_cmd mkdir -p /var/www/poltergeist/templates
    do_cmd mkdir -p /opt/poltergeist
    rsync -av $POLTERGEIST_DIR/* /opt/poltergeist/ 2>&1 >/dev/null
    rsync -av $POLTERGEIST_DIR/server/server.py /var/www/poltergeist/ 2>&1 >/dev/null

    echo "Symlinking files${tostring}..."
    do_cmd ln -s /opt/poltergeist/webdirs/* /var/www/poltergeist/static/ 2>/dev/null
    do_cmd ln -s /opt/poltergeist/webdirs/* /var/www/poltergeist/templates/ 2>/dev/null

    echo "Chowning directories${onstring}..."
    do_cmd chown -R www-data:www-data /var/www/poltergeist/

    echo "Restarting apache2 service${onstring}..."
    do_cmd systemctl restart apache2
}

POLTERGEIST_DIR="/root/poltergeist"
source config-local.conf
if [ "$LOCAL" -eq 1 ] ; then
    deploy
fi
for DEVICE in $SERVER_DEVICES ; do
    deploy $DEVICE
done
