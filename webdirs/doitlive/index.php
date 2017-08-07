<html>
	<head>
		<link rel="shortcut icon" href="doitlive.png" />
		<title>We'll Do It Live!</title>
	</head>
	<body>
		<p align="center"><img height='300px' src='doitlive.jpg' /></p>
<?php
exec('/usr/bin/play /var/www/doitlive/doitlive.mp3 pad 30000s@0:00 >/dev/null 2>&1 &');
?>
	</body>
</html>
