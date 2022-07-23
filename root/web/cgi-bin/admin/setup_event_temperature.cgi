 <?
require('../_define.inc');
require('../class/system.class');

$sys_conf = new CSystemConfiguration();

//--- ip
function getTemperatureInfo($name)   
{	
		echo $name."['mode']="		.$GLOBALS['sys_conf']->DeviceIo->TemperatureSettings->mode."\r\n";
		echo $name."['threshold']="		.$GLOBALS['sys_conf']->DeviceIo->TemperatureSettings->threshold."\r\n"; 
}
?> 
<!DOCTYPE html>
<html>
	<head>
		<title>schedule configuration</title>
		<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />

	</head>
	<body oncontextmenu="return false" onselectstart="return false"  ondragstart="return false">
		<div class="contentTitle"><span tkey="setup_event_temperature"></span></div>
		<div class="content">
			<label class="maintitle"><span tkey="setup_general_setting"></span></label>
			
			<label class="subtitle"><span tkey="setup_event_temperatemode"></span></label>
			<div class="select">
				<select id="mode">
					<option value="0" tkey="Celsius"></option>
					<option value="1" tkey="Fahrenheit"></option>
				</select>
			</div><br>	
			<label class="subtitle"><span tkey="setup_event_temptreshold"></span></label>
			<input type="number" id="threshold" class="short" ><label id="threshold_label" ></span></label><br>
			<label class="subtitle"><span tkey="setup_event_temperature"></span></label>
			<label id="temperatureval" style="margin-left:6px;"></span></label>
		</div>	
		<center>
			<button id="btOK" class="button" ><span tkey="apply"></span></button>
		</center>
		
		<script type="text/javascript">
			var temperatureInfo = new Object();
		<? 
				getTemperatureInfo("temperatureInfo"); 
		?>
		</script>
		<script src="./setup_event_temperature.js"></script>
	</body>
</html>
