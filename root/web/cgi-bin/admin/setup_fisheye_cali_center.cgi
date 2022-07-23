<?
require('../_define.inc');
require('../class/capability.class');
require('../class/media.class');

$shm_id      = shmop_open(KEY_SM_SHARED_CONFIG, "a", 0, 0);
$system_caps = new CCapability($shm_id);
$media_conf  = new CMediaConfiguration($shm_id);
shmop_close($shm_id);

$fish_conf = $media_conf->ProfileConfig->VideoSourceConfiguration->Extension->FishEyeConf;
?>
<!DOCTYPE html>
<html>
	<head>
		<meta content="text/html; charset=utf-8" http-equiv="Content-Type">
		<title>calibration center</title>
	</head>
	<body oncontextmenu="return false" onselectstart="return false"  ondragstart="return false">
		<div class="contentTitle">calibration center</div>
		<div class="content">
			<label class="maintitle">Fisheye Center Information</label>
			<label class="subtitle">FishEye Center Mode</label>
			<label id="finded"></label><br>
			<label class="subtitle">Pos-X</label>
			<label id="pos_x"></label><br>
			<label class="subtitle">Pos-Y</label>
			<label id="pos_y"></label><br>
			<label class="subtitle">Radius</label>
			<label id="radius"></label><br>
		</div>
		<div class="content">
			<label class="maintitle">Note for Center Auto Calibration</label>
				<ul>
					<li>Put the camera into the light box before starting this fisheye tunning. If you didn't put the camera into that, dewarping video is distorted and strange.</li>
					<li>Change the source mode to 1.</li>
					<li>Click the start button and wait moment. All of prosedure will be autumatically done for couple of minutes.</li>
					<li>You can restore the tune using by Factory Default button.</li>
				</ul>
		</div>
		<center>
			<button id="btAutoCalibration" class="button" >Auto Calibration</button>
			<button id="btDefault" class="button" >Factory Default</button>
		</center> 
		<script type="text/javascript">
			var fishInfo = <? $GLOBALS['media_conf']->getFisheyeInformation(NULL, 1); ?>;
		</script>
		<script type="text/javascript" src="./setup_fisheye_cali_center.js"></script>
	</body>
</html>
