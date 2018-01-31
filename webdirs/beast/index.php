<html>
	<head>
		<title>I Am The Beast!</title>
	</head>
	<body>
<?php
srand();
$beast_number = rand(1,16);
exec("/usr/bin/play /var/www/beast/beast$beast_number.mp3 pad 30000s@0:00 >/dev/null 2>&1 &");
?>
	</body>
</html>
