<?
require('../_define.inc');
require('../class/network.class');

$net_conf = new CNetworkConfiguration();

//--- ip
function getddnsInfo($name)
{	
	echo $name."['ddns_enable']="			.$GLOBALS['net_conf']->DDNS->Enabled."\r\n";	
	echo $name."['ddns_type']="			.$GLOBALS['net_conf']->DDNS->Type."\r\n";	

	echo $name."['ddns_hostname']='"	.trim($GLOBALS['net_conf']->DDNS->HostName)."';\r\n";
	echo $name."['ddns_username']='"	.trim($GLOBALS['net_conf']->DDNS->UserId)."';\r\n";
	echo $name."['ddns_password']='"	.trim($GLOBALS['net_conf']->DDNS->Password)."';\r\n";
	echo $name."['ddns_service']='"	    .trim($GLOBALS['net_conf']->DDNS->ServiceAddr)."';\r\n";
}

?>
<!DOCTYPE html>
<html>
	<head>
		<meta content="text/html; charset=utf-8" http-equiv="Content-Type">
		<title>DDNS CONFIGURATION</title>
	</head>

	<body onload="onLoadPage();" oncontextmenu="return false" onselectstart="return false"  ondragstart="return false">
		<div class="contentTitle"><span tkey="setup_ddns_config"></span></div>
		<div class="content">

			<input id="ddns_off" type="radio" value="0" name="ddns_enable">
			<label for="ddns_off"></label><span tkey="setup_disable" ></span><br>
			<input id="ddns_on" type="radio" value="1" name="ddns_enable" >
			<label for="ddns_on"></label><span tkey="setup_public_ddns" ></span><br>

			<label class="subtitle2"><span tkey="setup_address" ></span></label>
			<div class="select">
				<select id="ddns_type"> 
					<option value=1>www.dyndns.com</option>
					<option value=2>www.no-ip.com</option>
				</select>
			</div><br>

			<label class="subtitle2"><span tkey="setup_hostname" ></span></label>
			<input id="ddns_hostname" type="text" maxlength="64" class="inputText"><br>

			<label class="subtitle2"><span tkey="setup_username" ></span></label>
			<input id="ddns_username" type="text" maxlength="32" class="inputText"><br>

			<label class="subtitle2"><span tkey="setup_password" ></span></label>
			<input id="ddns_password" type="password" maxlength="32" class="inputText">

		</div>

		<center>
			 <button id="btOK" class="button" ><span tkey="apply" ></span></button>
		</center>

		<script>
			var ddnsInfo = new Object();
		<? 
				getddnsInfo("ddnsInfo"); 
		?>
		</script>
		<script src="./setup_network_ddns.js"></script>
	</body>
</html>
