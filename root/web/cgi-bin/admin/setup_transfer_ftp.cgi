<?
require('../_define.inc');
require('../class/network.class');
require('../class/event.class');

$event_conf = new CEventConfiguration();
$net_conf = new CNetworkConfiguration();

//--- ip
function getFtpInfo()
{	
	$data['enabled']     = $GLOBALS['net_conf']->FtpSetting->Enabled;
//	$data['pasv_mode']   = $GLOBALS['net_conf']->FtpSetting->PassiveModeEnabled;
	$data['ftp_addr']    = trim($GLOBALS['net_conf']->FtpSetting->Server);
	$data['upload_path'] = trim($GLOBALS['net_conf']->FtpSetting->Directory);
	$data['port']        = trim($GLOBALS['net_conf']->FtpSetting->Port);
	$data['id']          = trim($GLOBALS['net_conf']->FtpSetting->Username);
	$data['pass']        = trim($GLOBALS['net_conf']->FtpSetting->Password);
	$data['mode']        = $GLOBALS['event_conf']->transfer_conf->mode;
	echo json_encode($data);
}
?>

<!DOCTYPE html>
<html>
	<head>
		<meta content="text/html; charset=utf-8" http-equiv="Content-Type">
		<title>ftp settings</title>
	</head>

	<body oncontextmenu="return false" onselectstart="return false"  ondragstart="return false">
		<div class="contentTitle"><span tkey="setup_ftp_config"></span></div>
		<div class="content">
			<label class="maintitle"><span tkey="setup_general_setting"></span></label>
			<input type="radio" value="0" name="enabled" id="enabled_off" >
			<label for="enabled_off"></label><span tkey="off"></span>
			<input type="radio" value="1" name="enabled" id="enabled_on" >
			<label for="enabled_on"></label><span tkey="on"></span><br>
		</div>
		<div  id="Ftpcontent" class="content">
			<label class="maintitle"><span tkey="setup_server_info"></span></label>
			<!-- 
			<label class="subtitle"><span tkey="setup_ftp_mode"></span></label>
			<input type="radio" value="1" name="pasv_mode" id="pasv_mode_on" >
			<label for="pasv_mode_on"></label><span tkey="setup_passive_mode"></span>
			<input type="radio" value="0" name="pasv_mode" id="pasv_mode_off" >
			<label for="pasv_mode_off"></label><span tkey="setup_active_mode"></span><br>
			 -->
			<label class="subtitle"><span tkey="setup_ftp_serveraddress"></span></label>
			<input id="ftp_addr" type="text" class="inputText"><br>	
			
			<label class="subtitle"><span tkey="setup_upload_path"></span></label>
			<input id="upload_path" type="text" class="inputText"><br>
				
			<label class="subtitle"><span tkey="setup_ftp_port"></span></label>
			<input id="port" type="text" class="inputText"><br>
			
			<label class="subtitle"><span tkey="setup_user_id"></span></label>
			<input id="id" type="text" class="inputText"><br>
			
			<label class="subtitle"><span tkey="setup_user_passwd"></span></label>
			<input id="pass" type="password" class="inputText"><br>
		</div>	 
		<center>
			<button id="btOK" class="button" ><span tkey="apply"></span></button>
		</center>
		<script type="text/javascript">
			var FtpInfo = <?  getFtpInfo(); ?>
		</script>
		<script src="./setup_transfer_ftp.js"></script>
	</body>
</html>
