<html>
	<head>
		<link rel="shortcut icon" href="gaary.png" />
		<title>Gary!</title>
	</head>
	<body>
		<p align="center"><img src='gaary.png' /></p>
<?php
if ($_SERVER["REQUEST_METHOD"] != "GET") die();
exec('/usr/bin/play /var/www/gaary/gaary.mp3 pad 30000s@0:00 >/dev/null 2>&1 &');
?>
	</body>
</html>
