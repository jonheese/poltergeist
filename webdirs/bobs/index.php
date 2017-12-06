<html>
	<head>
		<title>The Bobs</title>
	</head>
	<body>
		<p align="center"><img height='100%' src='bobs.jpg' /></p>
<?php
$bob_number = rand(1,5);
exec("/usr/bin/play /var/www/bobs/bobs$bob_number.mp3 pad 30000s@0:00 >/dev/null 2>&1 &");
?>
	</body>
</html>
