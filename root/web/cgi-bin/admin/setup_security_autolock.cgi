<?
require('../_define.inc');
require('../class/system.class');

$shm_id		= shmop_open(KEY_SM_SHARED_CONFIG, "a", 0, 0);
$system_conf= new CSystemConfiguration();
$security_conf = $system_conf->Security;
shmop_close($shm_id);
function getAutoLock($name){
	echo $name . "['AutoLockEnabled']=" . $GLOBALS['security_conf']->AutoLock->AutoLockEnabled . ";\r\n";
}
?>
<!DOCTYPE html>
<html>
	<head>
		<meta content="text/html; charset=utf-8" http-equiv="Content-Type">
	</head>
	<body>
		<div class="contentTitle"><span tkey="autolock_configuration"></span></div>

		<div class="content">
			<label class="subtitle"><span tkey="Auto_lock"></label>
			<input type="radio" name="AutoLockEnabled" value="1" id="enable">
			<label for="enable"></label><span tkey="setup_enable"></span>
			<input type="radio" name="AutoLockEnabled" value="0" id="disable">
			<label for="disable"></label><span tkey="setup_disable"></span>
		</div>

		<center>
			<button id="btOK" class="button"><span tkey="apply"></span></button>
		</center>
	</body>
	<script>
		var AutolockInfo = new Object;
	<? 
		getAutoLock('AutolockInfo');	
	?>
	</script>
	<script src="./setup_security_autolock.js"></script>
</html>
