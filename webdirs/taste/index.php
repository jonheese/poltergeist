<html>
	<head>
		<title>Mmmmmmm</title>
	</head>
	<body>
<?php
if ($_SERVER["REQUEST_METHOD"] != "GET") die();
$mp3_number = rand(1,7);
exec("/usr/bin/play /var/www/taste/taste$mp3_number.mp3 pad 30000s@0:00 >/dev/null 2>&1 &");
?>
	</body>
</html>
