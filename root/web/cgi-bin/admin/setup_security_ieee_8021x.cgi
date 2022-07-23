<?
require('../_define.inc');
require('../class/system.class');

$shm_id = shmop_open(KEY_SM_SHARED_CONFIG, "a", 0, 0);
$system_conf = new CSystemConfiguration();
$ieee8021x_conf = $system_conf->Security->IEEE8021X;
$cert   = $system_conf->Security->Certificates;
shmop_close($shm_id);
?>
<!DOCTYPE html>
<html>
	<head>
		<meta content="text/html; charset=utf-8" http-equiv="Content-Type">
	</head>
	<body>
		<div class="contentTitle" tkey="ieee_8021x_configuration"></div>
		<div class="content">
			<label class="maintitle" tkey="setup_general_setting"></label>
			<label class="subtitle"><span tkey="ieee_8021x"></label>
			<input type="radio" name="enabled" value="1" id="enable">
			<label for="enable"></label><span tkey="on"></span>
			<input type="radio" name="enabled" value="0" id="disable">
			<label for="disable"></label><span tkey="setup_off"></span><br>
			<label class="subtitle" tkey="setup_protocol"></label>
			<div class="select">
				<select id="protocol">
					<option value="0">MD5</option>
					<option value="1">PEAP</option>
					<option value="2">TTLS/MD5</option>
					<option value="3">TLS</option>
				</select>
			</div><br>
			<label class="subtitle"><span tkey="setup_eapol_version"></span></label>
			<div class="select third">
				<select id="eapol_version" class="third">
					<option value="1">1</option>
					<option value="2">2</option>
				</select>
			</div><br>
			<label class="subtitle"><span tkey="setup_system_id"></span></label>
			<input id="id" type="text" class="inputText"><br>
			<label class="subtitle"><span tkey="setup_system_passwd"></span></label>
			<input id="password" type="password" class="inputText"><br>
			<label class="subtitle"><span tkey="setup_system_verify"></span></label>
			<input id="password_confirm" type="password" class="inputText"><br>
			<label class="subtitle" tkey="setup_ca_cert"></label>
			<div class="select">
				<select id="ca_id">
					<option value="0" tkey="setup_none"></option>
				</select>
			</div><br>
			<label class="subtitle" tkey="Certificate"></label>
			<div class="select">
				<select id="cert_id">
					<option value="0" tkey="setup_none"></option>
				</select>
			</div><br>
		</div>
		<center>
			<button id="btOK" class="button" tkey="apply"></span></button>
		</center>
	</body>
	<script>
		var caInfo = <? show_certificates($GLOBALS['cert']->CA, true);?>;
		var certInfo= <? show_certificates($GLOBALS['cert']->Certificate, true);?>;
		var ieee8021xInfo= <? show_ieee8021x($GLOBALS["ieee8021x_conf"], true); ?>;
	</script>
	<script src="./setup_security_ieee_8021x.js"></script>
</html>
