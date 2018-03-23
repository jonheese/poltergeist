<html>
	<head>
		<title>Time to Have Sex!</title>
	</head>
	<body>
<!--		<p align="center"><img src='@imgfile@' /></p>-->
<?php
if ($_SERVER["REQUEST_METHOD"] != "GET") die();
exec('/usr/bin/play /var/www/time/time.mp3 pad 30000s@0:00 >/dev/null 2>&1 &');
?>
	</body>
</html>
