#!/bin/bash
#set -x

hostname=$(/bin/hostname)
apachectl=$(/usr/sbin/apachectl -S | grep -v hdmi)
root_sites=$(echo "$apachectl" | grep namevhost | awk '{print $4}' | sort)
all_sites=$(echo "$apachectl" | grep "namevhost\|alias")
sites=""

IFS=$'\n'

for root_site in $root_sites; do
	indent=""
	dns_lookup=$(dig +short $root_site)
	hostname_found=$(echo "$dns_lookup" | grep $hostname)
	[ -n "$hostname_found" ]&& sites=$(printf "%s\n@%s" "$sites" "$root_site") && indent="&nbsp;&nbsp;&nbsp;"
	possible_aliases=$(echo "$all_sites" | grep -A99 $root_site | tail -n+2)
	for possible_alias in $possible_aliases ; do
		namevhost_found=$(echo "$possible_alias" | grep "namevhost")
		[ -n "$namevhost_found" ] && break
		alias=$(echo "$possible_alias" | awk '{print $2}')
		dns_lookup=$(dig +short $alias)
		hostname_found=$(echo "$dns_lookup" | grep $hostname)
		[ -n "$hostname_found" ] && sites=$(printf "%s\n%s@%s" "$sites" "$indent" "$alias") && indent="&nbsp;&nbsp;&nbsp;"
	done
done

for site in $sites ; do
	raw_site="$site"
	site=$(echo "$site" | sed 's/&nbsp;//g')
	echo "<a href=\"$site\">$raw_site</a><br />" | sed 's/\@/http:\/\//g'
done
