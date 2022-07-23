<?
require('/root/web/cgi-bin/_define.inc');
require('/root/web/cgi-bin/class/system.class');
require('/root/web/cgi-bin/class/network.class');

$system_conf = new CSystemConfiguration();
$net_conf = new CNetworkConfiguration();

function getsysInfo($name)
{   
            echo "var ". $name ." = new Object();";
            echo $name."['model_name']='"              .trim($GLOBALS['system_conf']->DeviceInfo->Model)."';\r\n";    
            echo $name."['mac']='"   .trim($GLOBALS['net_conf']->HwAddress)."';\r\n"; 
            echo $name."['fw_info']='". trim($GLOBALS['system_conf']->DeviceInfo->BuildVersion)."_". trim($GLOBALS['system_conf']->DeviceInfo->FirmwareVersion)."';\r\n";
            echo "return ". $name .";";
}
getsysInfo("SysInfo");
?>
