<html>
	<head>
		<link rel="shortcut icon" href="bang.png" />
		<title>Bang bang bang!</title>
	</head>
	<body>
		<p align="center"><img src='bang.jpg' /></p>
<?php
exec('/usr/bin/play /var/www/bang/bang.mp3 pad 30000s@0:00 >/dev/null 2>&1 &');
?>
	</body>
</html>
