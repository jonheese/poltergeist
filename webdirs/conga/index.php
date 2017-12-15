<html>
	<head>
		<link rel="shortcut icon" href="conga.jpg" />
		<title>Come on shake your body, baby, do that conga!!</title>
	</head>
	<body>
		<p align="center"><img src='conga.gif' /></p>
<?php
exec('/usr/bin/play /var/www/conga/conga.mp3 pad 30000s@0:00 >/dev/null 2>&1 &');
?>
	</body>
</html>
