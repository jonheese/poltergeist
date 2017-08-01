<html>
	<head>
		<link rel="shortcut icon" href="vitas.jpg" />
		<title>Vitas</title>
	</head>
	<body>
		<p align="center"><img height='100%' src='vitas.jpg' /></p>
<?php
exec('/usr/bin/play /var/www/vitas/vitas.mp3 pad 30000s@0:00 >/dev/null 2>&1 &');
?>
	</body>
</html>
