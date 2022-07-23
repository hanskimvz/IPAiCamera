 <?
require('../_define.inc');
require('../class/event.class');

$event_conf = new CEventConfiguration();

//--- ip
function getalramInfo($name)   
{	
		echo $name."['device']="		.$GLOBALS['event_conf']->alarm_input_conf[0]->device."\r\n";
//		echo $name."['device']="		.$GLOBALS['event_conf']->alarm_input_conf[1]->device."\r\n";

	
}
?> 
<!DOCTYPE html>
<html>
	<head>
		<title>schedule configuration</title>
		<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />

	</head>
	<body oncontextmenu="return false" onselectstart="return false"  ondragstart="return false">
		<div class="contentTitle"><span tkey="setup_alarm_config"></span></div>
		<div class="content">
			<label class="maintitle"><span tkey="setup_alarm_input_setup"></span></label>
			<input type="radio" value="0" name="device"  id="optDeviceTime1" > <label for="optDeviceTime1" class="margin_right_20"></label><span tkey="setup_alarm_off"></span>
			<input type="radio" value="1" name="device"  id="optDeviceTime2" > <label for="optDeviceTime2" class="margin_right_20"></label> <span tkey="setup_alarm_open"></span>
			<input type="radio" value="2" name="device"  id="optDeviceTime3" > <label for="optDeviceTime3" class="margin_right_20"></label> <span tkey="setup_alarm_close"></span>
		</div>
		<center>
			<button id="btOK" class="button" ><span tkey="apply"></span></button>
		</center>
		<script type="text/javascript">
			var alramInfo = new Object();
		<? 
				getalramInfo("alramInfo"); 
		?>
		</script>
		<script src="./setup_event_alarm_input.js"></script>
	</body>
</html>


