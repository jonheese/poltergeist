<html>
	<head>
		<title>Woohoo!</title>
	</head>
	<body>
<?php
if ($_SERVER["REQUEST_METHOD"] != "GET") die();
$mp3_number = rand(1,18);
exec("/usr/bin/play /var/www/woohoo/woohoo$mp3_number.mp3 pad 30000s@0:00 >/dev/null 2>&1 &");
?>
	</body>
</html>