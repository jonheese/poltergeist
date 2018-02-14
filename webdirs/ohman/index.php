<html>
	<head>
		<title>Oh man, oh man, oh man</title>
	</head>
	<body>
<!--		<p align="center"><img src='@imgfile@' /></p>-->
<?php
exec('/usr/bin/play /var/www/ohman/ohman.mp3 pad 30000s@0:00 >/dev/null 2>&1 &');
?>
	</body>
</html>
