 <?
require('../_define.inc');
require('../class/system.class');
require('../class/network.class');
$sys_conf = new CSystemConfiguration();
$net_conf = new CNetworkConfiguration();

//--- ip
function getTemperatureInfo($name)   
{	
	echo $name."['mode']="		.$GLOBALS['sys_conf']->DeviceIo->TemperatureSettings->mode."\r\n";
	echo $name."['threshold']="	.$GLOBALS['sys_conf']->DeviceIo->TemperatureSettings->threshold."\r\n"; 
}
function getsysInfo($name)
{
      echo $name."['model_name']='"   .trim($GLOBALS['sys_conf']->DeviceInfo->Model)."';\r\n";
      echo $name."['manufacturer']='" .trim($GLOBALS['sys_conf']->DeviceInfo->Manufacturer)."';\r\n";
      echo $name."['device_name']='"  .trim($GLOBALS['sys_conf']->DeviceInfo->DeviceName)."';\r\n";
      echo $name."['location']='"     .trim($GLOBALS['sys_conf']->DeviceInfo->Location)."';\r\n";
      echo $name."['serialnum']='"    .trim($GLOBALS['net_conf']->HwAddress)."';\r\n";
      echo "fwInfo='". trim($GLOBALS['sys_conf']->DeviceInfo->BuildVersion)."_". trim($GLOBALS['sys_conf']->DeviceInfo->FirmwareVersion)."';\r\n;";
}

?> 
<!DOCTYPE html>
<html>
	<head>
		<title>schedule configuration</title>
		<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />

	</head>
	<body oncontextmenu="return false" onselectstart="return false"  ondragstart="return false">
		<div class="contentTitle">3x Status</div>
	        <div class="content">
			<label class="maintitle">Camera Information</label>
            <table id="info">
                <tr>
                    <th width="150"><span tkey="setup_system_chipset"></span></th>
                    <td id='model_name'></td>
                </tr>
                <tr>
                    <th width="150"><span tkey="setup_system_chipset"></span></th>
                    <td id='fwInfo'></td>
                </tr>
                <tr id='serial_num'>
                    <th width="150"><span tkey="setup_mac_address"></span></th>
                    <td id='serialnum'></td>
                </tr>
                <tr>
                    <th width="150"><span tkey="setup_system_cameramodule"></span></th>
                    <td id='manufacturer'></td>
                </tr>
	    </table>
        </div>

		<div class="content">
			<label class="maintitle">Camera Status</label>
			<label class="subtitle">Current Time</span></label>
			<label id="timeval_3x" style="margin-left:6px;"></span></label> <br>
			<label class="subtitle">Cpu </label>
			<label id="cpuval_3x" style="margin-left:6px;"></span></label><br>
			<label class="subtitle">mem Info</label>
			<label id="meminfoval_3x" style="margin-left:6px;"></span></label><br>
			<label class="subtitle">Temperature</label>
			<label id="temperatureval_3x" style="margin-left:6px;"></span></label><br>
			<label class="subtitle">cds</label>
			<label id="cds_3x" style="margin-left:6px;"></span></label><br>
			<label class="subtitle">Bandwidth</label>
			<label id="bandwidth_3x" style="margin-left:6px;"></span></label><br>
		</div>	
		
		<script type="text/javascript">
			var temperatureInfo = new Object();
			var SysInfo = new Object();
			var fwInfo;
		<? 
				getsysInfo("SysInfo");
				getTemperatureInfo("temperatureInfo"); 
		?>
		</script>
		<script src="./setup_plugin_3x_status.js"></script>
	</body>
</html>
