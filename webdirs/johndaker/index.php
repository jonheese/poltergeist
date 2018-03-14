<html>
	<head>
		<title>I Am John Daker</title>
	</head>
	<body>
<?php
$mp3_number = rand(1,17);
exec("/usr/bin/play /var/www/johndaker/johndaker$mp3_number.mp3 pad 30000s@0:00 >/dev/null 2>&1 &");
?>
	</body>
</html>
