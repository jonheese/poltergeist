<html>
	<head>
		<title>You'se Are Mates!</title>
	</head>
	<body>
<!--		<p align="center"><img src='@imgfile@' /></p>-->
<?php
exec('/usr/bin/play /var/www/mates/mates.mp3 pad 30000s@0:00 >/dev/null 2>&1 &');
?>
	</body>
</html>
