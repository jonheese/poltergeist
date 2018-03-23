<html>
	<head>
		<title>Burrlibubbadibabubbadibaboom!</title>
	</head>
	<body>
<?php
if ($_SERVER["REQUEST_METHOD"] != "GET") die();
exec('/usr/bin/play /var/www/triohatalaha/triohatalaha.mp3 pad 30000s@0:00 >/dev/null 2>&1 &');
?>
	</body>
</html>
