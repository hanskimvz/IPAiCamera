<?
require('../_define.inc');
require('../class/system.class');

$shm_id		= shmop_open(KEY_SM_SHARED_CONFIG, "a", 0, 0);
$system_conf= new CSystemConfiguration();
$security_conf = $system_conf->Security;
shmop_close($shm_id);
function getSystemService($name){
//	echo $name . "['support_telnet']=" . $GLOBALS['security_conf']->SystemService->SupportTelnet . ";\r\n";
	echo $name . "['support_ssh']=" . $GLOBALS['security_conf']->SystemService->SupportSSH . ";\r\n";
}
?>
<!DOCTYPE html>
<html>
	<head>
		<meta content="text/html; charset=utf-8" http-equiv="Content-Type">
	</head>
	<body>
		<div class="contentTitle"><span tkey="service_configuration"></span></div>
<!--
		<div class="content">
			<label class="subtitle"><span tkey="telnet_service"></label>
			<input type="radio" name="support_telnet" value="1" id="telnet_enable">
			<label for="telnet_enable"></label><span tkey="setup_enable"></span>
			<input type="radio" name="support_telnet" value="0" id="telnet_disable">
			<label for="telnet_disable"></label><span tkey="setup_disable"></span>
		</div>
-->
		<div class="content">
			<label class="subtitle"><span tkey="ssh_service"></label>
			<input type="radio" name="support_ssh" value="1" id="ssh_enable">
			<label for="ssh_enable"></label><span tkey="setup_enable"></span>
			<input type="radio" name="support_ssh" value="0" id="ssh_disable">
			<label for="ssh_disable"></label><span tkey="setup_disable"></span>
		</div>
		<center>
			<button id="btOK" class="button"><span tkey="apply"></span></button>
		</center>
	</body>
	<script>
		var ServiceInfo = new Object;
	<? 
		getSystemService('ServiceInfo');	
	?>
	</script>
	<script src="./setup_security_service.js"></script>
</html>
