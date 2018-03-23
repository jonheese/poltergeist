<html>
	<head>
		<title>Mom's Spaghetti</title>
	</head>
	<body>
<?php
if ($_SERVER["REQUEST_METHOD"] != "GET") die();
exec('/usr/bin/play /var/www/momsspaghetti/momsspaghetti.mp3 pad 30000s@0:00 >/dev/null 2>&1 &');
?>
	</body>
</html>
