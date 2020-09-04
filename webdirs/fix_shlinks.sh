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
        
	cat ${dir_path}/index.html | sed '/<script src="\/static\/poltergeist.js"><\/script>/a\\t\t<meta name=\"twitter:label1\" value=\"Listen to it here:\" \/>\n\t\t<meta name=\"twitter:data1\" value="{{ meta_url }}" />' > /tmp/index.html
	cp /tmp/index.html ${dir_path}/index.html

	echo "Fixed $dirname"
done
