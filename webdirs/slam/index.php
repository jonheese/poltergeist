<html>
	<head>
		<title>Don't Slam the Door!</title>
	</head>
	<body>
<?php
$mp3_number = rand(1,2);
exec("/usr/bin/play /var/www/slam/slam$mp3_number.mp3 pad 30000s@0:00 >/dev/null 2>&1 &");
?>
	</body>
</html>
