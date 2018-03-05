<html>
	<head>
		<title>Mmkay!</title>
	</head>
	<body>
<?php
$mp3_number = rand(1,10);
exec("/usr/bin/play /var/www/mmkay/mmkay$mp3_number.mp3 pad 30000s@0:00 >/dev/null 2>&1 &");
?>
	</body>
</html>
