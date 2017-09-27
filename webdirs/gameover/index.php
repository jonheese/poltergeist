<html>
	<head>
		<link rel="shortcut icon" href="gameover.png" />
		<title>Game over!</title>
	</head>
	<body>
		<p align="center"><img src='gameover.gif' /></p>
<?php
exec('/usr/bin/play /var/www/gameover/gameover.mp3 pad 30000s@0:00 >/dev/null 2>&1 &');
?>
	</body>
</html>
