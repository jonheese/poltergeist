<html>
	<head>
		<title>Pep talk</title>
	</head>
	<body>
<?php
exec('/usr/bin/play /var/www/peptalk/peptalk.mp3 pad 30000s@0:00 >/dev/null 2>&1 &');
?>
	</body>
</html>
