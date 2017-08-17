<table>
<tr>
<th>Namespace</th>
<th>Status</th>
<th style="width: 100%">Description</th>
<th>Check-in</th>
</tr>
<?php
$json = file_get_contents('http://localhost:5000');
$json = json_decode($json, true);

foreach ($json as $k => $v){
    echo "<tr class=\"STD\">";
    echo "<td>".$k."</td>";
    echo "<td>".$v['K']."</td>";
    echo "<td>".$v['T']."</td>";
    echo "<td>".$v['U']."</td>";
    echo "<td>".$v['F']."</td>";
    echo "</tr>";
}
?>
</table>
