<html>
	<head>
		<link rel="shortcut icon" href="td4w.png" />
		<title>Turn Down For What</title>
	</head>
	<body>
<?php
if ($_SERVER["REQUEST_METHOD"] != "GET") die();
#$ip = $_SERVER['REMOTE_ADDR'];
#if ($ip == "10.156.88.234" || $ip == "10.156.88.226" || $ip == "10.156.88.212") {
	print "<p align='center'><img src='td4w.jpg' /></p>";
	exec('/usr/bin/play /var/www/td4w/td4w.mp3 pad 30000s@0:00 >/dev/null 2>&1 &');
#} else {
#	print "<p align='center'><img src='sad_panda.gif' /></p>";
#}
?>
	</body>
</html>
