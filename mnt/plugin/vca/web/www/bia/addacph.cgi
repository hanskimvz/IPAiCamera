<?
$xmlfile = '../../../../../../root/web/plugin_info_list.xml';
$file = '../../../../../../mnt/plugin/.config/plugin_user_event_index.txt';
$listcmd = '/cgi-bin/admin/trigger.cgi?msubmenu=event&action=get';
$sendurl = '';
$add = 'add';
$modify = 'mod';
$delete = 'del';
$response = '';
$eventid = '';
$plugname = '';
$name = 'name';
$cmd = 'add';
$actionid = 'action_id';

if (isset($_GET["event"]) && isset($_GET["id"]) && isset($_GET["pluginname"])) {
  $sendurl = $_GET["event"];
  $eventid = $_GET["id"];
  $plugname = $_GET["pluginname"];
}
if (isset($_GET["drule"]) && ($sendurl != '') && ($eventid != '') && ($plugname != '')) {
  $cmd = $add;
  $value = $_GET["drule"];
  if(file_exists($file)) {
    $eventlist = file_get_contents($file);
    $str = "{$eventid}:{$value}=";
    $pos = strpos($eventlist, $str);
    if($pos !== false) {
      $realeventid = substr($eventlist, $pos+strlen($str), 2);
      echo $realeventid;
      return $realeventid;
    } else
      echo 'none';
  }
}
if (isset($_GET[$add]) && ($sendurl != '') && ($eventid != '') && ($plugname != '')) {
  $cmd = $add;
  $value = $_GET[$add];
  $stringsum = "$sendurl $add $eventid $plugname '{$_GET[$name]}' $value";
  $response = exec($stringsum,$ret);
  if(file_exists($file) && $response) {
    sleep(1);
    $eventlist = file_get_contents($file);
    $str = "{$eventid}:{$value}=";
    $pos = strpos($eventlist, $str);
    if($pos !== false) {
      $realeventid = substr($eventlist, $pos+strlen($str), 2);
    } else
      $realeventid = 'none';
    $addurl = "msubmenu=event&action={$cmd}&enabled=1&name={$_GET[$name]}{$value}&always=1&action_id={$_GET[$actionid]}&sun=0&mon=0&tue=0&wed=0&thu=0&fri=0&sat=0&shour=0&smin=0&ehour=0&emin=0&event0_type={$realeventid}&event0_enabled=1";
    echo $addurl;
    return $addurl;
  }
}
else if (isset($_GET[$modify]) && ($sendurl != '') && ($eventid != '') && ($plugname != '')) {
  $cmd = $modify;
  $value = $_GET[$modify];
  $id = $_GET['evt_id'];
  $stringsum = "$sendurl $add $eventid $plugname '{$_GET[$name]}' $value";
  $response = exec($stringsum);
  if(file_exists($file) && $response) {
    sleep(1);
    $eventlist = file_get_contents($file);
    $str = "{$eventid}:{$value}=";
    $pos = strpos($eventlist, $str);
    if($pos !== false) {
      $realeventid = substr($eventlist, $pos+strlen($str), 2);
    } else
      $realeventid = 'none';
    $modurl = "msubmenu=event&action=modify&enabled=1&name={$_GET[$name]}{$value}&action_id={$_GET[$actionid]}&event0_type={$realeventid}&event0_enabled=1&id={$id}";
    echo $modurl;
    return $modurl;
  }
}
else if (isset($_GET[$delete]) && isset($_GET["id"]) && ($sendurl != '')) {
  $cmd = 'remove';
  $value = $_GET[$delete];
  $stringsum = "$sendurl $delete $eventid $plugname '{$_GET[$name]}' $value";
  $response = exec($stringsum);
  $delurl = "msubmenu=event&action={$cmd}&id={$_GET["ueventid"]}";
  echo $delurl;
  return $delurl;
}
else if (isset($_GET["get"]) && ($sendurl != '') && ($eventid != '') && ($plugname != '')) {
  $cmd = 'get';
  $value = $_GET["get"];
  if(file_exists($file)) {
    $eventlist = file_get_contents($file);
    $str = "{$eventid}:{$value}=";
    $pos = strpos($eventlist, $str);
    if($pos !== false) {
      $realeventid = substr($eventlist, $pos+strlen($str), 2);
      echo $realeventid;
      return $realeventid;
    }
    else
      echo 'none';
  }
}

if(isset($response)) {
  echo $response;
}
?>