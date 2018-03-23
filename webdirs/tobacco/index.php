<html>
	<head>
		<title>You Don't Always Die From Tobacco!</title>
	</head>
	<body>
<?php
if ($_SERVER["REQUEST_METHOD"] != "GET") die();
exec('/usr/bin/play /var/www/tobacco/tobacco.mp3 pad 30000s@0:00 >/dev/null 2>&1 &');
?>
	</body>
</html>
