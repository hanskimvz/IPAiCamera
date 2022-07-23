<?
require('../_define.inc');
require('../class/system.class');
require('../class/capability.class');
require('../class/socket.class');
require('../class/media.class');

$system_conf = new CSystemConfiguration();
$system_caps = new CCapability();

$shm_id = shmop_open(KEY_SM_SHARED_CONFIG, "a", 0, 0);
$system_conf = new CSystemConfiguration($shm_id);
$media_conf = new CMediaConfiguration();
$profile_conf = $media_conf->ProfileConfig;
shmop_close($shm_id);

function getLangSetup($name)
{
    echo $name . "=" .$GLOBALS['system_conf']->SystemDatetime->Language.";\r\n";
}
?> 
<!DOCTYPE html>
<html>
    <head>
        <meta content="text/html; charset=utf-8" http-equiv="Content-Type">
        <title>PTZ Configuration</title>
    </head>
    <body oncontextmenu="return false" onselectstart="return false"  ondragstart="return false">
        <div class="contentTitle"><span tkey="setup_PTZ_shortcuts"></span></div>
        <div class="content">
            <label class="maintitle"><span tkey="setup_PTZ_shortcuts"></span></label>

			<div class="content" id="preset_no_content">
			<!-- =====preset shortcut no 1~6====== -->
			</div>

        </div>
        <center><button id="btOK" class="button" ><span tkey="apply"></span></button></center>

        <script type="text/javascript">
            var capInfo = <? $GLOBALS['system_caps']->getCapability() ?>;
            var parkingInfo = <? get_ParkingAction($GLOBALS['profile_conf']); ?>;
			var powerupInfo = <? get_PowerupAction($GLOBALS['profile_conf']); ?>;
			var autoflipInfo = <? get_AutoFlip($GLOBALS['profile_conf']); ?>;
			var dzoomInfo = <? get_Dzoom($GLOBALS['profile_conf']); ?>;
        </script>
        <script type="text/javascript" src="./setup_ptz_shortcuts.js"></script>
    </body>
</html>
