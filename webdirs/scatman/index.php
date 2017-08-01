<html>
	<head>
		<link rel="shortcut icon" href="scatman_small.jpg" />
		<title>Gary!</title>
	</head>
	<body>
		<p align="center"><img src='scatman.jpg' /></p>
<?php
exec('/usr/bin/play /var/www/scatman/scatman.mp3 pad 30000s@0:00 >/dev/null 2>&1 &');
?>
	</body>
</html>
