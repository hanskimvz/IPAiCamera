<?
require('../_define.inc');
require('../class/camera.class');
require('../class/capability.class');
require('../class/system.class');

$system_caps = new CCapability();
$camera_configs = new CCameraConfigurations(0, $system_caps->board_chipset, $system_caps->camera_module);
$system_conf = new CSystemConfiguration();


//--- ip
function setJavaScript()
{
	$support_isp   = '/(s2_internal_isp)|(s2l_internal_isp)|(s3l_internal_isp)|(s5l_internal_isp)|(cv22_internal_isp)|(s6lm_internal_isp)/';
	$external_isp = '/(sony_isp)|(wonwoo_isp)|(esca_isp)|(ytot_isp)|(ov_isp)/';
	$thermal_type = '/(thermal)/';
	$seekthermal_type = '/(seekware)/';
	$camera_module = trim($GLOBALS['system_caps']->camera_module);
	$image_sensor  = trim($GLOBALS['system_caps']->image_sensor );
	$camera_type = trim($GLOBALS['system_caps']->camera_type );

	if( preg_match($thermal_type, $camera_type) ) 
	{
		echo '<script src="../sensor/js/thermal.js"></script>';
	} 
	else if( preg_match($seekthermal_type, $camera_type) ) 
	{
		echo '<script src="../sensor/js/seek_thermal.js"></script>';
	} 
	else if( preg_match($support_isp, $camera_module) ) 
	{
		echo '<script src="../sensor/js/' . $image_sensor . '.js"></script>';
	} 
	else if( preg_match($external_isp ,  $camera_module))
	{
		echo '<script src="../sensor/js/' . $camera_module . '.js"></script>';
	}
	else{
		// external isp
	}
}
?>

<script language="javascript">
var CameraFunc = <? $GLOBALS['camera_configs']->getCameraInfo(); ?>;
var profileInfo = <? $GLOBALS['camera_configs']->getProfileInfo(); ?>;
var videoType;
<?
echo "videoType='". trim($system_conf->DeviceInfo->VideoType) ."';\r\n;";
?>
</script>

<? 
setJavaScript();
?>
