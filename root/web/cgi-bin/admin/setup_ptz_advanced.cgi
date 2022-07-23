<?
require('../_define.inc');
require('../class/system.class');
require('../class/capability.class');
require('../class/socket.class');
require('../class/media.class');

$system_conf = new CSystemConfiguration();
$system_caps = new CCapability();

$shm_id = shmop_open(KEY_SM_SHARED_CONFIG, "a", 0, 0);
//$presetconfig = new CPresetConfig();
//$presettourconfig = new CPresetTourConfig();
$system_conf = new CSystemConfiguration($shm_id);
$media_conf = new CMediaConfiguration();
$profile_conf = $media_conf->ProfileConfig;
shmop_close($shm_id);
//$presetconfig = $media_conf->ProfileConfig->PTZConfiguration->presetConfig ;
//$presettourconfig = $media_conf->ProfileConfig->PTZConfiguration->presetTourConfig ;
//$presettour = new CPresetTour();
//$presettourconfig =  new CPresetTourConfig();
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
        <div class="contentTitle"><span tkey="setup_PTZ_advanced"></span></div>
        <div class="content">
            <label class="maintitle"><span tkey="wiper_action"></span></label>
            <label class="subtitle"><span tkey="setup_wiper_speed"></span></label>
            <input type="text" id="wiper_speed" maxlength="2" class="third"/>
			<label for="wiper_speed"></label><span tkey="setup_wiper130"></span><br>

            <label class="subtitle"><span tkey="setup_wiper_timeout"></span></label>
            <input type="text" id="wiper_timeout" maxlength="2" class="third"/>
			<label for="wiper_timeout"></label><span tkey="setup_parking_seconds"></span>[ 1 ~ 120 ]<br>

        </div>
        <center><button id="btOK" class="button" ><span tkey="apply"></span></button></center>

        <div class="content">
            <label class="maintitle"><span tkey="Camera_Orientation"></span></label>
            <label class="subtitle"><span tkey="Mode"></span></label>
			<input id="hanging" type="radio" name="invert" value="0" ><label for="hanging"></label><span tkey=hanging></span>
			<input id="standing" type="radio" name="invert" value="1" ><label for="standing"></label><span tkey=standing></span>
		</div>
		<center><button id="btinvert" class="button"><span tkey="apply"></span></button></center>

        <script type="text/javascript">
            var capInfo = <? $GLOBALS['system_caps']->getCapability() ?>;
            var wiperInfo = <? get_WiperAction($GLOBALS['profile_conf']); ?>;
			var invertInfo = <? get_InvertMode($GLOBALS['profile_conf']); ?>;
        </script>
        <script type="text/javascript" src="./setup_ptz_advanced.js"></script>
    </body>
</html>
