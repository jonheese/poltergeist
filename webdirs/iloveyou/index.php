<html>
	<head>
		<link rel="shortcut icon" href="iloveyou.png" />
		<title>I love you and I miss you</title>
	</head>
	<body>
<!--		<p align="center"><img src='nowords.jpg' /></p>-->
<?php
if ($_SERVER["REQUEST_METHOD"] != "GET") die();
exec('/usr/bin/play /var/www/iloveyou/iloveyou.mp3 pad 30000s@0:00 >/dev/null 2>&1 &');
?>
	</body>
</html>
