<html>
	<head>
		<title>Wilson!</title>
	</head>
    <body>
		<p align="center"><img src='wilson.png' /></p>
<?php
srand();
$wilson_number = rand(1,16);
exec("/usr/bin/play /var/www/wilson/wilson$wilson_number.mp3 pad 30000s@0:00 >/dev/null 2>&1 &");
?>
	</body>
</html>
