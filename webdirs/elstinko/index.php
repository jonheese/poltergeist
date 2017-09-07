<html>
	<head>
		<link rel="shortcut icon" href="elstinko.png" />
		<title>El Stinko</title>
	</head>
	<body>
		<p align="center"><img height='100%' src='elstinko.png' /></p>
<?php
exec('/usr/bin/play /var/www/elstinko/elstinko.mp3 pad 30000s@0:00 >/dev/null 2>&1 &');
?>
	</body>
</html>
