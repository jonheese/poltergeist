<html>
	<head>
		<title>Hello, Darkness, My Old Friend</title>
	</head>
	<body>
<?php
exec('/usr/bin/play /var/www/hellodarkness/hellodarkness.mp3 pad 30000s@0:00 >/dev/null 2>&1 &');
?>
	</body>
</html>
