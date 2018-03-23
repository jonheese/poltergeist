<html>
	<head>
		<title>I didn't get no sleep cause' of y'all -- Y'all not gon' get no sleep cause of me!</title>
	</head>
	<body>
<?php
if ($_SERVER["REQUEST_METHOD"] != "GET") die();
exec('/usr/bin/play /var/www/nosleep/nosleep.mp3 pad 30000s@0:00 >/dev/null 2>&1 &');
?>
	</body>
</html>
