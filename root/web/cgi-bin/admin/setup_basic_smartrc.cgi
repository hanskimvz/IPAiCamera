<?
require('../_define.inc');
require('../class/media.class');
require('../class/etc.class');
require('../class/system.class');

$shm_id       = shmop_open(KEY_SM_SHARED_CONFIG, "a", 0, 0);
$profile_conf = new CProfileConfiguration($shm_id);
$etc_conf     = new CEtcConfiguration($shm_id);
$system_conf  = new CSystemConfiguration($shm_id);
shmop_close($shm_id);
?>
<!DOCTYPE html>
<html>
	<head>
		<meta content="text/html; charset=utf-8" http-equiv="Content-Type">
		<title>ACV+ configuration</title>
	</head>
	<body>
		<div class="contentTitle" id="rate_control"><span tkey="rate_control_configuration"></span></div>


		<div id="contents" class="content video">
			<label class="maintitle"><span tkey="setup_general_setting"></span></label>
    		<label class="subtitle"><span tkey="stream"></span></label>
    		<div class="select" >
    			<select id="channel">
    			</select>
    		</div><br>
        </div>

        <div id="sub_contents" class="content video">
			<div  id="stream_quality_div">
			<label class="subtitle"><span tkey="stream_quality"></span></label>
			<div class="select">
				<select id="stream_quality"></select>
			</div>
			</div>
			<div  id="dynamic_roi_div">
            <label class="subtitle"><span tkey="dyn_roi_enable"></span></label>
			<input id="roi_enabled_off" type="radio" name="dyn_roi_enable" value=0 >
			<label for="roi_enabled_off"></label><span tkey=off></span>
			<input id="roi_enabled_on" type="radio" name="dyn_roi_enable" value=1 >
			<label for="roi_enabled_on"></label><span tkey=on></span><br>
			</div>
            <label class="subtitle"><span tkey="dyn_gop_enable"></span></label>
			<input id="gop_enabled_off" type="radio" name="dyn_gop_enable" value=0 >
			<label for="gop_enabled_off"></label><span tkey=off></span>
			<input id="gop_enabled_on" type="radio" name="dyn_gop_enable" value=1 >
			<label for="gop_enabled_on"></label><span tkey=on></span><br>

            <label class="subtitle"><span tkey="fps_drop_enable"></span></label>
			<input id="fps_enabled_off" type="radio" name="fps_drop_enable" value=0 >
			<label for="fps_enabled_off"></label><span tkey=off></span>
			<input id="fps_enabled_on" type="radio" name="fps_drop_enable" value=1 >
			<label for="fps_enabled_on"></label><span tkey=on></span><br>

        </div>
		<center>
			<button id="btOK" class="button"><span tkey="apply"></span></button>
		</center>
		<script>
			var VinStreamInfo = <? getVinStreamInfo($GLOBALS['profile_conf']); ?>;
			var VideoInfo = <? getChannelInfo($GLOBALS['profile_conf']); ?>;
            var RCInfo= <? get_rate_control_info($GLOBALS['profile_conf']); ?>;
		
		</script>
        <script src="./setup_basic_smartrc.js"></script>
	</body>
</html>
