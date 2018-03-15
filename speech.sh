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

	catcmd="/bin/cat ${output}*.mp3"
	if [ $UID -eq 0 ] ; then
		sudo -u $user $catcmd > ${output}.mp3
	else
		$catcmd > ${output}.mp3
	fi
}

function download_single_file() {
	query=$(echo $* | xxd -plain | tr -d '\n' | sed 's/\(..\)/%\1/g')
	if [ $UID -eq 0 ] ; then
		sudo -u $user wget -q -U "Mozilla" -O ${output}.mp3 "http://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob&q=$query&tl=En-us"
	else
		wget -q -U "Mozilla" -O ${output}.mp3 "http://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob&q=$query&tl=En-us"
	fi
}

INPUT=$*
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
download_sound_file "$INPUT"

date=$(date)
echo "${date} - ${PROGNAME}: $*" >> /var/log/speech.log

playcmd="/usr/bin/play ${output}.mp3 silence 0 -1 0.0 0.1% pad 28000s@0:00"
if [ $UID -eq 0 ] ; then
	sudo -u $user $playcmd >/dev/null 2>&1
else
	$playcmd >/dev/null 2>&1
fi
[ "$PROGNAME" == "speech" ] && rm -f ${output}*.mp3
