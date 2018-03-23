<html>
	<head>
		<title>Winnie Hicks - Flatliners Insults</title>
	</head>
	<body>
<?php
if ($_SERVER["REQUEST_METHOD"] != "GET") die();
$mp3_number = rand(1,14);
exec("/usr/bin/play /var/www/insult/insult$mp3_number.mp3 pad 30000s@0:00 >/dev/null 2>&1 &");
?>
	</body>
</html>
