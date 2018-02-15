<html>
	<head>
		<title>Key & Peele - East/West College Bowl</title>
	</head>
	<body>
<?php
$mp3_number = rand(1,27);
exec("/usr/bin/play /var/www/eastwest/eastwest$mp3_number.mp3 pad 30000s@0:00 >/dev/null 2>&1 &");
?>
	</body>
</html>
