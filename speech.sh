#!/bin/bash

INPUT=$*
STRINGNUM=0

user="www-data"

if [ "$(realpath -s $0)" == "/root/speech.sh" ] ; then
	PROGNAME="trump"
else
	PROGNAME="speech"
fi
output="/tmp/${PROGNAME}"

if [ -z "$INPUT" ] ; then
	echo "No input found"
	exit 0
fi

export DISPLAY="[0]:0"
ary=($INPUT)
for key in "${!ary[@]}" ; do
	SHORTTMP[$STRINGNUM]="${SHORTTMP[$STRINGNUM]} ${ary[$key]}"
	LENGTH=$(echo ${#SHORTTMP[$STRINGNUM]})
	#echo "word:$key, ${ary[$key]}"
	#echo "adding to: $STRINGNUM"
	if [[ "$LENGTH" -lt "100" ]]; then
		#echo starting new line
		SHORT[$STRINGNUM]=${SHORTTMP[$STRINGNUM]}
	else
		STRINGNUM=$(($STRINGNUM+1))
		SHORTTMP[$STRINGNUM]="${ary[$key]}"
		SHORT[$STRINGNUM]="${ary[$key]}"
	fi
done

rm -f ${output}*.mp3
keynum=0
for key in "${!SHORT[@]}" ; do
	#echo "line: $key is: ${SHORT[$key]}"
	#echo "Getting line: $(($key+1)) of $(($STRINGNUM+1))"
	NEXTURL=$(echo ${SHORT[$key]} | xxd -plain | tr -d '\n' | sed 's/\(..\)/%\1/g')
	if [ $UID -eq 0 ] ; then
		sudo -u $user wget -q -U "Mozilla" -O ${output}${keynum}.mp3 "http://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob&q=$NEXTURL&tl=En-us"
	else
		wget -q -U "Mozilla" -O ${output}${keynum}.mp3 "http://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob&q=$NEXTURL&tl=En-us"
	fi
	if [ $? -ne 0 ] ; then
		echo "Unable to play $NEXTURL"
		wgetcmd=wget -q -U "Mozilla" -O ${output}${keynum}.mp3 "http://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob&q=rururururururururururu&tl=En-us"
		if [ $UID -eq 0 ] ; then
			sudo -u $user $wgetcmd
		else
			$wgetcmd
		fi
	fi
	keynum=$(($keynum+1))
done

catcmd="/usr/bin/sox ${output}*.mp3 ${output}.mp3"
if [ $UID -eq 0 ] ; then
	sudo -u $user $catcmd
else
	$catcmd
fi
date=$(date)
echo "${date} - ${PROGNAME}: $*" >> /var/log/speech.log

playcmd="/usr/bin/play ${output}.mp3 silence 0 -1 0.0 0.1% pad 28000s@0:00"
if [ $UID -eq 0 ] ; then
	sudo -u $user $playcmd >/dev/null 2>&1
else
	$playcmd >/dev/null 2>&1
fi
#[ "$PROGNAME" == "speech" ] && rm -f ${output}*.mp3
