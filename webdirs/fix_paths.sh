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

	cat ${dir_path}/index.html | sed "s/<body>/<body onload=\"set_mp3_source(\'${dirname}\')\">/" > /tmp/index1.html
	cat /tmp/index1.html | sed '/<\/title>/a\\t\t<script src="\/static\/poltergeist.js"><\/script>' > /tmp/index2.html
	cat /tmp/index2.html | sed 's/<audio controls>/<audio controls id="player">/' > ${dir_path}/index.html

	echo "Fixed $dirname"
done
