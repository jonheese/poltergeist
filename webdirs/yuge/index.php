<html>
	<head>
		<title>Yuge!</title>
	</head>
	<body>
<!--		<p align="center"><img src='@imgfile@' /></p>-->
<?php
exec('/usr/bin/play /var/www/yuge/yuge.mp3 pad 30000s@0:00 >/dev/null 2>&1 &');
?>
	</body>
</html>
