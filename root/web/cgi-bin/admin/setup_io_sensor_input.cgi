 <?
require('../_define.inc');
require('../class/system.class');
require('../class/capability.class');

$sys_conf = new CSystemConfiguration();
$system_caps = new CCapability();

//--- ip
function getalramInfo($name)   
{	
		echo $name."['mode']="		.$GLOBALS['sys_conf']->DeviceIo->SensorSettings->Sensor[0]->Mode."\r\n";
		echo $name."['mode1']="		.$GLOBALS['sys_conf']->DeviceIo->SensorSettings->Sensor[1]->Mode."\r\n";
}
?> 
<!DOCTYPE html>
<html>
	<head>
		<title>schedule configuration</title>
		<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
		<script src="/js/Chart.bundle.min.js"></script>

	</head>
	<body oncontextmenu="return false" onselectstart="return false"  ondragstart="return false">
		<div class="contentTitle"><span tkey="setup_alarm_config"></span></div>
                <div id="alarm_div0" class="content">
                        <label class="maintitle"><span tkey="setup_alarm_input_setup"></span></label>
                        <input type="radio" value="0" name="mode"  id="optDeviceTime1" > <label for="optDeviceTime1"></label><span tkey="setup_alarm_off"></span>
                        <input type="radio" value="1" name="mode"  id="optDeviceTime2" > <label for="optDeviceTime2"></label><span id="alarm_open" tkey="setup_alarm_open"></span>
                        <input type="radio" value="2" name="mode"  id="optDeviceTime3" > <label for="optDeviceTime3"></label><span id="alarm_close" tkey="setup_alarm_close"></span>
                        <input type="radio" value="3" name="mode"  id="optDeviceTime4" > <label for="optDeviceTime4"></label><span id="optDeviceTime4_label">supervisor</span>
                </div>
                <center>
                        <button id="btOK0" class="button" ><span tkey="apply"></span></button>
                </center>
                <div id="alarm_div1" class="content">
                        <label class="maintitle"><span tkey="setup_alarm_input_setup"></span></label>
                        <input type="radio" value="0" name="mode1"  id="optDeviceADC1" > <label for="optDeviceADC1"></label><span tkey="setup_alarm_off"></span>
                        <input type="radio" value="1" name="mode1"  id="optDeviceADC2" > <label for="optDeviceADC2"></label><span tkey="setup_alarm_open"></span>
                        <input type="radio" value="2" name="mode1"  id="optDeviceADC3" > <label for="optDeviceADC3"></label><span tkey="setup_alarm_close"></span>
                        <input type="radio" value="3" name="mode1"  id="optDeviceADC4" > <label for="optDeviceADC4"></label><span id="optDeviceADC4_label">supervisor</span>
                </div>
                <center>
                        <button id="btOK1" class="button" ><span tkey="apply"></span></button>
                </center>
                <div id="alarm_chart" class="content">
                        <canvas id="ADCChart0" width="480" height="350"></canvas>
                        <button id="alarminput1_adc" class="button round">0</button> Value= <span id="ADC0" class="hidden"></span>
                        <button id="alarminput2_adc" class="button round">0</button> Value= <span id="ADC1" class="hidden"></span>
                        N.C (2.3) N.C(1.0) SUPER(UP(1.0,2,5) DOWN(0.8,2.3))
                </div>

		<script type="text/javascript">
			var capInfo = <? $GLOBALS['system_caps']->getCapability() ?>;
			var alramInfo = new Object();
		<? 
				getalramInfo("alramInfo"); 
		?>
		</script>
		<script src="./setup_io_sensor_input.js"></script>
	</body>
</html>


