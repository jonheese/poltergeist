<html>
	<head>
		<title>The Bobs</title>
	</head>
	<body>
		<p align="center"><img src='bobs.jpg' /></p>
<?php
if ($_SERVER["REQUEST_METHOD"] != "GET") die();
$mp3_number = rand(1,5);
exec("/usr/bin/play /var/www/bobs/bobs$mp3_number.mp3 pad 30000s@0:00 >/dev/null 2>&1 &");
?>
	</body>
</html>
