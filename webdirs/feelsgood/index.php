<html>
	<head>
		<title>Feels Good!</title>
	</head>
	<body>
<?php
exec('/usr/bin/play /var/www/feelsgood/feelsgood.mp3 pad 30000s@0:00 >/dev/null 2>&1 &');
?>
	</body>
</html>