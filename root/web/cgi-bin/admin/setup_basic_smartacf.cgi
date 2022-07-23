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
		<div class="contentTitle" id="acf_control"><span tkey="acf_plus_configuration"></span></div>


		<div id="contents" class="content video">
			<label class="maintitle"><span tkey="setup_general_setting"></span></label>
    		<label class="subtitle"><span tkey="stream"></span></label>
    		<div class="select" >
    			<select id="channel">
    			</select>
    		</div><br>
        </div>

        <div id="sub_contents" class="content video">

      			<label class="subtitle"><span tkey="frame_rate"></span></label>
      			<div class="select">
      				<select id="framerate"></select>
      			</div><br>
      			
  				<div id="gop">
  					<label class="subtitle"><span tkey="gop"></span></label>
  					<input id="target_gop" type="text" class="third">
  				</div>
  				
    				<label class="subtitle"><span tkey="bitrate_mode"></span></label>
    				<div class="select">
    					<select id="bitrateControl">
    						<option value="0" tkey="vbr"></option>
    						<option value="1" tkey="cbr"></option>
    					</select>
    				</div><br>	

            <div id="target_bitrate_div">
                <label class="subtitle"><span tkey="target_bitrate"></span></label>
                <input id="target_bitrate" type="text" maxlength="5" class="third" numberonly="true" >
            </div>

            <div id="hold_on_time_div">
                <label class="subtitle"><span tkey="hold_on_time"></span></label>
                <input id="hold_on_time" type="text" maxlength="5" class="third" numberonly="true" >
            </div>

            <label class="subtitle"><span tkey="trigger_event"></span></label>
            <div class="select">
                <select class="radius" id="trigger_event">
                </select>
            </div>
        </div>
		<center>
			<button id="btOK" class="button"><span tkey="apply"></span></button>
		</center>
		<script>
			var VinStreamInfo = <? getVinStreamInfo($GLOBALS['profile_conf']); ?>;
			var VideoInfo = <? getChannelInfo($GLOBALS['profile_conf']); ?>;
            var ACFInfo= <? get_acf_plus_info($GLOBALS['profile_conf']); ?>;
			var BitrateInfo;
		<? 
			getBitrateInfo($GLOBALS['etc_conf'], "BitrateInfo");
		?>
		</script>
        <script src="./setup_basic_smartacf.js"></script>
	</body>
</html>
