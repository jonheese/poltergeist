<html>
	<head>
		<link rel="shortcut icon" href="friday.png" />
		<title>Friday</title>
	</head>
	<body>
<?php
$day = date('l');
if ( $day == "Friday" ) {
	exec('/usr/bin/play /var/www/friday/friday.mp3 pad 30000s@0:00 >/dev/null 2>&1 &');
	print "<p align='center'><img src='friday.jpg' /></p>\n";
} else {
	print "<p align='center'><img src='stahp.jpg' /></p>\n";
}
?>
	</body>
</html>
