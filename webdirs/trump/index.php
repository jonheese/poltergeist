<html>
	<head>
		<link rel="shortcut icon" href="trump.png" />
		<title>What Did Trump Just Say?</title>
	</head>
	<body>
		<p align="center"><img height='100%' src='trump.jpg' /></p>
<?php
if ($_SERVER["REQUEST_METHOD"] != "GET") die();
exec('/usr/bin/play /tmp/trump.mp3 pad 30000s@0:00 >/dev/null 2>&1 &');
?>
	</body>
</html>
