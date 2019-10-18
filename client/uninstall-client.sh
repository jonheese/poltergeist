#!/bin/bash

systemctl=$(which systemctl 2>/dev/null)

echo "NOTE: You must enter your sudo password to perform this uninstall"

if [ ! -f "$systemctl" ] ; then
	if [ ! -d "/Library/LaunchAgents/" ] ; then
		echo "systemctl not found (not running SystemD) and this doesn't appear to be MacOS."
		echo "Unable to uninstall Poltergeist client!"
		exit 1
	else
		# MacOS
		launchctl unload /Library/LaunchAgents/com.jonheese.poltergeist-client.plist
		sudo rm -f /Library/LaunchAgents/com.jonheese.poltergeist-client.plist
	
		echo "The poltergeist-client service has been stopped and removed"
	fi
else
	# Linux (Ubuntu 18.04+ or RHEL/CentOS 7+)
	sudo systemctl disable poltergeist-client.service
	sudo systemctl stop poltergeist-client.service
	sudo rm -f /lib/systemd/system/poltergeist-client.service
	sudo systemctl daemon-reload

	echo "The poltergeist-client service has been stopped and removed"
fi
