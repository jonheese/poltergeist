<html>
	<head>
		<link rel="shortcut icon" href="twoweeks.jpg" />
		<title>Two Weeks!</title>
	</head>
	<body>
		<p align="center"><img height='100%' src='twoweeks.jpg' /></p>
<?php
exec('/usr/bin/play /var/www/twoweeks/twoweeks.mp3 pad 30000s@0:00 >/dev/null 2>&1 &');
?>
	</body>
</html>
