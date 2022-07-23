<?
require('../_define.inc');
require('../class/system.class');
require('../class/capability.class');

$system_conf = new CSystemConfiguration();
$system_caps = new CCapability();

//--- SmartLBR
function getSmartlBRInfo($name)
{	
  	 echo $name."['lbr_streamid']="   	  .$GLOBALS['system_conf']->SmartLBR->streamid.";\r\n";
	 echo $name."['lbr_style']="          .$GLOBALS['system_conf']->SmartLBR->style.";\r\n";  
	 echo $name."['lbr_bitrate']="		  .$GLOBALS['system_conf']->SmartLBR->bitrate.";\r\n";  
	 	 
	 echo $name."['lbr_motion_level']="   .$GLOBALS['system_conf']->SmartLBR->motion_level.";\r\n"; 
	 echo $name."['lbr_noise_level']="    .$GLOBALS['system_conf']->SmartLBR->noise_level.";\r\n"; 
	 echo $name."['lbr_autorun']="		  .$GLOBALS['system_conf']->SmartLBR->autorun.";\r\n"; 
	 echo $name."['lbr_onoff']='"         .$GLOBALS['system_conf']->SmartLBR->onoff."';\r\n";  
	 echo $name."['lbr_profile_0']='"     .$GLOBALS['system_conf']->SmartLBR->profile_0."';\r\n";  
	 echo $name."['lbr_profile_1']='"     .$GLOBALS['system_conf']->SmartLBR->profile_1."';\r\n";  
	 echo $name."['lbr_profile_2']='"     .$GLOBALS['system_conf']->SmartLBR->profile_2."';\r\n";  
	 echo $name."['lbr_profile_3']='"     .$GLOBALS['system_conf']->SmartLBR->profile_3."';\r\n";  
	 echo $name."['lbr_profile_4']='"     .$GLOBALS['system_conf']->SmartLBR->profile_4."';\r\n";  
}
?>

<!DOCTYPE html>
<html>
	<head>
		<meta content="text/html; charset=utf-8" http-equiv="Content-Type">
		<title>SmartLBR configuration</title>
	</head>
	<body oncontextmenu="return false" onselectstart="return false"  ondragstart="return false">
		<div class="contentTitle"><span tkey="setup_av_lbr_config"></span></div>
		<div class="content">

			<label class="maintitle" colspan="2" tkey="setup_mode">Mode</label>
			<input id="lbr_onoff_off" type="radio" name="lbr_onoff" value=0 >
			<label for="lbr_onoff_off"></label><span tkey="off">Off</span>
			<input id="lbr_onoff_on" type="radio" name="lbr_onoff" value=1 >
			<label for="lbr_onoff_on"></label><span tkey="setup_auto">Auto</span>
			<input id="lbr_onoff_manual" type="radio" name="lbr_onoff" value=2 >
			<label for="lbr_onoff_manual"></label><span tkey="setup_manual">Manual</span><br><br>
			
			<div style="display:none">
			<label class="maintitle" colspan="2">AUTO</label>
			<input id="lbr_auto_off" type="radio" name="lbr_autorun" value=0 >
			<label for="lbr_auto_off"></label><span tkey="off">Off</span>
			<input id="lbr_auto_on" type="radio" name="lbr_autorun" value=1 >
			<label for="lbr_auto_on"></label><span tkey="on">On</span><br><br>
			
			<label class="maintitle" colspan="2">Stream-ID</label>
			<label class="subtitle">StreamId</label>
			<input type="text" id="lbr_streamid" maxlength="1" class="third" name="lbr_streamid" />[ 0 ~ 4 ]<br><br>
			</div>

			<label class="maintitle" colspan="2" tkey="setup_manual">Manual</label>

			<input id="lbr_style_0" type="radio" name="lbr_style" value=0 >
			<label for="lbr_style_0"></label><span tkey="setup_lbrmode_0">Fullfps auto bitrate</span><br>
			<input id="lbr_style_1" type="radio" name="lbr_style" value=1 >
			<label for="lbr_style_1"></label><span tkey="setup_lbrmode_1">Enabel fps drop</span><br>
			<input id="lbr_style_2" type="radio" name="lbr_style" value=2 >
			<label for="lbr_style_2"></label><span tkey="setup_lbrmode_2">Security IPCam style CBR</span><br><br>
			
			<label class="subtitle" tkey="target_bitrate">Bitrate</label>
			<input type="text" id="lbr_bitrate" maxlength="5" class="third" name="lbr_bitrate" />[ 64 ~ 20000 ]kbps<br><br>

			<div style="display:none">
			<input id="lbr_motion_0" type="radio" name="lbr_motion_level" value=0 >
			<label for="lbr_motion_0"></label><span>no motion</span>
			<input id="lbr_motion_1" type="radio" name="lbr_motion_level" value=1 >
			<label for="lbr_motion_1"></label><span>small motion</span>
			<input id="lbr_motion_2" type="radio" name="lbr_motion_level" value=2 >
			<label for="lbr_motion_2"></label><span>big motion</span><br><br>

			<input id="lbr_noise_0" type="radio" name="lbr_noise_level" value=0 >
			<label for="lbr_noise_0"></label><span>no noise</span>
			<input id="lbr_noise_1" type="radio" name="lbr_noise_level" value=1 >
			<label for="lbr_noise_1"></label><span>low noise</span>
			<input id="lbr_noise_2" type="radio" name="lbr_noise_level" value=2 >
			<label for="lbr_noise_2"></label><span>high noise</span><br><br>

			<label class="subtitle">static</label>
			<input type="text" id="lbr_profile_0" maxlength="5" class="third" name="lbr_profile_0"/>[1~255]<br>
			<label class="subtitle">small motion</label>
			<input type="text" id="lbr_profile_1" maxlength="5" class="third" name="lbr_profile_1"/>[1~255]<br>
			<label class="subtitle">big motion</label>
			<input type="text" id="lbr_profile_2" maxlength="5" class="third" name="lbr_profile_2"/>[1~255]<br>
			<label class="subtitle">low light</label>
			<input type="text" id="lbr_profile_3" maxlength="5" class="third" name="lbr_profile_3"/>[1~255]<br>

			<label class="subtitle">big motion(frame drop)</label>
			<input type="text" id="lbr_profile_4" maxlength="5" class="third" name="lbr_profile_4"/>[1~255]<br>
			</div>
			
		</div>
		<center><button id="LBR_btOK" class="button" ><span tkey="apply"></span></button></center> 
		<script type="text/javascript">
			var SmartLBRInfo = new Object();
			<? 
				getSmartLBRInfo("SmartLBRInfo"); 
			?>
			console.log(SmartLBRInfo);
		</script>
		<script src="./setup_basic_lbr.js"></script>
	</body>
</html>
