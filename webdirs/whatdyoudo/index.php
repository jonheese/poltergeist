<html>
	<head>
		<title>What'd You Do?</title>
	</head>
	<body>
<!--		<p align="center"><img src='@imgfile@' /></p>-->
<?php
exec('/usr/bin/play /var/www/whatdyoudo/whatdyoudo.mp3 pad 30000s@0:00 >/dev/null 2>&1 &');
?>
	</body>
</html>
