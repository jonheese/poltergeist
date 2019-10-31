#!/bin/bash

systemctl=$(which systemctl 2>/dev/null)

echo "NOTE: You must enter your sudo password to perform this install"

if [ ! -f "$systemctl" ] ; then
	# Not SystemD
	if [ ! -d "/Library/LaunchAgents/" ] ; then
		echo "systemctl not found (not running SystemD) and this doesn't appear to be MacOS."
		echo "Unable to install Poltergeist client!"
		exit 1
	else
		# MacOS
		dirname=$( ( cd $(dirname "$0") && echo $(pwd) ) )
		plist="/Library/LaunchAgents/com.jonheese.poltergeist-client.plist"
		sudo cp $dirname/com.jonheese.poltergeist-client.plist /Library/LaunchAgents/
		sudo chown root:wheel $plist
		sudo chmod 0644 $plist
		sudo sed -i ""  "s,@@CLIENT_DIR@@,$dirname,g" $plist

		echo "The poltergeist-client service has been installed and will start automatically on your next login."
		echo "To start the poltergeist-client service run:"
		echo "   launchctl load /Library/LaunchAgents/com.jonheese.poltergeist-client.plist"
	fi
else
	# Linux (Ubuntu 18.04+ or RHEL/CentOS 7+)
	dirname=$(readlink -f $(dirname $0))
	apt=$(which apt)
	if [ -n "$apt" ] ; then
		# Ubuntu/Debian
		sudo apt update
		sudo apt install -y sox libsox-fmt-mp3 python-pip
	else
		# RHEL/CentOS
		sudo yum install -y sox python-pip
		echo "++++++++++++ YOU WILL NEED TO FIND/BUILD/INSTALL AN MP3 CODEC FOR sox BEFORE THIS WILL PLAY ++++++++++++"
	fi
	sudo pip install -y requests
	sudo cp $dirname/poltergeist-client.service /lib/systemd/system/
	sudo sed -i "s,@@CLIENT_DIR@@,$dirname,g" /lib/systemd/system/poltergeist-client.service
	sudo systemctl daemon-reload
	sudo systemctl enable poltergeist-client.service

	echo "The poltergeist-client service has been installed and will start automatically on your next login."
	echo "To start the poltergeist-client service run:"
	echo "   systemctl start poltergeist-client.service"
fi
