<?
$file = '../../../../../../root/web/cgi-bin/admin/vca/config/bia.conf';
$tag = "snapshotBIA";
$blob = "blob";
$zone = "zones";
$object = "objects";
$class = "class";
$height = "height";
$speed = "speed";
$area = "area";
$ticker = "evt_msg";
$sysmes = "sys_msg";
$linecounters = "line_counters";
$counters = "counters";
$json = json_decode(file_get_contents($file),TRUE);
if (isset($_GET[$tag]) && $_GET[$tag]!="") {
  $value = $_GET[$tag];
  $json[$tag] = $value;
  file_put_contents($file, json_encode($json));
}
if (isset($_GET[$blob]) && $_GET[$blob]!="") {
  $value = $_GET[$blob];
  $json[$blob] = $value;
  file_put_contents($file, json_encode($json));
}
if (isset($_GET[$zone]) && $_GET[$zone]!="") {
  $value = $_GET[$zone];
  $json[$zone] = $value;
  file_put_contents($file, json_encode($json));
}
if (isset($_GET[$object]) && $_GET[$object]!="") {
  $value = $_GET[$object];
  $json[$object] = $value;
  file_put_contents($file, json_encode($json));
}
if (isset($_GET[$class]) && $_GET[$class]!="") {
  $value = $_GET[$class];
  $json[$class] = $value;
  file_put_contents($file, json_encode($json));
}
if (isset($_GET[$height]) && $_GET[$height]!="") {
  $value = $_GET[$height];
  $json[$height] = $value;
  file_put_contents($file, json_encode($json));
}
if (isset($_GET[$speed]) && $_GET[$speed]!="") {
  $value = $_GET[$speed];
  $json[$speed] = $value;
  file_put_contents($file, json_encode($json));
}
if (isset($_GET[$area]) && $_GET[$area]!="") {
  $value = $_GET[$area];
  $json[$area] = $value;
  file_put_contents($file, json_encode($json));
}
if (isset($_GET[$ticker]) && $_GET[$ticker]!="") {
  $value = $_GET[$ticker];
  $json[$ticker] = $value;
  file_put_contents($file, json_encode($json));
}
if (isset($_GET[$sysmes]) && $_GET[$sysmes]!="") {
  $value = $_GET[$sysmes];
  $json[$sysmes] = $value;
  file_put_contents($file, json_encode($json));
}
if (isset($_GET[$linecounters]) && $_GET[$linecounters]!="") {
  $value = $_GET[$linecounters];
  $json[$linecounters] = $value;
  file_put_contents($file, json_encode($json));
}
if (isset($_GET[$counters]) && $_GET[$counters]!="") {
  $value = $_GET[$counters];
  $json[$counters] = $value;
  file_put_contents($file, json_encode($json));
}
if(isset($json[$tag])) {
  echo $tag . "=" . $json[$tag] . "<br>";
}
if(isset($json[$blob])) {
  echo $blob . "=" . $json[$blob];
}
if(!isset($json[$tag]) && !isset($json[$blob])) {
  echo json_encode($json) . "<br>";
}
?>