<html>
	<head>
		<link rel="shortcut icon" href="embarrased.jpg" />
		<title>You must be so embarrassed!</title>
	</head>
	<body>
		<p align="center"><img src='emabarrassed.gif' /></p>
<?php
exec('/usr/bin/play /var/www/embarrassed/embarrassed.mp3 pad 30000s@0:00 >/dev/null 2>&1 &');
?>
	</body>
</html>
