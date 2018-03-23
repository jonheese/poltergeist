<html>
	<head>
		<link rel="shortcut icon" href="dontknowmuch.png" />
		<title>Ow!</title>
	</head>
	<body>
		<p align="center"><img src='dontknowmuch.jpg' /></p>
<?php
if ($_SERVER["REQUEST_METHOD"] != "GET") die();
exec('/usr/bin/play /var/www/dontknowmuch/dontknowmuch.mp3 pad 30000s@0:00 >/dev/null 2>&1 &');
?>
	</body>
</html>
