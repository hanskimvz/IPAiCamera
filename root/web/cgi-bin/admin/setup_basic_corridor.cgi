<?
require('../_define.inc');
require('../class/system.class');
require('../class/capability.class');
require('../class/media.class');

$system_caps = new CCapability();
$system_conf = new CSystemConfiguration();

function get_corridor_Info($name)
{
	echo $name."['enabled']=" .$GLOBALS['system_conf']->Corridor->enabled.";\r\n";
}
?>

<!DOCTYPE html>
<html>
	<head>
		<meta content="text/html; charset=utf-8" http-equiv="Content-Type">
		<title>osd configuration</title>
	</head>
	<body oncontextmenu="return false" onselectstart="return false"  ondragstart="return false">
		<div class="contentTitle"><span tkey="setup_corridor_setting"></span></div>
		<div class="contentNotice margin_top_10">
			<span class="caution" tkey="corridor_caution"></span><br>
		</div>
		<div class="content" style="display:none">
			<label class="subtitle" tkey="setup_vin_source"></label>
			<div class="select">
				<select id="vin_source" autocomplete="off">
				</select>
			</div>
		</div>
		<div class="content">
			<label class="maintitle"><span tkey="setup_corridor_mode"></span></label>
				<input type="radio" name="enabled" value="0" id="corridor_off">
				<label for="corridor_off"></label><span tkey="off"></span>
				<input type="radio" name="enabled" value="1" id="corridor_90">
				<label for="corridor_90"></label> 90°
				<input type="radio" name="enabled" value="2" id="corridor_270">
				<label for="corridor_270"></label> 270° <br>
		</div>
		<center><button id="btOK" class="button" ><span tkey="apply"></span></button></center>
		<script type="text/javascript">
			var capInfo = <? $GLOBALS['system_caps']->getCapability() ?>;
			var corridor_info = new Object();
			<?
				get_corridor_Info("corridor_info");
			?>
		</script>
		<script type="text/javascript" src="./setup_basic_corridor.js"></script>
	</body>
</html>

