#!/bin/bash

sed -i -s 's/;extension=php_xsl.dll/safe_mode\ \=\ Off/' /etc/php/7.0/apache2/php.ini
