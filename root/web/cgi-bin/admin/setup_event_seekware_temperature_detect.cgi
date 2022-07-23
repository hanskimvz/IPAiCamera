<?
require('../_define.inc');
require('../class/event.class');
require('../class/media.class');
require('../class/camera.class');
require('../class/capability.class');

$event_conf = new CEventConfiguration();
$camera_configs = new CCameraConfigurations();
$profile_conf = new CProfileConfiguration();

$shm_id = shmop_open(KEY_SM_SHARED_CONFIG, "a", 0, 0);
$system_caps = new CCapability($shm_id);
$get_cameratype = $system_caps->camera_type; 


function getTemperatureDetectInfo()
{
	global $event_conf;
	//print_r($event_conf->temperature_confs->conf[0]);
	for($i=0 ; $i<4 ; ++$i )
	{
		for($j=0; $j < 8 ; ++$j ) 
		{
			$data[$i][$j]['temperature']   = ($event_conf->temperature_confs->conf[$i]->{"temperature".$j});
			$data[$i][$j]['filteringtime']   = ($event_conf->temperature_confs->conf[$i]->{"filteringtime".$j});
			$data[$i][$j]['tolerance']   = ($event_conf->temperature_confs->conf[$i]->{"tolerance".$j});
			$data[$i][$j]['rule']   = ($event_conf->temperature_confs->conf[$i]->{"rule".$j});
			$data[$i][$j]['enable'] = ($event_conf->temperature_confs->conf[$i]->{"enable".$j});
			$data[$i][$j]['x']      = $event_conf->temperature_confs->conf[$i]->area[$j]->x;
			$data[$i][$j]['y']      = $event_conf->temperature_confs->conf[$i]->area[$j]->y;
			$data[$i][$j]['w']      = $event_conf->temperature_confs->conf[$i]->area[$j]->w;
			$data[$i][$j]['h']      = $event_conf->temperature_confs->conf[$i]->area[$j]->h;
			$data[$i][$j]['type']   = $event_conf->temperature_confs->conf[$i]->area[$j]->type;
			$data[$i][$j]['emissivitytype']   = ($event_conf->temperature_confs->conf[$i]->{"emissivitytype".$j});
			$data[$i][$j]['emissivity']   = ($event_conf->temperature_confs->conf[$i]->{"emissivity".$j});
			$data[$i][$j]['measurement']   = ($event_conf->temperature_confs->conf[$i]->{"measurement".$j});
			$data[$i][$j]['slopegradient']   = ($event_conf->temperature_confs->conf[$i]->{"slopegradient".$j});
			$data[$i][$j]['osd'] = ($event_conf->temperature_confs->conf[$i]->{"osd".$j});
		}
	}
	echo json_encode($data);
}

function getTemperatureconvertInfo()
{
	global $event_conf;
	for($i=0 ; $i<4 ; ++$i )
	{
		$data[$i]['convert_md'] = ($event_conf->temperature_confs->conf[$i]->convert_md);
	}
	echo json_encode($data);
}

?>

<!DOCTYPE html>
<html>
<head>
</head>
<body>
	<div class="contentTitle bottom_10"><span tkey="setup_temp_config"></span>
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
	<!--
		<label class="subtitle"><span tkey="setup_motion_detection"></span></label>
		<span id="displayMotionStatusArea" class='right'></span><br>
		<div style="display:none">
			<label class="subtitle" tkey="setup_vin_source"></label>
			<div class="select">
				<select id="vin_source" autocomplete="off">
				</select>
			</div>
		</div>
	-->

		<label class="subtitle"><span tkey="setup_temperature_detected"></span></label>
		<span id="temperature_detected" class='right'></span><br>

		<label class="subtitle" tkey="setup_area">Area</label>
	  	<div class="select">
		<select id = "rectsel" onchange="javascript:setActiveRect(this.selectedIndex)">
		<option value=0 selected=true tkey="setup_measuring_area_1"> Measuring Area 1 </option>
		<option value=1 tkey="setup_measuring_area_2"> Measuring Area 2 </option>
		<option value=2 tkey="setup_measuring_area_3"> Measuring Area 3 </option>
		<option value=3 tkey="setup_measuring_area_4"> Measuring Area 4 </option>
		<option value=4 tkey="setup_measuring_area_5"> Measuring Area 5 </option>
		<option value=5 tkey="setup_measuring_area_6"> Measuring Area 6 </option>
		<option value=6 tkey="setup_measuring_area_7"> Measuring Area 7 </option>
		<option value=7 tkey="setup_measuring_area_8"> Measuring Area 8 </option>
		</select>
		</div> <br>

		<label class="subtitle"><span tkey="osd"></span></label>
		<div class="select">
		<select id = "osdsel" onchange="javascript:setRectOsd(this.selectedIndex)">
		<option selected=true tkey="setup_disable"> Disabled </option>
		<option tkey="setup_enable"> Enabled </option>
		</select>
		</div> <br>

		<label class="subtitle" tkey="setup_alarm_rule">Area</label>
	  	<div class="select">
		<select id = "rulesel" onchange="javascript:setChangeRule(this.selectedIndex)">

		<option value=0 selected=true tkey="temperature_rule_1"> Above </option>
		<option value=1 tkey="temperature_rule_2"> Below </option>
		<option value=2 tkey="temperature_rule_3"> Slope Rate </option>
		
		</select>
		</div> <br>
		<label class="subtitle"><span tkey="setup_temp_measure_activation"></span></label>
	  	<div class="select">
		<select id = "typesel" onchange="javascript:setRectType(this.selectedIndex)">
   		<option selected=true tkey="setup_disable"> Disabled </option>
    	<option tkey="setup_enable"> Enabled </option>
<!--
    	<option> Include </option>
	 	<option> Exclude </option>
-->
		</select> 
		</div> <br>

		<label class="subtitle" tkey="setup_measurement">Area</label>
		<div class="select">
		<select id = "measurementsel" onchange="javascript:setChangeMeasurement(this.selectedIndex)">
		<option value=0 selected=true tkey="setup_ae_average"> Average </option>
		<option value=1 tkey="setup_maximum"> Maximum </option>
		<option value=2 tkey="setup_minimum"> Minimum </option>
		</select>
		</div> <br>

		<label id="setup_temperature" class="subtitle"><span tkey="setup_temperature"></span></label>
		<input type="number" id="alarm_temp" class="short" ><label id="alarm_temp_label" ></span><br></label>

		<label id="setup_slope_gradient" class="subtitle"><span tkey="setup_slope_gradient"></span></label>
		<input type="number" id="slope_gradient" class="short" ><label id="slope_gradient_label" ></span></label><br>

		<label id="setup_autoup_interval" class="subtitle"><span tkey="setup_autoup_interval"></span></label>
		<input type="number" id="detection_inverval" class="short" ><label id="detection_inverval_label" ></span>Sec [ 10 ~ 600 ]<br></label>

		<label class="subtitle"><span tkey="setup_emissivity"></span></label>
		<div class="select">
		<select id = "emissivitysel" onchange="javascript:setChangeEmissivitytype(this.selectedIndex)">
		<option value=0 selected=true > Default </option>
		<option value=1 selected=true > Water, pure </option>
		<option value=2 selected=true > Glass, smooth(uncoated) </option>
		<option value=3 selected=true > Limestone </option>
		<option value=4 selected=true > Concrete, rough </option>
		<option value=5 selected=true > Aluminum, anodized </option>
		<option value=6 selected=true > Brick </option>
		<option value=7 selected=true > Paint(including white) </option>
		<option value=8 selected=true > Marble(polished) </option>
		<option value=9 selected=true > Plaster, rough </option>
		<option value=10 selected=true > Asphalt </option>
		<option value=11 selected=true > Paper, roofing or white </option>
		<option value=12 selected=true > Copper, oxidized </option>
		<option value=13 selected=true > Copper, polished </option>
		<option value=14 selected=true > Silver, oxidized </option>
		<option value=15 selected=true > Aluminum foil </option>
		<option value=16 selected=true > Silver, polished </option>
		<option value=17 selected=true > Custom </option>
		</select>
		</div>
		<input type="number" id="emissivity_custom" step="0.01" class="short" ><label id="emissivity_custom_label" ></span></label>[ 0.02 ~ 0.99 ]<br>

		<span id="displayAreaTemperature" onchange="javascript:getAreaTemperature()"></span>

	</div>

	<div class="content">
		<label class="subtitle"><span tkey="setup_temperature_convert_md"></span></label>
		<input type="checkbox" id="temp_convert_md" name="convert" /><label for="temp_convert_md"></label>
	</div>

	<center>
		<button class="button" id="btSave"><span tkey="setup_save"></span></button>
		<button class="button" id="btRestore"><span tkey="setup_cancel"></span></button>
	</center>

	<input type="text" id="m0_left" value=0 style="display:none" /> <br>
	<input type="text" id="m0_right" value=0 style="display:none" /> <br>
	<input type="text" id="m0_top" value=0 style="display:none" /> <br>
	<input type="text" id="m0_bottom" value=0 style="display:none" /> <br>
	<input type="text" id="m0_type" value=0 style="display:none" /> <br>
	<input type="text" id="m0_filteringtime" value=0 style="display:none" /> <br>
	<input type="text" id="m0_temperature" value=0 style="display:none" /> <br>
	<input type="text" id="m0_tolerance" value=0 style="display:none" /> <br>
	<input type="text" id="m0_rule" value=0 style="display:none" /> <br>
	<input type="text" id="m0_emissivitytype" value=0 style="display:none" /> <br>
	<input type="text" id="m0_emissivity" value=0 style="display:none" /> <br>
	<input type="text" id="m0_measurement" value=0 style="display:none" /> <br>
	<input type="text" id="m0_slopegradient" value=0 style="display:none" /> <br>
	<input type="text" id="m0_maxtemp" value=0 style="display:none" /> <br>
	<input type="text" id="m0_mintemp" value=0 style="display:none" /> <br>
	<input type="text" id="m0_avgtemp" value=0 style="display:none" /> <br>
	<input type="text" id="m0_osd" value=0 style="display:none" /> <br>

	<input type="text" id="m1_left" value=0 style="display:none" /> <br>
	<input type="text" id="m1_right" value=0 style="display:none" /> <br>
	<input type="text" id="m1_top" value=0 style="display:none" /> <br>
	<input type="text" id="m1_bottom" value=0 style="display:none" /> <br>
	<input type="text" id="m1_type" value=0 style="display:none" /> <br>
	<input type="text" id="m1_filteringtime" value=0 style="display:none" /> <br>
	<input type="text" id="m1_temperature" value=0 style="display:none" /> <br>
	<input type="text" id="m1_tolerance" value=0 style="display:none" /> <br>
	<input type="text" id="m1_rule" value=0 style="display:none" /> <br>
	<input type="text" id="m1_emissivitytype" value=0 style="display:none" /> <br>
	<input type="text" id="m1_emissivity" value=0 style="display:none" /> <br>
	<input type="text" id="m1_measurement" value=0 style="display:none" /> <br>
	<input type="text" id="m1_slopegradient" value=0 style="display:none" /> <br>
	<input type="text" id="m1_maxtemp" value=0 style="display:none" /> <br>
	<input type="text" id="m1_mintemp" value=0 style="display:none" /> <br>
	<input type="text" id="m1_avgtemp" value=0 style="display:none" /> <br>
	<input type="text" id="m1_osd" value=0 style="display:none" /> <br>

	<input type="text" id="m2_left" value=0 style="display:none" /> <br>
	<input type="text" id="m2_right" value=0 style="display:none" /> <br>
	<input type="text" id="m2_top" value=0 style="display:none" /> <br>
	<input type="text" id="m2_bottom" value=0 style="display:none" /> <br>
	<input type="text" id="m2_type" value=0 style="display:none" /> <br>
	<input type="text" id="m2_filteringtime" value=0 style="display:none" /> <br>
	<input type="text" id="m2_temperature" value=0 style="display:none" /> <br>
	<input type="text" id="m2_tolerance" value=0 style="display:none" /> <br>
	<input type="text" id="m2_rule" value=0 style="display:none" /> <br>
	<input type="text" id="m2_emissivitytype" value=0 style="display:none" /> <br>
	<input type="text" id="m2_emissivity" value=0 style="display:none" /> <br>
	<input type="text" id="m2_measurement" value=0 style="display:none" /> <br>
	<input type="text" id="m2_slopegradient" value=0 style="display:none" /> <br>
	<input type="text" id="m2_maxtemp" value=0 style="display:none" /> <br>
	<input type="text" id="m2_mintemp" value=0 style="display:none" /> <br>
	<input type="text" id="m2_avgtemp" value=0 style="display:none" /> <br>
	<input type="text" id="m2_osd" value=0 style="display:none" /> <br>

	<input type="text" id="m3_left" value=0 style="display:none" /> <br>
	<input type="text" id="m3_right" value=0 style="display:none" /> <br>
	<input type="text" id="m3_top" value=0 style="display:none" /> <br>
	<input type="text" id="m3_bottom" value=0 style="display:none" /> <br>
	<input type="text" id="m3_type" value=0 style="display:none" /> <br>
	<input type="text" id="m3_filteringtime" value=0 style="display:none" /> <br>
	<input type="text" id="m3_temperature" value=0 style="display:none" /> <br>
	<input type="text" id="m3_tolerance" value=0 style="display:none" /> <br>
	<input type="text" id="m3_rule" value=0 style="display:none" /> <br>
	<input type="text" id="m3_emissivitytype" value=0 style="display:none" /> <br>
	<input type="text" id="m3_emissivity" value=0 style="display:none" /> <br>
	<input type="text" id="m3_measurement" value=0 style="display:none" /> <br>
	<input type="text" id="m3_slopegradient" value=0 style="display:none" /> <br>
	<input type="text" id="m3_maxtemp" value=0 style="display:none" /> <br>
	<input type="text" id="m3_mintemp" value=0 style="display:none" /> <br>
	<input type="text" id="m3_avgtemp" value=0 style="display:none" /> <br>
	<input type="text" id="m3_osd" value=0 style="display:none" /> <br>

	<input type="text" id="m4_left" value=0 style="display:none" /> <br>
	<input type="text" id="m4_right" value=0 style="display:none" /> <br>
	<input type="text" id="m4_top" value=0 style="display:none" /> <br>
	<input type="text" id="m4_bottom" value=0 style="display:none" /> <br>
	<input type="text" id="m4_type" value=0 style="display:none" /> <br>
	<input type="text" id="m4_filteringtime" value=0 style="display:none" /> <br>
	<input type="text" id="m4_temperature" value=0 style="display:none" /> <br>
	<input type="text" id="m4_tolerance" value=0 style="display:none" /> <br>
	<input type="text" id="m4_rule" value=0 style="display:none" /> <br>
	<input type="text" id="m4_emissivitytype" value=0 style="display:none" /> <br>
	<input type="text" id="m4_emissivity" value=0 style="display:none" /> <br>
	<input type="text" id="m4_measurement" value=0 style="display:none" /> <br>
	<input type="text" id="m4_slopegradient" value=0 style="display:none" /> <br>
	<input type="text" id="m4_maxtemp" value=0 style="display:none" /> <br>
	<input type="text" id="m4_mintemp" value=0 style="display:none" /> <br>
	<input type="text" id="m4_avgtemp" value=0 style="display:none" /> <br>
	<input type="text" id="m4_osd" value=0 style="display:none" /> <br>

	<input type="text" id="m5_left" value=0 style="display:none" /> <br>
	<input type="text" id="m5_right" value=0 style="display:none" /> <br>
	<input type="text" id="m5_top" value=0 style="display:none" /> <br>
	<input type="text" id="m5_bottom" value=0 style="display:none" /> <br>
	<input type="text" id="m5_type" value=0 style="display:none" /> <br>
	<input type="text" id="m5_filteringtime" value=0 style="display:none" /> <br>
	<input type="text" id="m5_temperature" value=0 style="display:none" /> <br>
	<input type="text" id="m5_tolerance" value=0 style="display:none" /> <br>
	<input type="text" id="m5_rule" value=0 style="display:none" /> <br>
	<input type="text" id="m5_emissivitytype" value=0 style="display:none" /> <br>
	<input type="text" id="m5_emissivity" value=0 style="display:none" /> <br>
	<input type="text" id="m5_measurement" value=0 style="display:none" /> <br>
	<input type="text" id="m5_slopegradient" value=0 style="display:none" /> <br>
	<input type="text" id="m5_maxtemp" value=0 style="display:none" /> <br>
	<input type="text" id="m5_mintemp" value=0 style="display:none" /> <br>
	<input type="text" id="m5_avgtemp" value=0 style="display:none" /> <br>
	<input type="text" id="m5_osd" value=0 style="display:none" /> <br>

	<input type="text" id="m6_left" value=0 style="display:none" /> <br>
	<input type="text" id="m6_right" value=0 style="display:none" /> <br>
	<input type="text" id="m6_top" value=0 style="display:none" /> <br>
	<input type="text" id="m6_bottom" value=0 style="display:none" /> <br>
	<input type="text" id="m6_type" value=0 style="display:none" /> <br>
	<input type="text" id="m6_filteringtime" value=0 style="display:none" /> <br>
	<input type="text" id="m6_temperature" value=0 style="display:none" /> <br>
	<input type="text" id="m6_tolerance" value=0 style="display:none" /> <br>
	<input type="text" id="m6_rule" value=0 style="display:none" /> <br>
	<input type="text" id="m6_emissivitytype" value=0 style="display:none" /> <br>
	<input type="text" id="m6_emissivity" value=0 style="display:none" /> <br>
	<input type="text" id="m6_measurement" value=0 style="display:none" /> <br>
	<input type="text" id="m6_slopegradient" value=0 style="display:none" /> <br>
	<input type="text" id="m6_maxtemp" value=0 style="display:none" /> <br>
	<input type="text" id="m6_mintemp" value=0 style="display:none" /> <br>
	<input type="text" id="m6_avgtemp" value=0 style="display:none" /> <br>
	<input type="text" id="m6_osd" value=0 style="display:none" /> <br>

	<input type="text" id="m7_left" value=0 style="display:none" /> <br>
	<input type="text" id="m7_right" value=0 style="display:none" /> <br>
	<input type="text" id="m7_top" value=0 style="display:none" /> <br>
	<input type="text" id="m7_bottom" value=0 style="display:none" /> <br>
	<input type="text" id="m7_type" value=0 style="display:none" /> <br>
	<input type="text" id="m7_filteringtime" value=0 style="display:none" /> <br>
	<input type="text" id="m7_temperature" value=0 style="display:none" /> <br>
	<input type="text" id="m7_tolerance" value=0 style="display:none" /> <br>
	<input type="text" id="m7_rule" value=0 style="display:none" /> <br>
	<input type="text" id="m7_emissivitytype" value=0 style="display:none" /> <br>
	<input type="text" id="m7_emissivity" value=0 style="display:none" /> <br>
	<input type="text" id="m7_measurement" value=0 style="display:none" /> <br>
	<input type="text" id="m7_slopegradient" value=0 style="display:none" /> <br>
	<input type="text" id="m7_maxtemp" value=0 style="display:none" /> <br>
	<input type="text" id="m7_mintemp" value=0 style="display:none" /> <br>
	<input type="text" id="m7_avgtemp" value=0 style="display:none" /> <br>
	<input type="text" id="m7_osd" value=0 style="display:none" /> <br>

	<input type="text" id="m8_left" value=0 style="display:none" /> <br>
	<input type="text" id="m8_right" value=0 style="display:none" /> <br>
	<input type="text" id="m8_top" value=0 style="display:none" /> <br>
	<input type="text" id="m8_bottom" value=0 style="display:none" /> <br>
	<input type="text" id="m8_type" value=0 style="display:none" /> <br>
	<input type="text" id="m8_filteringtime" value=0 style="display:none" /> <br>
	<input type="text" id="m8_temperature" value=0 style="display:none" /> <br>
	<input type="text" id="m8_tolerance" value=0 style="display:none" /> <br>
	<input type="text" id="m8_rule" value=0 style="display:none" /> <br>
	<input type="text" id="m8_emissivitytype" value=0 style="display:none" /> <br>
	<input type="text" id="m8_emissivity" value=0 style="display:none" /> <br>
	<input type="text" id="m8_measurement" value=0 style="display:none" /> <br>
	<input type="text" id="m8_slopegradient" value=0 style="display:none" /> <br>
	<input type="text" id="m8_maxtemp" value=0 style="display:none" /> <br>
	<input type="text" id="m8_mintemp" value=0 style="display:none" /> <br>
	<input type="text" id="m8_avgtemp" value=0 style="display:none" /> <br>
	<input type="text" id="m8_osd" value=0 style="display:none" /> <br>

</body>

<script>
	//<!--#playinfo-->
	var CameraFunc = <? $GLOBALS['camera_configs']->getCameraInfo(); ?>;
	var TemperatureInfo = <? getTemperatureDetectInfo(); ?>;
	var ConvertInfo = <? getTemperatureconvertInfo(); ?>;
	var VideoInfo = <? getChannelInfo($GLOBALS['profile_conf']); ?>;
</script>
<script src="./setup_event_seekware_temperature_detect.js"></script>
</html>
