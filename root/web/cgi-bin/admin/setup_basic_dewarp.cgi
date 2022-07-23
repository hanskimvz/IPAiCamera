<?
require('../_define.inc');
require('../class/system.class');
require('../class/capability.class');
require('../class/media.class');

$system_caps = new CCapability();
$profile_conf = new CProfileConfiguration();
$video_source_confs = $GLOBALS['profile_conf']->VideoSourceConfigurations;

function get_dewarp_Info($name)
{
	$channel = 0;
	echo $name."['dewarp_enabled']=" .$GLOBALS['video_source_confs']->Config[$channel]->Dewarp->enabled.";\r\n";
} 
?>

<!DOCTYPE html>
<html>
	<head>
		<meta content="text/html; charset=utf-8" http-equiv="Content-Type">
		<title>osd configuration</title>
	</head>
	<body oncontextmenu="return false" onselectstart="return false"  ondragstart="return false">
		<div class="contentTitle"><span tkey="Dewarping_Configuration"></span></div>
		<div class="content" style="display:none">
			<label class="subtitle" tkey="setup_vin_source"></label>
			<div class="select">
				<select id="vin_source" autocomplete="off">
				</select>
			</div>
		</div>
		<div class="content">
			<label class="maintitle"><span tkey="Dewarping"></span></label>
			<input id="dewarp_off" type="radio" name="dewarp_enabled" value=0 >
			<label for="dewarp_off"></label><span tkey=off></span>
			<input id="dewarp_on" type="radio" name="dewarp_enabled" value=1 >
			<label for="dewarp_on"></label><span tkey=on></span><br>
		</div>
		<center><button id="btOK" class="button" ><span tkey="apply"></span></button></center> 
		<script type="text/javascript">
		    var capInfo = <? $GLOBALS['system_caps']->getCapability() ?>;
			var dewarp_info = new Object();
			<?
				get_dewarp_Info("dewarp_info"); 
			?>
		</script>
		<script type="text/javascript" src="./setup_basic_dewarp.js"></script>
	</body>
</html>
