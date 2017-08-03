#!/bin/bash

INPUT=$*
STRINGNUM=0
PROGNAME=$0

if [ "$PROGNAME" == "/root/speech.sh" ] ; then
	output="/tmp/trump"
else
	output="/tmp/speech"
fi

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
	wget -q -U "Mozilla" -O ${output}${keynum}.mp3 "http://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob&q=$NEXTURL&tl=En-us"
	if [ $? -ne 0 ] ; then
		echo "Unable to play $NEXTURL"
		wget -q -U "Mozilla" -O ${output}${keynum}.mp3 "http://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob&q=rururururururururururu&tl=En-us"
	fi
	keynum=$(($keynum+1))
done

cat ${output}*.mp3 > ${output}.mp3
/usr/bin/play ${output}.mp3 pad 28000s@0:00 >/dev/null 2>&1
echo "$*" >> /var/log/speech.log
