<html>
	<head>
		<!--<link rel="shortcut icon" href="ow.png" />-->
		<title>Damn it, Michael!</title>
	</head>
	<body>
		<!--<p align="center"><img src='ow.jpg' /></p>-->
<?php
if ($_SERVER["REQUEST_METHOD"] != "GET") die();
exec('/usr/bin/play /var/www/damnit/damnit.mp3 pad 30000s@0:00 >/dev/null 2>&1 &');
?>
	</body>
</html>
