<html>
	<head>
		<title>Key & Peele - Terries</title>
	</head>
	<body>
<?php
$mp3_number = rand(1,2);
exec("/usr/bin/play /var/www/terries/terries$mp3_number.mp3 pad 30000s@0:00 >/dev/null 2>&1 &");
?>
	</body>
</html>
