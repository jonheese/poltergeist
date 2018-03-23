<html>
	<head>
		<link rel="shortcut icon" href="nerds.png" />
		<title>NERDS!</title>
	</head>
	<body>
		<p align="center"><img src='nerds.jpg' /></p>
<?php
if ($_SERVER["REQUEST_METHOD"] != "GET") die();
exec('/usr/bin/play /var/www/nerds/nerds.mp3 pad 30000s@0:00 >/dev/null 2>&1 &');
?>
	</body>
</html>
