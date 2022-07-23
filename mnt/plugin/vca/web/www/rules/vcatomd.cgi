<?
require("../../../../../../root/web/cgi-bin/_define.inc");
require("../../../../../../root/web/cgi-bin/class/system.class");
$system_conf = new CSystemConfiguration();

$file = '../config/vcatomd.conf';
$get = "get";
$tag = "rule";
$fwinfo = "fwinfo";
$data = file_get_contents($file);

if (isset($_GET[$fwinfo])) {
  $value = trim($system_conf->DeviceInfo->BuildVersion)."_". trim($system_conf->DeviceInfo->FirmwareVersion);
  echo $value;
}

if (isset($_GET[$tag]) && $_GET[$tag]!="") {
  $value = $_GET[$tag];
  if(isset($_GET["add"])) {
    if(urlencode($data)=="%0A" || urlencode($data)=="")
      $data = $value;
    else
      $data = $data .",". $value;
    file_put_contents($file, $data);
  }
  else if(isset($_GET["del"])) {
    $tok = strtok($data, ",");
    $temp = "";
    while($tok !== false)
    {
      if($value != $tok)
      {
        $temp = $temp.$tok.",";
      }
      $tok = strtok(",");
    }
    $data = trim($temp, ",");
    file_put_contents($file, $data);
  }
  echo $tag . "=" . $data;
}
?>