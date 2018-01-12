#!/bin/bash
#set -x

. /var/www/list/pilist.txt
hostname=$(/bin/hostname | cut -d'.' -f1)
apachectl=$(/usr/sbin/apachectl -S 2>/dev/null | grep -v hdmi)
root_sites=$(echo "$apachectl" | grep namevhost | awk '{print $4}' | sort)
all_sites=$(echo "$apachectl" | grep "namevhost\|alias")
my_sites=$(echo "$site_pi_list" | grep $hostname | cut -d' ' -f2-)
sites=""

IFS=$'\n'

function is_my_site {
	hostname_found=""
	for my_site in $my_sites ; do
		hostname_found=$(echo "$1" | grep "$my_site")
		[ -n "$hostname_found" ] && break
	done
}

for root_site in $root_sites; do
	indent=""
	is_my_site $root_site
	[ -n "$hostname_found" ] && sites=$(printf "%s\n@%s" "$sites" "$root_site") && indent="&nbsp;&nbsp;&nbsp;"
	possible_aliases=$(echo "$all_sites" | grep -A99 $root_site | tail -n+2)
	for possible_alias in $possible_aliases ; do
		namevhost_found=$(echo "$possible_alias" | grep "namevhost")
		[ -n "$namevhost_found" ] && break
		alias=$(echo "$possible_alias" | awk '{print $2}')
		is_my_site $alias
		[ -n "$hostname_found" ] && sites=$(printf "%s\n%s@%s" "$sites" "$indent" "$alias") && indent="&nbsp;&nbsp;&nbsp;"
	done
done

for site in $sites ; do
	raw_site="$site"
	site=$(echo "$site" | sed 's/&nbsp;//g')
	echo "<a href=\"$site\">$raw_site</a><br />" | sed 's/\@/http:\/\//g'
done
