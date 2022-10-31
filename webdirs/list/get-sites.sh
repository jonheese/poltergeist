#!/bin/bash
#set -x

. /opt/poltergeist/webdirs/list/pilist.txt
HOSTNAME=$(which hostname)
hostname=$($HOSTNAME -f)
sites=$(find "${POLTERGEIST_DIR}/webdirs" -type d | sort)
suffix=".tv"$(echo "$site_pi_list" | grep $hostname | awk '{print $2}')

IFS=$'\n'

echo "<html>"
echo "<body>"

for site in $sites ; do
	site=$(basename $site)
	[ "$site" == "webdirs" ] && continue
	fqdn="${site}${suffix}"
	echo "<a href=\"http://${fqdn}\">http://${fqdn}</a><br />"
done

echo "</body>"
echo "</html>"
