<?

require('../_define.inc');
require('../class/system.class');
require('../class/capability.class');
require('../class/socket.class');
require('../class/network.class');
require('../class/camera.class');
require('../class/media.class');

define('MODULEINFO_JSON_PATH', '../ModuleInfo.json');
define('CAPABILITY_JSON_PATH', '../capability.json');

$shm_id = shmop_open(KEY_SM_SHARED_CONFIG, "a", 0, 0);

$system_caps 	= new CCapability($shm_id);
$net_conf 	= new CNetworkConfiguration($shm_id);
$camera_configs = new CCameraConfigurations($shm_id);
$profile_conf   = new CProfileConfiguration($shm_id);
$dev_info 	= new CDeviceInfomation($shm_id);

$encode_confs = $GLOBALS['profile_conf']->VideoEncoderConfigurations;
$video_source_confs = $GLOBALS['profile_conf']->VideoSourceConfigurations;
$ptz_conf = $GLOBALS['profile_conf']->PTZConfiguration;
$preset_conf = $ptz_conf->presetConfig;
$product_name = $dev_info->ProductName;

shmop_close($shm_id);

$ipc_sock = new IPCSocket();
$ipc_sock->Connection($GLOBALS['dev_info'], CMD_GET_DEVICE_INFORMATION);

$profiles = $camera_configs->config[0]->profile_info;

$thermal_type = '/(thermal)/';
$seekthermal_type = '/(seekware)/';

if( preg_match($thermal_type, $system_caps->camera_type) ) 
{
	require('../sensor/thermal.inc');
} 
else if( preg_match($seekthermal_type, $system_caps->camera_type) ) 
{
	require('../sensor/seekthermal.inc');
} 
else if( preg_match("/sony_/i", $system_caps->camera_module )){
	require('../sensor/sony_define.inc');
}
else if( preg_match("/wonwoo_/i", $system_caps->camera_module )){
	require('../sensor/wonwoo_define.inc');
}
else if( preg_match("/ytot_/i", $system_caps->camera_module )){
	require('../sensor/ytot_define.inc');
}
else if( preg_match("/esca_/i", $system_caps->camera_module )){
	require('../sensor/esca_define.inc');
}
else if( preg_match("/ov_/i", $system_caps->camera_module )){
	require('../sensor/ov_define.inc');
}
else{
	if( preg_match("/amba_s2e/i", $system_caps->board_chipset )){
		require('../sensor/_s2e_define.inc');
	} else if( preg_match("/amba_s2l/i", $system_caps->board_chipset)) {
		require('../sensor/_s2l_define.inc');
	} else if( preg_match("/amba_s3l/i", $system_caps->board_chipset)) {
		require('../sensor/_s3l_define.inc');
	} else if( preg_match("/amba_s5l/i", $system_caps->board_chipset)) {
		require('../sensor/_s5l_define.inc');
	} else if( preg_match("/amba_s2/i", $system_caps->board_chipset)) {
		require('../sensor/_s2_define.inc');
	} else if( preg_match("/amba_cv22/i", $system_caps->board_chipset)) {
		require('../sensor/_cv22_define.inc');
	} else if( preg_match("/amba_s6lm/i", $system_caps->board_chipset)) {
		require('../sensor/_s6lm_define.inc');
	} else {
		require('../sensor/_a5s_define.inc');
	}
}



//------------------------------------------------------------------------------------------------------
// 	Sdk
//------------------------------------------------------------------------------------------------------
function printSequenceValue($min, $max)
{
    $msg = '';
    for ($index=$min; $index<$max; ++$index)
    {
        $msg .= $index.',';
    }
    return $msg.$max;	
}

function printSequenceArray($arr)
{
    $msg = '';
    for ($index=0; $index<(count($arr)-1); ++$index)
    {
        $msg .= $arr[$index].',';
    }
    return $msg.$arr[count($arr)-1];
}

function ViewAbout()
{
	printf("model=%s \r\n"      , trim($GLOBALS['dev_info']->Model));
	printf("version=%s\r\n"     , trim($GLOBALS['dev_info']->FirmwareVersion));
	printf("build=%s\r\n"       , trim($GLOBALS['dev_info']->BuildVersion));
	printf("colorsystem=%d\r\n" , trim($GLOBALS['dev_info']->VideoType));
	printf("modelnum=%s\r\n"    , trim($GLOBALS['dev_info']->ProductName));
	printf("uptime=%dday %dhrs %dmins\r\n" , ($GLOBALS['dev_info']->UpTime/86400)    , ($GLOBALS['dev_info']->UpTime%86400/3600) , ($GLOBALS['dev_info']->UpTime%3600/60));
}

function ViewCapability()
{
	$arrCodec = array('H.264', 'MJPEG');
		
	if ( $GLOBALS['dev_info']->VideoType == 0 ) // ntsc
	{
		switch ($GLOBALS['system_caps']->max_resolution_width)
		{
			case 1920:
					$arrResol = array('1920x1080', '1280x720', '720x480', '352x240', '176x128');
				break;
			case 1280:
				$arrResol = array('1280x720', '720x480', '352x240', '176x128');
				break;
			case 704;
				$arrResol = array('704x480', '352x240', '176x128');
				break;
		}
		$MaxFrame = 30;
	}
	else
	{
		switch ($GLOBALS['system_caps']->max_resolution_width)
		{
			case 1920:
				$arrResol = array('1920x1080', '1280x720', '720x576', '352x288', '176x144');
				break;
			case 1280:
				$arrResol = array('1280x720', '720x576', '352x288', '176x144');
				break;
			case 704;
				$arrResol = array('704x576', '352x288', '176x128');
				break;
		}
		$MaxFrame = 25;
	}

	printf("model=%s\r\n", $GLOBALS['dev_info']->Model);
	printf("video.codec=%s\r\n", printSequenceArray($arrCodec));
	printf("video.resolution=%s\r\n", printSequenceArray($arrResol));
	printf("video.framerate=%s\r\n", printSequenceValue(1, $MaxFrame));
	printf("video.bitrate=%d-%d\r\n", 500, 8192);
	printf("video.quality=%s\r\n", printSequenceValue(1, 10));
	printf("video.gopsize=%s\r\n", printSequenceValue(1, 120));
	printf("video.output=%s\r\n", ($GLOBALS['system_caps']->video_out==1)?"true":"false");

	printf("audio.in.enable=%s\r\n", ($GLOBALS['system_caps']->audio_in==1)?"true":"false");
	printf("audio.in.gain=%s\r\n", printSequenceValue(1, $GLOBALS['system_caps']->audio_in_gain));
	printf("audio.out.enable=%s\r\n", ($GLOBALS['system_caps']->audio_out==1)?"true":"false");
	printf("audio.out.gain=%s\r\n", printSequenceValue(0, $GLOBALS['system_caps']->audio_out_gain));
	
	printf("alarm.in.number=%d\r\n", $GLOBALS['system_caps']->sensor_count);
	printf("alarm.out.number=%d\r\n", $GLOBALS['system_caps']->relay_count);

	printf("ptz.pantilt=%s\r\n", ($GLOBALS['system_caps']->have_pantilt==1)?"true":"false");
	printf("ptz.zoom=%s\r\n", ($GLOBALS['system_caps']->have_zoom==1)?"true":"false");

	printf("ptz.maxpreset=%d\r\n",0);
	printf("ptz.maxgroup=%d\r\n", 0);
	printf("ptz.maxpattern=%d\r\n", 0);
	printf("ptz.maxscan=%d\r\n", 0);
	printf("ptz.maxzoom=%d\r\n", 1);
	printf("ptz.maxdzoom=%d\r\n", 1);
}

function ViewModuleinfo()
{
	//$json_string = file_get_contents(MODULEINFO_JSON_PATH);
 	//$json = json_decode($json_string, true);

// 1. Basic
	// CAMERA
	$cam_brand = $GLOBALS['system_caps']->oem;
	$cam_model = $GLOBALS['dev_info']->Model;
	$json['Basic']['camera']['brand'] = trim($cam_brand);
	$json['Basic']['camera']['model'] = $cam_model;

	// BasicMCU
	$mcu_brand =  "ST Micro Electronics";
	$mcu_model = "STM32F";
	$json['Basic']['BasicMCU']['brand'] = $mcu_brand;
	$json['Basic']['BasicMCU']['model'] = $mcu_model;

	// SOC
	$soc = $GLOBALS['system_caps']->board_chipset;
	$soc_arr = explode("_", $soc);
	if( strcmp($soc_arr[0], "amba") == 0){
		$soc_brand = "Ambarella";
	}
	$soc_model = $soc_arr[1];
	$json['Basic']['SOC']['brand'] = $soc_brand;
	$json['Basic']['SOC']['model'] = $soc_model;
	
	// ISP
	$isp_brand = $soc_brand;
	$isp_model = $soc_model;
	$json['Basic']['ISP']['brand'] = $isp_brand;
	$json['Basic']['ISP']['model'] = $isp_model;

// 2. IMAGE
	// Image SENSOR
	$sensor_model = $GLOBALS['system_caps']->image_sensor;
	if(stristr("IMX",$sensor_model) == 0) {
		$sensor_brand = "Sony";
	}else if(stristr("MN",$sensor_model) == 0) {
		$sensor_brand = "Panasonic";
	} else {
		$sensor_brand = "unknown";
	}
	$json['Image']['Image Sensor']['brand'] = $sensor_brand;
	$json['Image']['Image Sensor']['model'] = $sensor_model;
	
	if( (stristr("IMX335",$sensor_model) == 0) || (stristr("IMX307",$sensor_model) == 0) ) {
		$mcu_size = "1,2.8";
	} else if(stristr("MN34422",$sensor_model) == 0) {
		$mcu_size = "1,3";
	} else {
		$mcu_size = "NULL";
	}
	
	$json['Image']['Image Sensor']['size'] = $mcu_size;
	$json['Image']['Image Sensor']['type'] = "CMOS";

	if( strcmp($GLOBALS['dev_info']->Model, "NAFD-SLAH5") == 0 ) {
		$json['Image']['AngleOfWiew']['tele'] 		= "2.64, 2.34, 1.36";
		$json['Image']['AngleOfWiew']['wide'] 		= "72.9, 65.1, 38.4";
		
		$json['Image']['Lens']['brand']       		= "Tamron";
		$json['Image']['Lens']['model']       		= "DF019";
		$json['Image']['Lens']['size']        		= "1,3";
		
		$json['Image']['FocalLength']['min']        	= "4.3";
		$json['Image']['FocalLength']['max']        	= "129.0";
	
		$json['Image']['ApertureRatio']['min']        	= "1.6";
		$json['Image']['ApertureRatio']['max']        	= "4.7";

		$json['Image']['zoom']['Digital Ratio']        	= "30";
		$json['Image']['zoom']['Optical Ratio']        	= "32";
		
		$json['Image']['shutter']['type']        	= "rolling";
		$json['Image']['shutter']['speed']        	= "1,320000";
	} else if( strcmp($GLOBALS['dev_info']->Model,"NPX5-52-R") == 0) {
		$json['Image']['AngleOfWiew']['tele'] 		= "2.64, 2.34, 1.36";
		$json['Image']['AngleOfWiew']['wide'] 		= "72.9, 65.1, 38.4";
		
		$json['Image']['Lens']['brand']       		= "Tamron";
		$json['Image']['Lens']['model']       		= "DF019";
		$json['Image']['Lens']['size']        		= "1,3";
		
		$json['Image']['FocalLength']['min']        	= "4.3";
		$json['Image']['FocalLength']['max']        	= "129.0";

		$json['Image']['ApertureRatio']['min']        	= "1.6";
		$json['Image']['ApertureRatio']['max']        	= "4.7";

		$json['Image']['zoom']['Digital Ratio']        	= "30";
		$json['Image']['zoom']['Optical Ratio']        	= "32";
		
		$json['Image']['shutter']['type']        	= "rolling";
		$json['Image']['shutter']['speed']        	= "1,32000";
	} else if( strcmp($GLOBALS['dev_info']->Model, "NBT5-45-RZ") == 0 ) {
		$json['Image']['AngleOfWiew']['tele'] 		= "8.6, 6.9, 5.2";
		$json['Image']['AngleOfWiew']['wide'] 		= "52, 40.8, 30.2";
		
		$json['Image']['Lens']['brand'] 		= "DAIWON";
		$json['Image']['Lens']['model'] 		= "60500-3MASPDNZ-14";
		$json['Image']['Lens']['size'] 			= "1,2.7";
		
		$json['Image']['FocalLength']['min']        	= "6.0";
		$json['Image']['FocalLength']['max']        	= "50.0";

		$json['Image']['ApertureRatio']['min']        	= "1.6";
		$json['Image']['ApertureRatio']['max']        	= "1.8";
	
		$json['Image']['zoom']['Digital Ratio']        	= "8.3";
		$json['Image']['zoom']['Optical Ratio']        	= "NULL";
		
		$json['Image']['shutter']['type']        	= "rolling";
		$json['Image']['shutter']['speed']        	= "1,32000";
	} else if( strcmp($GLOBALS['dev_info']->Model, "NVD9-45-R") == 0 ) {
		$json['Image']['AngleOfWiew']['tele'] 		= "39, 31, 24";
		$json['Image']['AngleOfWiew']['wide'] 		= "125, 96, 70";

		$json['Image']['Lens']['brand']       		= "Ricom";
		$json['Image']['Lens']['model']       		= "HD027135PB.ICR-MFZ2.1(4MP)";
		$json['Image']['Lens']['size']        		= "1,2.7";

		$json['Image']['FocalLength']['min']        	= "2.7";
		$json['Image']['FocalLength']['max']        	= "13.5";

		$json['Image']['ApertureRatio']['min']        	= "1.4";
		$json['Image']['ApertureRatio']['max']        	= "3.2";
	
		$json['Image']['zoom']['Digital Ratio']        	= "5";
		$json['Image']['zoom']['Optical Ratio']        	= "NULL";
		
		$json['Image']['shutter']['type']        	= "rolling";
		$json['Image']['shutter']['speed']        	= "1,32000";
	} else if( strcmp($GLOBALS['dev_info']->Model, "NBB2-SLEH2") == 0) {
		$json['Image']['AngleOfWiew']['tele'] 		= "7.6,6.7,3.8";
		$json['Image']['AngleOfWiew']['wide'] 		= "52.4,44.8,24.3";

		$json['Image']['Lens']['brand']       		= "DAIWON";
		$json['Image']['Lens']['model']       		= "60500-3MASPDNZ-14";
		$json['Image']['Lens']['size']        		= "1,2.7";

		$json['Image']['FocalLength']['min']        	= "2.8";
		$json['Image']['FocalLength']['max']        	= "8.0";

		$json['Image']['ApertureRatio']['min']        	= "1.6";
		$json['Image']['ApertureRatio']['max']        	= "1.8";
	
		$json['Image']['zoom']['Digital Ratio']        	= "50";
		$json['Image']['zoom']['Optical Ratio']        	= "NULL";
		
		$json['Image']['shutter']['type']        	= "rolling";
		$json['Image']['shutter']['speed']        	= "1,32000";
	} else {
		$json['Image']['AngleOfWiew']['tele'] 		= "NULL";
		$json['Image']['AngleOfWiew']['wide'] 		= "NULL";
		
		$json['Image']['Lens']['brand']       		= "NULL";
		$json['Image']['Lens']['model']       		= "NULL";
		$json['Image']['Lens']['size']        		= "NULL";
	
		$json['Image']['FocalLength']['min']        	= "NULL";
		$json['Image']['FocalLength']['max']        	= "NULL";

		$json['Image']['ApertureRatio']['min']        	= "NULL";
		$json['Image']['ApertureRatio']['max']        	= "NULL";
	
		$json['Image']['zoom']['Digital Ratio']        	= "NULL";
		$json['Image']['zoom']['Optical Ratio']        	= "NULL";
		
		$json['Image']['shutter']['type']        	= "NULL";
		$json['Image']['shutter']['speed']        	= "NULL";
	}
	// Lens

// 3. SOC(VideoProfile)
	$videoProfile_fps = $GLOBALS['system_caps']->max_fps;
	
	$json['VideoProfile']['Resolution']['Codec'] = "H.264,H.265,MJPEC";
	$json['VideoProfile']['Resolution']['frameRate'] = $videoProfile_fps;

	$videoProfile_maxWidth  = $GLOBALS['system_caps']->max_resolution_width;
	$videoProfile_maxHeight = $GLOBALS['system_caps']->max_resolution_height;

	$res = $videoProfile_maxWidth ."*". $videoProfile_maxHeight;
	$json['VideoProfile']['Resolution']['size'] = $res;
	
	$json['VideoProfile']['bandWidth']['1st'] = "10";
	$json['VideoProfile']['bandWidth']['2nd'] = "10";
	$json['VideoProfile']['bandWidth']['3rd'] = "2";
	$json['VideoProfile']['bandWidth']['4th'] = "0";

	$camData = $GLOBALS['camera_configs'];
	for( $i = (CAMERA_CODE_START + 1) ; $i < CAMERA_CODE_END ; $i ++) {
		$list = $GLOBALS['list'];
		if( $list[$i] == "hdr" ) {
			if($camData->config[0]->code[$i]->data == 1) {
				$json['VideoProfile']['addOn']['WDR'] = "yes";
			} else {
				$json['VideoProfile']['addOn']['WDR'] = "no";
			}
		} else if( $list[$i] == "flip" ) {
			if($camData->config[0]->code[$i]->data == 1) {
				$json['VideoProfile']['addOn']['flip'] = "yes";
			} else {
				$json['VideoProfile']['addOn']['flip'] = "no";
			}
		} else if( $list[$i] == "ir_enabled" ) {
			if($camData->config[0]->code[$i]->data == 1) {
				$json['VideoProfile']['ir']['ir'] = "yes";
			} else {
				$json['VideoProfile']['ir']['ir'] = "no";
			}
		} else {
		}
	}

	$json['VideoProfile']['Resolution']['speed'] = "1,30000";
// 4. mcu 
	
	$json['MCU']['MCU_OS']['brand'] = "Linux";
	$json['MCU']['MCU_OS']['model'] = "embedded";
	
	if( strcmp($GLOBALS['dev_info']->Model, "NAFD-SLAH5") == 0) {
		$json['MCU']['pantilt']['speed'] = "360";
		$json['MCU']['preset']['count'] = "255";
	} else if( strcmp($GLOBALS['dev_info']->Model,"NPX5-52-R") == 0) {
		$json['MCU']['pantilt']['speed'] = "360";
		$json['MCU']['preset']['count'] = "255";
	} else {
		$json['MCU']['pantilt']['speed'] = "NULL";
		$json['MCU']['preset']['count'] = "NULL";
	}

	$json['MCU']['ir']['ir distant'] = "NULL";
	//$json['MCU']['ir']['ir'] = "yes";
	
	$json['MCU']['wiper'] = "yes";

// 5. NETWORK
	// Gateway
	$network_gateway = $GLOBALS['net_conf']->IPv4->Gateway;
	$json['network']['networkInfo']['Gateway'] = trim($network_gateway);
	
	// IPV4 Addr
	if($GLOBALS['net_conf']->IPv4->Type == 0){
		$json['network']['networkInfo']['IPSet'] = "Static";
		$network_ipv4 = $GLOBALS['net_conf']->IPv4->StaticIpAddr;
	} else {
		$json['network']['networkInfo']['IPSet'] = "Dynamic";
		$network_ipv4 = $GLOBALS['net_conf']->IPv4->DynamicIpAddr;
	}
	$json['network']['networkInfo']['IP Address'] = trim($network_ipv4);
	

	//MAC Addr
	$network_mac = $GLOBALS['net_conf']->HwAddress;
	$json['network']['networkInfo']['Mac Address'] = trim($network_mac);

	// Running time
	$sec = exec("cat /proc/uptime|cut -d\" \" -f1|cut -d. -f1");
	$json['network']['networkInfo']['Running Time'] = gmdate("H:i:s", $sec);

	// traffic
	$rx_data = exec("cat /sys/class/net/eth0/statistics/rx_bytes");
	$tx_data = exec("cat /sys/class/net/eth0/statistics/tx_bytes");
	$json['network']['traffic']['Received Data']    = $rx_data;
	$json['network']['traffic']['Transmitted Data'] = $tx_data;

// 5. Status
	$status_connected = exec("netstat -nap | grep :80 | grep ESTABLISHED | wc -l");
	$json['status']['Connected']['Chnnel Count'] = $status_connected;
	
	$status_Firmware = $GLOBALS['dev_info']->FirmwareVersion;
	$json['status']['FirmwareVersion']['camera'] = $status_Firmware;
	
	//Storage Inserted
	$filepath = "/sdcard/index.db";
	exec("df|grep mmcblk", $data, $retval);
	
	if($retval == 0){
		$status_mounted = "yes";
	} else {
		$status_mounted = "no";
	}

	$json['status']['Storage Inserted'] = $status_mounted;
	$json['status']['ReservatePreset']['Count'] = "NULL";

	$ChannelInfo1 = $GLOBALS['encode_confs']->conf[0];
	$ChannelInfo2 = $GLOBALS['encode_confs']->conf[1];
	$ChannelInfo3 = $GLOBALS['encode_confs']->conf[2];
	
	// stream1
	if($ChannelInfo1->Encoding == 1) {
		$json['status']['stream1']['Codec'] =  "H.264";
	} else if($ChannelInfo1->Encoding == 2) {
		$json['status']['stream1']['Codec'] =  "MJPEG";
	} else if($ChannelInfo1->Encoding == 3) {
		$json['status']['stream1']['Codec'] =  "H.265";
	} else {
		$json['status']['stream1']['Codec'] =  "NULL";
	}
	$json['status']['stream1']['GOP'] = $ChannelInfo1->H264->GovLength;
	
	if($ChannelInfo1->Encoding == CODEC_HEVC) {
		$json['status']['stream1']['bitrate'] = $ChannelInfo1->RateControl->HevcBitrateLimit;
	} else {
		$json['status']['stream1']['bitrate'] = $ChannelInfo1->RateControl->BitrateLimit;
	}
	$json['status']['stream1']['resolution'] = $ChannelInfo1->Resolution->Width. "x" . $ChannelInfo1->Resolution->Height;
	$json['status']['stream1']['fps'] = $ChannelInfo1->RateControl->FrameRateLimit;
	
	if($ChannelInfo1->RateControl->ConstantBitRate == 0){
		$json['status']['stream1']['rate'] = "VBR";
	} else {
		$json['status']['stream1']['rate'] = "CBR";
	}
	// stream2
	if($ChannelInfo2->Encoding == 1) {
		$json['status']['stream2']['Codec'] =  "H.264";
	} else if($ChannelInfo2->Encoding == 2) {
		$json['status']['stream2']['Codec'] =  "MJPEG";
	} else if($ChannelInfo2->Encoding == 3) {
		$json['status']['stream2']['Codec'] =  "H.265";
	} else {
		$json['status']['stream2']['Codec'] =  "NULL";
	}
	
	$json['status']['stream2']['GOP'] = $ChannelInfo2->H264->GovLength;
	
	if($ChannelInfo2->Encoding == CODEC_HEVC) {
		$json['status']['stream2']['bitrate'] = $ChannelInfo2->RateControl->HevcBitrateLimit;
	} else {
		$json['status']['stream2']['bitrate'] = $ChannelInfo2->RateControl->BitrateLimit;
	}
	$json['status']['stream2']['resolution'] = $ChannelInfo2->Resolution->Width. "x" . $ChannelInfo2->Resolution->Height;
	$json['status']['stream2']['fps'] = $ChannelInfo2->RateControl->FrameRateLimit;
	
	if($ChannelInfo2->RateControl->ConstantBitRate == 0){
		$json['status']['stream2']['rate'] = "VBR";
	} else {
		$json['status']['stream2']['rate'] = "CBR";
	}
	
	// stream3
	$json['status']['stream3']['Codec'] = $ChannelInfo3->Encoding;

	if($ChannelInfo3->Encoding == 1) {
		$json['status']['stream3']['Codec'] =  "H.264";
	} else if($ChannelInfo3->Encoding == 2) {
		$json['status']['stream3']['Codec'] =  "MJPEG";
	} else if($ChannelInfo3->Encoding == 3) {
		$json['status']['stream3']['Codec'] =  "H.265";
	} else {
		$json['status']['stream3']['Codec'] =  "NULL";
	}
	
	$json['status']['stream3']['GOP'] = $ChannelInfo3->H264->GovLength;
	
	if($ChannelInfo3->Encoding == CODEC_HEVC) {
		$json['status']['stream3']['bitrate'] = $ChannelInfo3->RateControl->HevcBitrateLimit;
	} else {
		$json['status']['stream3']['bitrate'] = $ChannelInfo3->RateControl->BitrateLimit;
	}
	$json['status']['stream3']['resolution'] = $ChannelInfo3->Resolution->Width. "x" . $ChannelInfo3->Resolution->Height;
	$json['status']['stream3']['fps'] = $ChannelInfo3->RateControl->FrameRateLimit;
	
	if($ChannelInfo3->RateControl->ConstantBitRate == 0){
		$json['status']['stream3']['rate'] = "VBR";
	} else {
		$json['status']['stream3']['rate'] = "CBR";
	}
	// Preset
	if( ($GLOBALS['system_caps']->have_pantilt) && ($GLOBALS['system_caps']->have_zoom > 1) ) {
		for($i = 0; $i < MAX_PRESET_COUNT; $i++) {
			$preset = trim($GLOBALS['preset_conf']->preset[$i]->Name);
			if($preset != NULL){
				$presetArr[$i] = $i;
			}
		}
	} 

	$presetList = implode(", ", $presetArr);

	if($presetList == NULL){
		$json['status']['preset'] = "NULL";
	} else {
		$json['status']['preset'] = $presetList;
	}

	$json = json_encode($json, JSON_PRETTY_PRINT);
	
	file_put_contents(MODULEINFO_JSON_PATH, $json);

	echo $json;
}

function productTestinfo()
{
	$sensor_model = $GLOBALS['system_caps']->image_sensor;
	$soc = $GLOBALS['system_caps']->board_chipset;
	
	$hdr_support 	      = 0;
	$hdr_type 	      = 0;
	$hdr_level_support    = 0;
	$hdr_level_type       = 0;
	$hdr_cnt 	      = 0;
	$hdr_level_cnt 	      = 0;
	$blc_support 	      = 0;
	$dn_support 	      = 0;
	$ir_mode_support      = 0;
	$audio_in_support     = 0;
	$audio_out_support    = 0;
	$sdcard_support       = 0;
	$zoom_support         = 0;
	$pantilt_support      = 0;
	$focus_support        = 0;
	$mirror_support       = 0;
	$flip_support         = 0;

	$str = file_get_contents(CAPABILITY_JSON_PATH);
	$json =  json_decode($str, true);

	for($i=0; $i<count($json); $i++)
	{
		for($j=0; $j<count($json[$i]["model"]); $j++)
		{
			if(trim($GLOBALS['dev_info']->ProductName) == $json[$i]["model"][$j])
			{
				$json_d = json_encode($json[$i]["capability"], JSON_PRETTY_PRINT);
			}
		}
	}

	$json_d = json_decode($json_d, true);
	
	for($i=0; $i<count($json_d); $i++)
	{
		for($j=0; $j<count($json_d[$i]["camera"]); $j++)
		{
			$str_tmp = json_encode($json_d[$i]["camera"][$j]["name"], JSON_PRETTY_PRINT);
			$str_tmp = str_replace("\"","",$str_tmp);
			
			if(strcmp($str_tmp, "hdr") == 0 ){
				$hdr_cnt = count($json_d[$i]["camera"][$j]["value"]["option"]);
			} else if( strcmp($str_tmp, "hdr_level") == 0 ) {
				$hdr_level_cnt = count($json_d[$i]["camera"][$j]["value"]["option"]);
			} else if( strcmp($str_tmp, "dnmode") == 0 ) {
				$dn_support = 1;
			}
		}
	}
	
	if( (strcmp($sensor_model, "imx178") == 0)
	||  (strcmp($sensor_model, "imx322") == 0) 
	||  (strcmp($sensor_model, "imx226") == 0) 
	||  (strcmp($sensor_model, "bt1120_720p") == 0) )
	{
		$hdr_support=0;
		$blc_support=1;
	} else {
		$hdr_support=1;
		$blc_support=0;

		if(strcmp($soc, "amba_s2l66") == 0 ) {
		} else {
		}
	}

	if( strcmp($sensor_model, "imx226") == 0) {
		$mirror_support = 0;
		$flip_support   = 0;
	} else {
		$mirror_support = 1;
		$flip_support   = 1;
	}

	if($hdr_cnt == 2) {
		$hdr_type = 0;
	} else if($hdr_cnt == 3) {
		$hdr_type = 1;
	}
	if( (strcmp($sensor_model,"ov4689") == 0)
	||  (strcmp($sensor_model ,"imx334_mipi") == 0) 
	||  (strcmp($soc, "amba_s6lm33") == 0) 
	||  (strcmp($soc ,"amba_s6lm55") == 0) 
	||  (strcmp($soc ,"amba_cv22s88") == 0) ) {
		$hdr_level_support=0;
	} else {
		$hdr_level_support=1;
	}

	if($hdr_level_cnt == 3) {
		$hdr_level_type = 0;	
	} else if($hdr_level_cnt == 5) {
		$hdr_level_type = 1;
	}

	$ir_mode_support   = $GLOBALS['system_caps']->have_cds;
	$audio_in_support  = $GLOBALS['system_caps']->audio_in;
	$audio_out_support = $GLOBALS['system_caps']->audio_out;
	$sdcard_support    = $GLOBALS['system_caps']->have_sdcard;
	$zoom_support      = $GLOBALS['system_caps']->have_zoom;
	$pantilt_support   = $GLOBALS['system_caps']->have_pantilt;
	$focus_support     = $GLOBALS['system_caps']->have_focus;

	//echo "modelnum=" . trim($GLOBALS['dev_info']->ProductName) . "\r\n";
	//echo "soc=" . $soc . "\r\n";
	//echo "sensor_model=" . $sensor_model . "\r\n";
	echo "hdr_support=" . $hdr_support . "\r\n";
	echo "hdr_type=" . $hdr_type . "\r\n";
	echo "hdr_level_support=" . $hdr_level_support . "\r\n";
	echo "hdr_level_type=" . $hdr_level_type . "\r\n";
	echo "blc_support=" . $blc_support . "\r\n";
	echo "dn_support=" . $dn_support . "\r\n";
	echo "ir_mode_support=" . $ir_mode_support . "\r\n";
	echo "audio_in_support=" . $audio_in_support . "\r\n";
	echo "audio_out_support=" . $audio_out_support . "\r\n";
	echo "sdcard_support=" . $sdcard_support . "\r\n";
	echo "zoom_support=" . $zoom_support . "\r\n";
	echo "pantilt_support=" . $pantilt_support . "\r\n";
	echo "focus_support=" . $focus_support . "\r\n";
	echo "mirror_support=" . $mirror_support . "\r\n";
	echo "flip_support=" . $flip_support . "\r\n";
}

header("Content-Type: text/plain");
ob_end_clean ();
if ( $_REQUEST['msubmenu'] == 'about' )
{
	if ( $_REQUEST['action'] == 'view' )
		ViewAbout();
	else
		show_post_ng();
	
	exit;
}
else if ( $_REQUEST['msubmenu'] == 'capability' )
{
	if ( $_REQUEST['action'] == 'view' )
		ViewCapability();
	else
		show_post_ng();
	
	exit;
}
else if ( $_REQUEST['msubmenu'] == 'moduleinfo' )
{
	if ( $_REQUEST['action'] == 'view' )
		ViewModuleinfo();
	else
		show_post_ng();
	
	exit;
}
else if ( $_REQUEST['msubmenu'] == 'productTestinfo' )
{
	if ( $_REQUEST['action'] == 'view' )
		productTestinfo();
	else
		show_post_ng();
	
	exit;
}
else
	show_post_ng();
?>
