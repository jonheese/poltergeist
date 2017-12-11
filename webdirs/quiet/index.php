<html>
        <head>
                <link rel="shortcut icon" href="stahp.jpg" />
                <title>Vitas</title>
        </head>
        <body>
                <p align="center"><img height='100%' src='stahp.jpg' /></p>
<?php
$cmd = exec('ps -ef | grep play | grep -v grep | tr -s " " | cut -d" " -f8-');
exec($cmd);
?>
        </body>
</html>
