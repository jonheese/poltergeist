<html>
	<head>
		<title>I Keep Forgetting</title>
	</head>
	<body>
<?php
if ($_SERVER["REQUEST_METHOD"] != "GET") die();
exec('/usr/bin/play /var/www/keepforgetting/keepforgetting.mp3 pad 30000s@0:00 >/dev/null 2>&1 &');
?>
	</body>
</html>
