#!/bin/bash

if [[ $(pwd) != *webdirs ]] ; then
	echo "You need to run this in webdirs"
	exit 1
fi

for dir_path in $(find . -type d); do
	dirname=$(basename $dir_path)
	[ "$dirname" == "." ] && continue
	if [ ! -f ${dir_path}/index.html ] ; then
		echo "Skipping $dirname"
		continue
	fi
	cat ${dir_path}/index.html | sed 's/href=\"/href=\"\/static\/'${dirname}'\//' | tr \' '"' > /tmp/index.html
	cat /tmp/index.html | sed 's/src=\"/src=\"\/static\/'${dirname}'\//' > ${dir_path}/index.html
	echo "Fixed $dirname"
done
