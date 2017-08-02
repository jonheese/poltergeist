<html>
	<head>
		<link rel="shortcut icon" href="lips.jpg" />
		<title>Speech</title>
	</head>
	<body>
		<form method='POST'>
			<input name='text' width='100' /><br />
			<input type='submit' value='Speak' />
		</form>
<?php
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
	$text = $_POST['text'];
	exec('/usr/bin/speech.sh $text >/dev/null 2>&1');
	exec('/usr/bin/play /tmp/trump.mp3 pad 30000s@0:00 >/dev/null 2>&1 &');
}
?>
	</body>
</html>
