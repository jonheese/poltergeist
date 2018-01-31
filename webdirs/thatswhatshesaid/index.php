<html>
	<head>
		<title>That's What She Said!</title>
	</head>
	<body>
<!--		<p align="center"><img src='@imgfile@' /></p>-->
<?php
exec('/usr/bin/play /var/www/thatswhatshesaid/thatswhatshesaid.mp3 pad 30000s@0:00 >/dev/null 2>&1 &');
?>
	</body>
</html>
