<html>
	<head>
		<link rel="shortcut icon" href="cobra.png" />
		<title>Cobra!</title>
	</head>
	<body>
		<p align="center"><img src='cobra.jpg' /></p>
<?php
if ($_SERVER["REQUEST_METHOD"] != "GET") die();
exec('/usr/bin/play /var/www/cobrasong/cobrasong.mp3 pad 30000s@0:00 >/dev/null 2>&1 &');
?>
	</body>
</html>
