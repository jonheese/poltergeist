<html>
	<head>
		<link rel="shortcut icon" href="stahp.jpg" />
		<title>Vitas</title>
	</head>
	<body>
		<p align="center"><img height='100%' src='stahp.jpg' /></p>
<?php
if ($_SERVER["REQUEST_METHOD"] != "GET") die();
exec('/usr/bin/killall play >/dev/null 2>&1 &');
?>
	</body>
</html>
