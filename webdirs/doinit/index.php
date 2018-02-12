<html>
	<head>
		<title>Doin' It, and Doin' It, and Doin' In Well!</title>
	</head>
	<body>
<!--		<p align="center"><img src='@imgfile@' /></p>-->
<?php
exec('/usr/bin/play /var/www/doinit/doinit.mp3 pad 30000s@0:00 >/dev/null 2>&1 &');
?>
	</body>
</html>
