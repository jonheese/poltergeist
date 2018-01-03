<html>
	<head>
		<title>Lisa, It's Your Birthday!</title>
	</head>
	<body>
<?php
exec('/usr/bin/play /var/www/lisa/lisa.mp3 pad 30000s@0:00 >/dev/null 2>&1 &');
?>
	</body>
</html>
