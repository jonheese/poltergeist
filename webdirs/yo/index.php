<html>
	<head>
		<title>Key & Peele - Terries</title>
	</head>
	<body>
<?php
$yo_number = rand(1,4);
exec("/usr/bin/play /var/www/yo/yo$yo_number.mp3 pad 30000s@0:00 >/dev/null 2>&1 &");
?>
	</body>
</html>
