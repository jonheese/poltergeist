<html>
	<head>
		<link rel="shortcut icon" href="wow.jpg" />
		<title>Wow!</title>
	</head>
	<body>
		<p align="center"><img src='wow.gif' /></p>
<?php
exec('/usr/bin/play /var/www/wow/wow.mp3 pad 30000s@0:00 >/dev/null 2>&1 &');
?>
	</body>
</html>
