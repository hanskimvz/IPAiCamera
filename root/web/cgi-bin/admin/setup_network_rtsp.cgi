<?
require('../_define.inc');
require('../class/media.class');

//$media_conf = new CMediaConfiguration();
$profile_conf = new CProfileConfiguration();

function gertsp_timeoutInfo()
{
	$data = array();
	for($src=0; $src < MAX_MEDIA_SOURCE ; ++$src )
	{
		for($stream=0; $stream < MAX_VIDEO_CHANNEL; ++$stream )
		{
			$ch = $GLOBALS['profile_conf']->VideoSourceConfigurations->Config[$src]->StreamNums->num[$stream]->value;

			if( $ch < 0 ) continue;
			$data[$src][$stream]['rtsp_timeout'] = $GLOBALS['profile_conf']->VideoEncoderConfigurations->conf[$ch]->SessionTimeout;
			$data[$src][$stream]['dscp'] = $GLOBALS['profile_conf']->VideoEncoderConfigurations->conf[$ch]->DSCP;
			$data[$src][$stream]['Enabled']      = $GLOBALS['profile_conf']->VideoEncoderConfigurations->conf[$ch]->RTPMulticast->Enabled;
			$data[$src][$stream]['IPv4Address']  = trim($GLOBALS['profile_conf']->VideoEncoderConfigurations->conf[$ch]->RTPMulticast->IPv4Address);
			$data[$src][$stream]['Port']         = $GLOBALS['profile_conf']->VideoEncoderConfigurations->conf[$ch]->RTPMulticast->Port;
			$data[$src][$stream]['TTL']          = $GLOBALS['profile_conf']->VideoEncoderConfigurations->conf[$ch]->RTPMulticast->TTL;
			$data[$src][$stream]['AutoStart']    = $GLOBALS['profile_conf']->VideoEncoderConfigurations->conf[$ch]->RTPMulticast->AutoStart;
		}
	}
	echo json_encode($data);
}
function rtp_audioInfo()
{
    $data = array();
    for($src=0; $src < MAX_AUDIO_SOURCE ; ++$src ){
        $data[$src]['rtsp_timeout'] = $GLOBALS['profile_conf']->AudioEncoderConfiguration->SessionTimeout;
        $data[$src]['dscp'] = $GLOBALS['profile_conf']->AudioEncoderConfiguration->DSCP;
        $data[$src]['Enabled']      = $GLOBALS['profile_conf']->AudioEncoderConfiguration->RTPMulticast->Enabled;
        $data[$src]['IPv4Address']  = trim($GLOBALS['profile_conf']->AudioEncoderConfiguration->RTPMulticast->IPv4Address);
        $data[$src]['Port']         = $GLOBALS['profile_conf']->AudioEncoderConfiguration->RTPMulticast->Port;
        $data[$src]['TTL']          = $GLOBALS['profile_conf']->AudioEncoderConfiguration->RTPMulticast->TTL;
        $data[$src]['AutoStart']    = $GLOBALS['profile_conf']->AudioEncoderConfiguration->RTPMulticast->AutoStart;
    }
    echo json_encode($data);
}
function get_RtspSesstionInfo()
{
		$name = "RtspSessionInfo";
		$shm_id = shmop_open(KEY_SM_RTSP_CONNECTIONS, "a", 0, 0);
		if (!$shm_id) exit;
		
		$data = shmop_read($shm_id, 0, 4);
		$rtsp_connections = unpack("i1count", $data);

		$index = 0;
		if ($rtsp_connections['count'] > 0)
		{
			for($i=0; $i<20; $i++)
			{
				
				$data = shmop_read($shm_id, 4 + ($i)*16, 16);
				$rtsp_connections[$index] = unpack("i1sock/i1addr/i1port/i1type", $data);
				$type = ($rtsp_connections[$index]['type'] == 0) ? "TCP" : (($rtsp_connections[$index]['type'] == 2) ? "HTTP" : "UDP");
				if ( $rtsp_connections[$index]['sock'] >= 0)
				{
					echo $name."[".$index."] = new Object();\n";
					echo $name."[".$index."]['addr']='".trim(long2ip($rtsp_connections[$index]['addr']))."';\n" ;    
					echo $name."[".$index."]['port']=".$rtsp_connections[$index]['port'].";\n" ;
					echo $name."[".$index."]['type']='".trim($type)."';\n" ;
					$index++;
				}
			}
			echo $index."\r\n";
		}

		shmop_close($shm_id);	
}

?>
<!DOCTYPE html>
<html>
<head>
</head>
<body>
	<div class="contentTitle"><span tkey="RTSP_STATUS1"></span></div>
	<div class="content">
			<div class="selSource" style="display:none;">
				<div class="select" style="margin-left : 5px ;">
					<select id="vin_source" autocomplete="off">
					</select>
				</div>
			</div>
			<label class="maintitle">
				<span tkey="setup_rtsp_setup"></span>
			</label>
			<label class="subtitle"><span tkey="setup_record_stream"></span></label>
			<div class="select">
				<select id="target_stream">
				</select>
			</div>
	</div>
	<div class="content">
			<label class="maintitle" tkey="rtsp_session_timeout">RTSP Session TimeOut</label>
			<label class="subtitle" tkey="timeout"></label>
			<input type="text" id="rtsp_timeout" class="third">
			<input type="checkbox" id="ch0" name="SessionTimeout" value='0'><label for="ch0"></label><span tkey="rtsp_timeout"></span><br>
	</div>
	<div class="content" id="dscp_content">
			<label class="maintitle" tkey="setup_QoS">RTSP Session TimeOut</label>
			<label class="subtitle" tkey="setup_DSCP"></label>
			<input type="text" id="dscp" class="third">
			<span>[ 0~255 ]</span><br>
	</div>
	<div name="SmtpContent" class="content">
			<label class="maintitle"><span tkey="setup_rtp_multicast"></span></label>
			
			<label class="subtitle"><span tkey="MULTICAST"></span></label>			
			<input type="radio" value="0" name="Enabled" id="enabled" >
			<label for="enabled"></label><span tkey="setup_stop"></span>			
			<input type="radio" value="1" name="Enabled" id="disable" >
			<label for="disable"></label><span tkey="setup_start"></span><br>
	
			<label class="subtitle"><span tkey="IP"></span></label>
			<input id="IPv4Address" type="text" class="inputText"><br>	
			
			<div id="smtp_port_content">		
				<label class="subtitle"><span tkey="setup_port"></span></label>
				<input id="Port" type="text" class="inputText">[1024~60000]<br>
			</div>			
			<span></span>

			<label class="subtitle"><span tkey="TTL"></span></label>
			<input id="TTL" type="text" class="inputText">[1~255]<br>
	</div>
		<center>
			<button id="btOK" class="button" tkey="apply">Apply</button>
	</center>
	
	<div class="content padding_bottom_20">
		<table id="profile">
			<tr>
				<th tkey="num"></th>
				<th tkey="remote_ip"></th>
				<th tkey="port"></th>
				<th tkey="type"></th>
			</tr>
		</table>
		<div id="pages">
			<div class="left">
				<button class="button" id="prev_page"> < </button>
			</div>
			<div class="right">
				<button class="button" id="next_page"> > </button>
			</div>
		</div>
	</div>
		<script>				
			var VinStreamInfo  = <? getVinStreamInfo($GLOBALS['profile_conf']); ?>;
			var RtspTimeoutInfo = <? gertsp_timeoutInfo() ?>;
			var RtspSessionInfo = new Array();
            var RtpAudioInfo = <?rtp_audioInfo()?>;
			<?
				get_RtspSesstionInfo();
			?>
		</script>
		<script src="./setup_network_rtsp.js"></script>   
</body>
</html>
