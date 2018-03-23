<html>
	<head>
		<title>Nothing's Over, I Just Need Something to Drink!</title>
	</head>
	<body>
<!--		<p align="center"><img src='@imgfile@' /></p>-->
<?php
if ($_SERVER["REQUEST_METHOD"] != "GET") die();
exec('/usr/bin/play /var/www/nothingsover/nothingsover.mp3 pad 30000s@0:00 >/dev/null 2>&1 &');
?>
	</body>
</html>
