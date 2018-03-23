<html>
	<head>
		<title>Jobey, That's the Nastiest Thing!</title>
	</head>
	<body>
<!--		<p align="center"><img src='@imgfile@' /></p>-->
<?php
exec('/usr/bin/play /var/www/nasty/nasty.mp3 pad 30000s@0:00 >/dev/null 2>&1 &');
?>
	</body>
</html>
