<html>
	<head>
		<link rel="shortcut icon" href="onthephone.png" />
		<title>I'm on the phone!</title>
	</head>
	<body>
		<p align="center"><img src='onthephone.jpg' /></p>
<?php
if ($_SERVER["REQUEST_METHOD"] != "GET") die();
exec('/usr/bin/speech.sh "There is someone on the phone.  Please keep your voices down and language clean. Thank you" >/dev/null 2>&1 &');
?>
	</body>
</html>
