<html>
	<head>
		<title>That's Brisk Baby!</title>
	</head>
	<body>
<!--		<p align="center"><img src='@imgfile@' /></p>-->
<?php
exec('/usr/bin/play /var/www/brisk/brisk.mp3 pad 30000s@0:00 >/dev/null 2>&1 &');
?>
	</body>
</html>
