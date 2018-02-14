#!/bin/bash

echo -n "Enter site name: "
read site_name
echo -n "Enter page title: "
read page_title

mkdir webdirs/$site_name
cp webdirs/index.php.template webdirs/$site_name/index.php
sed -i "s/@site@/$site_name/g" webdirs/${site_name}/index.php
sed -i "s/@title@/$page_title/g" webdirs/${site_name}/index.php

if [ -f webdirs/${site_name}.jpg ] ; then
    imgfilepath="webdirs/${site_name}.jpg"
elif [ -f webdirs/${site_name}.png ] ; then
    imgfilepath="webdirs/${site_name}.png"
fi

if [ -n "$imgfilepath" ] ; then
    imgfile=$(basename $imgfilepath)
    sed -i "s/@imgfile@/$imgfile/g" webdirs/${site_name}/index.php
    sed -i "s/<\!\-\-//g" webdirs/${site_name}/index.php
    sed -i "s/\-\->//g" webdirs/${site_name}/index.php
    mv $imgfilepath webdirs/${site_name}/
fi

mv webdirs/${site_name}.mp3 webdirs/$site_name/${site_name}.mp3

cp apache-confs/site.conf.template apache-confs/${site_name}.conf
sed -i "s/@site@/$site_name/g" apache-confs/${site_name}.conf

echo -n "Do you have any customizations to make before commit/push? [y/N]: "
read custom

if [ "$custom" == "y" -o "$custom" == "Y" ] ; then
    echo "Please do the following steps manually after customization is complete:"
    echo "   git add ."
    echo "   git commit -a"
    echo "   git push -u origin master"
    echo "   /root/jh/bin/deploy-poltergeist.sh"
    exit 0
fi

git add .
git commit -a -m "Add $site_name site"
if [ $? -ne 0 ] ; then
    echo "Error committing changes.  Please do the following steps manually:"
    echo "   git commit -a"
    echo "   git push -u origin master"
    echo "   /root/jh/bin/deploy-poltergeist.sh"
    exit 1
fi
git push -u origin master
/root/jh/bin/deploy-poltergeist.sh
