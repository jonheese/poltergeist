<html>
	<head>
		<link rel="shortcut icon" href="grapefruit.png" />
		<title>Grapefruit</title>
	</head>
	<body>
		<p align="center"><img src='grapefruit.jpg' /></p>
<?php
if ($_SERVER["REQUEST_METHOD"] != "GET") die();
exec('/usr/bin/play /var/www/grapefruit/grapefruit.mp3 pad 30000s@0:00 >/dev/null 2>&1 &');
?>
	</body>
</html>
