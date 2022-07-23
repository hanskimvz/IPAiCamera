<?
require('../_define.inc');
require('../class/capability.class');

$shm_id = shmop_open(KEY_SM_SHARED_CONFIG, "a", 0, 0);
$system_caps = new CCapability($shm_id);
$get_oem = $system_caps->getOEM(); 
?>
<!DOCTYPE html>
<html>
<head>
	<title>Event Rule Configuration</title>
	<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
</head>
<body  oncontextmenu="return false" onselectstart="return false"  ondragstart="return false">
	<div class="contentTitle"><span tkey="setup_event_rules_config"></span></div>
	<div id="actions_list">
		<div class="content">
			<label class="maintitle"><span tkey="setup_event_rule"></span></label>
			<div class="result_table">
				<table class="result_filed">
					<thead>
						<tr class="headline">
							<th class="qt"><span tkey="setup_name"></span></th>
							<th class="qt"><span tkey="setup_reserve_event"></span></th>
							<th class="qt"><span tkey="setup_schedule"></span></th>
							<th class="qt"><span tkey="setup_action"></span></th>
						</tr>
					</thead>
					<tbody id="result_table">
					</tbody>
				</table>
			</div>
		</div>
		<center>
			<button id="add" class="button"><span tkey="setup_add"></span></button>
			<button id="modify" class="button"><span tkey="setup_modify"></span></button>
			<button id="delete" class="button"><span tkey="setup_delete"></span></button>
		</center>
	</div>
	<div id="action_add_modify">
		<div class="content">
			<div class="maintitle"><span tkey="setup_general"></span></div>
<? if ( $get_oem != 2) { ?>
			<div id="activation_ui">
				<label class="subtitle"><span tkey="setup_event_activation"></span></label>
				<input type="radio" value="1" name="enabled" id="enabled_on" >
				<label for="enabled_on"></label>
				<span class="c_title" tkey="on"></span>

				<input type="radio" value="0" name="enabled" id="enabled_off" >
				<label for="enabled_off"></label>
				<span class="c_title" tkey="off">Off</span><br>
			</div>
<? } ?>
			<label class="subtitle"><span tkey="setup_name"></span></label>
			<input type="text" id="name" />
		</div>
		<div id="event_contidion" class='content'>
			<div class='maintitle'><span tkey="setup_event_condition"></span></div>
			<label class='subtitle'><span tkey="setup_event"></span></label>
			<?
			for($i = 0 ; $i < 1 ; $i++)
			{
				if( $i == 0) echo "<div class='select'>";
				else echo "<div class='select event_type'>";
				echo "<select id='event". $i . "_type' name='event_type'>";
				echo "</select></div><br>";
			}
			?>
<? if ( $get_oem == 2) { ?>
			<div class="contentNotice">
			<ul class="padding_left30">
			<span tkey="setup_msg_sysinit">If "System Initialize" is selected, "Recoding" does not work.</span>
			</ul>
			</div>
<? } ?>
<? if ( $get_oem != 2) { ?>
			<label class='subtitle'><span tkey="setup_schedule"></span></label>
			<input type='radio' value='1' name='always'  id='always_on' >
			<label for='always_on'></label>
			<span class='c_title' tkey="setup_always"></span>
			<input type='radio' value='0' name='always'  id='always_off'>
			<label for='always_off'></label>
			<span class='c_title' tkey="setup_manual"></span><br>
			<div id="schedule_dtail">
				<label class='subtitle'><span tkey="setup_week"></span></label>
				<input type='checkbox' id='sun' name='schedule'>
				<label for='sun'></label><span class='c_title'  tkey="setup_sun"></span>
				<input type='checkbox' id='mon' name='schedule'>
				<label for='mon'></label><span class='title' tkey="setup_mon"></span>
				<input type='checkbox' id='tue' name='schedule'>
				<label for='tue'></label><span class='c_title' tkey="setup_tue"></span>
				<input type='checkbox' id='wed' name='schedule'>
				<label for='wed'></label><span class='c_title' tkey="setup_wed"></span>
				<input type='checkbox' id='thu' name='schedule'>
				<label for='thu'></label><span class='c_title' tkey="setup_thu"></span>
				<input type='checkbox' id='fri' name='schedule'>
				<label for='fri'></label><span class='c_title' tkey="setup_fri"></span>
				<input type='checkbox' id='sat' name='schedule'>
				<label for='sat'></label><span class='c_title' tkey="setup_sat"></span><br>

				<label class='subtitle'><span tkey="setup_time"></span></label>
				<div class='select third'>
					<select id='shour' name='schedule' class='third'></select>
				</div>
				<div class='select third'>
					<select id='smin' name='schedule' class='third'></select>
				</div>~
				<div class='select third'>
					<select id='ehour' name='schedule' class='third'></select>
				</div>
				<div class='select third'>
					<select id='emin' name='schedule' class='third'></select>
				</div>
			</div>
<? } ?>
		</div>
		<div class="content">
			<div class="maintitle"><span tkey="setup_action"></span></div>
			<label class="subtitle"><span tkey="setup_rules"></span></label>
			<div class="select long">
				<select id="action_id" class="long">
				</select>
			</div>
			<div id="action_detail">
			</div>
		</div>
		<center>
			<button class="button" id="save"><span tkey="setup_save"></span></button>
			<button class="button" id="cancel"><span tkey="setup_cancel"></span></button>
		</center>	
	</div>
	<script>
		var MaxNumTrigger     = <? echo MAX_NUM_TRIGGER ?>;
		var EventConditionMax = <? echo MAX_NUM_EVENT_TYPE ?> ;

<? 
	echo "var ON_EVENT_NONE = 0; ";
	echo "var ON_EVENT_MOTION="               . ON_EVENT_MOTION               . ";";
	echo "var ON_EVENT_SCHEDULER="            . ON_EVENT_SCHEDULER            . ";";
	echo "var ON_EVENT_SENSOR_ALARM="         . ON_EVENT_SENSOR_ALARM         . ";";
	echo "var ON_EVENT_TEMPERATURE_CRITICAL=" . ON_EVENT_TEMPERATURE_CRITICAL . ";";
	echo "var ON_EVENT_NETWORK_DISCONNECTED=" . ON_EVENT_NETWORK_DISCONNECTED . ";";
	echo "var ON_EVENT_SD_FULL="              . ON_EVENT_SD_FULL              . ";";
	echo "var ON_EVENT_ILLEGAL_LOGIN=" . ON_EVENT_ILLEGAL_LOGIN . ";";
	echo "var ON_EVENT_TEMPERATURE_DETECTED=" . ON_EVENT_TEMPERATURE_DETECTED . ";";
	echo "var ON_EVENT_CUSTOM_SNAP=" . ON_EVENT_CUSTOM_SNAP . ";";
	echo "var ON_EVENT_PIR_DETECTED=" 		  . ON_EVENT_PIR_DETECTED . ";";
	echo "var ON_EVENT_SYS_INIT=" 		  	  . ON_EVENT_SYS_INIT . ";";
?>
	</script>	
	<script src="./setup_event_event_rules.js"></script>
</body>
</html>
