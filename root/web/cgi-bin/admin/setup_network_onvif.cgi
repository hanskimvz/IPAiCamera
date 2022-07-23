<?
require('../_define.inc');
require('../class/system.class');

$sys_conf = new CSystemConfiguration();

//--- ip
function getonvifInfo($name)
{	
	echo $name."['onvif_discovery']="			.$GLOBALS['sys_conf']->DeviceInfo->OnvifConf->discovery_mode."\r\n";	
	echo $name."['onvif_auth']="			.$GLOBALS['sys_conf']->DeviceInfo->OnvifConf->auth_mode."\r\n";	
}

?>
<!DOCTYPE html>
<html>
	<head>
		<meta content="text/html; charset=utf-8" http-equiv="Content-Type">
		<title>ONVIF CONFIGURATION</title>
	</head>

	<body onload="onLoadPage();" oncontextmenu="return false" onselectstart="return true"  ondragstart="return false">
		<div class="contentTitle" tkey="setup_onvif_config">ONVIF CONFIGURATION</div>
		<div class="content">
			<label class="maintitle"><span tkey="setup_onvif_auth">Authentication</span></label>
			<input type="radio" value="0" name="onvif_auth" id="onvif_auth_none" >
			<label for="onvif_auth_none"></label><span tkey="onvif_auth_none">None</span>
			<input type="radio" value="1" name="onvif_auth" id="onvif_auth_usertoken" >
			<label for="onvif_auth_usertoken"></label><span tkey="onvif_auth_usertoken">WS-Usertoken</span>
			<input type="radio" value="2" name="onvif_auth" id="onvif_auth_digest" >
			<label for="onvif_auth_digest"></label><span tkey="onvif_auth_digest">WS-Usertoken + Digest</span><br>
		</div>
		<div class="content">
			<label class="maintitle"><span tkey="setup_onvif_discovery">Discovery mode</span></label>
			<input type="radio" value="0" name="onvif_discovery" id="onvif_discoverable" >
			<label for="onvif_discoverable"></label><span tkey="onvif_discoverable">Discoverable</span>
			<input type="radio" value="1" name="onvif_discovery" id="onvif_non_discoverable" >
			<label for="onvif_non_discoverable"></label><span tkey="onvif_non_discoverable">Nondiscoverable</span><br>
		</div>
		<center>
			<button id="btOK" class="button" ><span tkey="apply" ></span></button>
		</center>

		<script>
			var onvifInfo = new Object();
			<? 
				getonvifInfo("onvifInfo"); 
			?>
		</script>
		<script src="./setup_network_onvif.js"></script>
	</body>
</html>
