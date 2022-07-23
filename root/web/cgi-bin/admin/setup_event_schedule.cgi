 <?
require('../_define.inc');
require('../class/event.class');

$event_conf = new CEventConfiguration();

//--- ip
function getscheduleInfo($name)   
{	  
		echo $name."['enable']="		.$GLOBALS['event_conf']->schedule_conf->enable."\r\n";
		echo $name."['interval']="	.$GLOBALS['event_conf']->schedule_conf->interval_value."\r\n";
/*		echo $name."['unit']="		.$GLOBALS['event_conf']->schedule_conf->interval_unit."\r\n";
		echo $name."['activation']="	.$GLOBALS['event_conf']->schedule_conf->always."\r\n";
		echo $name."['sun']="			.$GLOBALS['event_conf']->schedule_conf->week->sun."\r\n";
		echo $name."['mon']="			.$GLOBALS['event_conf']->schedule_conf->week->mon."\r\n";
		echo $name."['tue']="			.$GLOBALS['event_conf']->schedule_conf->week->tue."\r\n";
		echo $name."['wed']="			.$GLOBALS['event_conf']->schedule_conf->week->wed."\r\n";
		echo $name."['thu']="			.$GLOBALS['event_conf']->schedule_conf->week->thu."\r\n";
		echo $name."['fri']="			.$GLOBALS['event_conf']->schedule_conf->week->fri."\r\n";
		echo $name."['sat']="			.$GLOBALS['event_conf']->schedule_conf->week->sat."\r\n";
		echo $name."['shour']="		.$GLOBALS['event_conf']->schedule_conf->time_range->start_hour."\r\n";
		echo $name."['smin']="		.$GLOBALS['event_conf']->schedule_conf->time_range->start_min."\r\n";
		echo $name."['ehour']="		.$GLOBALS['event_conf']->schedule_conf->time_range->end_hour."\r\n";
		echo $name."['emin']="		.$GLOBALS['event_conf']->schedule_conf->time_range->end_min."\r\n";*/
}
?>
<!DOCTYPE html>
<html>
	<head>
		<title>schedule configuration</title>
		<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />

	</head>
	<body oncontextmenu="return false" onselectstart="return false"  ondragstart="return false">
		<div class="contentTitle" id="schedule_config"></div>
		<div class="content">
			<label class="maintitle"><span tkey="setup_recurrences"></span></label>

			<label class="subtitle" tkey="setup_mode">Mode</label>
			<input type="radio" value="1" name="enable"  id="optSchedTime1" ><label for="optSchedTime1"></label><span tkey="setup_enable"></span>
			<input type="radio" value="0" name="enable"  id="optSchedTime2" ><label for="optSchedTime2"></label><span tkey="setup_disable_off"></span><br>
			<label class="subtitle"><span tkey="setup_repeat"></span></label>
			<div class="select">
				<select id="interval">
					<option value="0" tkey="setup_each_5min">Every 5  minutes </option>
					<option value="1" tkey="setup_each_10min">Every 10 minutes </option>
					<option value="2" tkey="setup_each_15min">Every 15 minutes </option>
					<option value="3" tkey="setup_each_30min">Every 30 minutes </option>
					<option value="4" tkey="setup_each_45min">Every 45 minutes </option>
					<option value="5" tkey="setup_each_1hour">Every 1  hour </option>
					<option value="6" tkey="setup_each_6hour">Every 6  hours </option>
					<option value="7" tkey="setup_each_12hour">Every 12 hours </option>
					<option value="8" tkey="setup_each_1day">Every 1  Day </option>
					<option value="9" tkey="setup_each_week">Every Week </option>
				</select>
			</div>
		</div>
		<!-- <div class="content" id="Transfer_Interval">
			<label class="maintitle">Transfer Interval</label>
			<label class="subtitle">One Image Per</label>
			<div class="select">
				<select id="interval">
					<option value="0">5 Sec</option>
					<option value="1">15 Sec</option>
					<option value="2">30 Sec</option>
					<option value="3">45 Sec</option>
					<option value="4">60 Sec</option>
					<option value="5">5 Min</option>
					<option value="6">15 Min</option>
					<option value="7">30 Min</option>
					<option value="8">45 Min</option>
					<option value="9">60 Min</option>
				</select>
			</div>

		</div>
		<div class="content" id="Activation_Time">
			<label class="maintitle">Activation Time</label>
			<div class="line">
				<input type="radio" value="1" name="activation"  id="optActivationTime1" >Always<label for="optActivationTime1"></label>
				<input type="radio" value="0" name="activation"  id="optActivationTime2" >Only Scheduled Time<label for="optActivationTime2"></label><br>
			</div>
			<div class="line">
				<input type="checkbox" id="sun" value="1">Sun<label for="sun"></label>
				<input type="checkbox" id="mon" value="1">Mon<label for="mon"></label>
				<input type="checkbox" id="tue" value="1">Tue<label for="tue"></label>
				<input type="checkbox" id="wed" value="1">Wed<label for="wed"></label>
				<input type="checkbox" id="thu" value="1">Thu<label for="thu"></label>
				<input type="checkbox" id="fri" value="1">Fri<label for="fri"></label>
				<input type="checkbox" id="sat" value="1">Sat<label for="sat"></label>
			</div>

			<label class="subtitle">Time</label>
			<div class="select third">
				<select id="shour" class="third"></select>
			</div> :
			<div class="select third">
				<select id="smin" class="third"></select>
			</div>~
			<div class="select third">
				<select id="ehour" class="third"></select>
			</div> :
			<div class="select third">
				<select id="emin" class="third"></select>
			</div>
		</div> -->
		<center>
			<button id="btOK"  class="button" ><span tkey="apply"></span></button>
		</center>
		
		<script type="text/javascript">
			var scheduleInfo = new Object();
		<? 
				getscheduleInfo("scheduleInfo"); 
		?>
		</script>
		
		<script src="./setup_event_schedule.js"></script>
	</body>
</html>
