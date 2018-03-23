<html>
	<head>
		<title>Squeetz! Squeetz! Squeetz!</title>
	</head>
	<body>
<!--		<p align="center"><img src='@imgfile@' /></p>-->
<?php
if ($_SERVER["REQUEST_METHOD"] != "GET") die();
exec('/usr/bin/play /var/www/squeetz/squeetz.mp3 pad 30000s@0:00 >/dev/null 2>&1 &');
?>
	</body>
</html>
