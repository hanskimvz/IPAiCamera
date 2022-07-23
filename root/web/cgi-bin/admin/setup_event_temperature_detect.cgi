<?
require('../_define.inc');
require('../class/event.class');
require('../class/media.class');

$event_conf = new CEventConfiguration();
$profile_conf = new CProfileConfiguration();

function getTemperatureDetectInfo()
{
	global $event_conf;
	//print_r($event_conf->temperature_confs->conf[0]);
	for($i=0 ; $i<4 ; ++$i )
	{
		for($j=0; $j < 4 ; ++$j ) 
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
	-->
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
		<option value=0 selected=true tkey="setup_measuring_area_1"> Measuring Area 1 </option>
		<option value=1 tkey="setup_measuring_area_2"> Measuring Area 2 </option>
		<option value=2 tkey="setup_measuring_area_3"> Measuring Area 3 </option>
		<option value=3 tkey="setup_measuring_area_4"> Measuring Area 4 </option>
		</select>
		</div> <br>
		<label class="subtitle" tkey="setup_alarm_rule">Area</label>
	  	<div class="select">
		<select id = "rulesel" onchange="javascript:setChangeRule(this.selectedIndex)">
		<option value=0 selected=true tkey="setup_rule_1"> Above (Average Temperature) </option>
		<option value=1 tkey="setup_rule_2"> Below (Average Temperature) </option>
		<option value=2 tkey="setup_rule_3"> Above(Max Temperature) </option>
		<option value=3 tkey="setup_rule_4"> Below (Min Temperature) </option>
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

		<label id="sensitivity_sub" class="subtitle"><span tkey="setup_temperature"></span></label>
		<div class="slider_box">
			<div id="sensslider" class="long"></div>        
			[<label id="senslabel">0</label> °C]
		</div>
		<label id="tolerance_sub" class="subtitle"><span tkey="setup_tolerance"></span></label>
		<div class="slider_box">
			<div id="toleranceslider" class="long"></div>        
			[<label id="tolerancelabel">0</label> °C]
		</div>
		<label id="threshold_sub" class="subtitle"><span tkey="setup_filter_time"></span></label>
		<div class="slider_box">
			<div id="sizeslider" class="long"></div>        
			[<label id="sizelabel">0</label> Sec]
		</div><br>
		

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

	<input type="text" id="m1_left" value=0 style="display:none" /> <br>
	<input type="text" id="m1_right" value=0 style="display:none" /> <br>
	<input type="text" id="m1_top" value=0 style="display:none" /> <br>
	<input type="text" id="m1_bottom" value=0 style="display:none" /> <br>
	<input type="text" id="m1_type" value=0 style="display:none" /> <br>
	<input type="text" id="m1_filteringtime" value=0 style="display:none" /> <br>
	<input type="text" id="m1_temperature" value=0 style="display:none" /> <br>
	<input type="text" id="m1_tolerance" value=0 style="display:none" /> <br>
	<input type="text" id="m1_rule" value=0 style="display:none" /> <br>

	<input type="text" id="m2_left" value=0 style="display:none" /> <br>
	<input type="text" id="m2_right" value=0 style="display:none" /> <br>
	<input type="text" id="m2_top" value=0 style="display:none" /> <br>
	<input type="text" id="m2_bottom" value=0 style="display:none" /> <br>
	<input type="text" id="m2_type" value=0 style="display:none" /> <br>
	<input type="text" id="m2_filteringtime" value=0 style="display:none" /> <br>
	<input type="text" id="m2_temperature" value=0 style="display:none" /> <br>
	<input type="text" id="m2_tolerance" value=0 style="display:none" /> <br>
	<input type="text" id="m2_rule" value=0 style="display:none" /> <br>

	<input type="text" id="m3_left" value=0 style="display:none" /> <br>
	<input type="text" id="m3_right" value=0 style="display:none" /> <br>
	<input type="text" id="m3_top" value=0 style="display:none" /> <br>
	<input type="text" id="m3_bottom" value=0 style="display:none" /> <br>
	<input type="text" id="m3_type" value=0 style="display:none" /> <br>
	<input type="text" id="m3_filteringtime" value=0 style="display:none" /> <br>
	<input type="text" id="m3_temperature" value=0 style="display:none" /> <br>
	<input type="text" id="m3_tolerance" value=0 style="display:none" /> <br>
	<input type="text" id="m3_rule" value=0 style="display:none" /> <br>

	<input type="text" id="m4_left" value=0 style="display:none" /> <br>
	<input type="text" id="m4_right" value=0 style="display:none" /> <br>
	<input type="text" id="m4_top" value=0 style="display:none" /> <br>
	<input type="text" id="m4_bottom" value=0 style="display:none" /> <br>
	<input type="text" id="m4_type" value=0 style="display:none" /> <br>
	<input type="text" id="m4_filteringtime" value=0 style="display:none" /> <br>
	<input type="text" id="m4_temperature" value=0 style="display:none" /> <br>
	<input type="text" id="m4_tolerance" value=0 style="display:none" /> <br>
	<input type="text" id="m4_rule" value=0 style="display:none" /> <br>
</body>

<script>
	//<!--#playinfo-->
	var TemperatureInfo = <? getTemperatureDetectInfo(); ?>;
	var VideoInfo = <? getChannelInfo($GLOBALS['profile_conf']); ?>;
</script>
<script src="./setup_event_temperature_detect.js"></script>
</html>
