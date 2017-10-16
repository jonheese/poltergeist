<html>
	<head>
		<title>Run Tell That!</title>
	</head>
	<body>
<?php
exec('/usr/bin/play /var/www/runtellthat/runtellthat.mp3 pad 30000s@0:00 >/dev/null 2>&1 &');
?>
	</body>
</html>
