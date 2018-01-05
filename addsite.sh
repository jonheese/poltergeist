#!/bin/bash

echo -n "Enter site name: "
read site_name
echo -n "Enter page title: "
read page_title

mkdir webdirs/$site_name
cp webdirs/index.php.template webdirs/$site_name/index.php
sed -i "s/@site@/$site_name/g" webdirs/${site_name}/index.php
sed -i "s/@title@/$page_title/g" webdirs/${site_name}/index.php
mv webdirs/${site_name}.mp3 webdirs/$site_name/${site_name}.mp3

cp apache-confs/site.conf.template apache-confs/${site_name}.conf
sed -i "s/@site@/$site_name/g" apache-confs/${site_name}.conf
