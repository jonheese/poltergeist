<html>
	<head>
		<title>Me! That's Who!</title>
	</head>
	<body>
<!--		<p align="center"><img src='@imgfile@' /></p>-->
<?php
exec('/usr/bin/play /var/www/me/me.mp3 pad 30000s@0:00 >/dev/null 2>&1 &');
?>
	</body>
</html>
