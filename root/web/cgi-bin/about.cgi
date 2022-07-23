<?
require('_define.inc');
require('class/system.class');
require('class/capability.class');
require('class/socket.class');

$shm_id = shmop_open(KEY_SM_SHARED_CONFIG, "a", 0, 0);
$system_caps = new CCapability($shm_id);
shmop_close($shm_id);

$dev_info = new CDeviceInfomation();
$ipc_sock = new IPCSocket();
$ipc_sock->Connection($GLOBALS['dev_info'], CMD_GET_DEVICE_INFORMATION);
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
	printf("brand=%s\r\n"       , trim($GLOBALS['dev_info']->Manufacturer));
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
else
	show_post_ng();

?>
