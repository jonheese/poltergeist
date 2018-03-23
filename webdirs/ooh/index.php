<html>
	<head>
		<link rel="shortcut icon" href="ooh.png" />
		<title>Ooh!</title>
	</head>
	<body>
		<p align="center"><img height='100%' src='ooh.jpg' /></p>
<?php
if ($_SERVER["REQUEST_METHOD"] != "GET") die();
exec('/usr/bin/play /var/www/ooh/ooh.mp3 pad 30000s@0:00 >/dev/null 2>&1 &');
?>
	</body>
</html>
