<html>
	<head>
		<link rel="shortcut icon" href="onthephone.png" />
		<title>I'm on the phone!</title>
	</head>
	<body>
		<p align="center"><img src='onthephone.jpg' /></p>
<?php
exec('/usr/bin/play /var/www/onthephone/onthephone.mp3 pad 30000s@0:00 >/dev/null 2>&1 &');
?>
	</body>
</html>
