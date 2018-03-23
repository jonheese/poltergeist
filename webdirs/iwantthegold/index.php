<html>
	<head>
		<link rel="shortcut icon" href="iwantthegold-small.png" />
		<title>I Want the Gold</title>
	</head>
	<body>
		<p align="center"><img src='iwantthegold.png' /></p>
<?php
if ($_SERVER["REQUEST_METHOD"] != "GET") die();
exec('/usr/bin/play /var/www/iwantthegold/iwantthegold.mp3 pad 30000s@0:00 >/dev/null 2>&1 &');
?>
	</body>
</html>
