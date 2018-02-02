<html>
	<head>
		<title>It's So Warm in the D</title>
	</head>
	<body>
<!--		<p align="center"><img src='@imgfile@' /></p>-->
<?php
exec('/usr/bin/play /var/www/sowarm/sowarm.mp3 pad 30000s@0:00 >/dev/null 2>&1 &');
?>
	</body>
</html>
