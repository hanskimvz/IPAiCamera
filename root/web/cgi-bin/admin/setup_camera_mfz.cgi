<?
require('../_define.inc');
require('../class/system.class');
require('../class/capability.class');
require('../class/network.class');
require('../class/socket.class');
require('../class/ptz.class');
require('../class/media.class');

$focus_mode = new CFocusModeRequest();	
$shm_id = shmop_open(KEY_SM_SHARED_CONFIG, "a", 0, 0);
$system_conf = new CSystemConfiguration($shm_id);
$system_caps = new CCapability($shm_id);
$net_conf = new CNetworkConfiguration($shm_id);
$profile_conf = new CProfileConfiguration();
shmop_close($shm_id);

function getRTSPPort($name)
{
	echo $name . "=" .$GLOBALS['net_conf']->Protocols->Protocol[1]->Port.";\r\n";
}
?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html>
	<head>
		<meta content="text/html; charset=utf-8" http-equiv="Content-Type">
		<meta http-equiv="X-UA-Compatible" content="IE=10" /> 
		<meta name="google" content="notranslate">
		<meta HTTP-EQUIV="Pragma" CONTENT="no-cache">
		<title>Sensor Alignment</title>
		<link rel="stylesheet" href="/css/jqueryui.css" type="text/css" />
		<link rel="stylesheet" href="/css/main.css" type="text/css" />
		<link rel="stylesheet" href="/css/dom.css" type="text/css" /> 
		<? DependencyOem(); ?>
	</head>
	<body id="mfz_body" oncontextmenu="return false" onselectstart="return false"  ondragstart="return false">
		<div class="content2">
			<div id="image_box" class="multi-view-oneline"></div>
		</div>
		<script>
			var capInfo = <? $GLOBALS['system_caps']->getCapability() ?>;
			var userInfo = new Object();
			var VideoInfo = <?  getChannelInfo($GLOBALS['profile_conf']); ?>;
			var VideoInputInfo = <? $GLOBALS['profile_conf']->VideoSourceConfigurations->getVideoSourceInfo(); ?>;
			var gLanguage = <? $GLOBALS['system_conf']->getLanguageSetup(); ?>;
			var rtspPort = <? $GLOBALS['net_conf']->getRTSPPort(); ?>;
			<?
				$ipc_sock = new IPCSocket();					
				$ipc_sock->Connection($focus_mode, CMD_GET_FOCUS_MODE);	
				printf("var focus_mode = %d ;\r\n",  $focus_mode->mode->mode);
				$GLOBALS['system_conf']->Users->getAccessUserInfo("userInfo");

			?>
		</script>
		<script defer src="/js/jquery1.11.1.min.js"></script>
		<script defer src="/js/jqueryui.js"></script>
		<script defer src="/js/jquery.cookie.js"></script>		
		<script defer src="/js/page.js"></script>
        <script defer src="/js/jpeg.js"></script>
		<script defer src="/js/vlc_v3.js"></script>
		<script src="/js/lang.js"></script>
		<script defer src="./setup_camera_mfz.js"></script>
	</body>
</html>
