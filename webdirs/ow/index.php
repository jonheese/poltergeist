<html>
	<head>
		<link rel="shortcut icon" href="ow.png" />
		<title>Ow!</title>
	</head>
	<body>
		<p align="center"><img src='ow.jpg' /></p>
<?php
exec('/usr/bin/play /var/www/ow/ow.mp3 pad 30000s@0:00 >/dev/null 2>&1 &');
?>
	</body>
</html>
