<html>
	<head>
		<title>It's So Cold in the D</title>
	</head>
	<body>
<?php
exec('/usr/bin/play /var/www/socold/socold.mp3 pad 30000s@0:00 >/dev/null 2>&1 &');
?>
	</body>
</html>
