<html>
	<head>
		<title>Will Ya Do Me a Kindness?</title>
	</head>
	<body>
<!--		<p align="center"><img src='@imgfile@' /></p>-->
<?php
exec('/usr/bin/play /var/www/kindness/kindness.mp3 pad 30000s@0:00 >/dev/null 2>&1 &');
?>
	</body>
</html>
