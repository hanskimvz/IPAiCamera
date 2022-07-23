<?
require('../_define.inc');
require('../class/capability.class');
require('../class/media.class');

$shm_id      = shmop_open(KEY_SM_SHARED_CONFIG, "a", 0, 0);
$system_caps = new CCapability($shm_id);
$media_conf  = new CMediaConfiguration($shm_id);
shmop_close($shm_id);

?>
<!DOCTYPE html>
<html>
	<head>
		<meta content="text/html; charset=utf-8" http-equiv="Content-Type">
		<title>fisheye configuration</title>
	</head>
	<body oncontextmenu="return false" onselectstart="return false"  ondragstart="return false">
		<div class="contentTitle">fisheye configuration</div>

		<div class="content">
			<label class="maintitle" colspan="2">Basic Type</label>
			<label class="subtitle">Mount Settings</label>
			<input id="wall_mount" type="radio" name="mount_type" value=0 >
			<label for="wall_mount"></label><span>Wall</span>
			<input id="ceiling_mount" type="radio" name="mount_type" value=1 >
			<label for="ceiling_mount"></label><span>Celing</span>
			<input id="desk_mount" type="radio" name="mount_type" value=2 >
			<label for="desk_mount"></label><span>Desk</span>
		</div>
		<div class="content">
			<label class="maintitle">Source Mode</label>
			<input id="source_type1" type="radio" name="source_type" value=0 >
			<label for="source_type1"></label><span>Mode1</span>
			None-Dewarping Mode
			<br>
			<input id="source_type2" type="radio" name="source_type" value=1 >
			<label for="source_type2"></label><span>Mode2</span>
			Fisheye(x1), Panorama(x1), Sub-Region(x3)
			<br>
			<input id="source_type3" type="radio" name="source_type" value=2 >
			<label for="source_type3"></label><span>Mode3</span>
			 Sub-Region(x4)
			<br>
			<input id="source_type4" type="radio" name="source_type" value=3 >
			<label for="source_type4"></label><span>Mode4</span>
			Fisheye(x2), Sub-Region(x3)
			<br>
			<input id="source_type5" type="radio" name="source_type" value=4 >
			<label for="source_type5"></label><span>Mode5</span>
			Panorama(x2)
			<br>
			<input id="source_type6" type="radio" name="source_type" value=5 >
			<label for="source_type6"></label><span>Mode6</span>
			Fisheye(x1), Panorama(x1)
		</div>
		<center><button id="btOK" class="button" >Apply</button></center> 
		<script type="text/javascript">
			var fishInfo = <? $GLOBALS['media_conf']->getFisheyeInformation(NULL, 1); ?>;
		</script>
		<script type="text/javascript" src="./setup_fisheye_setting.js"></script>
	</body>
</html>
