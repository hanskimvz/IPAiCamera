<?php

// Global variable
$dic = [];
$operation_code = [];
$event_code = [];

function get_lang( $k ){
    global $dic;
    //var_dump($dic);
    return $dic[$k];
}
function get_ip($ipnum){
	/*
    $ip = "";
    $ip = strval(($ipnum & 0xff000000)>>24);
    $ip = $ip.".".strval(($ipnum & 0x00ff0000)>>16);
    $ip = $ip.".".strval(($ipnum & 0x0000ff00)>>8);
    $ip = $ip.".".strval($ipnum & 0x000000ff);
	*/
	$ip = ($ipnum%256 >= 0) ? ($ipnum%256) : (($ipnum%256) + 256) ;
	for ($i=1;$i<=3;$i++)
	{
		$ipnum=floor($ipnum/256);
		$ip=($ipnum%256 >= 0) ? ($ipnum%256).'.'.$ip : (($ipnum%256) + 256).'.'.$ip;
	}
    return $ip;
}
function trans_log( $type, $code, $value, $id, $obj){
    $log = "";
    global $operation_code, $event_code, $dic;
	$operation_code = [
		"LOG_SET_DEVICE_INFORMATION",
		"LOG_SET_USERS"              ,
		"LOG_ADD_USER"               ,
		"LOG_DEL_USER"               ,
		"LOG_SET_USER"               ,	
		"LOG_SET_DATETIME"           ,
		"LOG_SET_IO_CONFIGURATION"         ,
		"LOG_SET_RELAY_OUTPUT_STATE"       ,
		"LOG_SET_OSD"           ,
		"LOG_SET_SYSTEM_FACTORY_DEFAULT" ,
		"LOG_SYSTEM_REBOOT"          ,
		"LOG_SET_NETWORK_CONFIGURATION"    ,
		"LOG_SET_EVENT_CONFIGURATION"     ,
		"LOG_SET_CHANNEL_CONFIGURATION",	
		"LOG_SET_VIDEO_ENCODE_CONFIGURATION"     ,		
		"LOG_SET_PROFILES"                  ,
		"LOG_SET_PROFILE_CONFIGURATION"    , 
		"LOG_ADD_PROFILE"                  ,
		"LOG_DEL_PROFILE"                  ,
		"LOG_SET_PROFILE"                  ,
		"LOG_START_MULTICAST_STREAMING"    ,
		"LOG_STOP_MULTICAST_STREAMING"     ,
		"LOG_SET_SYNCHRONIZATION_POINT"     ,
		"LOG_DEL_RTSP_CONNECTION"      ,
		"LOG_SYSTEM_UPGRADE"		,
		"LOG_SET_CAMERA_SETUP",
		"LOG_SET_NTP_SYNC",
		"LOG_SET_CAMERA_DEAFULT",
		"LOG_SET_SETUP_INI",
		"LOG_TEST_FTP",
		"LOG_TEST_SMTP",
		"LOG_SET_CAMERA_RESTORE", 
		"LOG_ADD_RECORDING_JOB",
		"LOG_SET_RECORDING_JOB",
		"LOG_DEL_RECORDING_JOB",
		"LOG_ADD_EVENT_CONF",
		"LOG_SET_EVENT_CONF",
		"LOG_DEL_EVENT_CONF",
		"LOG_ADD_ACTION_RULE",
		"LOG_SET_ACTION_RULE",
		"LOG_DEL_ACTION_RULE",
		"LOG_SET_FORMAT_SDCARD",
		"LOG_SET_UNMOUNT_SDCARD",
		"LOG_SET_FTP_UPGRADE",
		"LOG_START_FTP_UPGRADE",
		"LOG_PTZ_MOVE",
		"LOG_PTZ_ARROW",
		"LOG_PTZ_ZOOM",
		"LOG_PTZ_POSITION_MOVE",
		"LOG_PTZ_STOP",
		"LOG_PTZ_SET_SPEED",
		"LOG_FOCUS_MOVE",
		"LOG_FOCUS_POSITION_MOVE",
		"LOG_IRIS_MOVE",
		"LOG_IRIS_POSITION_MOVE",	
		"LOG_SET_FOCUS_MODE",	
		"LOG_SET_RECORDING_CHANNEL",
		"LOG_SET_VIDEO_QPROI",
		"LOG_SET_SMART_LBR",
		"LOG_SET_IMAGING_SETTINGS",
		"LOG_SET_PRIVACY_MASK",
		"LOG_ADD_CAMERA_PROFILES", 
		"LOG_MODIFY_CAMERA_PROFILES",
		"LOG_APPLY_CAMERA_PROFILES",
		"LOG_DELETE_CAMERA_PROFILES",
		"LOG_ADD_STREAM_CLIENT",
		"LOG_SET_LANGUAGE",
		"LOG_SET_SECURITY_SERVICE",
		"LOG_SET_SECURITY_IP_FILTER",
		"LOG_ADD_SECURITY_IP_FILTER_ADDR",
		"LOG_DEL_SECURITY_IP_FILTER_ADDR",
		"LOG_DEL_ALL_SECURITY_IP_FILTER_ADDR",
		"LOG_SET_IEEE_8021X",
		"LOG_ADD_SELF_SIGNED_CERT",
		"LOG_DEL_CERTIFICATE",
		"LOG_CREATE_CSR",	
		"LOG_INSTALL_CERTIFICATE",	
		"LOG_INSTALL_CA",	
		"LOG_DEL_CA",	
		"LOG_SET_HTTPS",	
		"LOG_SET_RTSP_AUTHENTICATION",	
		"LOG_EXPORT_RECORDFILE",
		"LOG_SET_PRESET",
		"LOG_REMOVE_PRESET",
		"LOG_SET_PRESET_TOUR",
		"LOG_REMOVE_PRESET_TOUR",
		"LOG_SET_HOME_POSITION",
		"LOG_END_CODE",
	];
	$event_code = [
		"ON_SYSTEM_INIT",	// 1
		"ON_SYSTEM_TERMINATE",
		"ON_INITIALIZED_NETWORK",
		"ON_CHANGED_PROFILE",
		"ON_CHANGED_PROFILECONFIG",
		"ON_CHANGED_ENCODER",
		"ON_CHANGED_IP",
		"ON_CHANGE_DATETIME",
		"ON_CHANGE_USERINFO",
		"ON_REBOOTING_SYSTEM",
		"ON_REBOOT_RTSP_SERVER",
		//----------------------------------//
		"ON_EVENT_BASE",	//12
		"ON_EVENT_MOTION",
		"ON_EVENT_SCHEDULER",
		"ON_EVENT_SENSOR_ALARM",
		"ON_EVENT_RELAY",
		"ON_EVENT_NETWORK_DISCONNECTED",
		"ON_EVENT_SD_FULL",
		"ON_EVENT_SD_FAILURE",
		"ON_EVENT_IP_ADDR_CONFLICTED",
		"ON_EVENT_TEMPERATURE_CRITICAL",
		"ON_EVENT_ILLEGAL_LOGIN",	
        "ON_EVENT_USER_EVENT1",
        "ON_EVENT_USER_EVENT2",
        "ON_EVENT_USER_EVENT3",
        "ON_EVENT_USER_EVENT4",
        "ON_EVENT_USER_EVENT5",
        "ON_EVENT_USER_EVENT6",
        "ON_EVENT_USER_EVENT7",
        "ON_EVENT_USER_EVENT8",
        "ON_EVENT_USER_EVENT9",
        "ON_EVENT_USER_EVENT10",
        "ON_EVENT_USER_EVENT11",
        "ON_EVENT_USER_EVENT12",
        "ON_EVENT_USER_EVENT13",
        "ON_EVENT_USER_EVENT14",
        "ON_EVENT_USER_EVENT15",
        "ON_EVENT_USER_EVENT16",        
		"ON_EVENT_TEMPERATURE_DETECTED", //hdseo for thermal
		"ON_EVENT_CUSTOM_SNAP", //hdseo for iNode
		"ON_EVENT_PIR_DETECTED", 
		"ON_EVENT_SYS_INIT",		// cmlee
		"ON_EVENT_END",
    ];
    if ( $type == 2 ){
        $log = get_lang($operation_code[$code -1]);
    }else{
        if( $code == 13 || $code == 15 || $code == 39 || $code == 40 || $code == 16 ){
            if( $code == 39 || $code == 40 ){
                $log = get_lang($event_code[$code -1]) . " : " . ($value) . " : " . get_lang("EVENT_ON");
            }else{
                if($value == 1){
                    $log = get_lang($event_code[$code -1]) . " : " . ($id + 1) . " : " . get_lang("EVENT_ON");
                }else{
                    $log = get_lang($event_code[$code -1]) . " : " . ($id + 1) . " : " . get_lang("EVENT_OFF");
                }
            }
        }else{
            $log = get_lang($event_code[$code -1]);
        }
    }
    if( $obj == 0 ){
        $log = $log."(system)";
    }else{
        $log = $log."(".get_ip((int)$obj).")";
    }
    return $log;
}
function parse2($line)
{
	return "hello";
}

function parse($line){
    $ptext = "";
    $l = explode("IPNC: ", $line);
    
    if( count($l) > 1 ){
        $datetime = $l[0];
        $s = explode("::", $l[1]);
        if ( count($s) == 0 ){
            return "";
        }
        if ( $s[0] == 'legacy' ){
            $contents = explode(",", $s[1]);
            if( count($contents) < 7 ){
                return "";
            }
            // type, code, value, id, obj
            $str_contents = $datetime.": ".trans_log($contents[2],$contents[3],$contents[5],$contents[4],$contents[6])."\n";
        }else if( $s[0] == 'plain'){
            $str_contents = $datetime.": ".$s[2];
        }
    }else{
        return "";
    }
    return $str_contents;
}

function trans_lang($filepath, $lang){
    $f = fopen($filepath, "r") or die("unable to open file");
    $jd = fread($f, filesize($filepath));
    fclose($f);
    $res = [];
    
    $j = json_decode($jd);
    $arr = $j->{'language'};
        
    foreach( $arr as $item){
        $res[$item->{'key'}] = $item->{$lang};
    }
    
    return $res;
}


function generate_plain_logfile($logpath, $output, $lang, $langpath){
    global $dic;
	
    $dic = trans_lang($langpath, $lang);

    $log_fd = fopen($logpath, "r") or die("unable to open file");
    $target_fd = fopen($output, "w");

    while(!feof($log_fd)){
        $line = fgets($log_fd);
        if ( strlen($line) > 1 ){
            $ptext = parse($line);
           	fwrite($target_fd, $ptext, strlen($ptext));
        }
    }

    fclose($log_fd);
    fclose($target_fd);
}


//generate_plain_logfile('ipnc.log', 'result.txt', 'English', 'lang.json');


?>
