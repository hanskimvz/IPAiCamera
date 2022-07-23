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
		<title>video configuration</title>
	</head>
	<body>
		<div class="contentTitle"><span tkey="video_configuration"></span></div>
		<div id="content_preset" class="content video" style="display:none">
			<label class="subtitle subtitle_width"><span tkey="preset_config"></span></label>
			<div class="select">
			<select id="preset_conf" style="width:180px;">
			</select>
			</div>
			<button id="btpreset" class="button button_margin_left half" style="margin-left:30px;">
				<span tkey="apply">Apply</span>
			</button>
		</div>
		<div class="content" style="display:none">
			<label class="subtitle" tkey="setup_vin_source"></label>
			<div class="select">
				<select id="vin_source" autocomplete="off">
				</select>
			</div>
		</div>
		<div id="content_vout" class="content video" style="display:none">
			<label class="subtitle subtitle_width"><span tkey="hdmi_resolution"></span></label>
			<div class="select">
			<select id="vout_conf" style="width:180px;">
			</select>
			</div>
			<button id="btvout" class="button button_margin_left half" style="margin-left:30px;">
				<span tkey="apply">Apply</span>
			</button>
		</div>
		<div class="content padding_zero">
			<table id="profile">
				<tr id="profile_title">
					<th class="channel" colspan="2"><span tkey="stream"></span></th>
					<th class="conn"><span tkey="codec"></span></th>
					<th class="desc"><span tkey="description" maxlength="30"></span></th>
				</tr>
			</table>
		</div>
		<div id="contents" class="content video">
			<label class="maintitle"><span tkey="codec"></span></label>

			<label class="subtitle"><span tkey="codec"></span></label>
			<div class="select" >
				<select id="codec">
				</select>
			</div><br>

			<label class="subtitle"><span tkey="description"></span></label>
			<input type="text" id="codec_name"><br>

			<label class="subtitle"><span tkey="resolution"></span></label>
			<div class="select">
				<select id="resolution"> 
				</select>
			</div><br>

			<label class="subtitle"><span tkey="frame_rate"></span></label>
			<div class="select">
				<select id="framerate"></select>
			</div><br>

			<div id="DisableUI_MJPEG" >
				<div id="gop">
					<label class="subtitle"><span tkey="gop"></span></label>
					<input id="gopsize" type="text" class="third">
				</div>
				<div id="profile_div" >		
					<label class="subtitle"><span tkey="h264_profile"></span></label>
					<div class="select">
						<select id="h264_profile">
						</select>
					</div><br>	
				</div>	
				<label class="subtitle"><span tkey="bitrate_mode"></span></label>
				<div class="select">
					<select id="bitrate_mode">
						<option value="0" tkey="vbr"></option>
						<option value="1" tkey="cbr"></option>
					</select>
				</div><br>					
				<div id="target_bitrate_div">
					<label class="subtitle"><span tkey="target_bitrate"></span></label>
					<input id="bitrate" type="text" maxlength="5" class="third" numberonly="true" >
				</div>
			</div>
				<label class="subtitle"><span tkey="quality"></span></label>
				<input id="quality" type="text" class="third"><br>
            <div id="DisableUI_MJPEG_Second"  >
				<label class="subtitle" colspan="2" tkey="smart_core" id="smart_core_label"></label>
				<label class="subtitle" colspan="2" tkey="smart_lbr" id="smart_lbr_label"></label>
				<div class="select ">
					<select class="" id="lbr_mode">
						<option value="0" tkey="off"></option>
                        <!-- <option value="1" tkey="setup_auto"></option> -->
                        <option value="2" tkey="setup_lbrmode_0"></option>
                        <option value="3" tkey="setup_lbrmode_1"></option>
                        <option value="4" tkey="setup_lbrmode_2"></option>
					</select>
					<select class="" id="SmartCoreMode">
						<option value="0" tkey="off"></option>
						<option value="1" tkey="setup_coremode_0" id="RC"></option>
						<option value="2" tkey="setup_coremode_1" id="ACF"></option>
					</select>
				</div><br>
				<div id="h264_extension_option_div">
					<label class="subtitle"><span tkey="h264_extension_option"></span></label>
					<div class="select">
						<select id="h264_extension_option">
							<option value="0" tkey="off"></option>
	<!--					<option value="1" tkey="h264_exention_mode1">B-Frame On(BP)</option>
							<option value="2" tkey="h264_exention_mode2">B-Frame On(BBP)</option> -->
							<option value="3" tkey="h264_exention_mode3">SVCT</option>
						</select>
					</div>
				</div>
            </div>
		</div>
		
		</div>
	<div id="rtsptimeout_contents" class="content">
		<label class="maintitle"><span tkey="rtsp_session"></span></label>

		<label class="subtitle" ><span tkey="timeout"></span></label>	
		<input type="text" id="rtsp_timeout" class="third">
		<input type="checkbox" id="crtsp_timeout"><label for="crtsp_timeout"></label>[Default:Off, 30~120] <br>
		<!--onclick="check_rtsp_timeout(this.value)"-->
	</div>
		<center>
			<button id="btOK" class="button"><span tkey="apply"></span></button>
		</center>
		<script>
			var VinStreamInfo = <? getVinStreamInfo($GLOBALS['profile_conf']); ?>;
			var VideoInfo = <? getChannelInfo($GLOBALS['profile_conf']); ?>;
			var VoutInfo = <? get_vout_resoultion($GLOBALS['profile_conf']); ?>;
			var VideoOption;
		<? 
		
		get_video_option($GLOBALS['etc_conf'], "VideoOption");
		?>
		</script>
        <script src="./setup_basic_video.js"></script>
	</body>
</html>
