<?
require('../_define.inc');
require('../class/network.class');

$net_conf = new CNetworkConfiguration();

//--- ip
function getupnpInfo($name)
{	
	echo $name."['upnp_enable']="			.$GLOBALS['net_conf']->UpnpSetting->Enabled."\r\n";	
	echo $name."['upnp_friendlyname']='"	.trim($GLOBALS['net_conf']->UpnpSetting->FriendlyName)."';\r\n";
}

?>
<!DOCTYPE html>
<html>
	<head>
		<meta content="text/html; charset=utf-8" http-equiv="Content-Type">
		<title>UPNP CONFIGURATION</title>
	</head>

	<body onload="onLoadPage();" oncontextmenu="return false" onselectstart="return false"  ondragstart="return false">
		<div class="contentTitle"><span tkey="setup_upnp_config"></span></div>
		<div class="content">
			<label class="maintitle"><span tkey="setup_general_setting"></span></label>
			<input type="radio" value="0" name="upnp_enable" id="enabled_off" >
			<label for="enabled_off"></label><span tkey="off"></span>
			<input type="radio" value="1" name="upnp_enable" id="enabled_on" >
			<label for="enabled_on"></label><span tkey="on"></span><br>
		</div>
		<div  id="Upnpcontent" class="content">
			<label class="maintitle"><span tkey="setup_upnp_deviceinfo"></span></label>
			<label class="subtitle2" tkey="setup_upnp_friendlyname"></label>
			<input id="upnp_friendlyname" type="text" maxlength="30" class="inputText"><br>			
		</div>
		<center>
			<button id="btOK" class="button"><span tkey="apply"></span></button>
		</center>

		<script>
			var upnpInfo = new Object();
			<? 
				getupnpInfo("upnpInfo"); 
			?>
		</script>
		<script src="./setup_network_upnp.js"></script>
	</body>
</html>
