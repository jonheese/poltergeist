<html>
	<head>
		<link rel="shortcut icon" href="jinglebell.jpg" />
		<title>Jingle Bell</title>
	</head>
	<body>
		<p align="center"><img height='75%' src='jinglebell.jpg' /></p>
<?php
exec('/usr/bin/play /var/www/jinglebell/jinglebell.mp3 pad 30000s@0:00 >/dev/null 2>&1 &');
?>
	</body>
</html>
