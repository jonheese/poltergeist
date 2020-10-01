#!/bin/bash

GOOGLE_TRANSLATE_LIMIT=0

function download_sound_file() {
	INPUT=$*
	if [ ${#INPUT} -lt 100 ] || [ $GOOGLE_TRANSLATE_LIMIT -lt 1 ] ; then
		download_single_file $INPUT
	else
		download_multiple_files $INPUT
	fi
}

function download_multiple_files() {
	STRINGNUM=0
	ary=($*)
	for key in "${!ary[@]}" ; do
		SHORTTMP[$STRINGNUM]="${SHORTTMP[$STRINGNUM]} ${ary[$key]}"
		LENGTH=$(echo ${#SHORTTMP[$STRINGNUM]})
		if [[ "$LENGTH" -lt "100" ]]; then
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
		NEXTURL=$(echo ${SHORT[$key]} | xxd -plain | tr -d '\n' | sed 's/\(..\)/%\1/g')
		wget -q -U "Mozilla" -O ${output}${keynum}.mp3 "http://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob&q=$NEXTURL&tl=En-us"
		if [ $? -ne 0 ] ; then
			echo "Unable to play $NEXTURL"
			wgetcmd=wget -q -U "Mozilla" -O ${output}${keynum}.mp3 "http://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob&q=rururururururururururu&tl=En-us"
			$wgetcmd
		fi
		keynum=$(($keynum+1))
	done

	catcmd="/bin/cat ${output}*.mp3"
	$catcmd > ${output}.mp3
}

function download_single_file() {
	query=$(echo $* | xxd -plain | tr -d '\n' | sed 's/\(..\)/%\1/g')
	wget -q -U "Mozilla" -O ${output}.mp3 "http://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob&q=$query&tl=En-us"
}

INPUT=$*
PROGNAME=$(echo $0 | awk -F'.' '{print $(NF-1)}' | awk -F'/' '{print $NF}')
output="/tmp/${PROGNAME}"

if [ -z "$INPUT" ] ; then
	echo "No input found"
	exit 0
fi

export DISPLAY="[0]:0"
download_sound_file "$INPUT"

date=$(date)
if [ -f "/var/log/speech.log" ] ; then
    echo "${date} - ${PROGNAME}: $*" >> /var/log/speech.log
fi

playcmd="/usr/bin/afplay ${output}.mp3"
$playcmd >/dev/null 2>&1
#rm -f /tmp/${PROGNAME}*.mp3
