<html>
	<head>
		<link rel="shortcut icon" href="gary.png" />
		<title>Gary!</title>
	</head>
	<body>
		<p align="center"><img src='gary.png' /></p>
<?php
exec('/usr/bin/play /var/www/gary/gary.mp3 pad 30000s@0:00 >/dev/null 2>&1 &');
?>
	</body>
</html>
