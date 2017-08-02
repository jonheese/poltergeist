<html>
	<head>
		<link rel="shortcut icon" href="lips.jpg" />
		<title>Speech</title>
	</head>
	<body>
		<form method='POST'>
			<table cellpadding='10'>
				<tr><td>Text:</td><td><input name='text' size='100' /></td></tr>
				<tr><td colspan='2' width='100%' align='right'><input type='submit' value='Speak' /></td></tr>
			</table>
		</form>
<?php
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
	$text = $_POST['text'];
	exec("/usr/bin/speech.sh $text");
	exec("/usr/bin/play /tmp/speech.mp3 pad 30000s@0:00 >/dev/null 2>&1 &");
}
?>
	</body>
</html>
