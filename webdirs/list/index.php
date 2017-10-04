<html>
	<head>
		<title>Site List</title>
	</head>
	<body>
        <pre>
<?php
exec('/usr/sbin/apachectl -S | grep namevhost | grep -v hdmi | awk '{print $4}' | cut -d'.' -f1 | sort');
?>
        </pre>
	</body>
</html>
