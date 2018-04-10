#!/bin/bash

systemctl=$(which systemctl 2>/dev/null)
dirname=$(readlink -f $(dirname $0))

if [ ! -f "$systemctl" ] ; then
    echo "Sorry, this install script only works on SystemD-based machines."
    exit 1
fi

cp $dirname/poltergeist-client.service /lib/systemd/system/
systemctl daemon-reload
systemctl enable poltergeist-client.service

echo "To start the poltergeist-client service run:"
echo "   systemctl start poltergeist-client.service"
