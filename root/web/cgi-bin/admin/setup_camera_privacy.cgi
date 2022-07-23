<?
require('../_define.inc');
require('../class/camera.class');
require('../class/media.class');

$shm_id       = shmop_open(KEY_SM_SHARED_CONFIG, "a", 0, 0);
$camera_confs = new CCameraConfigurations($shm_id);
$profile_conf = new CProfileConfiguration($shm_id);
?>
<!DOCTYPE html>
<html>
<head>
</head>
<body>
	<div class="contentTitle"><span tkey="privacy_mask_conf"></span>
<!--		
		<div class="contentNotice">
			<span class="caution" tkey="setup_notice"></span>
			<ul>
				<li><span tkey="setup_privacy_message"></li>
			</ul>
		</div> 
-->				
	</div>
	<div id="display_box">
		<div id="overlay_box"></div>
		<div id="vlc_box" class="content padding_zero">
	</div>
	</div>
	<div class="content">
		<div style="display:none">
			<label class="subtitle" tkey="setup_vin_source"></label>
			<div class="select">
				<select id="vin_source" autocomplete="off">
				</select>
			</div>
		</div>

		<label class="subtitle"><span tkey="setup_motion_activation"></span></label>
		<input type="radio" name="enabled" value=1 id="enabled_on"><label for="enabled_on"></label><span tkey="on"></span>
		<input type="radio" name="enabled" value=0 id="enabled_off"><label for="enabled_off"></label> <span tkey="off"></span><br>

		<label class="subtitle"><span tkey="setup_area"></span></label>
		<div class="select">
			<select id="selAreas">
			</select>
		</div><br>
	</div>
	<center>
		<button id="btClearSelectedArea" class="button" tkey="setup_clear_area"></button>
		<button id="btPrivacySave" class="button" tkey="setup_save"></button>
		<button id="btPrivacyRestore" class="button" tkey="setup_cancel"></button>
	</center>
	<script type="text/javascript">
		var VideoInfo = <? getChannelInfo($GLOBALS['profile_conf']); ?>;
		var privInfo = <? $GLOBALS['camera_confs']->getPrivacyMaskInfo(); ?>;
	</script>
	<script type="text/javascript" src="./setup_camera_privacy.js"></script>
</body>
</html>
