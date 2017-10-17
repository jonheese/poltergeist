#!/bin/bash

chown www-data:www-data /var/www/* 2>/dev/null
if [ ! -f /var/www/hostile/level.txt ] ; then
    touch /var/www/hostile/level.txt
    echo "1" > /var/www/hostile/level.txt
fi
