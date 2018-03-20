#!/bin/bash

echo -n "Enter site name: "
read site_name

if [ ! -f apache-confs/${site_name}.conf ] ; then
    echo "Site $site_name not found!"
    exit 1
fi

git rm -r webdirs/$site_name
git rm apache-confs/${site_name}.conf

echo "$site_name" >> deletion_list.txt
git add deletion_list.txt

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
git commit -a -m "Remove $site_name site"
if [ $? -ne 0 ] ; then
    echo "Error committing changes.  Please do the following steps manually:"
    echo "   git commit -a"
    echo "   git push -u origin master"
    echo "   /root/jh/bin/deploy-poltergeist.sh"
    exit 1
fi
git push -u origin master
/root/jh/bin/deploy-poltergeist.sh
