<?
require('../_define.inc');
require('../class/system.class');
require('../class/capability.class');
require('../class/media.class');
require('../class/ptz.class');
require('../class/socket.class');
require('../class/etc.class');

$shm_id       = shmop_open(KEY_SM_SHARED_CONFIG, "a", 0, 0);
$system_conf  = new CSystemConfiguration($shm_id);
$system_caps  = new CCapability($shm_id);
$profile_conf = new CProfileConfiguration($shm_id);
$encode_confs = $GLOBALS['profile_conf']->VideoEncoderConfigurations;
$video_source_confs = $GLOBALS['profile_conf']->VideoSourceConfigurations;

//$media_conf   = new CMediaConfiguration($shm_id);
//$encode_confs = $GLOBALS['media_conf']->ProfileConfig->VideoEncoderConfigurations;
//$profile_conf = $GLOBALS['media_conf']->ProfileConfig;

$osds_conf    = $GLOBALS['system_conf']->Osds;
$encode_qprio = null;
$SmartACF     = null;
$SmartRC     = null;
$Dewarp     = null;
$SmartLBR     = $GLOBALS['system_conf']->SmartLBR;
$etc_conf = new CEtcConfiguration($shm_id); 
shmop_close($shm_id);

$Corridor     = $GLOBALS['system_conf']->Corridor;
//--- video
function video_view_post($channel)
{
	if( isset($_REQUEST['profile_no']) )
		echo "profile_no="			.$_REQUEST['profile_no']."\r\n";
	else if( isset($_REQUEST['channel_no']) )
		echo "channel_no="			.$_REQUEST['channel_no']."\r\n";
	else
		echo "channel_no=".$channel."\r\n";
		
	$ChannelInfo = $GLOBALS['encode_confs']->conf[$channel];	
	echo "codec="				.$ChannelInfo->Encoding."\r\n";
	if ( $ChannelInfo->Encoding != CODEC_NONE )
	{
		echo "codec_name="		.trim($ChannelInfo->Name)."\r\n";
		
/*
		if($ChannelInfo->Resolution->Width == 1920 && $ChannelInfo->Resolution->Height == 1080)
		  echo "resolution="		.RESOL_1080p."\r\n";
		else if($ChannelInfo->Resolution->Width == 1280 && $ChannelInfo->Resolution->Height == 720)
		  echo "resolution="		.RESOL_720p."\r\n";
		else if($ChannelInfo->Resolution->Width == 800 && $ChannelInfo->Resolution->Height == 640)
		  echo "resolution="		.RESOL_SVGA."\r\n";
		else if( ($ChannelInfo->Resolution->Width == 704 || $ChannelInfo->Resolution->Width == 720) 
			&& $ChannelInfo->Resolution->Height == 480 )
		  echo "resolution="		.RESOL_D1."\r\n";
		else if($ChannelInfo->Resolution->Width == 640 && $ChannelInfo->Resolution->Height == 480)
		  echo "resolution="		.RESOL_VGA."\r\n"; 
		else if(($ChannelInfo->Resolution->Width == 352 || $ChannelInfo->Resolution->Width == 360 )
			&& $ChannelInfo->Resolution->Height == 240)
		  echo "resolution="		.RESOL_CIF."\r\n";
		else if(($ChannelInfo->Resolution->Width == 176 || $ChannelInfo->Resolution->Width == 180)
			&& $ChannelInfo->Resolution->Width == 120)
		  echo "resolution="		.RESOL_QCIF."\r\n";		
		else
*/
		  echo "resolution="		.$ChannelInfo->Resolution->Width. "x" . $ChannelInfo->Resolution->Height . "\r\n";		  		  		  
		  		  
		echo "framerate="		.$ChannelInfo->RateControl->FrameRateLimit."\r\n";
		
		if (  $ChannelInfo->Encoding == CODEC_MJPEG )
			echo "bitratemode="		.BITRATE_VBR."\r\n";
		else
			echo "bitratemode="		.$ChannelInfo->RateControl->ConstantBitRate."\r\n";

		if ( $ChannelInfo->RateControl->ConstantBitRate == BITRATE_CBR && $ChannelInfo->Encoding != CODEC_MJPEG )
		{
			if($ChannelInfo->Encoding == CODEC_HEVC)
			{
			echo "bitrate="     .$ChannelInfo->RateControl->HevcBitrateLimit."\r\n";
			}
			else
			{
			echo "bitrate="		.$ChannelInfo->RateControl->BitrateLimit."\r\n"; 
			}
			echo "quality="		.$ChannelInfo->Compression."\r\n";
		}
		else
		{
			if($ChannelInfo->Encoding == CODEC_HEVC)
			{
			echo "bitrate="		.$ChannelInfo->RateControl->HevcBitrateLimit."\r\n";
			}
			else
			{
			echo "bitrate="		.$ChannelInfo->RateControl->BitrateLimit."\r\n";
			}
			echo "quality="		.$ChannelInfo->Compression."\r\n";
		}
		echo "h264_profile="		.$ChannelInfo->H264->CodecProfile."\r\n";
		echo "lbr_mode="			.$ChannelInfo->Extension->SmartLBR->mode."\r\n";
		echo "h264_extension_option="		.$ChannelInfo->Extension->SVCT_Mode."\r\n";
		echo "SmartCoreMode="	.$ChannelInfo->Extension->SmartCoreMode."\r\n";

	}
	
//	if ( $ChannelInfo->Encoding == CODEC_H264 )
	 echo "gopsize="				.$ChannelInfo->H264->GovLength."\r\n";
	 echo "rtp_mcast_enable="		.$ChannelInfo->RTPMulticast->Enabled."\r\n";
	 echo "rtp_mcast_ttl="			.$ChannelInfo->RTPMulticast->TTL."\r\n";
 	 echo "rtsp_timeout="			.$ChannelInfo->SessionTimeout."\r\n"; 	
 	 echo "dscp="			.$ChannelInfo->DSCP."\r\n"; 	 
//   echo "rtp_mcast_ip="			.$ChannelInfo->RTPMulticast->IPv4Address."\r\n";
//   echo "rtp_mcast_port="			.$ChannelInfo->RTPMulticast->Port."\r\n";
  	 echo "\r\n";
}

function video_delete($channel)
{
	if ($channel == 0)
	{
		show_post_ng();
		return;
	}
	$ChannelInfo = $GLOBALS['encode_confs']->conf[$channel];	
	$ChannelInfo->Encoding = CODEC_NONE;
	
	
	$ipc_sock = new IPCSocket();
  $ipc_sock->Connection($ChannelInfo, CMD_SET_VIDEO_ENCODE_CONFIGURATION);
  if ($ipc_sock->dataInfo['ErrorCode']['value'] == APP_OK)
  {
  	show_post_ok();
  }
  else
  {
    show_post_ng();
  }
}

function video_view_capability($channel)
{
	$availableFrames = getAvailableFrame($channel);
	for ($i=RESOL_1080p; $i<=RESOL_QCIF; $i++)
	{
		if ($GLOBALS['system_conf']->DeviceInfo->VideoType == COLORSYS_NTSC)	$MaxFrame = 30;
		else													$MaxFrame = 25;
		
		if ($i == RESOL_1080p)
		{
			if ($channel == 0)	printf("%d=%d\r\n", $i, $MaxFrame );
			else				printf("%d=%d\r\n", $i, 0 );
		} 
		else 
		{
			printf("%d=%d\r\n", $i, $MaxFrame );
		}
	}
}

function change_video_codec($channel)
{
	if (!isset($_REQUEST['codec'])) return 1;
	//if ($_REQUEST['codec'] < CODEC_NONE || $_REQUEST['codec'] > CODEC_MJPEG) return -1;

	$ChannelInfo = $GLOBALS['encode_confs']->conf[$channel];	
	$ChannelInfo->Encoding = $_REQUEST['codec'];
	return 0;
}
function change_video_codecname($channel)
{
	if (!isset($_REQUEST['codec_name'])) return 1;
	if (strlen($_REQUEST['codec_name']) > 30) return -1;
	//if (strlen($_REQUEST['codec_name']) > 32 ) return -1;

	$ChannelInfo = $GLOBALS['encode_confs']->conf[$channel];	
	$ChannelInfo->Name = $_REQUEST['codec_name'];
	return 0;
}
function change_video_resolution($channel)
{
	if (!isset($_REQUEST['resolution'])) return 1;
	$pattern = '([[:digit:]]{3,4}[x|X][[:digit:]]{3,4})';
	$exist = preg_match($pattern, $_REQUEST['resolution']);
	if (($_REQUEST['resolution'] < RESOL_1080p || $_REQUEST['resolution'] > RESOL_QCIF) && $exist == 0) return -1;
	
	$ChannelInfo = $GLOBALS['encode_confs']->conf[$channel];	
	
	if ($_REQUEST['resolution'] == RESOL_1080p)
	{
		$ChannelInfo->Resolution->Width  = 1920;
		$ChannelInfo->Resolution->Height = 1080;
	}
	else if ($_REQUEST['resolution'] == RESOL_720p)
	{
		$ChannelInfo->Resolution->Width  = 1280;
		$ChannelInfo->Resolution->Height = 720;
	}
	else if ($_REQUEST['resolution'] == RESOL_SVGA)
	{
		$ChannelInfo->Resolution->Width  = 800;
		$ChannelInfo->Resolution->Height = 600;    
	}	
	else if ($_REQUEST['resolution'] == RESOL_D1)
	{
		$ChannelInfo->Resolution->Width  = 704;
		$ChannelInfo->Resolution->Height = 480;    
	}	
	else if ($_REQUEST['resolution'] == RESOL_VGA)
	{
		$ChannelInfo->Resolution->Width  = 640;
		$ChannelInfo->Resolution->Height = 480;    
	}	
	else if ($_REQUEST['resolution'] == RESOL_CIF)
	{
		$ChannelInfo->Resolution->Width  = 352;
		$ChannelInfo->Resolution->Height = 240;   
	}	
	else if ($_REQUEST['resolution'] == RESOL_QCIF)
	{
		$ChannelInfo->Resolution->Width  = 176;
		$ChannelInfo->Resolution->Height = 120;    
	}	    
	else 
	{
		$data = explode("x", $_REQUEST['resolution']);
		$ChannelInfo->Resolution->Width = $data[0];
		$ChannelInfo->Resolution->Height = $data[1];
	}
	return 0;
}
function change_video_framerate($channel)
{
	if ( !isset($_REQUEST['framerate']) ) return 1;
	//if ( $_REQUEST['framerate'] < 1 || $_REQUEST['framerate'] > $GLOBALS['system_caps']->max_fps ) return -1;

	$ChannelInfo = $GLOBALS['encode_confs']->conf[$channel];	
	$ChannelInfo->RateControl->FrameRateLimit = $_REQUEST['framerate'];
	return 0;
}
function change_video_bitratemode($channel)
{
	if (!isset($_REQUEST['bitrate_mode'])) return 1;
	//if ($_REQUEST['bitrate_mode'] < BITRATE_VBR || $_REQUEST['bitrate_mode'] > BITRATE_CBR) return -1;
	
	$ChannelInfo = $GLOBALS['encode_confs']->conf[$channel];	
	$ChannelInfo->RateControl->ConstantBitRate = $_REQUEST['bitrate_mode'];
	return 0;
}
function change_video_bitrate($channel)
{
	if (!isset($_REQUEST['bitrate'])) return 1;
	
	$ChannelInfo = $GLOBALS['encode_confs']->conf[$channel];	
	//if ($ChannelInfo->RateControl->ConstantBitRate == BITRATE_VBR)	return 1;
	//if( $_REQUEST['bitrate'] < 100 || $_REQUEST['bitrate'] > 10240) return -1;  
	if($ChannelInfo->Encoding == CODEC_HEVC)
	{
	$ChannelInfo->RateControl->HevcBitrateLimit = $_REQUEST['bitrate'];  
	}
	else
	{
	$ChannelInfo->RateControl->BitrateLimit = $_REQUEST['bitrate'];    
	}
	
	return 0;
}
function change_video_quality($channel)
{
	if (!isset($_REQUEST['quality'])) return 1;

	$ChannelInfo = $GLOBALS['encode_confs']->conf[$channel];	
	//if ($ChannelInfo->RateControl->ConstantBitRate == BITRATE_CBR && $ChannelInfo->Encoding == CODEC_H264)	return 1;
	//if ($_REQUEST['quality'] < 1 || $_REQUEST['quality'] > 9) return -1;

	$ChannelInfo->Compression = $_REQUEST['quality'];

	return 0;
}

function change_video_gopsize($channel)
{
	if (!isset($_REQUEST['gopsize'])) return 1;
	//if ($_REQUEST['gopsize'] < 1 || $_REQUEST['gopsize'] > 120) return -1;

	$ChannelInfo = $GLOBALS['encode_confs']->conf[$channel];
	$ChannelInfo->H264->GovLength	= $_REQUEST['gopsize']; 

	return 0;
}

function change_video_h264_profile($channel)
{
	if (!isset($_REQUEST['h264_profile'])) return 1;
	//if ($_REQUEST['h264_profile'] < 0 || $_REQUEST['h264_profile'] > 3) return -1;

	$ChannelInfo = $GLOBALS['encode_confs']->conf[$channel];
	$ChannelInfo->H264->CodecProfile = $_REQUEST['h264_profile']; 

	return 0;
}
function change_video_h264_extension_option($channel)
{
	if (!isset($_REQUEST['h264_extension_option'])) return 1;

	$ChannelInfo = $GLOBALS['encode_confs']->conf[$channel];
	$ChannelInfo->Extension->SVCT_Mode= $_REQUEST['h264_extension_option']; 

	return 0;
}
function change_video_lbr_mode($channel)
{
	if (!isset($_REQUEST['lbr_mode'])) return 1;

	$ChannelInfo = $GLOBALS['encode_confs']->conf[$channel];
	$ChannelInfo->Extension->SmartLBR->mode= $_REQUEST['lbr_mode']; 

	return 0;
}
function change_video_smart_core_mode($channel)
{
	if (!isset($_REQUEST['SmartCoreMode'])) return 1;

	$ChannelInfo = $GLOBALS['encode_confs']->conf[$channel];
	$ChannelInfo->Extension->SmartCoreMode= $_REQUEST['SmartCoreMode']; 

	return 0;
}

//------------------ (RTP Multicast)----------------------------------------
function checkValidationRtpMulticast($channel)
{
	$RtpMcastEnable = 0;
	$RtpMcastIp = "0.0.0.0";
	$RtpMcastPort = 0;
	$RtpMcastTTL = 0;
	
	
	$ChannelInfo = $GLOBALS['encode_confs']->conf[$channel];
	if (!isset($_REQUEST['Enabled'])) {
		$RtpMcastEnable = $ChannelInfo->RTPMulticast->Enabled;
	} else {
		echo "as32d";
		$ChannelInfo->RTPMulticast->Enabled = $_REQUEST['Enabled'];
		$RtpMcastEnable = $_REQUEST['Enabled'];
	}
	
	if (!isset($_REQUEST['IPv4Address'])) {
		$RtpMcastIp = $ChannelInfo->RTPMulticast->IPv4Address;
	} else {
		$ChannelInfo->RTPMulticast->IPv4Address = $_REQUEST['IPv4Address'];
		$RtpMcastIp = $_REQUEST['IPv4Address'];
	}
	
	if (!isset($_REQUEST['Port'])) {
		$RtpMcastPort = $ChannelInfo->RTPMulticast->Port;
	} else {
		$ChannelInfo->RTPMulticast->Port = $_REQUEST['Port'];
		$RtpMcastPort = $_REQUEST['Port'];
	}
	
	if (!isset($_REQUEST['TTL'])) {
		$RtpMcastTTL = $ChannelInfo->RTPMulticast->TTL;
	} else {
		$ChannelInfo->RTPMulticast->TTL = $_REQUEST['TTL'];
		$RtpMcastTTL = $_REQUEST['TTL'];
	}
	
	if (checkRtpMulticastAddress($RtpMcastIp) == false || $RtpMcastPort < 1024 || $RtpMcastPort > 60000 || $RtpMcastTTL < 0 || $RtpMcastTTL > 255) {
			return false;			
	}

	return true;
}

function checkRtpMulticastAddress($addr)
{
	$mcastArray = explode(".", $addr);
	if (count($mcastArray) != 4)	return false;
	
	if ($mcastArray[0] < 224 || $mcastArray[0] > 239)	return false;
	for ($i=1;$i<4;$i++) {
		if ($mcastArray[$i] < 0 || $mcastArray[$i] > 255)	return false;
	}
	return true;
}

function change_video_rtp_mcast_enable($channel)
{
	if (!isset($_REQUEST['Enabled'])) return 1;
	if ($_REQUEST['Enabled'] < 0 || $_REQUEST['Enabled'] > 1)	return -1;
	
	//echo "ad";
	$ChannelInfo = $GLOBALS['encode_confs']->conf[$channel];
	$ChannelInfo->RTPMulticast->Enabled = $_REQUEST['Enabled'];
	return 0;
}

function change_video_rtp_mcast_ip($channel)
{
	if (!isset($_REQUEST['IPv4Address'])) return 1;
	if (strlen($_REQUEST['IPv4Address']) < 9 || strlen($_REQUEST['IPv4Address']) > 15) return -1;
	if (!checkRtpMulticastAddress($_REQUEST['IPv4Address']))	return -1;
	
	$ChannelInfo = $GLOBALS['encode_confs']->conf[$channel];
	$ChannelInfo->RTPMulticast->IPv4Address = $_REQUEST['IPv4Address'];
	return 0;
}

function change_video_rtp_mcast_port($channel)
{
	if (!isset($_REQUEST['Port'])) return 1;
	if ($_REQUEST['Port'] < 1024 || $_REQUEST['Port'] > 60000)	return -1;
	
	$ChannelInfo = $GLOBALS['encode_confs']->conf[$channel];
	$ChannelInfo->RTPMulticast->Port = $_REQUEST['Port'];
	return 0;
}

function change_video_rtp_mcast_ttl($channel)
{
	if (!isset($_REQUEST['TTL'])) return 1;
	if ($_REQUEST['TTL'] < 0 || $_REQUEST['TTL'] > 255)	return -1;
	
	$ChannelInfo = $GLOBALS['encode_confs']->conf[$channel];
	$ChannelInfo->RTPMulticast->TTL = $_REQUEST['TTL'];
	return 0;
}

function change_video_rtsp_timeout($channel)
{
	if (!isset($_REQUEST['rtsp_timeout'])) return 1;
	if ($_REQUEST['rtsp_timeout'] != 0  && $_REQUEST['rtsp_timeout'] < 30 || $_REQUEST['rtsp_timeout'] > 120)	return -1;
	
	$ChannelInfo = $GLOBALS['encode_confs']->conf[$channel];
	$ChannelInfo->SessionTimeout = $_REQUEST['rtsp_timeout'];

	return 0;
}
function change_video_dscp($channel)
{
	if (!isset($_REQUEST['dscp'])) return 1;
	if ($_REQUEST['dscp'] < 0 || $_REQUEST['dscp'] > 255)	return -1;
	
	$ChannelInfo = $GLOBALS['encode_confs']->conf[$channel];
	$ChannelInfo->DSCP = $_REQUEST['dscp'];

	return 0;
}
function change_video($channel)
{
	$other_multi_view_mode = 1;
	if(isset($_REQUEST['saveall'])){
       $saveall =  4; 
       $mod = 1;
	   if($_REQUEST['saveall'] == 2){
		   $other_multi_view_mode = 2;
	   }
	}
    else {
       $saveall =  1;
       $mod = MAX_VIDEO_ENCODER;
    }
		
    for($channel_num= ($channel % ($saveall * $mod)); $channel_num < (MAX_VIDEO_ENCODER / $other_multi_view_mode); $channel_num= $channel_num + (MAX_VIDEO_ENCODER / $saveall)){
    	if (change_video_codec($channel_num) < 0) return -1;
    	if (change_video_codecname($channel_num) < 0) return -1;
    	if (change_video_resolution($channel_num) < 0) return -1;
    	if (change_video_framerate($channel_num) < 0) return -1;
    	if (change_video_bitratemode($channel_num) < 0) return -1;
    	if (change_video_bitrate($channel_num) < 0) return -1;
    	if (change_video_quality($channel_num) < 0) return -1;
    	if (change_video_gopsize($channel_num) < 0) return -1;
    	if (change_video_h264_profile($channel_num) < 0) return -1;
    	if (change_video_h264_extension_option($channel_num) < 0 ) return -1;
    	if (change_video_lbr_mode($channel_num) < 0 ) return -1;
    	if (change_video_smart_core_mode($channel_num) < 0 ) return -1;
    
    	if (change_video_rtp_mcast_enable($channel_num) < 0) return -1;
    	if (change_video_rtp_mcast_ip($channel_num) < 0) return -1;
    	if (change_video_rtp_mcast_port($channel_num) < 0) return -1;
    	if (change_video_rtp_mcast_ttl($channel_num) < 0) return -1;
    	if (change_video_rtsp_timeout($channel_num) < 0) return -1;
      if (change_video_dscp($channel_num) < 0) return -1;
        
        sync_video_allsetting($channel,$channel_num);

    }
	return 0;
}

function sync_video_allsetting($channel,$channel_num){
    $ChannelInfo = $GLOBALS['encode_confs']->conf[$channel];
    $change_ENCODE_INFO = $GLOBALS['encode_confs']->conf[$channel_num];

    if(!isset($_REQUEST['codec'])){
            $change_ENCODE_INFO->Encoding = $ChannelInfo->Encoding ;
    }
    if(!isset($_REQUEST['resolution'])){
            $change_ENCODE_INFO->Resolution->Width = $ChannelInfo->Resolution->Width;
            $change_ENCODE_INFO->Resolution->Height = $ChannelInfo->Resolution->Height;
    }
    if(!isset($_REQUEST['framerate'])){
            $change_ENCODE_INFO->RateControl->FrameRateLimit = $ChannelInfo->RateControl->FrameRateLimit;
    }
    if(!isset($_REQUEST['bitrate_mode'])){
            $change_ENCODE_INFO->RateControl->ConstantBitRate = $ChannelInfo->RateControl->ConstantBitRate;
    }
    if(!isset($_REQUEST['bitrate'])){
    		if($change_ENCODE_INFO->Encoding == CODEC_HEVC)
    		{
    		$change_ENCODE_INFO->RateControl->HevcBitrateLimit = $ChannelInfo->RateControl->HevcBitrateLimit;
    		}
    		else
    		{
            $change_ENCODE_INFO->RateControl->BitrateLimit = $ChannelInfo->RateControl->BitrateLimit;
            }
    }
    if(!isset($_REQUEST['quality'])){
            $change_ENCODE_INFO->Compression = $ChannelInfo->Compression;
    }
    if(!isset($_REQUEST['gopsize'])){
            $change_ENCODE_INFO->H264->GovLength = $ChannelInfo->H264->GovLength;
    }
    if(!isset($_REQUEST['h264_profile'])){
            $change_ENCODE_INFO->H264->CodecProfile = $ChannelInfo->H264->CodecProfile;
    }
    if(!isset($_REQUEST['h264_extension_option'])){
            $change_ENCODE_INFO->Extension->SVCT_Mode = $ChannelInfo->Extension->SVCT_Mode;
    }
    if(!isset($_REQUEST['lbr_mode'])){
            $change_ENCODE_INFO->Extension->SmartLBR->mode = $ChannelInfo->Extension->SmartLBR->mode;
    }
    return 0;
 }

function get_video_options($channel)
{
	echo "channel : " . $channel  . "\r\n";
	if( $channel < 0 || $channel > MAX_VIDEO_ENCODER ) return -1;

	$codec= $GLOBALS['encode_confs']->conf[$channel]->Encoding;	
	$opt = $GLOBALS['etc_conf']->VideoEncoderOptions[--$channel];
	$data = NULL;

	switch ($codec)
	{
		case 1: //h264
			if( $opt->bH264Support )
			{
				$numValidRes = $opt->h264->numValidRes;
				$data['numValidRes'] = $numValidRes;
				for($i=0; $i < $numValidRes ; $i++)
				{
					$res = $opt->h264->Resolutions->Resolution[$i];
					$data['res'.$i] = $res->Width . 'x'.  $res->Height;
				}
				$data['govMin'] = $opt->h264->govMin;
				$data['govMax'] = $opt->h264->govMax;
				$data['frMin'] = $opt->h264->frMin;
				$data['frMax'] = $opt->h264->frMax;
				$data['eiMin'] = $opt->h264->eiMin;
				$data['eiMax'] = $opt->h264->eiMax;
				$data['brMin'] = $opt->h264->brMin;
				$data['brMax'] = $opt->h264->brMax;
			}
			break;
		case 2: //mjpeg
			if( $opt->bJpegSupport )
			{
				$numValidRes = $opt->jpeg->numValidRes;
				$data['numValidRes'] = $numValidRes;
				for($i=0; $i < $numValidRes ; $i++)
				{
					$res = $opt->jpeg->Resolutions->Resolution[$i];
					$data['res'.$i] = $res->Width . 'x'.  $res->Height;
				}
				$data['frMin'] = $opt->jpeg->frMin;
				$data['frMax'] = $opt->jpeg->frMax;
				$data['eiMin'] = $opt->jpeg->eiMin;
				$data['eiMax'] = $opt->jpeg->eiMax;
				$data['brMin'] = $opt->jpeg->brMin;
				$data['brMax'] = $opt->jpeg->brMax;
			}
			break;
		default :
			show_post_ng();
			break;
	}
	$data['qMin'] = $opt->qMin;	
	$data['qMax'] = $opt->qMax;	

	echo view_encode($data);
}
//--- rtsptimeout
function change_rtsptimeout(){
	$changed = 0 ;
	if (isset($_REQUEST['rtsp_timeout1'])){
		if ($_REQUEST['rtsp_timeout1'] != 0  && $_REQUEST['rtsp_timeout1'] < 30 || $_REQUEST['rtsp_timeout1'] > 120)	return -1;
		
		$ChannelInfo = $GLOBALS['encode_confs']->conf[$channel];
		$ChannelInfo->SessionTimeout = $_REQUEST['rtsp_timeout1'];
		
		$changed = 1; 
	}	
	if (isset($_REQUEST['rtsp_timeout2'])){ 
		if ($_REQUEST['rtsp_timeout2'] != 0  && $_REQUEST['rtsp_timeout2'] < 30 || $_REQUEST['rtsp_timeout2'] > 120)	return -1;
		
		$ChannelInfo = $GLOBALS['encode_confs']->conf[$channel];
		$ChannelInfo->SessionTimeout = $_REQUEST['rtsp_timeout2'];
	
		$changed = 1; 
	}
	if (isset($_REQUEST['rtsp_timeout3'])){
		if ($_REQUEST['rtsp_timeout3'] != 0  && $_REQUEST['rtsp_timeout3'] < 30 || $_REQUEST['rtsp_timeout3'] > 120)	return -1;
		
		$ChannelInfo = $GLOBALS['encode_confs']->conf[$channel];
		$ChannelInfo->SessionTimeout = $_REQUEST['rtsp_timeout3'];
		
		$changed = 1; 
	}	
	if( $changed ) 	return 0;
}
//--- audio
function audio_view_post()
{
	echo "input_volume=" . (int)$GLOBALS['profile_conf']->AudioEncoderConfiguration->Volume . "\r\n";
	echo "input_samplerate=" . (int)$GLOBALS['profile_conf']->AudioEncoderConfiguration->SampleRate. "\r\n";
	echo "output_volume=" . (int)$GLOBALS['profile_conf']->AudioOutputConfiguration->OutputLevel . "\r\n";
}

function change_audio_input_gain()
{
	if (!isset($_REQUEST['input_gain'])) return 1;
	if ($_REQUEST['input_gain'] < 1 || $_REQUEST['input_gain'] > 10) return -1;
	
	$GLOBALS['audio_conf']->InputLevel = $_REQUEST['input_gain'];

	return 0;
}
function change_audio_output_gain()
{
	if (!isset($_REQUEST['output_gain'])) return 1;
	if ($_REQUEST['output_gain'] < 0 || $_REQUEST['output_gain'] > 10) return -1;
	
	
	return 0;
}
function change_audio_enabled()
{
	if (!isset($_REQUEST['audio_enabled'])) return 1;
	$GLOBALS['profile_conf']->AudioEncoderConfiguration->Enabled = $_REQUEST['audio_enabled'];
	return 0;
}
function change_audio_input_volume()
{
	if (!isset($_REQUEST['input_volume'])) return 1;
	$GLOBALS['profile_conf']->AudioEncoderConfiguration->Volume = $_REQUEST['input_volume'];
	return 0;
}
function change_audio_input_samplerate()
{
	if (!isset($_REQUEST['input_samplerate'])) return 1;
	$GLOBALS['profile_conf']->AudioEncoderConfiguration->SampleRate= $_REQUEST['input_samplerate'];
	return 0;
}
function change_audio_input_encode()
{
	if (!isset($_REQUEST['input_encode'])) return 1;
	if($_REQUEST['input_encode'] == 10)
		$GLOBALS['profile_conf']->AudioEncoderConfiguration->Encoding = G711_CODEC;
	else
		$GLOBALS['profile_conf']->AudioEncoderConfiguration->Encoding = $_REQUEST['input_encode'];
	return 0;
}
function change_audio_input_format()
{
	if (!isset($_REQUEST['input_format'])) return 1;
	$GLOBALS['profile_conf']->AudioEncoderConfiguration->Format = $_REQUEST['input_format'];
	return 0;
}
function change_audio_input_ampenable()
{
	if (!isset($_REQUEST['input_AmpEnabled'])) return 1;
	$GLOBALS['profile_conf']->AudioEncoderConfiguration->AmpEnabled = $_REQUEST['input_AmpEnabled'];
	return 0;
}
function change_audio_output_volume()
{
	if (!isset($_REQUEST['output_volume'])) return 1;
	$GLOBALS['profile_conf']->AudioOutputConfiguration->OutputLevel = $_REQUEST['output_volume'];
	return 0;
}
function change_audio_rtp_mcast_enable()
{
	if (!isset($_REQUEST['Enabled'])) return 1;
	if ($_REQUEST['Enabled'] < 0 || $_REQUEST['Enabled'] > 1)	return -1;
	
	//echo "ad";
	$AudioInfo = $GLOBALS['profile_conf']->AudioEncoderConfiguration;
	$AudioInfo->RTPMulticast->Enabled = $_REQUEST['Enabled'];
	return 0;
}
function change_audio_rtp_mcast_ip()
{
	if (!isset($_REQUEST['IPv4Address'])) return 1;
	if (strlen($_REQUEST['IPv4Address']) < 9 || strlen($_REQUEST['IPv4Address']) > 15) return -1;
	if (!checkRtpMulticastAddress($_REQUEST['IPv4Address']))	return -1;
	
	$AudioInfo = $GLOBALS['profile_conf']->AudioEncoderConfiguration;
	$AudioInfo->RTPMulticast->IPv4Address = $_REQUEST['IPv4Address'];
	return 0;
}
function change_audio_rtp_mcast_port()
{
	if (!isset($_REQUEST['Port'])) return 1;
	if ($_REQUEST['Port'] < 1024 || $_REQUEST['Port'] > 60000)	return -1;
	
	$AudioInfo = $GLOBALS['profile_conf']->AudioEncoderConfiguration;
	$AudioInfo->RTPMulticast->Port = $_REQUEST['Port'];
	return 0;
}
function change_audio_rtp_mcast_ttl()
{
	if (!isset($_REQUEST['TTL'])) return 1;
	if ($_REQUEST['TTL'] < 0 || $_REQUEST['TTL'] > 255)	return -1;
	
	$AudioInfo = $GLOBALS['profile_conf']->AudioEncoderConfiguration;
	$AudioInfo->RTPMulticast->TTL = $_REQUEST['TTL'];
	return 0;
}
function change_audio_rtsp_timeout()
{
	if (!isset($_REQUEST['rtsp_timeout'])) return 1;
	if ($_REQUEST['rtsp_timeout'] != 0  && $_REQUEST['rtsp_timeout'] < 30 || $_REQUEST['rtsp_timeout'] > 120)	return -1;
	
	$AudioInfo = $GLOBALS['profile_conf']->AudioEncoderConfiguration;
	$AudioInfo->SessionTimeout = $_REQUEST['rtsp_timeout'];

	return 0;
}
function change_audio_dscp()
{
	if (!isset($_REQUEST['dscp'])) return 1;
	if ($_REQUEST['dscp'] < 0 || $_REQUEST['dscp'] > 255)	return -1;
	
	$AudioInfo = $GLOBALS['profile_conf']->AudioEncoderConfiguration;
	$AudioInfo->DSCP = $_REQUEST['dscp'];

	return 0;
}
function change_audio()
{
  if( change_audio_input_encode() < 0 ) return -1;
  if( change_audio_enabled() < 0 ) return -1;
	if( change_audio_input_volume() < 0 ) return -1;
	if( change_audio_input_samplerate() < 0) return -1;
	if( change_audio_input_format() < 0 ) return -1;
	if( change_audio_input_ampenable() < 0 ) return -1;
	if( change_audio_output_volume() < 0) return -1;
	//if (change_audio_input_gain() < 0)	return -1;
	//if (change_audio_output_gain() < 0)	return -1;

    if (change_audio_rtp_mcast_enable() < 0) return -1;
    if (change_audio_rtp_mcast_ip() < 0) return -1;
    if (change_audio_rtp_mcast_port() < 0) return -1;
    if (change_audio_rtp_mcast_ttl() < 0) return -1;
    if (change_audio_rtsp_timeout() < 0) return -1;
    if (change_audio_dscp() < 0) return -1;
	return 0;
}

//--- osd
function osd_view_post($src=0)
{
	for( $i=0 ; $i < $GLOBALS['system_caps']->video_in ; ++$i)
	{
		echo "[source=".($i+1) ."]\r\n";
		echo "time_enabled=" . $GLOBALS['osds_conf']->Osd[$i]->time_enabled . "\r\n";
		echo "text_enabled=" . $GLOBALS['osds_conf']->Osd[$i]->text_enabled . "\r\n";
		echo "time_x="       . $GLOBALS['osds_conf']->Osd[$i]->time_x       . "\r\n";
		echo "time_y="       . $GLOBALS['osds_conf']->Osd[$i]->time_y       . "\r\n";
		echo "text_x="       . $GLOBALS['osds_conf']->Osd[$i]->text_x       . "\r\n";
		echo "text_y="       . $GLOBALS['osds_conf']->Osd[$i]->text_y       . "\r\n";
		if( isset($GLOBALS['osds_conf']->Osd[$i]->text) ) {
			echo "text="     . $GLOBALS['osds_conf']->Osd[$i]->text         . "\r\n";
		}
		if($GLOBALS['system_caps']->have_pantilt && $GLOBALS['system_caps']->have_zoom > 1)
		{
		  echo "ptz_enabled=" . $GLOBALS['osds_conf']->Osd[$i]->ptz_enabled . "\r\n";
		  echo "ptz_x="       . $GLOBALS['osds_conf']->Osd[$i]->ptz_x       . "\r\n";
		  echo "ptz_y="       . $GLOBALS['osds_conf']->Osd[$i]->ptz_y       . "\r\n";		  
		} 
		if($GLOBALS['system_caps']->camera_type == 'thermal')
		{
			echo "temperature_enabled=" . $GLOBALS['osds_conf']->Osd[$i]->temperature_enabled . "\r\n";
			echo "temperature_x="       . $GLOBALS['osds_conf']->Osd[$i]->temperature_x       . "\r\n";
			echo "temperature_y="       . $GLOBALS['osds_conf']->Osd[$i]->temperature_y       . "\r\n";
		}	
        if(trim($GLOBALS['system_caps']->oem) == "DW")
        {
            echo "osd_stream="       . $GLOBALS['osds_conf']->Osd[$i]->osd_stream       . "\r\n";
        }
		echo "\r\n";
	}
	exit;
}

function change_osd($src=0)
{
	function change_osd_time_enable($src)
	{
		if (!isset($_REQUEST['time_enabled'])) return 1;
		if ($_REQUEST['time_enabled'] < 0 || $_REQUEST['time_enabled'] > 1) return -1;
		$GLOBALS['osds_conf']->Osd[$src]->time_enabled = $_REQUEST['time_enabled'];
		return 0;
	}
	function change_osd_ptz_enable($src)
	{
		if (!isset($_REQUEST['ptz_enabled'])) return 1;
		if ($_REQUEST['ptz_enabled'] < 0 || $_REQUEST['ptz_enabled'] > 1) return -1;
		$GLOBALS['osds_conf']->Osd[$src]->ptz_enabled = $_REQUEST['ptz_enabled'];
		return 0;
	}	
	function change_osd_temperature_enable($src)
	{
		if (!isset($_REQUEST['temperature_enabled'])) return 1;
		if ($_REQUEST['temperature_enabled'] < 0 || $_REQUEST['temperature_enabled'] > 1) return -1;
		$GLOBALS['osds_conf']->Osd[$src]->temperature_enabled = $_REQUEST['temperature_enabled'];
		return 0;
	}	
    function change_osd_stream($src)
	{
		if (!isset($_REQUEST['osd_stream'])) return 1;
		if ($_REQUEST['osd_stream'] < 0 || $_REQUEST['osd_stream'] > 7) return -1;
		$GLOBALS['osds_conf']->Osd[$src]->osd_stream = $_REQUEST['osd_stream'];
		return 0;
	}	
	function change_osd_text_enable($src)
	{
		if (!isset($_REQUEST['text_enabled'])) return 1;
		if ($_REQUEST['text_enabled'] < 0 || $_REQUEST['text_enabled'] > 1) return -1;

		$GLOBALS['osds_conf']->Osd[$src]->text_enabled = $_REQUEST['text_enabled']; return 0;
	}
	function change_osd_time_x($src)
	{
		if (!isset($_REQUEST['time_x'])) return 1;
		if ($_REQUEST['time_x'] < 0 || $_REQUEST['time_x'] > 100) return -1;

		$GLOBALS['osds_conf']->Osd[$src]->time_x = $_REQUEST['time_x'];
		return 0;
	}
	function change_osd_time_y($src)
	{
		if (!isset($_REQUEST['time_y'])) return 1;
		if ($_REQUEST['time_y'] < 0 || $_REQUEST['time_y'] > 100) return -1;

		$GLOBALS['osds_conf']->Osd[$src]->time_y = $_REQUEST['time_y'];
		return 0;
	}
	function change_osd_ptz_x($src)
	{
		if (!isset($_REQUEST['ptz_x'])) return 1;
		if ($_REQUEST['ptz_x'] < 0 || $_REQUEST['ptz_x'] > 100) return -1;

		$GLOBALS['osds_conf']->Osd[$src]->ptz_x = $_REQUEST['ptz_x'];
		return 0;
	}
	function change_osd_ptz_y($src)
	{
		if (!isset($_REQUEST['ptz_y'])) return 1;
		if ($_REQUEST['ptz_y'] < 0 || $_REQUEST['ptz_y'] > 100) return -1;

		$GLOBALS['osds_conf']->Osd[$src]->ptz_y = $_REQUEST['ptz_y'];
		return 0;
	}
	function change_osd_temperature_x($src)
	{
		if (!isset($_REQUEST['temperature_x'])) return 1;
		if ($_REQUEST['temperature_x'] < 0 || $_REQUEST['temperature_x'] > 100) return -1;

		$GLOBALS['osds_conf']->Osd[$src]->temperature_x = $_REQUEST['temperature_x'];
		return 0;
	}
	function change_osd_temperature_y($src)
	{
		if (!isset($_REQUEST['temperature_y'])) return 1;
		if ($_REQUEST['temperature_y'] < 0 || $_REQUEST['temperature_y'] > 100) return -1;

		$GLOBALS['osds_conf']->Osd[$src]->temperature_y = $_REQUEST['temperature_y'];
		return 0;
	}
	function change_osd_text_x($src)
	{
		if (!isset($_REQUEST['text_x'])) return 1;
		if ($_REQUEST['text_x'] < 0 || $_REQUEST['text_x'] > 100) return -1;

		$GLOBALS['osds_conf']->Osd[$src]->text_x = $_REQUEST['text_x'];
		return 0;
	}
	function change_osd_text_y($src)
	{
		if (!isset($_REQUEST['text_y'])) return 1;
		if ($_REQUEST['text_y'] < 0 || $_REQUEST['text_y'] > 100) return -1;

		$GLOBALS['osds_conf']->Osd[$src]->text_y = $_REQUEST['text_y'];
		return 0;
	}
	function change_osd_text($src)
	{
		if (!isset($_REQUEST['text'])) return 1;
		if (strlen($_REQUEST['text']) > 30) return -1;

		$GLOBALS['osds_conf']->Osd[$src]->text = $_REQUEST['text'];
		return 0;
	}

	if (change_osd_time_enable($src) < 0)   return -1;
	if (change_osd_time_x($src) < 0)        return -1;
	if (change_osd_time_y($src) < 0)        return -1;
	if (change_osd_text_enable($src) < 0)   return -1;
	if (change_osd_text_x($src) < 0)        return -1;
	if (change_osd_text_y($src) < 0)        return -1;
	if (change_osd_text($src) < 0)          return -1;
  if($GLOBALS['system_caps']->have_pantilt && $GLOBALS['system_caps']->have_zoom > 1)
  {
	if (change_osd_ptz_enable($src) < 0)   return -1;
	if (change_osd_ptz_x($src) < 0)        return -1;
	if (change_osd_ptz_y($src) < 0)        return -1;  
  }
  if($GLOBALS['system_caps']->camera_type == 'thermal' )
  {
	if (change_osd_temperature_enable($src) < 0)   return -1;
	if (change_osd_temperature_x($src) < 0)        return -1;
	if (change_osd_temperature_y($src) < 0)        return -1;  
  }
  if(trim($GLOBALS['system_caps']->oem) == "DW")
  {
    if(change_osd_stream($src) < 0)        return -1;
  }
	return 0;
}

//-- qproi
function qproi_view_post()
{
	for( $ch = 0 ; $ch < $GLOBALS['system_caps']->max_stream; ++$ch ) {
		$ROI = $GLOBALS['encode_confs']->conf[$ch]->Extension->Roi;
		echo "[channel" . ($ch+1) ."]\r\n";
		echo "x0=" . $ROI->Qproi_x . "\r\n";
		echo "y0=" . $ROI->Qproi_y . "\r\n";
		echo "w0=" . $ROI->Qproi_w . "\r\n";
		echo "h0=" . $ROI->Qproi_h . "\r\n";
		echo "t0=" . $ROI->Qproi_t . "\r\n";
		echo "s0=" . $ROI->Qproi_s . "\r\n\r\n";
	}
}

function change_qproi()
{
	function change_qproi_x()
	{
		if (!isset($_REQUEST['x0'])) return 1;
		if($GLOBALS['system_conf']->Corridor->enabled == 0)
			if ($_REQUEST['x0'] < 0 || $_REQUEST['x0'] > 100) return -1;
		$GLOBALS['encode_qprio']->Extension->Roi->Qproi_x = $_REQUEST['x0'];
		return 0;
	}
	function change_qproi_y()
	{
		if (!isset($_REQUEST['y0'])) return 1;
		if($GLOBALS['system_conf']->Corridor->enabled == 0)
			if ($_REQUEST['y0'] < 0 || $_REQUEST['y0'] > 100) return -1;
		$GLOBALS['encode_qprio']->Extension->Roi->Qproi_y = $_REQUEST['y0'];
		return 0;
	}
	function change_qproi_w()
	{
		if (!isset($_REQUEST['w0'])) return 1;
		if($GLOBALS['system_conf']->Corridor->enabled == 0)
			if ($_REQUEST['w0'] < 0 || $_REQUEST['w0'] > 100) return -1;
		$GLOBALS['encode_qprio']->Extension->Roi->Qproi_w = $_REQUEST['w0'];
		return 0;
	}
	function change_qproi_h()
	{
		if (!isset($_REQUEST['h0'])) return 1;
		if($GLOBALS['system_conf']->Corridor->enabled == 0)
			if ($_REQUEST['h0'] < 0 || $_REQUEST['h0'] > 100) return -1;
		$GLOBALS['encode_qprio']->Extension->Roi->Qproi_h = $_REQUEST['h0'];
		return 0;
	}
	function change_qproi_t()
	{
		if (!isset($_REQUEST['t0'])) return 1;
		if ($_REQUEST['t0'] < 0 || $_REQUEST['t0'] > 1) return -1;
		$GLOBALS['encode_qprio']->Extension->Roi->Qproi_t = $_REQUEST['t0'];
		return 0;
	}
	function change_qproi_s()
	{
		if (!isset($_REQUEST['s0'])) return 1;
		if ($_REQUEST['s0'] < 0 || $_REQUEST['s0'] > 100) return -1;
		$GLOBALS['encode_qprio']->Extension->Roi->Qproi_s = $_REQUEST['s0'];
		return 0;
	}

	$ch = get_channel_index(
		$GLOBALS['profile_conf']->VideoSourceConfigurations);
	if( $ch < 0 ) return -1;
	$GLOBALS['encode_qprio'] = $GLOBALS['encode_confs']->conf[$ch];

	if (change_qproi_x() < 0)    return -1;
	if (change_qproi_y() < 0)    return -1;
	if (change_qproi_w() < 0)    return -1;
	if (change_qproi_h() < 0)    return -1;

	if (change_qproi_t() < 0)    return -1;
	if (change_qproi_s() < 0)    return -1;

	return 0;
}


//--- SmartLBR

function change_SmartLBR($channel)
{

	function change_SmartLBR_streamid()
	{
		if (!isset($_REQUEST['lbr_streamid'])) return 1;
		if ($_REQUEST['lbr_streamid'] < 0 || $_REQUEST['lbr_streamid'] > 4) return -1;
		$GLOBALS['SmartLBR']->streamid = $_REQUEST['lbr_streamid'];
		return 0;
	}
	
	function change_SmartLBR_style()
	{
		if (!isset($_REQUEST['lbr_style'])) return 1;
		if ($_REQUEST['lbr_style'] < 0 || $_REQUEST['lbr_style'] > 4) return -1;
		$GLOBALS['SmartLBR']->style = $_REQUEST['lbr_style'];
		return 0;
	}
	function change_SmartLBR_bitrate()
	{
		if (!isset($_REQUEST['lbr_bitrate'])) return 1;
//		if ($_REQUEST['lbr_bitrate'] < 0 || $_REQUEST['lbr_bitrate'] > 20 *1024 * 1024 ) return -1;
		if ($_REQUEST['lbr_bitrate'] < 64 || $_REQUEST['lbr_bitrate'] > 20000 ) return -1;
		$GLOBALS['SmartLBR']->bitrate = $_REQUEST['lbr_bitrate'];
		return 0;
	}
	function change_SmartLBR_motionlevel()
	{
		if (!isset($_REQUEST['lbr_motion_level'])) return 1;
		if ($_REQUEST['lbr_motion_level'] < 0 || $_REQUEST['lbr_motion_level'] > 4) return -1;
		$GLOBALS['SmartLBR']->motion_level= $_REQUEST['lbr_motion_level'];
		return 0;
	}
	function change_SmartLBR_noiselevel()
	{
		if (!isset($_REQUEST['lbr_noise_level'])) return 1;
		if ($_REQUEST['lbr_noise_level'] < 0 || $_REQUEST['lbr_noise_level'] > 4) return -1;
		$GLOBALS['SmartLBR']->noise_level = $_REQUEST['lbr_noise_level'];
		return 0;
	}
	function change_SmartLBR_autorun()
	{
		if (!isset($_REQUEST['lbr_autorun'])) return 1;
		if ($_REQUEST['lbr_autorun'] < 0 || $_REQUEST['lbr_autorun'] > 1) return -1;
		$GLOBALS['SmartLBR']->autorun = $_REQUEST['lbr_autorun'];
		return 0;
	}
	function change_SmartLBR_onoff()
	{
		if (!isset($_REQUEST['lbr_onoff'])) return 1;
		if ($_REQUEST['lbr_onoff'] < 0 || $_REQUEST['lbr_onoff'] > 4) return -1;
		$GLOBALS['SmartLBR']->onoff = $_REQUEST['lbr_onoff'];
		return 0;
	}
	function change_SmartLBR_profile_0()
	{
		if (!isset($_REQUEST['lbr_profile_0'])) return 1;
		if ($_REQUEST['lbr_profile_0'] < 0 || $_REQUEST['lbr_profile_0'] > 4) return -1;
		$GLOBALS['SmartLBR']->profile_0 = $_REQUEST['lbr_profile_0'];
		return 0;
	}
	function change_SmartLBR_profile_1()
	{
		if (!isset($_REQUEST['lbr_profile_1'])) return 1;
		if ($_REQUEST['lbr_profile_1'] < 0 || $_REQUEST['lbr_profile_1'] > 4) return -1;
		$GLOBALS['SmartLBR']->profile_1 = $_REQUEST['lbr_profile_1'];
		return 0;
	}
	function change_SmartLBR_profile_2()
	{
		if (!isset($_REQUEST['lbr_profile_2'])) return 1;
		if ($_REQUEST['lbr_profile_2'] < 0 || $_REQUEST['lbr_profile_2'] > 4) return -1;
		$GLOBALS['SmartLBR']->profile_2 = $_REQUEST['lbr_profile_2'];
		return 0;
	}
	function change_SmartLBR_profile_3()
	{
		if (!isset($_REQUEST['lbr_profile_3'])) return 1;
		if ($_REQUEST['lbr_profile_3'] < 0 || $_REQUEST['lbr_profile_3'] > 4) return -1;
		$GLOBALS['SmartLBR']->profile_3 = $_REQUEST['lbr_profile_3'];
		return 0;
	}
	function change_SmartLBR_profile_4()
	{
		if (!isset($_REQUEST['lbr_profile_4'])) return 1;
		if ($_REQUEST['lbr_profile_4'] < 0 || $_REQUEST['lbr_profile_4'] > 4) return -1;
		$GLOBALS['SmartLBR']->profile_4 = $_REQUEST['lbr_profile_4'];
		return 0;
	}
	if (change_SmartLBR_streamid() < 0)    return -1;
	if (change_SmartLBR_style() < 0)       return -1;
	if (change_SmartLBR_bitrate() < 0)     return -1;
	if (change_SmartLBR_motionlevel() < 0) return -1;
	if (change_SmartLBR_noiselevel() < 0)  return -1;

	if (change_SmartLBR_autorun() < 0)     return -1;
	if (change_SmartLBR_onoff() < 0)       return -1;
	if (change_SmartLBR_profile_0() < 0)   return -1;
	if (change_SmartLBR_profile_1() < 0)   return -1;
	if (change_SmartLBR_profile_2() < 0)   return -1;
	if (change_SmartLBR_profile_3() < 0)   return -1;
	if (change_SmartLBR_profile_4() < 0)   return -1;

	return 0;
}

//--- Smart ACF

function change_SmartACF()
{
	function change_SmartACF_framerate()
	{
		if (!isset($_REQUEST['framerate'])) return 1;
		if ($_REQUEST['framerate'] < 1 || $_REQUEST['framerate'] > $GLOBALS['system_caps']->max_fps) return -1;
		$GLOBALS['SmartACF']->Extension->SmartACF->framerate = $_REQUEST['framerate'];
		return 0;
	}
	function change_SmartACF_targetbitrate($encoding)
	{
		if (!isset($_REQUEST['target_bitrate'])) return 1;
		if ($_REQUEST['target_bitrate'] < 100 || $_REQUEST['target_bitrate'] > 10240) return -1;
		if($encoding == 3)
		{
		  $GLOBALS['SmartACF']->Extension->SmartACF->target_bitrate_hevc = $_REQUEST['target_bitrate'];
		}
		else
		{
		  $GLOBALS['SmartACF']->Extension->SmartACF->target_bitrate = $_REQUEST['target_bitrate'];
		}
		return 0;
	}
	function change_SmartACF_targetgop()
	{
		if (!isset($_REQUEST['target_gop'])) return 1;
		if ($_REQUEST['target_gop'] < 1 || $_REQUEST['target_gop'] > 120) return -1;
		$GLOBALS['SmartACF']->Extension->SmartACF->target_gop = $_REQUEST['target_gop'];
		return 0;
	}
	function change_SmartACF_bitrateControl()
	{
		if (!isset($_REQUEST['bitrateControl'])) return 1;
		if ($_REQUEST['bitrateControl'] < 0 || $_REQUEST['bitrateControl'] > 1) return -1;
		$GLOBALS['SmartACF']->Extension->SmartACF->bitrateControl = $_REQUEST['bitrateControl'];
		return 0;
	}		
	function change_SmartACF_holdontime()
	{
		if (!isset($_REQUEST['hold_on_time'])) return 1;
		if ($_REQUEST['hold_on_time'] < 5 || $_REQUEST['hold_on_time'] > 60) return -1;
		$GLOBALS['SmartACF']->Extension->SmartACF->hold_on_time = $_REQUEST['hold_on_time'];
		return 0;
	}
	function change_SmartACF_triggerevent()
	{
		if (!isset($_REQUEST['trigger_event'])) return 1;
		if ($_REQUEST['trigger_event'] < 0 || $_REQUEST['trigger_event'] >= ON_EVENT_END) return -1; //UDP change event limit
		$GLOBALS['SmartACF']->Extension->SmartACF->trigger_event = $_REQUEST['trigger_event'];
		return 0;
	}

	$ch = get_channel_index(
		$GLOBALS['profile_conf']->VideoSourceConfigurations);
	if( $ch < 0 ) return -1;
	$GLOBALS['SmartACF'] = $GLOBALS['encode_confs']->conf[$ch];

	if (change_SmartACF_framerate() < 0)       return -1;
	if (change_SmartACF_targetbitrate($GLOBALS['encode_confs']->conf[$ch]->Encoding) < 0)     return -1;
	if (change_SmartACF_targetgop() < 0)     return -1;
	if (change_SmartACF_bitrateControl() < 0)     return -1;
	if (change_SmartACF_holdontime() < 0) return -1;
	if (change_SmartACF_triggerevent() < 0)  return -1;

    return 0;

}


//--- Smart Rate Control

function change_SmartRC()
{
    function change_SmartRC_stream_quality()
    {
        if (!isset($_REQUEST['stream_quality'])) return 1;
        if ($_REQUEST['stream_quality'] < 0 || $_REQUEST['stream_quality'] > 3) return -1;
        $GLOBALS['SmartRC']->Extension->SmartLBR->stream_quality = $_REQUEST['stream_quality'];
        return 0;
    }
    function change_SmartRC_dyn_roi_enable()
    {
        if (!isset($_REQUEST['dyn_roi_enable'])) return 1;
        if ($_REQUEST['dyn_roi_enable'] < 0 || $_REQUEST['dyn_roi_enable'] > 1) return -1;
        $GLOBALS['SmartRC']->Extension->SmartLBR->stream_quality = $_REQUEST['dyn_roi_enable'];
        return 0;
    }    
    function change_SmartRC_dyn_gop_enable()
    {
        if (!isset($_REQUEST['dyn_gop_enable'])) return 1;
        if ($_REQUEST['dyn_gop_enable'] < 0 || $_REQUEST['dyn_gop_enable'] > 1) return -1;
        $GLOBALS['SmartRC']->Extension->SmartLBR->dyn_gop_enable = $_REQUEST['dyn_gop_enable'];
        return 0;
    }
    function change_SmartRC_fps_drop_enable()
    {
        if (!isset($_REQUEST['fps_drop_enable'])) return 1;
        if ($_REQUEST['fps_drop_enable'] < 0 || $_REQUEST['fps_drop_enable'] > 1) return -1;
        $GLOBALS['SmartRC']->Extension->SmartLBR->fps_drop_enable = $_REQUEST['fps_drop_enable'];
        return 0;
    }

    $ch = get_channel_index(
            $GLOBALS['profile_conf']->VideoSourceConfigurations);
    if( $ch < 0 ) return -1;
    $GLOBALS['SmartRC'] = $GLOBALS['encode_confs']->conf[$ch];

    if (change_SmartRC_stream_quality() < 0)     return -1;
    if (change_SmartRC_dyn_roi_enable() < 0) return -1;
    if (change_SmartRC_dyn_gop_enable() < 0) return -1;
    if (change_SmartRC_fps_drop_enable() < 0)  return -1;

    return 0;

}

function change_Corridor_Mode()
{
	if (!isset($_REQUEST['enabled'])) return 1;
    if ($_REQUEST['enabled'] < 0 || $_REQUEST['enabled'] > 2) return -1;

	$GLOBALS['Corridor']->enabled= $_REQUEST['enabled'];
	return 0;
}

function change_dewarp_enable()
{
	$GLOBALS['Dewarp'] = $GLOBALS['video_source_confs']->Config[0]->Dewarp;

	if (!isset($_REQUEST['dewarp_enabled'])) return -1;
	if ($_REQUEST['dewarp_enabled'] < 0 || $_REQUEST['dewarp_enabled'] > 1) return -1;
	$GLOBALS['Dewarp']->enabled= $_REQUEST['dewarp_enabled'];
	return 0;
}


//------------------------------------------------------------------------------------------------------
// 	Html
//------------------------------------------------------------------------------------------------------

$src = 0;
if( isset( $_REQUEST['source'] ) ) {
	$val = $_REQUEST['source'];
	if( $val >= 0 && $val <= $GLOBALS['system_caps']->video_in )
		$src = $val;
}
if(isset($_REQUEST['submenu']))
{
	if ( $_REQUEST['submenu'] == 'video' )
{
	$channel = $_REQUEST['profile_no'];

	if ( $_REQUEST['action'] == 'view' )
	{
		echo '<meta http-equiv="Refresh" content="0; URL=setup_basic_video.cgi">';
	}
	else if ( $_REQUEST['action'] == 'apply' )
	{
		if( change_video($channel) != 0)
		{
			show_post_ng();
			exit;
		}
		$ipc_sock = new IPCSocket();
		$ipc_sock->Connection($GLOBALS['system_conf'], CMD_SET_VIDEO_ENCODE_CONFIGURATION);
		if ($ipc_sock->dataInfo['ErrorCode']['value'] == APP_OK)
		{
			show_post_ok();
		}
		else
		{
			show_post_ng();
		}
	}
	exit;
}
else if ( $_REQUEST['submenu'] == 'audio' )
{
	if ( $_REQUEST['action'] == 'view' )
	{
		echo '<meta http-equiv="Refresh" content="0; URL=setup_basic_audio.cgi">';
	}
	else if ( $_REQUEST['action'] == 'apply' )
	{
		change_audio();
		// TO DO
	}
	exit;
}
else if ( $_REQUEST['submenu'] == 'osd' )
{
	if ( $_REQUEST['action'] == 'view' )
	{
		osd_view_post($src);
	}
	else if ( $_REQUEST['action'] == 'apply' )
	{
		if( change_osd($src) < 0 )
		{
			show_post_ng();
		}
		else 
		{
			$ipc_sock = new IPCSocket();
			$ipc_sock->Connection($GLOBALS['osds_conf'], CMD_SET_OSD);
			if ($ipc_sock->dataInfo['ErrorCode']['value'] == APP_OK)
			{
				show_post_ok();
			}
			else
			{
				show_post_ng();
			}
		}
		// TO DO
	}
	exit;
}
else if ($_REQUEST['submenu'] == 'motionsetup' )
{
	if ( $_REQUEST['action'] == 'view' )
	{
		echo '<meta http-equiv="Refresh" content="0; URL=setup_basic_motion_setup.cgi">';
	}
	else if ( $_REQUEST['action'] == 'apply' )
	{
		// TO DO
	}
	exit;
}
else if ( $_REQUEST['submenu'] == 'rs485' )
{
	if ( $_REQUEST['action'] == 'view' )
	{
		echo '<meta http-equiv="Refresh" content="0; URL=setup_basic_rs485.cgi">';
	}
	else if ( $_REQUEST['action'] == 'apply' )
	{
		// TO DO
	}
	exit;
}
else if ( $_REQUEST['submenu'] == 'qproi' )
{

	if ( $_REQUEST['action'] == 'view' )
	{
		//video_view_post($channel);
	}
	else if ( $_REQUEST['action'] == 'apply' )
	{

		if ( change_qproi() != 0 )
		{
			show_post_ng();
			exit;
		}
	  
		$ipc_sock = new IPCSocket();
		$ipc_sock->Connection($GLOBALS['encode_qprio'], CMD_SET_VIDEO_QPROI);
		if ($ipc_sock->dataInfo['ErrorCode']['value'] == APP_OK)
		{
			show_post_ok();
		}
		else
		{
			show_post_ng();
		}
		echo "result : ".$ipc_sock->dataInfo['ErrorCode']['value'];
	}
	else
		show_post_ng();
	exit;
}

}
//------------------------------------------------------------------------------------------------------
// 	Sdk
//------------------------------------------------------------------------------------------------------
header("Content-Type: text/plain");
ob_end_clean();
if(isset($_REQUEST['msubmenu']))
{
if ( $_REQUEST['msubmenu'] == 'video' )
{
	if( isset($_REQUEST['profile_no']) &&  isset($_REQUEST['channel_no'])  )		// ??????????
	{
		show_post_ng();
		return;
	}
	if(isset($_REQUEST['profile_no']))
	{
	  if( $_REQUEST['profile_no'] < 0 || $_REQUEST['profile_no'] >= MAX_VIDEO_ENCODER)
	  {
  		show_post_ng();
  		return;	  
	  }
	}
	if(isset($_REQUEST['channel_no']))
	{
	  if( $_REQUEST['channel_no'] < 0 || $_REQUEST['channel_no'] >= MAX_VIDEO_ENCODER)
	  {
  		show_post_ng();
  		return;	  
	  }	
	}
	
	if( isset($_REQUEST['profile_no']) )
		$channel = $_REQUEST['profile_no'];
	else if( isset($_REQUEST['channel_no']) )
		$channel = $_REQUEST['channel_no'];

	if ( $_REQUEST['action'] == 'view' )
	{
		if( !isset($_REQUEST['profile_no']) &&  !isset($_REQUEST['channel_no'])  )		// ??????????
		{
			video_view_post(0);
			video_view_post(1);
			video_view_post(2);
		}
		else
			video_view_post($channel);
	}
	else if ( $_REQUEST['action'] == 'options')
	{
		if( $channel )
		{
			get_video_options($channel);
		}
		else
		{
			show_post_ng();
		}
	}
	else if ( $_REQUEST['action'] == 'apply' )
	{
		if( change_rtsptimeout() != 0)
		{
			show_post_ng();
		}
		if ( change_video($channel) != 0 )
		{
			show_post_ng();
			exit;
		}
	  
    $ipc_sock = new IPCSocket();
    $ipc_sock->Connection($GLOBALS['encode_confs'], CMD_SET_VIDEO_ENCODE_CONFIGURATION);
    if ($ipc_sock->dataInfo['ErrorCode']['value'] == APP_OK)
    {
    	show_post_ok();
    }
    else
    {
      show_post_ng();
    }
    echo "result : ".$ipc_sock->dataInfo['ErrorCode']['value'];
	}
	else if ( $_REQUEST['action'] == 'delete' )
	{
		video_delete($channel);
	}
	else if ( $_REQUEST['action'] == 'viewcap')
	{
		video_view_capability($channel);
	}
	else
		show_post_ng();
	exit;
}
else if ( $_REQUEST['msubmenu'] == 'profile' )
{
	if ( $_REQUEST['action'] == 'apply' )
	{
		if(!isset($_REQUEST['value']))
		{
			show_post_ng();
		}
		else
		{
			$VideoProfile = new CVideoProfile();
			$VideoProfile->Value = $_REQUEST['value'];
			$ipc_sock = new IPCSocket();
			$ipc_sock->Connection($VideoProfile, CMD_SET_VIDEO_PROFILE);
			if ($ipc_sock->dataInfo['ErrorCode']['value'] == APP_OK)
			{
				show_post_ok();	
			}
			else
			{
				show_post_ng();
			}
		}
	}
	else
		show_post_ng();
	exit;
}
else if ( $_REQUEST['msubmenu'] == 'vout_resolution' )
{
	if ( $_REQUEST['action'] == 'apply' )
	{
		if(!isset($_REQUEST['value']))
		{
			show_post_ng();
		}
		else
		{
			$vout_resolution_value = new CVideoProfile();
			$vout_resolution_value->Value = $_REQUEST['value'];
			$ipc_sock = new IPCSocket();
			$ipc_sock->Connection($vout_resolution_value, CMD_SET_VOUT_RESOLUTION);
			if ($ipc_sock->dataInfo['ErrorCode']['value'] == APP_OK)
			{
				show_post_ok();	
			}
			else
			{
				show_post_ng();
			}
		}
	}
	else
		show_post_ng();
	exit;
}
else if ( $_REQUEST['msubmenu'] == 'rtsp' )
{
	if ( $_REQUEST['action'] == 'view' )
	{
		echo '<meta http-equiv="Refresh" content="0; URL=setup_basic_audio.cgi">';
	}
	else if ( $_REQUEST['action'] == 'apply' )
	{
		if( change_rtsptimeout() != 0)
		{
			show_post_ng();
		}
		$ipc_sock = new IPCSocket();
		$ipc_sock->Connection($GLOBALS['profile_conf'], CMD_SET_VIDEO_ENCODE_CONFIGURATION);
		if ($ipc_sock->dataInfo['ErrorCode']['value'] == APP_OK)
		{
			show_post_ok();	
		}
		else
			show_post_ng();
	}
	else
		show_post_ng();
	exit;
}
else if ( $_REQUEST['msubmenu'] == 'audio' )
{
	if ($GLOBALS['system_caps']->audio_in == 0)
	{
		show_post_ng();
		exit;
	}
	
	if ( $_REQUEST['action'] == 'view' )
	{
		audio_view_post();
	}
	else if ( $_REQUEST['action'] == 'apply' )
	{
		if ( change_audio() == 0 )
		{
			$ipc_sock = new IPCSocket();
			$ipc_sock->Connection($GLOBALS['profile_conf'], CMD_SET_PROFILE_CONFIGURATION);
			if ($ipc_sock->dataInfo['ErrorCode']['value'] == APP_OK)
			{
				show_post_ok();
			}
			else
			{
				show_post_ng();
				echo "result : ".$ipc_sock->dataInfo['ErrorCode']['value'];
			}
		}
		else
			show_post_ng();
	}
	else
		show_post_ng();
	exit;
}
else if ( $_REQUEST['msubmenu'] == 'testaudio' )
{
	if ($_REQUEST['action'] == 'apply' )
	{
		if(isset ($_REQUEST['audio']))
		{
			$req = new CFocusMode();
			$req->mode = $_REQUEST['audio'];
			$ipc_sock = new IPCSocket();
			$ipc_sock->Connection($req, CMD_TEST_AUDIOOUT);
			if ($ipc_sock->dataInfo['ErrorCode']['value'] == APP_OK)
			{
				show_post_ok();
			}
			else
			{
				show_post_ng();
			}
		}
		show_post_ng();
	}
	else
		show_post_ng();
	exit;
}
else if ( $_REQUEST['msubmenu'] == 'osd' )
{
	$src = 0;
	if( isset( $_REQUEST['source'] ) ) {
		$val = $_REQUEST['source'];
		if( $val >= 0 && $val <= $GLOBALS['system_caps']->video_in )
			$src = $val;
	}
	if( $src > 0 ) $src--;
	if ( $_REQUEST['action'] == 'view' )
	{
		osd_view_post($src);
	}
	else if ( $_REQUEST['action'] == 'apply' )
	{
		if( change_osd($src) < 0 )
		{
			show_post_ng();
		}
		else 
		{
			$ipc_sock = new IPCSocket();
			$ipc_sock->Connection($GLOBALS['osds_conf'], CMD_SET_OSD);
			if ($ipc_sock->dataInfo['ErrorCode']['value'] == APP_OK)
			{
				show_post_ok();
			}
			else
			{
				show_post_ng();
			}
		}
		// TO DO
	}
	exit;
}
else if ( $_REQUEST['msubmenu'] == 'motionsetup' )
{
	if ( $_REQUEST['action'] == 'view' )
	{
		// TO DO		
	}
	else if ( $_REQUEST['action'] == 'apply' )
	{
		// TO DO
	}
	else
		show_post_ng();
	exit;
}
else if ( $_REQUEST['msubmenu'] == 'rs485' )
{
	// TO DO
	
	exit;
}
else if ( $_REQUEST['msubmenu'] == 'qproi' )
{

	if ( $_REQUEST['action'] == 'view' )
	{
		qproi_view_post();
	}
	else if ( $_REQUEST['action'] == 'apply' )
	{
		if ( change_qproi() != 0 )
		{
			show_post_ng();
			exit;
		}
		$ipc_sock = new IPCSocket();
		$ipc_sock->Connection($GLOBALS['encode_qprio'], CMD_SET_VIDEO_QPROI);
		if ($ipc_sock->dataInfo['ErrorCode']['value'] == APP_OK)
		{
			show_post_ok();
		}
		else
		{
			show_post_ng();
		}
		echo "result : ".$ipc_sock->dataInfo['ErrorCode']['value'];
	}
	else
		show_post_ng();
	exit;
}
else if ( $_REQUEST['msubmenu'] == 'SmartLBR' )
{
	if ( $_REQUEST['action'] == 'view' )
	{
		//video_view_post($channel);
	}
	else if ( $_REQUEST['action'] == 'apply' )
	{
			show_post_ng();
	}
	else
		show_post_ng();
	exit;
}
else if ( $_REQUEST['msubmenu'] == 'SmartACF' )
{
	if ( $_REQUEST['action'] == 'view' )
	{
    }
	else if ( $_REQUEST['action'] == 'apply' )
	{
        if(change_SmartACF() != 0)
        {
            show_post_ng();
            exit;
        }
        
		$ipc_sock = new IPCSocket();
		$ipc_sock->Connection($GLOBALS['SmartACF'], CMD_SET_SMART_ACF);
		if ($ipc_sock->dataInfo['ErrorCode']['value'] == APP_OK)
		{
			show_post_ok();
		}
		else
		{
			show_post_ng();
		}
		echo "result : ".$ipc_sock->dataInfo['ErrorCode']['value'];


    }
	else
		show_post_ng();
	exit;

}
else if ( $_REQUEST['msubmenu'] == 'SmartRC' )
{
	if ( $_REQUEST['action'] == 'view' )
	{
    }
	else if ( $_REQUEST['action'] == 'apply' )
	{
        if(change_SmartRC() != 0)
        {
            show_post_ng();
            exit;
        }
        
		$ipc_sock = new IPCSocket();
		$ipc_sock->Connection($GLOBALS['SmartRC'], CMD_SET_SMART_RC);
		if ($ipc_sock->dataInfo['ErrorCode']['value'] == APP_OK)
		{
			show_post_ok();
		}
		else
		{
			show_post_ng();
		}
		echo "result : ".$ipc_sock->dataInfo['ErrorCode']['value'];


    }
	else
		show_post_ng();
	exit;

}
else if ( $_REQUEST['msubmenu'] == 'Corridor' )
{
    if ( $_REQUEST['action'] == 'view' )
    {
    }
    else if ( $_REQUEST['action'] == 'apply' )
    {
        echo $_REQUEST['enabled']."\n";
        if(change_Corridor_Mode() != 0)
        {
            show_post_ng();
            exit;
        }

        $ipc_sock = new IPCSocket();
        $ipc_sock->Connection($GLOBALS['Corridor'], CMD_SET_CORRIDOR);
        if ($ipc_sock->dataInfo['ErrorCode']['value'] == APP_OK)
        {
            show_post_ok();
        }
        else
        {
            show_post_ng();
        }
    }
	else
		show_post_ng();
	exit;
}
else if ( $_REQUEST['msubmenu'] == 'dewarp' )
{
    if ( $_REQUEST['action'] == 'view' )
    {
    }
    else if ( $_REQUEST['action'] == 'apply' )
    {
        if(change_dewarp_enable() != 0)
        {
            show_post_ng();
            exit;
        }
        $ipc_sock = new IPCSocket();
        $ipc_sock->Connection($GLOBALS['Dewarp'], CMD_SET_DEWARP);
        echo "result : ".$ipc_sock->dataInfo['ErrorCode']['value'];
    }
    else
        show_post_ng();
    exit;

}

}
show_post_ng();

?>
