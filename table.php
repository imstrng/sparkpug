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
    if ($v['status'] == 'ERROR') {
      echo "<tr class=\"".$v['status']."\">";
      echo "<td>".$k."</td>";
      echo "<td>".$v['status']."</td>";
      echo "<td>".$v['descr']."</td>";
      echo "<td>".$v['checkedin']."</td>";
      echo "</tr>";
    }
}
foreach ($json as $k => $v){
    if ($v['status'] == 'STALE') {
      echo "<tr class=\"".$v['status']."\">";
      echo "<td>".$k."</td>";
      echo "<td>".$v['status']."</td>";
      echo "<td>Timeout : ".$v['timeout']."</td>";
      echo "<td>".$v['checkedin']."</td>";
      echo "</tr>";
    }
}
foreach ($json as $k => $v){
    if ($v['status'] == 'WARN') {
      echo "<tr class=\"".$v['status']."\">";
      echo "<td>".$k."</td>";
      echo "<td>".$v['status']."</td>";
      echo "<td>".$v['descr']."</td>";
      echo "<td>".$v['checkedin']."</td>";
      echo "</tr>";
    }
}
foreach ($json as $k => $v){
    if ($v['status'] == 'INFO') {
      echo "<tr class=\"".$v['status']."\">";
      echo "<td>".$k."</td>";
      echo "<td>".$v['status']."</td>";
      echo "<td>".$v['descr']."</td>";
      echo "<td>".$v['checkedin']."</td>";
      echo "</tr>";
    }
}
foreach ($json as $k => $v){
    if ($v['status'] == 'SNOOZE') {
      echo "<tr class=\"".$v['status']."\">";
      echo "<td>".$k."</td>";
      echo "<td>".$v['status']."</td>";
      echo "<td>".$v['descr']."</td>";
      echo "<td>".$v['checkedin']."</td>";
      echo "</tr>";
    }
}
?>
</table>
