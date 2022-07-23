<?
require('../_define.inc');
require('../class/media.class');

$profile_conf = new CProfileConfiguration();
//$media_conf = new CMediaConfiguration;
//$profile_conf = $media_conf->ProfileConfig;

//--- VideoQproi

?>

<!DOCTYPE html>
<html>
<head>
</head>
<body>
	<div class="contentTitle bottom_10"><span tkey="setup_av_roi_config"></span>
	</div>
	<div id="display_box">
		<div id="overlay_box"></div>
		<div id="vlc_box" class="content padding_zero"></div>
	</div>

	<div class="content">
		<div style="display:none">
			<label class="subtitle" tkey="setup_vin_source"></label>
			<div class="select">
				<select id="vin_source" autocomplete="off">
				</select>
			</div>
		</div>
		<label class="subtitle"><span tkey="stream"></span></label>
		<div class="select" >
			<select id="channel">
			</select>
		</div><br>

		<label class="subtitle"><span tkey="setup_motion_activation"></span></label>
	  	<div class="select">
			<select id = "enable">
				<option value=0 tkey="setup_disable"></option>
				<option value=1 tkey="setup_enable"></option>
			</select> 
		</div> <br>
		<label class="subtitle"><span tkey="quality"></span></label>
		<div class="slider_box">
			<div id="sensslider" class="long"></div>        
			<label id="senslabel" style="width:auto;">0</label>%
		</div>
	</div>
	<center>
		<button class="button" id="btSave"><span tkey="setup_save"></span></button>
		<button class="button" id="btRestore"><span tkey="setup_cancel"></span></button>
	</center>
	<script type="text/javascript">
		var VinStreamInfo  = <? getVinStreamInfo($GLOBALS['profile_conf']); ?>;
		var VideoInfo      = <? getChannelInfo($GLOBALS['profile_conf']); ?>;
		var VideoQproiInfo = <? $GLOBALS['profile_conf']->getVideoQproiInfo(); ?> ;
	</script>
	<script type="text/javascript" src="./setup_basic_roi.js"></script>

</body>
</html>
