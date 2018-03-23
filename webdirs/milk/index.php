<html>
	<head>
		<link rel="shortcut icon" href="milk.jpg" />
		<title>He need some milk!</title>
	</head>
	<body>
		<p align="center"><img height='100%' src='milk.png' /></p>
<?php
if ($_SERVER["REQUEST_METHOD"] != "GET") die();
exec('/usr/bin/play /var/www/milk/milk.mp3 pad 30000s@0:00 >/dev/null 2>&1 &');
?>
	</body>
</html>
