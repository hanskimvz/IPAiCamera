<?php
  require('/root/web/cgi-bin/_define.inc');
  require('/root/web/cgi-bin/class/system.class');
  require('/root/web/cgi-bin/class/network.class');
  
  $system_conf = new CSystemConfiguration();
  $net_conf = new CNetworkConfiguration();
  if(isset($_GET['getToken']) && !empty($_POST['guid']) && !empty($_POST['license_value']))
  {
    $guid=$_POST['guid'];
    $token=$_POST['license_value'];
    $plugin=$_POST['plugin_info'];
    $contextFile = "/root/web/plugin/vca/vca_license_url";
    $urlFile = fopen($contextFile, "r") or die("Unable to open file!");
    $url = fread($urlFile,filesize($contextFile));
    fclose($urlFile);
    
    $mac = trim($GLOBALS['net_conf']->HwAddress);
    $model_name =  trim($GLOBALS['system_conf']->DeviceInfo->Model);
    $fw_info = trim($system_conf->DeviceInfo->BuildVersion)."_". trim($system_conf->DeviceInfo->FirmwareVersion);
    $string = "curl -k -d 'guid=" . $guid . "&email_address=&comments=auto&license_value=" . $token . "&mac=". $mac ."&model=". $model_name ."&firmware=". $fw_info ."&type=IP&plugin=". $plugin ."' " . trim($url) . "/vca/activate";
    $ret = exec($string . " 2>&1", $output, $status);
    if($status == 0)
      echo $ret;
    else {
      if ($GLOBALS['net_conf']->IPv4->Type == 0 ){
        $ip       = trim($GLOBALS['net_conf']->IPv4->StaticIpAddr);
      } else {
        $ip       = trim($GLOBALS['net_conf']->IPv4->DynamicIpAddr);
      }
      
      //echo json_encode(print_r($output[0])) . $mac;
      echo "mac::" . $mac . ",ip::" . $ip;
    }
  }
  if(isset($_GET['deactivate']) && !empty($_POST['deactivation_code']))
  {
    $deactCode=$_POST['deactivation_code'];
    $plugin=$_POST['plugin_info'];
    $contextFile = "/root/web/plugin/vca/vca_license_url";
    $urlFile = fopen($contextFile, "r") or die("Unable to open file!");
    $url = fread($urlFile,filesize($contextFile));
    fclose($urlFile);
    
    $mac = trim($GLOBALS['net_conf']->HwAddress);
    $model_name =  trim($GLOBALS['system_conf']->DeviceInfo->Model);
    $fw_info = trim($system_conf->DeviceInfo->BuildVersion)."_". trim($system_conf->DeviceInfo->FirmwareVersion);
    $string = "curl -k -d 'deactivation_code=" . $deactCode . "&email_address=&mac=". $mac ."&model=". $model_name ."&firmware=". $fw_info ."&type=IP&plugin=". $plugin ."' " . trim($url) . "/vca/deactivate";
    $ret = exec($string . " 2>&1", $output, $status);
    if($status == 0)
      echo $ret;
    else {
      if ($GLOBALS['net_conf']->IPv4->Type == 0 ){
        $ip       = trim($GLOBALS['net_conf']->IPv4->StaticIpAddr);
      } else {
        $ip       = trim($GLOBALS['net_conf']->IPv4->DynamicIpAddr);
      }
      
      //echo json_encode(print_r($output[0])) . $mac;
      echo "mac::" . $mac . ",ip::" . $ip;
    }
  }
?>