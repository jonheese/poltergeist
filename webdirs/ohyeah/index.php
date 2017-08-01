<html>
	<head>
		<link rel="shortcut icon" href="ohyeah.png" />
		<title>Oh Yeah!</title>
	</head>
	<body>
		<p align="center"><img height='100%' src='ohyeah.jpg' /></p>
<?php
exec('/usr/bin/play /var/www/ohyeah/ohyeah.mp3 pad 30000s@0:00 >/dev/null 2>&1 &');
?>
	</body>
</html>
