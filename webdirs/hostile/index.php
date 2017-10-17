<html>
	<head>
		<title>Fucking Hostile!</title>
	</head>
	<body>
<?php
$home_dir = "/var/www/hostile";
$level_file = "$home_dir/level.txt";
$level = file_get_contents($level_file);
if ($level == "2") {
    file_put_contents($level_file, "3", LOCK_EX);
    exec("/usr/bin/play $home_dir/hostile2.mp3 pad 30000s@0:00 >/dev/null 2>&1 &");
} elseif ($level == "3") {
    file_put_contents($level_file, "4", LOCK_EX);
    exec("/usr/bin/play $home_dir/hostile3.mp3 pad 30000s@0:00 >/dev/null 2>&1 &");
} elseif ($level == "4") {
    file_put_contents($level_file, "1", LOCK_EX);
    exec("/usr/bin/play $home_dir/hostile4.mp3 pad 30000s@0:00 >/dev/null 2>&1 &");
} else {
    file_put_contents($level_file, "2", LOCK_EX);
    exec("/usr/bin/play $home_dir/hostile1.mp3 pad 30000s@0:00 >/dev/null 2>&1 &");
}
?>
	</body>
</html>
