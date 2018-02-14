<html>
	<head>
		<title>Key & Peele - Terries</title>
	</head>
	<body>
<?php
$terries_number = rand(1,2);
exec("/usr/bin/play /var/www/terries/terries$terries_number.mp3 pad 30000s@0:00 >/dev/null 2>&1 &");
?>
	</body>
</html>
