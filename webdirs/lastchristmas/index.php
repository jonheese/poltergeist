<html>
	<head>
		<link rel="shortcut icon" href="lastchristmas.png" />
		<title>Wham! - Last Christmas</title>
	</head>
	<body>
<?php
if ( date('F') == "December" ) {
	exec('/usr/bin/play lastchristmas.mp3 pad 30000s@0:00 >/dev/null 2>&1 &');
	print "<p align='center'><img src='lastchristmas.jpg' /></p>\n";
} else {
	print "<p align='center'><img src='stahp.jpg' /></p>\n";
}
?>
	</body>
</html>
