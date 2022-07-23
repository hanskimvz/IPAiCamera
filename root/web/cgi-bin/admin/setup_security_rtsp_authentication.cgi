<?
require('../_define.inc');
require('../class/system.class');

$shm_id		= shmop_open(KEY_SM_SHARED_CONFIG, "a", 0, 0);
$system_conf= new CSystemConfiguration();
$security_conf = $system_conf->Security;
shmop_close($shm_id);
function getRtspAuthentication($name){
	echo $name . "['AuthEnabled']=" . $GLOBALS['security_conf']->RtspAuthentication->AuthEnabled . ";\r\n";
}
?>
<!DOCTYPE html>
<html>
	<head>
		<meta content="text/html; charset=utf-8" http-equiv="Content-Type">
	</head>
	<body>
		<div class="contentTitle"><span tkey="rtsp_auth_config"></span></div>
		<div class="content">	
			<label class="subtitle"><span tkey="rtsp_auth"></label>
			<input type="radio" name="AuthEnabled" value="1" id="rtsp_auth_enable">
			<label for="rtsp_auth_enable"></label><span tkey="setup_enable"></span>
			<input type="radio" name="AuthEnabled" value="0" id="rtsp_auth_disable">
			<label for="rtsp_auth_disable"></label><span tkey="setup_disable_off"></span>			
		</div>

		<center>
			<button id="btOK" class="button"><span tkey="apply"></span></button>
		</center>
	</body>
	<script>
		var CRtspAuthinfo = new Object;
	<? 
		getRtspAuthentication('CRtspAuthinfo');	
	?>
	</script>
	<script src="./setup_security_rtsp_authentication.js"></script>
</html>
