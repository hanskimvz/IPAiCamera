<?
require('../_define.inc');
require('../class/network.class');
require('../class/event.class');

$event_conf = new CEventConfiguration();
$net_conf = new CNetworkConfiguration();

//--- ip
function getSmtpInfo($name)
{	
	echo  $name."['enabled']='"    .trim($GLOBALS['net_conf']->SmtpSetting->Enabled)   ."'\r\n";
	echo  $name."['smtp_addr']='"  .trim($GLOBALS['net_conf']->SmtpSetting->Server)    ."'\r\n";
    echo  $name."['ssl_enable']="  .$GLOBALS['net_conf']->SmtpSetting->SSL_Enabled     ."\r\n";
	echo  $name."['smtp_port']="   .$GLOBALS['net_conf']->SmtpSetting->Port            ."\r\n";
	echo  $name."['ssl_port']="    .$GLOBALS['net_conf']->SmtpSetting->SSL_Port        ."\r\n";
	echo  $name."['id']='"         .trim($GLOBALS['net_conf']->SmtpSetting->Username)  ."';\r\n";
	echo  $name."['pass']='"       .trim($GLOBALS['net_conf']->SmtpSetting->Password)  ."';\r\n";
	echo  $name."['sender']='"     .trim($GLOBALS['net_conf']->SmtpSetting->Sender)    ."';\r\n";
	echo  $name."['receiver']='"   .trim($GLOBALS['net_conf']->SmtpSetting->Receiver)  ."';\r\n";
	echo  $name."['title']='"      .trim($GLOBALS['net_conf']->SmtpSetting->Subject)   ."';\r\n";
	echo  $name."['message']='"    .trim($GLOBALS['net_conf']->SmtpSetting->Body)      ."';\r\n";
	echo  $name."['mode']="        .$GLOBALS['event_conf']->transfer_conf->mode        ."\r\n";
	echo  $name."['detailedinfo']=" .$GLOBALS['net_conf']->SmtpSetting->DetailedInfo   ."\r\n";
	echo  $name."['cameraname']=" .$GLOBALS['net_conf']->SmtpSetting->CameraName       ."\r\n";
	echo  $name."['eventrulename']=" .$GLOBALS['net_conf']->SmtpSetting->EventRuleName ."\r\n";
}
?>

<!DOCTYPE html>
<html>
	<head>
		<meta content="text/html; charset=utf-8" http-equiv="Content-Type">
		<title>smtp settings</title>
	</head>

	<body onload="onLoadPage();" oncontextmenu="return false" onselectstart="return false"  ondragstart="return false">
		<div class="contentTitle"><span tkey="setup_smtp_config"></span></div>
		<div class="content">
			<label class="maintitle"><span tkey="setup_general_setting"></span></label>
			<input type="radio" value="0" name="enabled" id="enabled_off" >
			<label for="enabled_off"></label><span tkey="off" ></span>
			<input type="radio" value="1" name="enabled" id="enabled_on" >
			<label for="enabled_on"></label><span tkey="on" ></span><br>
		</div>
		<div name="SmtpContent" class="content">
			<label class="maintitle"><span tkey="setup_account"></span></label>
			<label class="subtitle"><span tkey="setup_mode"></span></label>
			<input type="radio" value="0" name="ssl_enable" id="Plain" >
			<label for="Plain"></label><span tkey="setup_smtp_plain"></span>
			
			<input type="radio" value="1" name="ssl_enable" id="SSLTLS" >
			<label for="SSLTLS"></label><span tkey="setup_smtp_ssltls"></span><br>
	
			<label class="subtitle"><span tkey="setup_smtp_serveraddress"></span></label>
			<input id="smtp_addr" type="text" class="inputText"><br>	
			
			<div id="smtp_port_content">		
				<label class="subtitle"><span tkey="setup_port"></span></label>
				<input id="smtp_port" type="text" class="inputText"><br>
			</div><span></span>
			
			<div id="ssl_port_content">			
				<label class="subtitle"><span tkey="setup_port"></span></label>
				<input id="ssl_port" type="text" class="inputText"><br>
			</div>
			
			<label class="subtitle"><span tkey="setup_user_id"></span></label>
			<input id="id" type="text" class="inputText"><br>
			
			<label class="subtitle"><span tkey="setup_user_passwd"></span></label>
			<input id="pass" type="password" class="inputText"><br>
			
			<label class="subtitle"><span tkey="setup_email_sender"></span></label>
			<input id="sender" type="text" class="inputText"><br>
			
			<label class="subtitle"><span tkey="setup_email_receiver"></span></label>
			<input id="receiver" type="text" class="inputText" style="width:300px;"><br>
		</div>	 
		<div name="SmtpContent" class="content">
			<label class="maintitle"><span tkey="setup_mail_contents"></span></label>
			<label class="subtitle"><span tkey="setup_title"></span></label>
			<input id="title" type="text" class="inputText"><br>

			<label class="subtitle"><span tkey="setup_message"></span></label>
			<textarea id="message" maxlength="255">
			</textarea><br>

			<input type="checkbox" id="cameraname" name="cameraname" value="1"/>
			<label id="showcb" style="margin-left: 132px; margin-top: 7px; margin-right: 5px;" for="cameraname"></label><span id="showcb2" class="subject" tkey="setup_camera_name"></span>

			<input type="checkbox" id="eventrulename" name="eventrulename" value="1"/>
			<label id="showcb" style="margin-left: 132px; margin-top: 7px; margin-right: 5px;" for="eventrulename"></label><span id="showcb2" class="subject" tkey="setup_event_rule_name"></span><br>

			<input type="checkbox" id="detailedinfo" name="detailedinfo" value="1"/>
			<label id="showcb" style="margin-left: 132px; margin-top: 7px; margin-right: 5px;" for="detailedinfo"></label><span id="showcb2" class="subject" tkey="contain_smtp_info"></span><br>
		</div>
		<center>
			<button id="btTest" class="button"><span tkey="msg_action_test"></span></button>
			<button id="btOK" class="button" ><span tkey="apply"></span></button>
		</center>
		<script type="text/javascript">
			var SmtpInfo = new Object();
		<? 
				getSmtpInfo("SmtpInfo"); 
		?>
		</script>
		<script src="./setup_transfer_smtp.js"></script>
	</body>
</html>
