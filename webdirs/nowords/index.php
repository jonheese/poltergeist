<html>
	<head>
		<link rel="shortcut icon" href="nowords.png" />
		<title>No Words There!</title>
	</head>
	<body>
		<p align="center"><img src='nowords.jpg' /></p>
<?php
exec('/usr/bin/play /var/www/nowords/nowords.mp3 pad 30000s@0:00 >/dev/null 2>&1 &');
?>
	</body>
</html>
