 <?
require('../_define.inc');
require('../class/system.class');
require('../class/capability.class');

$sys_conf = new CSystemConfiguration();
$system_caps = new CCapability();
//--- ip
function getrelayInfo($name)   
{	
		echo $name."['size']="		.$GLOBALS['system_caps']->relay_count."\r\n";
//   	echo $name."['id']="		.0."\r\n";
		for ($num=0; $num<$GLOBALS['system_caps']->relay_count; $num++){
			echo $name."[$num]['mode']="		.$GLOBALS['sys_conf']->DeviceIo->RelaySettings->Relay[$num]->Mode."\r\n";
			echo $name."[$num]['idlestate']="		.$GLOBALS['sys_conf']->DeviceIo->RelaySettings->Relay[$num]->IdleState."\r\n";
			if($GLOBALS['sys_conf']->DeviceIo->RelaySettings->Relay[$num]->DelayTime == 0)
			  echo $name."[$num]['duration']="		."1\r\n";
			else
			  echo $name."[$num]['duration']="		.$GLOBALS['sys_conf']->DeviceIo->RelaySettings->Relay[$num]->DelayTime."\r\n";
		}
}
?> 
<!DOCTYPE html>
<html>
	<head>
		<title>RELAYOUT CONFIGURATION</title>
		<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />

	</head>
	<body oncontextmenu="return false" onselectstart="return false"  ondragstart="return false">
		<div class="contentTitle"><span tkey="setup_relay_out_config">RELAYOUT CONFIGURATION</span></div>
		<div class="content">
  		<label class="subtitle" tkey="setup_relay_out_select">Relay output</label>
  	  	<div class="select">
  		<select id ="RelayoutIndex" onchange="javascript:setActiveRect(this.selectedIndex)">
   		</select>
  		</div> 
  	</div>
  	<div class="content">
			<label class="subtitle"><span tkey="setup_relay_out_mode"></span></label>
			<input type="radio" value="0" name="mode"  id="optRelayMode1" > <label for="optRelayMode1"></label><span tkey="setup_relay_out_mode_mono"></span>
			<input type="radio" value="1" name="mode"  id="optRelayMode2" > <label for="optRelayMode2" ></label> <span tkey="setup_relay_out_mode_bi"></span>
			<br>	
			<label class="subtitle"><span tkey="setup_relay_out_idle"></span></label>
			<input type="radio" value="0" name="idlestate"  id="optRelayIdle1" > <label for="optRelayIdle1" ></label><span tkey="setup_relay_out_idle_close"></span>
			<input type="radio" value="1" name="idlestate"  id="optRelayIdle2" > <label for="optRelayIdle2" ></label><span tkey="setup_relay_out_idle_open"></span>
			<br>	
			<label class="subtitle"><span tkey="setup_relay_out_duration"></span></label>
			<input type="number" id="duration" class="short" min="1" max="30"><span tkey="setup_transfer_sec"></span> [ 1 ~ 30 ]<br>						
		</div>	
		<center>
			<button id="btOK" class="button" ><span tkey="apply"></span></button>
		</center>
		<script type="text/javascript">
			var relayInfo = new Array(4);
			relayInfo[0] = new Object();
			relayInfo[1] = new Object();
		<? 
			getrelayInfo("relayInfo"); 
		?>
		</script>
		<script src="./setup_io_relay_output.js"></script>
	</body>
</html>


