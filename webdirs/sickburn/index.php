<html>
	<head>
		<link rel="shortcut icon" href="sickburn.png" />
		<title>Sick burn!</title>
	</head>
	<body>
		<p align="center"><img src='sickburn.jpg' /></p>
<?php
exec('/usr/bin/play /var/www/sickburn/sickburn.mp3 pad 30000s@0:00 >/dev/null 2>&1 &');
?>
	</body>
</html>
