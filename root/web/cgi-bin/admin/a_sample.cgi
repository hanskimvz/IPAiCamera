<?
require('../_define.inc');
require('../class/system.class');
require('../class/capability.class');

$shm_id       = shmop_open(KEY_SM_SHARED_CONFIG, "a", 0, 0);
$sys_conf = new CSystemConfiguration($shm_id);
$system_caps  = new CCapability($shm_id);

shmop_close($shm_id);

function getrs485($name)
{
	echo $name.'.protocol='.$GLOBALS['sys_conf']->DeviceIo->SerialPortsSetting->protocol.';';
	echo $name.'.address='.$GLOBALS['sys_conf']->DeviceIo->SerialPortsSetting->address.';';
	echo $name.'.baudrate='.$GLOBALS['sys_conf']->DeviceIo->SerialPortsSetting->baudrate.';';
	echo $name.'.databit='.$GLOBALS['sys_conf']->DeviceIo->SerialPortsSetting->databit.';';
	echo $name.'.stopbit='.$GLOBALS['sys_conf']->DeviceIo->SerialPortsSetting->stopbit.';';
	echo $name.'.parity='.$GLOBALS['sys_conf']->DeviceIo->SerialPortsSetting->parity.';';
}
?>

<!DOCTYPE html>
<html>
	<head>
		<meta content="text/html; charset=utf-8" http-equiv="Content-Type">
		<title>AUDIO CONFIGURATION</title>
	</head>
	<body oncontextmenu="return false" onselectstart="return false"  ondragstart="return false">
		<div class="contentTitle"><span tkey="rs485_configuration"></span></div>
		<div class="content">
			<label class="maintitle" colspan="2"><span tkey="rs485"></span></label>
			
			<label class="subtitle"><span tkey="rs485_protocol"></label>
			<div class="select">
				<select id="protocol">
					<option value=0> pelco-D</option>
					<option value=1> pelco-P</option>
				</select>
			</div><br>
			
			<label class="subtitle"><span tkey="rs485_address"></label>
			<div class="select">
				<select id="address">
					<option value=0> pelco-D</option>
					<option value=1> pelco-P</option>
				</select>
			</div><br>

			<label class="subtitle"><span tkey="rs485_baudrate"></label>
			<div class="select">
				<select id="baudrate">
					<option value=0> 110</option>
					<option value=1> 300</option>
					<option value=2> 1200</option>
					<option value=3> 2400</option>
					<option value=4> 4800</option>
					<option value=5> 9600</option>
					<option value=6> 19200</option>
					<option value=7> 38400</option>
					<option value=8> 57600</option>	
					<option value=9> 115200</option>						
				</select>
			</div><br>

			<label class="subtitle"><span tkey="rs485_databit"></label>
			<div class="select">
				<select id="databit">
					<option value=0> 5</option>
					<option value=1> 6</option>
					<option value=2> 7</option>
					<option value=3> 8</option>
				</select>
			</div><br>	
			
			<label class="subtitle"><span tkey="rs485_stopbit"></label>
			<div class="select">
				<select id="stopbit">
					<option value=0 > 0 </option>
					<option value=1> 1</option>
				</select>
			</div><br>
			
			<label class="subtitle"><span tkey="rs485_parity"></label>
			<div class="select">
				<select id="parity">
					<option value=0 tkey="none"> </option>
					<option value=1 tkey="odd"> </option>
					<option value=2 tkey="even"> </option>
				</select>
			</div><br>								
		</div>
		<center>
			<button class="button" id="btOK" type="button"><span tkey="setup_save"></span></button>
		</center>
	<script>
		var rs485 = new Object;
		<?
			getrs485("rs485");
		?>
	</script>
	<script src="./setup_system_rs485.js"></script>
	</body>
</html>
