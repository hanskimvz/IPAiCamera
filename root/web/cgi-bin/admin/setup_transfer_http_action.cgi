<?
require('../_define.inc');
require('../class/network.class');
require('../class/event.class');

$event_conf = new CEventConfiguration();
$net_conf = new CNetworkConfiguration();

//--- ip
function getHTTPActionInfo($name)
{	
	echo  $name."['enabled']='"     .$GLOBALS['net_conf']->HTTPAction->Enabled          ."'\r\n";
//	echo  $name."['name']='"        .trim($GLOBALS['net_conf']->HTTPAction->Name)       ."';\r\n";
    echo  $name."['description']='" .trim($GLOBALS['net_conf']->HTTPAction->Description)."';\r\n";
    echo  $name."['http_addr']='" .trim($GLOBALS['net_conf']->HTTPAction->Server)     ."';\r\n";
	echo  $name."['http_port']='"   .$GLOBALS['net_conf']->HTTPAction->Port             ."'\r\n";
	echo  $name."['id']='"          .trim($GLOBALS['net_conf']->HTTPAction->Username)   ."';\r\n";
	echo  $name."['pass']='"        .trim($GLOBALS['net_conf']->HTTPAction->Password)   ."';\r\n";
	echo  $name."['message']='"     .trim($GLOBALS['net_conf']->HTTPAction->Body)       ."';\r\n";
}
?>

<!DOCTYPE html>
<html>
	<head>
		<meta content="text/html; charset=utf-8" http-equiv="Content-Type">
		<title>HTTP Action settings</title>
	</head>

	<body onload="onLoadPage();" oncontextmenu="return false" onselectstart="return false"  ondragstart="return false">
		<div class="contentTitle"><span tkey="HTTP_ACTION"></span></div>
		<div class="content">
			<label class="maintitle"><span tkey="setup_general_setting"></span></label>
			<input type="radio" value="0" name="enabled" id="enabled_off" >
			<label for="enabled_off"></label><span tkey="off" ></span>
			<input type="radio" value="1" name="enabled" id="enabled_on" >
			<label for="enabled_on"></label><span tkey="on" ></span><br>
		</div>
		<div name="SmtpContent" class="content">
			<label class="maintitle"><span tkey="setup_account"></span></label>
<!--
            <label class="subtitle"><span tkey="setup_name"></span></label>
			<input id="name" type="text" class="inputText"><br>	
-->
            <label class="subtitle"><span tkey="description"></span></label>
			<input id="description" type="text" class="inputText"><br>	

			<label class="subtitle"><span tkey="setup_http_server"></span></label>
			<input id="http_addr" type="text" class="inputText"><br>	
			
			<label class="subtitle"><span tkey="setup_port"></span></label>
			<input id="http_port" type="text" class="inputText"><br>
			
			<label class="subtitle"><span tkey="setup_user_id"></span></label>
			<input id="id" type="text" class="inputText"><br>
			
			<label class="subtitle"><span tkey="setup_user_passwd"></span></label>
			<input id="pass" type="password" class="inputText"><br>
		</div>	 
		<div name="SmtpContent" class="content">
			<label class="maintitle"><span tkey="setup_message"></span></label>
			<label class="subtitle"><span tkey="setup_message"></span></label>
			<textarea id="message" maxlength="255">
			</textarea><br>
		</div>
		<center>
			<button id="btOK" class="button" ><span tkey="apply"></span></button>
		</center>
		<script type="text/javascript">
			var HTTPActionInfo = new Object();
		<? 
				getHTTPActionInfo("HTTPActionInfo"); 
		?>
		</script>
		<script src="./setup_transfer_http_action.js"></script>
	</body>
</html>
