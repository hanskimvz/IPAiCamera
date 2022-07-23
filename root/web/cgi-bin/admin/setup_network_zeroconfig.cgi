<?
require('../_define.inc');
require('../class/network.class');

$net_conf = new CNetworkConfiguration();

//--- ip
function getzeroconfigInfo($name)
{	
		echo $name."['zeroconfig_enable']="	.$GLOBALS['net_conf']->ZeroConfig->Enabled."\r\n";				
		echo $name."['zeroconfig_id']='"		.trim($GLOBALS['net_conf']->ZeroConfig->InterfaceToken)."';\r\n";
		echo $name."['zeroconfig_addr']='"		.trim($GLOBALS['net_conf']->ZeroConfig->Addr)."';\r\n";
}

?>
<!DOCTYPE html>
<html>
	<head>
		<meta content="text/html; charset=utf-8" http-equiv="Content-Type">
		<title>AUTO CONFIGURATION</title>
	</head>

	<body onload="onLoadPage();" oncontextmenu="return false" onselectstart="return false"  ondragstart="return false">
		<div class="contentTitle"><span tkey="setup_zero_config"></span></div>
		<div class="content">
			<label class="maintitle"><span tkey="setup_general_setting"></span></label>
			<input type="radio" value="0" name="zeroconfig_enable" id="enabled_off" >
			<label for="enabled_off"></label><span tkey="off"></span>
			<input type="radio" value="1" name="zeroconfig_enable" id="enabled_on" >
			<label for="enabled_on"></label><span tkey="on"></span><br>
		</div>
<div class="content">
			<table id="info">
				<tr>
				<th width="150"><span tkey="setup_zeroconfig_uniqueid"></span></th>
					<td id="zeroconfig_id"></td>
				</tr>
				<tr>
					<th><span tkey="setup_zeroconfig_addr"></span></th>
					<td id="zeroconfig_addr"></td>
				</tr>
			</table>
		</div>
		<center>
			<button id="btOK" class="button"><span tkey="apply"></span></button>
		</center>

		<script>
			var zeroconfigInfo = new Object();
			var targetinfo = zeroconfigInfo;
			<? 
				getzeroconfigInfo("zeroconfigInfo"); 
			?>
		</script>
		<script src="./setup_network_zeroconfig.js"></script>
	</body>
</html>
