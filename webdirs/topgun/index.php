<html>
	<head>
		<title>Top Gun Theme</title>
	</head>
	<body>
		<p align="center"><img src='topgun.png' /></p>
<?php
exec('/usr/bin/play /var/www/topgun/topgun.mp3 pad 30000s@0:00 >/dev/null 2>&1 &');
?>
	</body>
</html>
