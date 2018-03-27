<html>
	<head>
		<title>Uhhhhhhhh.... Moonbase Alpha</title>
	</head>
	<body>
<?php
if ($_SERVER["REQUEST_METHOD"] != "GET") die();
$mp3_number = rand(1,2);
exec("/usr/bin/play /var/www/uh/uh$mp3_number.mp3 pad 30000s@0:00 >/dev/null 2>&1 &");
?>
	</body>
</html>
