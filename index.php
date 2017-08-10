<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>sparkpug</title>
<link href="style.css" rel="stylesheet" type="text/css"></link>
<script src="jquery-3.2.1.min.js"></script>
<script>
function refresh_result1() { $( "#result1" ).load( "table.php" ); } 
window.setInterval(refresh_result1, 1000);
</script>
</head>
<body>
<?php include 'menu.php'; ?>
<div id="result1"></div>
</body>
</html>

