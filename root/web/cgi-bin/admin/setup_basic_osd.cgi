<?
require('../_define.inc');
require('../class/system.class');
require('../class/capability.class');

$system_conf = new CSystemConfiguration();
$system_caps = new CCapability();
?>

<!DOCTYPE html>
<html>
	<head>
		<meta content="text/html; charset=utf-8" http-equiv="Content-Type">
		<title>osd configuration</title>
	</head>
	<body oncontextmenu="return false" onselectstart="return false"  ondragstart="return false">
		<div class="contentTitle"><span tkey="osd_configuration"></span></div>
		<div class="content" style="display:none">
			<label class="subtitle" tkey="setup_vin_source"></label>
			<div class="select">
				<select id="vin_source" autocomplete="off">
				</select>
			</div>
		</div>
		<div class="content">
			<label class="maintitle"><span tkey="date_time"></span></label>
			<input id="time_off" type="radio" name="time_enabled" value=0 >
			<label for="time_off"></label><span tkey=off></span>
			<input id="time_on" type="radio" name="time_enabled" value=1 >
			<label for="time_on"></label><span tkey=on></span><br>

			<label class="subtitle"><span tkey="start_x"></span></label>
			<input type="text" id="time_x" maxlength="3" class="third"/>[ 0 ~ 100 ]<br>

			<label class="subtitle"><span tkey="start_y"></span></label>
			<input type="text" id="time_y" maxlength="3" class="third"/>[ 0 ~ 100 ]<br>
		</div>
		<div id="temperature_div" class="content">
			<label class="maintitle" colspan="2"><span tkey="user_temperature"></span></label>
			<input id="temperature_off" type="radio" name="temperature_enabled" value=0 >
			<label for="temperature_off"></label><span tkey=off></span>
			<input id="temperature_on" type="radio" name="temperature_enabled" value=1 >
			<label for="temperature_on"></label><span tkey=on></span><br><br>
		
			<label class="subtitle"><span tkey="start_x"></span></label>
			<input type="text" id="temperature_x" maxlength="3" class="third" />[ 0 ~ 100 ]<br>
		
			<label class="subtitle"><span tkey="start_y"></span></label>
			<input type="text" id="temperature_y" maxlength="3" class="third" />[ 0 ~ 100 ]<br><br>
		</div>
		<div class="content">
			<label class="maintitle"><span tkey="user_text"></span></label>
			<input id="text_off" type="radio" name="text_enabled" value=0 >
			<label for="text_off"></label><span tkey="off"></span>
			<input id="text_on" type="radio" name="text_enabled" value=1 >
			<label for="text_on"></label><span tkey="on"></span><br>

			<label class="subtitle"><span tkey="start_x"></span></label>
			<input type="text" id="text_x" maxlength="3" class="third" />[ 0 ~ 100 ]<br>

			<label class="subtitle"><span tkey="start_y"></span></label>
			<input type="text"  id="text_y" maxlength="3" class="third" />[ 0 ~ 100 ]<br>

			<label class="subtitle"><span tkey="text"></span></label>
			<input type="text" id="text" class="long" /><br>
		</div>
		<div class="content" id="div_ptz">
			<label class="maintitle"><span tkey="setup_system_ptz"></span></label>
			<input id="ptz_off" type="radio" name="ptz_enabled" value=0 >
			<label for="ptz_off"></label><span tkey=off></span>
			<input id="ptz_on" type="radio" name="ptz_enabled" value=1 >
			<label for="ptz_on"></label><span tkey=on></span><br>

			<label class="subtitle"><span tkey="start_x"></span></label>
			<input type="text" id="ptz_x" maxlength="3" class="third"/>[ 0 ~ 100 ]<br>

			<label class="subtitle"><span tkey="start_y"></span></label>
			<input type="text" id="ptz_y" maxlength="3" class="third"/>[ 0 ~ 100 ]<br>
		</div>		
        <div class="content" id="osd_stream">
			<label class="maintitle"><span tkey="main_stream"></span></label>

			<input id="main_stream" type="checkbox" name="main_stream" value=0 >
            <label for="main_stream"></label><span tkey=setup_main_stream></span>

            <input id="sub_stream" type="checkbox" name="sub_stream" value=0 >
            <label for="sub_stream"></label><span tkey=setup_sub_stream></span>

            <input id="third_stream" type="checkbox" name="third_stream" value=0 >
            <label for="third_stream"></label><span tkey=setup_third_stream></span>
		</div>		        
		<center><button id="btOK" class="button" ><span tkey="apply"></span></button></center> 
		<script type="text/javascript">
		    var capInfo = <? $GLOBALS['system_caps']->getCapability() ?>;
				var OsdInfo = <?  $GLOBALS['system_conf']->Osds->getOsdInfo(); ?>
		</script>
		<script type="text/javascript" src="./setup_basic_osd.js"></script>
	</body>
</html>
