<html>
	<head>
		<title>Site List</title>
	</head>
	<body>
<?php
$output = shell_exec('/var/www/list/get-sites.sh');
echo "$output";
?>
	</body>
</html>
