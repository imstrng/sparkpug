<?php
$json = file_get_contents('http://localhost:5000');
$json = json_decode($json, true);
?>
<html>
<body>
<table>
<?php
foreach ($json as $k => $v){
    echo "<tr class=\"SNOOZE\">";
    echo "<td>".$k."</td>";
    echo "<td>".$v['A']."</td>";
    echo "</tr>";
}
?>
</table>
<pre>
</pre>
</body>
</html>
