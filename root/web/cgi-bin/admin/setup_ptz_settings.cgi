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
        <div class="contentTitle"><span tkey="setup_PTZ_settings"></span></div>
        <div class="content">
            <label class="maintitle"><span tkey="parking_action"></span></label>
			<label class="subtitle" tkey="setup_mode">mode</label>
            <input id="parking_enable" type="radio" name="parking_enabled" value="1" ><label for="parking_enable"></label><span tkey=setup_enable></span>
            <input id="parking_disable" type="radio" name="parking_enabled" value="0" ><label for="parking_disable"></label><span tkey=setup_disable></span><br>

            <label class="subtitle"><span tkey="setup_parking_waittime"></span></label>
            <input type="text" id="wait_time" maxlength="5" class="third"/>
			<label for="wait_time"></label><span tkey="setup_parking_seconds"></span>[ 5 ~ 14400 ]<br>

			<label class="subtitle"><span tkey="setup_actiontype"></span></label>
			<div class="select">
				<select id="actiontype">
                	<option value="0" tkey="homeposition">HomePosition</option>
                    <option value="1" tkey="preset1">Preset</option>
                    <option value="2" tkey="preset_tour1">preset tour</option>
                </select>
			</div><br>

			<label class="subtitle"><span tkey="preset1"></span></label>
			<div class="select">
				<select id="preset_no">
				</select>
			</div><br>

			<div name ="tourdiv">
			<label class="subtitle"><span tkey="preset_tour1"></span></label>
			<div class="select">
				<select id="presettour_no">
				</select>
			</div><br>
			</div>

        </div>
        <center><button id="btOK" class="button" ><span tkey="apply"></span></button></center>

		<div class="content">
			<label class="maintitle"><span tkey="powerupaction"></span></label>
			<label class="subtitle" tkey="setup_mode">mode</label>
            <input id="powerup_enable" type="radio" name="powerup_enabled" value="1" ><label for="powerup_enable"></label><span tkey=setup_enable></span>
            <input id="powerup_disable" type="radio" name="powerup_enabled" value="0" ><label for="powerup_disable"></label><span tkey=setup_disable></span><br>

			<label class="subtitle"><span tkey="setup_actiontype"></span></label>
			<div class="select">
				<select id="actiontype_power">
					<option value="0" tkey="homeposition">HomePosition</option>
					<option value="1" tkey="preset1">Preset</option>
					<option value="2" tkey="preset_tour1">preset tour</option>
				</select>
			</div><br>

			<label class="subtitle"><span tkey="preset1"></span></label>
				<div class="select">
				<select id="preset_no_power">
				</select>
				</div><br>
			
			<div name ="tourdiv">
			<label class="subtitle"><span tkey="preset_tour1"></span></label>
				<div class="select">
					<select id="presettour_no_power">
					</select>
				</div><br>
			</div>
		</div>
		<center><button id="btOK_power" class="button" ><span tkey="apply"></span></button></center>

		<div class="content">
			<label id="AutoFlipDzoom" class="maintitle"><span tkey="AutoFlip_Dzoom"></span></label>
			<label id="AutoFlip" class="maintitle"><span tkey="AutoFlip"></span></label>
			<label class="subtitle" tkey="AutoFlip">mode</label>
			<input id="autoflip_enable" type="radio" name="autoflip_enabled" value="1" ><label for="autoflip_enable"></label><span tkey=setup_enable></span>
            <input id="autoflip_disable" type="radio" name="autoflip_enabled" value="0" ><label for="autoflip_disable"></label><span tkey=setup_disable></span><br>
			<div id="Dzoom">
			<label class="subtitle" tkey="Dzoom">mode</label>
			<input id="Dzoom_enable" type="radio" name="Dzoom_enabled" value="1" ><label for="Dzoom_enable"></label><span tkey=setup_enable></span>
            <input id="Dzoom_disable" type="radio" name="Dzoom_enabled" value="0" ><label for="Dzoom_disable"></label><span tkey=setup_disable></span><br>
			</div>
		</div>
		<center><button id="btOK_autoflip_dzoom" class="button" ><span tkey="apply"></span></button></center>

        <script type="text/javascript">
            var capInfo = <? $GLOBALS['system_caps']->getCapability() ?>;
            var parkingInfo = <? get_ParkingAction($GLOBALS['profile_conf']); ?>;
			var powerupInfo = <? get_PowerupAction($GLOBALS['profile_conf']); ?>;
			var autoflipInfo = <? get_AutoFlip($GLOBALS['profile_conf']); ?>;
			var dzoomInfo = <? get_Dzoom($GLOBALS['profile_conf']); ?>;
        </script>
        <script type="text/javascript" src="./setup_ptz_settings.js"></script>
    </body>
</html>
