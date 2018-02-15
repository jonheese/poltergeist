<html>
	<head>
		<title>It's Friday!</title>
	</head>
	<body>
<?php
$day = date('l');
if ( $day == "Friday" ) {
    exec('/usr/bin/play /var/www/itsfriday/itsfriday.mp3 pad 30000s@0:00 >/dev/null 2>&1 &');
} else {
	print "<p align='center'><img src='stahp.jpg' /></p>\n";
}
?>
	</body>
</html>
