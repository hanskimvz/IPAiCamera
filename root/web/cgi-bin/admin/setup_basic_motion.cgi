<?
require('../_define.inc');
require('../class/event.class');
require('../class/media.class');

$event_conf = new CEventConfiguration();
$profile_conf = new CProfileConfiguration();

function getMotionInfo()
{
	global $event_conf;
//print_r($event_conf->motion_confs->conf[0]);
	for($i=0 ; $i<4 ; ++$i )
	{
		for($j=0; $j < 4 ; ++$j ) 
		{
			$data[$i][$j]['sens']   = ($event_conf->motion_confs->conf[$i]->{"sens".$j} & 0xff);
			$data[$i][$j]['size']   = (($event_conf->motion_confs->conf[$i]->{"sens".$j} >> 16) & 0xff);
			$data[$i][$j]['enable'] = ($event_conf->motion_confs->conf[$i]->{"enable".$j} & 0xff);
			$data[$i][$j]['x']      = $event_conf->motion_confs->conf[$i]->area[$j]->x;
			$data[$i][$j]['y']      = $event_conf->motion_confs->conf[$i]->area[$j]->y;
			$data[$i][$j]['w']      = $event_conf->motion_confs->conf[$i]->area[$j]->w;
			$data[$i][$j]['h']      = $event_conf->motion_confs->conf[$i]->area[$j]->h;
			$data[$i][$j]['type']   = $event_conf->motion_confs->conf[$i]->area[$j]->type;
		}
	}
	echo json_encode($data);
}
?>

<!DOCTYPE html>
<html>
<head>
</head>
<body>
	<div class="contentTitle bottom_10"><span tkey="setup_motion_config"></span>
<!--	
		<div class="contentNotice">
			<span class="caution" tkey="setup_notice"></span>
			<ul>
				<li><span tkey="setup_motion_message"></span></li>
			</ul>
		</div> 
-->		
	</div>
	<div id="display_box">
		<div id="overlay_box"></div>
		<div id="vlc_box" class="content padding_zero"></div>
	</div>

	<div class="content">
		<label class="subtitle"><span tkey="setup_motion_detection"></span></label>
		<span id="displayMotionStatusArea" class='right'></span><br>
		<div style="display:none">
			<label class="subtitle" tkey="setup_vin_source"></label>
			<div class="select">
				<select id="vin_source" autocomplete="off">
				</select>
			</div>
		</div>
		<label class="subtitle" tkey="setup_area">Area</label>
	  	<div class="select">
		<select id = "rectsel" onchange="javascript:setActiveRect(this.selectedIndex)">
		<option value=0 selected=true tkey="setup_area_1"> Motion Area 1</option>
		<option value=1 tkey="setup_area_2"> Motion Area 2 </option>
		<option value=2 tkey="setup_area_3"> Motion Area 3 </option>
		<option value=3 tkey="setup_area_4"> Motion Area 4 </option>
		</select>
		</div> <br>
		<label class="subtitle"><span tkey="setup_motion_activation"></span></label>
	  	<div class="select">
		<select id = "typesel" onchange="javascript:setRectType(this.selectedIndex)">
   		<option selected=true tkey="setup_disable_off"> Disabled </option>
    	<option tkey="setup_enable"> Enabled </option>
<!--
    	<option> Include </option>
	 	<option> Exclude </option>
-->
		</select> 
		</div> <br>

		<div id="motion_threshold_setup">
		<label id="threshold_sub" class="subtitle"></label>
		<div class="slider_box">
			<div id="sizeslider" class="long"></div>        
			<label id="sizelabel">0</label>
		</div><br>
		</div>

		<label id="sensitivity_sub" class="subtitle"><span tkey="setup_sensitivity"></span></label>
		<div class="slider_box">
			<div id="sensslider" class="long"></div>        
			<label id="senslabel">0</label>
		</div>
	</div>
	<center>
		<button class="button" id="btSave"><span tkey="setup_save"></span></button>
		<button class="button" id="btRestore"><span tkey="setup_cancel"></span></button>
	</center>

	<input type="text" id="m0_left" value=0 style="display:none" /> <br>
	<input type="text" id="m0_right" value=0 style="display:none" /> <br>
	<input type="text" id="m0_top" value=0 style="display:none" /> <br>
	<input type="text" id="m0_bottom" value=10 style="display:none" /> <br>
	<input type="text" id="m0_type" value=0 style="display:none" /> <br>
	<input type="text" id="m0_size" value=0 style="display:none" /> <br>
	<input type="text" id="m0_sens" value=0 style="display:none" /> <br>

	<input type="text" id="m1_left" value=0 style="display:none" /> <br>
	<input type="text" id="m1_right" value=30 style="display:none" /> <br>
	<input type="text" id="m1_top" value=0 style="display:none" /> <br>
	<input type="text" id="m1_bottom" value=10 style="display:none" /> <br>
	<input type="text" id="m1_type" value=1 style="display:none" /> <br>
	<input type="text" id="m1_size" value=50 style="display:none" /> <br>
	<input type="text" id="m1_sens" value=20 style="display:none" /> <br>

	<input type="text" id="m2_left" value=0 style="display:none" /> <br>
	<input type="text" id="m2_right" value=30 style="display:none" /> <br>
	<input type="text" id="m2_top" value=0 style="display:none" /> <br>
	<input type="text" id="m2_bottom" value=10 style="display:none" /> <br>
	<input type="text" id="m2_type" value=1 style="display:none" /> <br>
	<input type="text" id="m2_size" value=50 style="display:none" /> <br>
	<input type="text" id="m2_sens" value=20 style="display:none" /> <br>

	<input type="text" id="m3_left" value=0 style="display:none" /> <br>
	<input type="text" id="m3_right" value=30 style="display:none" /> <br>
	<input type="text" id="m3_top" value=0 style="display:none" /> <br>
	<input type="text" id="m3_bottom" value=10 style="display:none" /> <br>
	<input type="text" id="m3_type" value=1 style="display:none" /> <br>
	<input type="text" id="m3_size" value=50 style="display:none" /> <br>
	<input type="text" id="m3_sens" value=20 style="display:none" /> <br>

	<input type="text" id="m4_left" value=0 style="display:none" /> <br>
	<input type="text" id="m4_right" value=30 style="display:none" /> <br>
	<input type="text" id="m4_top" value=0 style="display:none" /> <br>
	<input type="text" id="m4_bottom" value=10 style="display:none" /> <br>
	<input type="text" id="m4_type" value=1 style="display:none" /> <br>
	<input type="text" id="m4_size" value=50 style="display:none" /> <br>
	<input type="text" id="m4_sens" value=20 style="display:none" /> <br>
</body>

<script>
	//<!--#playinfo-->
	var MotionInfo = <? getMotionInfo(); ?>;
	var VideoInfo = <? getChannelInfo($GLOBALS['profile_conf']); ?>;
</script>
<script src="./setup_basic_motion.js"></script>
</html>
