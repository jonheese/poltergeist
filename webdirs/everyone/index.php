<html>
	<head>
		<link rel="shortcut icon" href="everyone.png" />
		<title>Everyone is stupid except for me</title>
	</head>
	<body>
		<p align="center"><img src='everyone.png' /></p>
<?php
if ($_SERVER["REQUEST_METHOD"] != "GET") die();
exec('/usr/bin/play /var/www/everyone/everyone.mp3 pad 30000s@0:00 >/dev/null 2>&1 &');
?>
	</body>
</html>
