<html>
	<head>
		<link rel="shortcut icon" href="notyou-small.png" />
		<title>Not You</title>
	</head>
	<body>
		<p align="center"><img src='notyou.png' /></p>
<?php
if ($_SERVER["REQUEST_METHOD"] != "GET") die();
exec('/usr/bin/play /var/www/notyou/notyou.mp3 pad 30000s@0:00 >/dev/null 2>&1 &');
?>
	</body>
</html>
