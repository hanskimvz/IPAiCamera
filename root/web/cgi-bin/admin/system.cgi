<?
require('../_define.inc');
require("../_upgrade.inc");
require('../class/system.class');
require('../class/capability.class');
require('../class/network.class');
require('../class/socket.class');

define('RESET_STATUS_PATH', '../resetStatus');

$shm_id = shmop_open(KEY_SM_SHARED_CONFIG, "a", 0, 0);
$system_conf = new CSystemConfiguration($shm_id);
$system_caps = new CCapability($shm_id);
$net_conf = new CNetworkConfiguration($shm_id);
$get_oem = $system_caps->getOEM();
shmop_close($shm_id);

$GLOBALS['system_conf']->SystemDatetime->SystemTime->year = 0;
//--- users
function users_view_post()
{
	$user_count = 0;
	for ($index=0; $index<MAX_USER; $index++)
	{
		if($GLOBALS['system_conf']->Users->User[$index]->Enabled)
		{
//			echo "".$index	. ":" . $GLOBALS['system_conf']->Users->User[$index]->Name . ":" . $GLOBALS['system_conf']->Users->User[$index]->Password . ":" . $GLOBALS['system_conf']->Users->User[$index]->Level . "\r\n" ;
			$user_count++;
		}
	}
	echo "user_count="	.$user_count."\r\n";
}
function users_count()
{
	$user_count = 0;
	for ($index=0; $index<MAX_USER; $index++)
	{
		
		if($GLOBALS['system_conf']->Users->User[$index]->Enabled)
		{
			$user_count++;
		}		
	}
	echo "user_count="	.$user_count."\r\n";
}

function user_change_name($index)
{
	if (!isset($_REQUEST['id'])) return 1;
	if (strlen($_REQUEST['id']) < 4) return -1;
	if (strlen($_REQUEST['id']) > 30) return -1;
//	if ($index == 0 && $_REQUEST['id'] != $GLOBALS['system_conf']->Users->User[$index]->Name) 
//	{
//		return -1;
//	}
//	if ($index == 0 && $_REQUEST['id'] != 'admin') )
//		return -1;
	//2012-11-14 : PITS #0001246 ; check duplication
	for ($i=0; $i<MAX_USER; $i++) {
		if($GLOBALS['system_conf']->Users->User[$index]->Enabled)
		{
			if ($index == $i)	continue;
			if ($GLOBALS['system_conf']->Users->User[$i]->Name == $_REQUEST['id'])
				return -1;
		}
	}

	$GLOBALS['system_conf']->Users->User[$index]->Name = $_REQUEST['id'];
	return 0;
}

function user_change_pass($index)
{
	$strongRegex = '/^(?=.{12,})(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])(?=.*[\W_]).*$/';
	if ($GLOBALS['get_oem'] == 2){
		$goodRegex = '/^(?=.{8,})(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])(?=.*[\W_]).*$/';
	}
	else {
		$goodRegex = '/^(?=.{8,})(((?=.*[A-Z])(?=.*[a-z])(?=.*[\W_]))|((?=.*[A-Z])(?=.*[0-9])(?=.*[\W_]))|((?=.*[a-z])(?=.*[0-9])(?=.*[\W_]))|((?=.*[A-Z])(?=.*[a-z])(?=.*[0-9]))).*$/';
	}
	$weakRegex   = '/^(?=.{8,})(((?=.*[A-Z])(?=.*[a-z]))|((?=.*[A-Z])(?=.*[0-9]))|((?=.*[a-z])(?=.*[0-9]))|((?=.*[A-Z])(?=.*[\W_]))|((?=.*[a-z])(?=.*[\W_]))|((?=.*[0-9])(?=.*[\W_]))).*$/';

	if (!isset($_REQUEST['pass'])) return 1;
//	if (strlen($_REQUEST['pass']) < 8) return -1;
	if (strlen($_REQUEST['pass']) > 30) return -1;

    if(preg_match($strongRegex, $_REQUEST['pass'])){
        ;
    }
    else if(preg_match($goodRegex, $_REQUEST['pass'])){
        ;
    }
    else {
		// print_r($_GET);
       return -1;
    }
	if ($GLOBALS['get_oem'] == 2)
	{
		if ((strpos($_REQUEST['pass'], 'admin') > 0)
		|| (strpos($_REQUEST['pass'], 'admin') === 0))
		{
			return -1;
		}
	}
	$GLOBALS['system_conf']->Users->User[$index]->Password = $_REQUEST['pass'];
	return 0;
}

function user_change_password_hint($index)
{
	if (!isset($_REQUEST['passhint'])) return 1;
	//if (strlen($_REQUEST['passhint']) < 4) return -1;
	if (strlen($_REQUEST['passhint']) > 62) return -1;

	$GLOBALS['system_conf']->Users->User[$index]->PasswordHint = $_REQUEST['passhint'];
	return 0;
}

function user_change_auth($index)
{
	if (!isset($_REQUEST['auth'])) return 1;
	if ($_REQUEST['auth'] != USER_ADMIN && $_REQUEST['auth'] != USER_OPERATOR && $_REQUEST['auth'] != USER_VIEWER && $_REQUEST['auth'] != 5) return -1;
	if ($index == 0 && ($_REQUEST['auth'] != USER_ADMIN && $_REQUEST['auth'] != 5))	return -1;
	if ($index != 0 && ($_REQUEST['auth'] == USER_ADMIN && $_REQUEST['auth'] == 5))	return -1;

	$GLOBALS['system_conf']->Users->User[$index]->Level = $_REQUEST['auth'];
	return 0;
}

function user_change_auto_login($index)
{
	if (!isset($_REQUEST['auto_login'])) return 1;


	return 0;
}

function update_lighttd_user()
{
	// lighttpd.user?? ?????? ???.
	$fp = fopen("/usr/lighttpd/lighttpd.user", 'w');

	for($i=0; $i<MAX_USER; $i++)
	{
		if($GLOBALS['system_conf']->Users->User[$index]->Enabled)
		{
			$data = $GLOBALS['system_conf']->Users->User[$i]->Name.":".$GLOBALS['system_conf']->Users->User[$index]->Password."\n";
			fwrite($fp, $data, strlen($data));
		}
	}
	fclose($fp);
}

function user_add()
{
	$user_count = 0;
	for($user_count=0; $user_count<MAX_USER; $user_count++)
	{
		if(!($GLOBALS['system_conf']->Users->User[$user_count]->Enabled))
		{
			$GLOBALS['system_conf']->Users->User[$user_count]->Enabled = 1;
			break;
		}
	}	
	if ($user_count > MAX_USER)	return -1;		
	if (!isset($_REQUEST['id']) || !isset($_REQUEST['pass']) || !isset($_REQUEST['auth']))	return -1;

	if (user_change_name($user_count) < 0)  return -1;
	if (user_change_pass($user_count) < 0)  return -1;
	if (user_change_password_hint($user_count) < 0)  return -1;
	if (user_change_auth($user_count) < 0)  return -1;

	$ipc_sock = new IPCSocket();
	$ipc_sock->Connection($GLOBALS['system_conf']->Users->User[$user_count], CMD_ADD_USER);
	if ($ipc_sock->dataInfo['ErrorCode']['value'] == APP_OK)
	{
		return 0;
	}
	else
	{
		return -1;
	}	
}

function user_modify($index)
{
	if (user_change_name($index) < 0)   return -1;
	if (user_change_auth($index) < 0)   return -1;
	if (user_change_pass($index) < 0)   return -1;
  	if (user_change_password_hint($index) < 0)   return -1;

	$ipc_sock = new IPCSocket();
	$ipc_sock->Connection($GLOBALS['system_conf']->Users->User[$index], CMD_SET_USER);
	if ($ipc_sock->dataInfo['ErrorCode']['value'] == APP_OK)
	{
		return 0;
	}
	else
	{
		return -1;
	}	

}

function user_delete($index)
{
	//0 (admin) ?? ???? ???.
	if ( $index < 1 || $index >= MAX_USER ) return -1;

	$ipc_sock = new IPCSocket();
	$ipc_sock->Connection($GLOBALS['system_conf']->Users->User[$index], CMD_DEL_USER);
	if ($ipc_sock->dataInfo['ErrorCode']['value'] == APP_OK)
	{
		return 0;
	}
	else
	{
		return -1;
	}	
}
function user_logout()
{
	$ipc_sock = new IPCSocket();
	$ipc_sock->Connection(NULL, CMD_USER_LOGOUT);
	if ($ipc_sock->dataInfo['ErrorCode']['value'] == APP_OK)
	{
		return 0;
	}
	else
	{
		return -1;
	}	
}

function user_validate($id,$password)
{
	$GLOBALS['system_conf']->Users->User[0]->Name = $id;
	$GLOBALS['system_conf']->Users->User[0]->Password = $password;

	$ipc_sock = new IPCSocket();
	$ipc_sock->Connection($GLOBALS['system_conf']->Users->User[0], CMD_VALIDATE_USER);
	if ($ipc_sock->dataInfo['ErrorCode']['value'] == APP_OK)
	{
		return 0;
	}
	else
	{
		return -1;
	}	
}


//--- date/time
function datetime_view_post()
{
	$ipc_sock = new IPCSocket();
	$ipc_sock->Connection($GLOBALS['system_conf']->SystemDatetime, CMD_GET_DATETIME);
	if ($ipc_sock->dataInfo['ErrorCode']['value'] == APP_OK)
	{
		$SystemTime = $GLOBALS['system_conf']->SystemDatetime->SystemTime;
		printf("system_time=%04d/%02d/%02d %02d:%02d:%02d\r\n", $SystemTime->year, $SystemTime->mon, $SystemTime->day, $SystemTime->hour, $SystemTime->min, $SystemTime->sec);
		echo "sync_type="   . $GLOBALS['system_conf']->SystemDatetime->Type . "\r\n";
		if ( $GLOBALS['system_conf']->SystemDatetime->Type == 0 )
		{	//sync with ntp
			echo "ntp_server="	. $GLOBALS['net_conf']->NTP->Index . "\r\n";
			echo "ntp_addr="	. trim($GLOBALS['net_conf']->NTP->Address) . "\r\n";
		}  	
	}
	else
	{
		show_post_ng();
	}	
}
function timezone_view_post()
{
	echo "timezone="	. 	$GLOBALS['system_conf']->SystemDatetime->TimeZoneIndex . "\r\n";
	echo "dst_enable="			.$GLOBALS['system_conf']->SystemDatetime->dst_enable.";\r\n";
	
	echo "dst_start_mon="	    .$GLOBALS['system_conf']->SystemDatetime->dst_start_mon.";\r\n";
	echo "dst_start_ordinal="	.$GLOBALS['system_conf']->SystemDatetime->dst_start_ordinal.";\r\n";
	echo "dst_start_week="	.$GLOBALS['system_conf']->SystemDatetime->dst_start_week.";\r\n";
	echo "dst_start_hour="	.$GLOBALS['system_conf']->SystemDatetime->dst_start_hour.";\r\n";

	echo "dst_end_mon="	    .$GLOBALS['system_conf']->SystemDatetime->dst_end_mon.";\r\n";
	echo "dst_end_ordinal="	.$GLOBALS['system_conf']->SystemDatetime->dst_end_ordinal.";\r\n";
	echo "dst_end_week="	.$GLOBALS['system_conf']->SystemDatetime->dst_end_week.";\r\n";
	echo "dst_end_hour="	.$GLOBALS['system_conf']->SystemDatetime->dst_end_hour.";\r\n";
	
//	echo "dst_bias="	.$GLOBALS['system_conf']->SystemDatetime->dst_bias.";\r\n";
//	echo "dst_enable="	.	$GLOBALS['system_conf']->SystemDatetime->DaylightSavings . "\r\n";
}

function reset_status_view_post()
{
	$fp = fopen(RESET_STATUS_PATH, "r") or die("read Fail!!");
	$buffer = @fread($fp, filesize(RESET_STATUS_PATH));

	if ($buffer) {
		echo htmlspecialchars($buffer)."\r\n";
	} else {
		echo "reset_status=0";
	}

	fclose($fp);
}

function change_date_synctype()
{
	if (!isset($_REQUEST['sync_type'])) return 1;
	if ( $_REQUEST['sync_type'] < 0 || $_REQUEST['sync_type'] > 2 ) return -1;

	$GLOBALS['system_conf']->SystemDatetime->Type = $_REQUEST['sync_type'];
	return 0;
}

function change_date_timezone() // BY LEO : TIMEZONE
{
	// print_r($_REQUEST);
	if (!isset($_REQUEST['gmt']))	return 1;
	// check on CamHandler
	// if ($_REQUEST['gmt'] < 0 || $_REQUEST['gmt'] > 96)	return -1;

	$GLOBALS['system_conf']->SystemDatetime->TimeZoneIndex = $_REQUEST['gmt'];
	return 0;
}
function view_language() 
{
	echo "language="	. $GLOBALS['system_conf']->SystemDatetime->Language. "\r\n";
}
function change_language() 
{
	if (!isset($_REQUEST['language']))	return 1;
	if ($_REQUEST['language'] < 0 || $_REQUEST['language'] > 20)	return -1;

	$GLOBALS['system_conf']->SystemDatetime->Language = $_REQUEST['language'];
	return 0;
}

function change_device_info()
{
	if (!isset($_REQUEST['device_name']))	return 1;
	if (strlen($_REQUEST['device_name']) > 30) return -1;

	$GLOBALS['system_conf']->DeviceInfo->DeviceName = $_REQUEST['device_name'];
	return 0;
}

function change_location_info()
{
	if (!isset($_REQUEST['location']))	return 1;
	if (strlen($_REQUEST['location']) > 30) return -1;

	$GLOBALS['system_conf']->DeviceInfo->Location = $_REQUEST['location'];
	return 0;
}
function change_system_device(){
	if(change_device_info() < 0) return -1;
	if(change_location_info() < 0) return -1;

	return 0;
}
function change_date_dst_enable()
{
	$SystemTime = $GLOBALS['system_conf']->SystemDatetime;

	if(isset($_REQUEST['dst_enable'])){	
		if($_REQUEST['dst_enable'] < 0 || $_REQUEST['dst_enable'] > 1)	return -1;
		$SystemTime->dst_enable = $_REQUEST['dst_enable'];
	}
	if(isset($_REQUEST['dst_start_mon'])){			
		 if($_REQUEST['dst_start_mon']<0 || $_REQUEST['dst_start_mon']>11 ) return -1;
		 $SystemTime->dst_start_mon = $_REQUEST['dst_start_mon'];
	}
	if(isset($_REQUEST['dst_start_ordinal'])){
		 if($_REQUEST['dst_start_ordinal']<0|| $_REQUEST['dst_start_ordinal']>4 ) return -1;
		 $SystemTime->dst_start_ordinal = $_REQUEST['dst_start_ordinal'];
	} 
	if(isset($_REQUEST['dst_start_week'])){
		 if($_REQUEST['dst_start_week']<0|| $_REQUEST['dst_start_week']>6 ) return -1;
		 $SystemTime->dst_start_week = $_REQUEST['dst_start_week'];
	}   
	if(isset($_REQUEST['dst_start_hour'])){
		 if($_REQUEST['dst_start_hour']<0 || $_REQUEST['dst_start_hour']>23 ) return -1;
		 $SystemTime->dst_start_hour = $_REQUEST['dst_start_hour'];
	}   
	
	if(isset($_REQUEST['dst_end_mon'])){			
		 if($_REQUEST['dst_end_mon']<0 || $_REQUEST['dst_end_mon']>11 ) return -1;
		 $SystemTime->dst_end_mon = $_REQUEST['dst_end_mon'];
	}
	if(isset($_REQUEST['dst_end_ordinal'])){
		 if($_REQUEST['dst_end_ordinal']<0|| $_REQUEST['dst_end_ordinal']>4 ) return -1;
		 $SystemTime->dst_end_ordinal = $_REQUEST['dst_end_ordinal'];
	} 
	if(isset($_REQUEST['dst_end_week'])){
		 if($_REQUEST['dst_end_week']<0|| $_REQUEST['dst_end_week']>6 ) return -1;
		 $SystemTime->dst_end_week = $_REQUEST['dst_end_week'];
	}   
	if(isset($_REQUEST['dst_end_hour'])){
		 if($_REQUEST['dst_end_hour']<0 || $_REQUEST['dst_end_hour']>23 ) return -1;
		 $SystemTime->dst_end_hour = $_REQUEST['dst_end_hour'];
	}  


	return 0;
}

function change_date_ntp()
{
	if(isset($_REQUEST['ntp_server']))
	{
    	if($_REQUEST['ntp_server']<0 || $_REQUEST['ntp_server']>5) return -1;
		if($_REQUEST['ntp_server'] == 5)
		{
			if(!isset($_REQUEST['ntpurl'])) return -1;
      		$GLOBALS['net_conf']->NTP->Index   = 5;
      		$GLOBALS['net_conf']->NTP->Address = $_REQUEST['ntpurl'];
		}
		else
		{
			$GLOBALS['net_conf']->NTP->Index   = $_REQUEST['ntp_server'];
		}  
		$ipc_sock = new IPCSocket();
		$ipc_sock->Connection($GLOBALS['net_conf'], CMD_SET_NETWORK_CONFIGURATION);				  
	}
	else if(isset($_REQUEST['ntpurl']))
	{
		$GLOBALS['net_conf']->NTP->Address = $_REQUEST['ntpurl'];
		$ipc_sock = new IPCSocket();
		$ipc_sock->Connection($GLOBALS['net_conf'], CMD_SET_NETWORK_CONFIGURATION);		
	}
	else return 1;
	return 0;
}

function change_date_date()
{
	$changed = false;
	if( isset($_REQUEST['sync_type'] ) ) {
		if ( $_REQUEST['sync_type'] == 1 || $_REQUEST['sync_type'] == 2 ) {
			$SystemTime = $GLOBALS['system_conf']->SystemDatetime->SystemTime;
			if(!isset($_REQUEST['year'])) return -1;
			if(!isset($_REQUEST['mon']))  return -1;
			if(!isset($_REQUEST['day']))  return -1;
			if(!isset($_REQUEST['hour'])) return -1;
			if(!isset($_REQUEST['min']))  return -1;
			if(!isset($_REQUEST['sec']))  return -1;

			$SystemTime->Type = $_REQUEST['sync_type'];
			$SystemTime->year = $_REQUEST['year'];
			$SystemTime->mon = $_REQUEST['mon'];
			$SystemTime->day = $_REQUEST['day'];
			$SystemTime->hour = $_REQUEST['hour'];
			$SystemTime->min = $_REQUEST['min'];
			$SystemTime->sec = $_REQUEST['sec'];
			$SystemTime->is_gmt = 0;

			$changed = true;
		}
		else if ( $_REQUEST['sync_type'] == 0 ) {
			$changed = true;
		}
	}
	if ( isset($_REQUEST['time_format']) ) {
		$GLOBALS['system_conf']->SystemDatetime->TimeFormat = $_REQUEST['time_format'];	
		$changed = true;
	}
	if( $changed ) {
		$ipc_sock = new IPCSocket();
		$ipc_sock->Connection($GLOBALS['system_conf']->SystemDatetime, CMD_SET_DATETIME);
		if ($ipc_sock->dataInfo['ErrorCode']['value'] == APP_OK)
			return 0;
		else
			return -1;
	}
	return -1;
}

function change_date()
{
	if (change_date_synctype() < 0) return -1;
	if (change_date_ntp() < 0) return -1;

	return 0;
}

function change_timezone()
{
	if (change_language() < 0)   return -1;
	if (change_date_timezone() < 0)		return -1;
	if (change_date_dst_enable() < 0)	return -1;

	return 0;
}

// timezone add
function get_gmt_offset()
{
	$gmt_offset = 0;

	return $gmt_offset;
}


function change_time_format()
{
	if( !isset($_REQUEST['format']) < 0 || !isset($_REQUEST['hourformat']) < 0 ) return -1;
	if( isset($_REQUEST['format']))
		$GLOBALS['system_conf']->SystemDatetime->TimeFormat = $_REQUEST['format'];
	if( isset($_REQUEST['hourformat']))
		$GLOBALS['system_conf']->SystemDatetime->HourFormat = $_REQUEST['hourformat'];
	return 0;
}

function time_format_view()
{
	echo "timeformat=".$GLOBALS['system_conf']->SystemDatetime->TimeFormat."\r\n";
	echo "hourformat=".$GLOBALS['system_conf']->SystemDatetime->HourFormat."\r\n";
}
/*
function get_system_log($isJson=false)
{
	$log_data = array();
	do {
		$shm_id = shmop_open(KEY_SM_LOG_LIST_SYS, "a", 0, 0);
		if (!$shm_id) {
			break;
		}

		// read and prase a log header file
		$data = shmop_read($shm_id, 0, LOG_HEADER_SIZE );
		$BasketHeader = unpack("i1targetBasket/i1offset/icount/i1start/i1end", $data);

		$StartPoint = $BasketHeader['start'];
		if( $BasketHeader['start'] > $BasketHeader['end'] ) {
			$StartPoint--;
		}

		$offset = LOG_HEADER_SIZE;
		$count = 0;
		for($BasketIndex=1 ; $BasketIndex <= MAX_LOG_BASKET; $BasketIndex++)
		{
			$data = shmop_read($shm_id, $offset, 4);
			$Basket = unpack("i1count", $data);
			$offset += BASKET_HEADER_SIZE;
			for($i=0 ; $i < $Basket['count'] ; $i++, $offset += 30)
			{
				$StartPoint = $StartPoint % MAX_LOG_ON_BASKET;
				$data = shmop_read($shm_id, $offset, 30);
				$tmp = unpack("i1time/c1year/c1month/c1day/c1hour/c1min/c1sec/i1type/i1code/i1id/i1value/i1object", $data);
				array_unshift($log_data, $tmp);
				$count++;
			}
		}
		shmop_close($shm_id);

		if( $BasketHeader['start'] > $BasketHeader['end']){
			for($i=0; $i < $BasketHeader['end'] ; $i++) {
				$data = array_pop($log_data);
				array_unshift($log_data, $data);
			}
		}
	} while(0);
	if( count($log_data) ){
		if( $isJson ) {
			echo json_encode($log_data);
		}
		else {
			return $log_data;
		}
	} else {
		echo "[]";
	}
}
*/

define('LOG_FILE_LAST_INDEX', 7);
define('LOG_FILE_PATH_PREFIX', '/log/ipnc');
define('LOG_MODULE_NAME', 'IPNC');
define('LOG_LEGACY', 'legacy');
define('LOG_PLAIN', 'plain');
function get_system_log($isJson=false)
{
    $log_data = array();
    $log_raw_data = array();
    
    $log_file_list = array();

    // get log file list
    for($i = LOG_FILE_LAST_INDEX; $i >= 0 ; $i-- ){
        $tmp = LOG_FILE_PATH_PREFIX.'.log.'.$i;
        //echo($tmp);
        if( file_exists($tmp) ){
            $log_file_list[] = $tmp;
            //echo('exists');
        }
    }
	$tmp = LOG_FILE_PATH_PREFIX.'.log';
    if( file_exists($tmp) ){
		$log_file_list[] = $tmp;
	}


    // load log
    foreach( $log_file_list as $file){
        $h = fopen($file, 'r');
        while(($line = fgets($h)) !== false){
            $log_raw_data[] = $line;
        }
        fclose($h);
    }

    $log_raw_data = array_reverse($log_raw_data);

    // re-formating
    
    foreach( $log_raw_data as $l ){
        $d = array();
		if (($l <= 'A') || ($l >= 'Z')) continue;   // 잘못된 로그 데이타 필터링, 삭제 // written by cmlee
        $ret = explode(": ", $l);
        $info = sscanf($ret[0], "%s %s %s %s");
        //print_r($info);
        if( $info[3] != LOG_MODULE_NAME ) continue;
        $t = explode("::", $ret[1]);
        
        $tmp = explode(",", $t[1]);
        $d['time'] = $tmp[0];
        $dt = sscanf($tmp[1],"%04d-%02d-%02d %02d:%02d:%02d");

        $d['year'] = $dt[0];
        $d['month'] = $dt[1];
        $d['day'] = $dt[2];
        $d['hour'] = $dt[3];
        $d['min'] = $dt[4];
        $d['sec'] = $dt[5];
        
        if( $t[0] == LOG_LEGACY){
            $d['logtype'] = 'legacy';
            $d['type'] = $tmp[2];
            $d['code'] = $tmp[3];
            $d['id'] = $tmp[4];
            $d['value'] = $tmp[5];
            $d['object'] = $tmp[6];
        }else{
            $d['logtype'] = 'plain';
            $d['log'] = $t[2];
            $d['type'] = $tmp[2];
        }
        
        $log_data[] = $d;
    }
    if ( count($log_data) == 0 ){
        echo '[]';
    }else{
        if ( $isJson ){
            echo json_encode($log_data);
        }else{
            return $log_data;
        }
    }
    
    
}
function backup_log()
{
	$log_path = '/log/ipnc.log';
	$dst_path = '/tmp/log_file';
	$lang_path = '/root/web/js/lang.json';
	$dst_log = '/root/web/log.txt';
	if(file_exists($dst_log))
	{
		system( 'rm '.$dst_log);
	}

	$cmd = '';
	include_once("/root/web/cgi-bin/admin/log_transfer.cgi");
	for($i=7; $i>=0; $i--){
		$log_file = $log_path.'.'.$i;
		echo $log_file;
		if(file_exists($log_file)){
			generate_plain_logfile($log_file, $dst_path.$i.'.txt', $_REQUEST['lang'], $lang_path);
			$cmd = $cmd.$dst_path.$i.'.txt ';
		}
	}
	generate_plain_logfile($log_path, $dst_path.'.txt', $_REQUEST['lang'], $lang_path);
	$cmd = $cmd.$dst_path.'.txt ';
	system( 'cat '.$cmd.'> '.$dst_log);
	system( 'rm '.$cmd);
}
function encrypt_config()
{
	include_once("/root/web/cgi-bin/admin/encrypt.cgi");
	$data =  $_REQUEST['key'];
	enc_main($data);
	return 0;
}
function download_config()
{
	$path = "/root/web/pconf_enc.tar";
	if(file_exists($path)) {
		header('Content-Description: File Transfer');
		header('Content-Type:  multipart/form-data');
		header('Content-Disposition: attachment; filename="'.basename($path).'"');
		header('Content-Length: ' . filesize($path));
		readfile($path);
	} 
	unlink($path);
	return 0;
}
function upload_config()
{
	if( !isset($_FILES['file']['tmp_name'])) return -1;
	$file_type_check = explode('.',$_FILES['file']['name']);

	//파일 확장자 체크
	$file_type = $file_type_check[count($file_type_check)-1];
	$file = "/root/web/"."pconf_enc.".$file_type;
	if( !move_uploaded_file($_FILES['file']['tmp_name'],$file)) return -1;

	include_once("/root/web/cgi-bin/admin/decrypt.cgi");
	$data =  $_REQUEST['key'];
	return dec_main($data);

}
    
//------------------------------------------------------------------------------------------------------
// 	Html
//------------------------------------------------------------------------------------------------------
if(isset($_REQUEST['submenu']))
{
	if ( $_REQUEST['submenu'] == 'users' )
	{
		if ( $_REQUEST['action'] == 'view' )
		{
			echo '<meta http-equiv="Refresh" content="0; URL=setup_system_users.cgi">';
		}
		else if ( $_REQUEST['action'] == 'apply' )
		{
			echo "Apply";
		}
		else if ( $_REQUEST['action'] == 'add' )
		{
			if( user_add() == 0)
				show_post_ok();
			else
				show_post_ng();
		}
		else if ( $_REQUEST['action'] == 'modify' )
		{
			if (isset($index))
			{
				$index = $_REQUEST['index'];
				if( user_modify($index) == 0)
					show_post_ok();
				else
					show_post_ng();
			}
			else if ( $_REQUEST['action'] == 'del' )
			{
				$index = $_REQUEST['index'];
				if (isset($index))
				{
					if ( user_delete($index) == 0 )
						show_post_ok();
					else
						show_post_ng();
				}
			}
			exit;
		}
	}
	else if ( $_REQUEST['submenu'] == 'datetime' )
	{
		if ( $_REQUEST['action'] == 'view' )
		{
			echo '<meta http-equiv="Refresh" content="0; URL=setup_system_date_time.cgi">';
		}
		else if ( $_REQUEST['action'] == 'server' )
		{

		}
		else if ( $_REQUEST['action'] == 'apply' )
		{
			if( change_date() == 0 && change_date_date() == 0 )
			{
				show_post_ok();
			}
			else
			{
				show_post_ng();
			}
		}
		else if ( $_REQUEST['action'] == 'ntpstop' )
		{

		}
		exit;
	}
	else if ( $_REQUEST['submenu'] == 'timezone' )  // BY LEO : TIMEZONE
	{
		if ( $_REQUEST['action'] == 'apply' )
		{
			change_timezone();
			$ipc_sock = new IPCSocket();
			$ipc_sock->Connection($GLOBALS['system_conf']->SystemDatetime, CMD_SET_DATETIME);
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
	else if ( $_REQUEST['submenu'] == 'defaultset' )
	{
		if ($_REQUEST['action'] == 'view' )
		{
			echo '<meta http-equiv="Refresh" content="0; URL=setup_system_default_set.cgi">';
		}
		else if ( $_REQUEST['action'] == 'apply' )
		{
			if (!isset($_REQUEST['all'])) exit;

			$factorySet = new CFactoryDefault();
			if ($_REQUEST['all'] == true)	
			{
				$factorySet->Type = 0;
			}
			else				
			{
				$factorySet->Type = 1;
			}
			$ipc_sock = new IPCSocket();
			$ipc_sock->Connection($factorySet, CMD_SET_SYSTEM_FACTORY_DEFAULT);
			if ($ipc_sock->dataInfo['ErrorCode']['value'] == APP_OK)
			{
				show_post_ok();
				echo ("System will restart!");	
			}
			else
			{
				show_post_ng();
			}		
		}
		exit;
	}
	else if ( $_REQUEST['submenu'] == 'upgrade' )
	{
		if ( $_REQUEST['action'] == 'apply' )
		{
			$uploadRequest = new CUploadRequest();
			//$uploadRequest->Cmd
			//$uploadRequest->Param
			
			$ipc_sock = new IPCSocket();
			$ipc_sock->Connection($uploadRequest, CMD_SYSTEM_UPGRADE);
			if ($ipc_sock->dataInfo['ErrorCode']['value'] == APP_OK)
			{
			  show_post_ok();
			  //echo ("System will upgrade!");	
			}
			else
			{
			  show_post_ng();
			}		
		}
		else if ( $_REQUEST['action'] == 'start' )
		{
			$uploadRequest = new CUploadRequest();
			//$uploadRequest->Cmd
			//$uploadRequest->Param
			
			$ipc_sock = new IPCSocket();
			$ipc_sock->Connection($uploadRequest, CMD_SYSTEM_UPDATE_READY);
			if ($ipc_sock->dataInfo['ErrorCode']['value'] == APP_OK)
			{
			  show_post_ok();
			  //echo ("System will upgrade!");	
			}
			else
			{
			  show_post_ng();
			}		
		}
		else if ( $_REQUEST['action'] == 'stop' )
		{
			$uploadRequest = new CUploadRequest();
			//$uploadRequest->Cmd
			//$uploadRequest->Param
			
			$ipc_sock = new IPCSocket();
			$ipc_sock->Connection($uploadRequest, CMD_SYSTEM_UPDATE_STOP);
			if ($ipc_sock->dataInfo['ErrorCode']['value'] == APP_OK)
			{
			  show_post_ok();
			  //echo ("System will upgrade!");	
			}
			else
			{
			  show_post_ng();
			}		
		}				
		else if ( $_REQUEST['action'] == 'status' )
		{
			$ipc_sock = new IPCSocket(UPGRADE_SOCKET_PATH);
			$ipc_sock->Connection($GLOBALS["status"], M_UPGRADE_STATUS);
			echo "status=".$GLOBALS["status"]->Status."\r\n";
			echo "progress=".$GLOBALS["status"]->Value."\r\n";
		}
		else if ( $_REQUEST['action'] == 'check_end' )// ???? ???? ??? ????
		{
			$dir = "/firmware/";
			$newfile = "upgrade.img";
			
			if( file_exists(($dir.$newfile)) ) 
			{
				echo ("0");
			}
			else
			{
				echo ("1");
			}
		}
		else if ( $_REQUEST['action'] == 'check' )// ???????????
		{
			$dir = "/firmware/";
			$newfile = "upgrade.img";
			
			$exec = exec('du -a /firmware/lighttpd-*');
			
			if( $exec ) {
				echo ("1");
			}else{
				if( file_exists(($dir.$newfile)) ) {
					if (!unlink($dir.$newfile))
					{
					   exec('rm -rf /firmware/upgrade.img');
					}
				}
				echo ("0");
			}
		}
		exit;
	}
	else if ( $_REQUEST['submenu'] == 'restart' )
	{
		if ( $_REQUEST['action'] == 'apply' )
		{
			if ( $_REQUEST['action'] == 'apply' )
			{
				$ipc_sock = new IPCSocket();
				$ipc_sock->Connection(NULL, CMD_SYSTEM_REBOOT);
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
		exit;
	}
	else if ( $_REQUEST['submenu'] == 'log' )
	{
		if ( $_REQUEST['action'] == 'view' )
		{
			echo '<meta http-equiv="Refresh" content="0; URL=setup_system_log.cgi">';
		}
		else if ( $_REQUEST['action'] == 'getlog' )
		{
			$shm_id = shmop_open(KEY_SM_LOG_LIST_SYS, "a", 0, 0);
			if (!$shm_id) exit;
			
			$data = shmop_read($shm_id, 0, 4);
			$log_list = unpack("i1count", $data);

			$time_stamp = 0;
			$total_page = 1;
			if ($log_list['count'] > 0)
			{
				$total_page = (int)($log_list['count']/17);
				if (($log_list['count']%17) != 0)
					$total_page++;
			}

			// time zone add
			// $tz = get_gmt_offset();

			$current_page = 1;
			if (isset($_REQUEST['page']))
			{
				if ($_REQUEST['page'] < 1) $current_page = 1;
				else if ($_REQUEST['page'] > $total_page) $current_page = $total_page;
				else $current_page = $_REQUEST['page'];
			}

			$index = $log_list['count'] - (($current_page - 1) * 17) -1;

			echo "@$current_page@$total_page@\r\n";

			for($i=0; $i<17; $i++)
			{
				if ($index < 0) break;

				$data = shmop_read($shm_id, 4 + ($index)*30, 30);
				$log_list[$i] = unpack("i1time/c1year/c1month/c1day/c1hour/c1min/c1sec/i1type/i1code/i1id/i1value/i1object", $data);
				$t_year = $log_list[$i]['year']+1900;
				$t_mon= $log_list[$i]['month']+1;
				echo '['.$t_year .'/'.$t_mon.'/'.$log_list[$i]['day'].' '.$log_list[$i]['hour'].':'.$log_list[$i]['min'].':'.$log_list[$i]['sec'].','.$log_list[$i]['type'].','.$log_list[$i]['code'].','.$log_list[$i]['id'].','.$log_list[$i]['value'].','.long2ip($log_list[$i]['object'])."]\r\n";
				//echo '['.date('Y/m/d H:i:s', $time_stamp).','.$log_list[$i]['type'].','.long2ip($log_list[$i]['ip']).','.$log_list[$i]['id']."]\r\n";
				$index --;
			}

			shmop_close($shm_id);

		}
		exit;
	}
}

//------------------------------------------------------------------------------------------------------
// 	Sdk
//------------------------------------------------------------------------------------------------------
header("Content-Type: text/plain");
ob_end_clean ();
if(isset($_REQUEST['msubmenu']))
{
	if ( $_REQUEST['msubmenu'] == 'users' )
	{
		if ( $_REQUEST['action'] == 'view' )
		{
			users_view_post();
		}
		else if ( $_REQUEST['action'] == 'count' )
		{
			users_count();
		}
		else if ( $_REQUEST['action'] == 'add' )
		{
			if ( user_add() == 0 )
			{
				show_post_ok();
			}
			else
			{
				show_post_ng();
			}
		}
		else if ( $_REQUEST['action'] == 'modify' )
		{
			if( !isset($_REQUEST['index']) )
			{
				show_post_ng();
			}
			else
			{
				$index = $_REQUEST['index'];
				if ( user_modify($index) == 0 )
				{
					show_post_ok();
				}	
				else
				{
					show_post_ng();
				}
			}
		}
		else if ( $_REQUEST['action'] == 'del' )
		{
			$index = $_REQUEST['index'];
			if (!isset($index))
			{
				show_post_ng();
			}
			else
			{
				if ( user_delete($index) == 0 )
				{
					show_post_ok();
				}
				else
				{
					show_post_ng();
				}
			}
		}
		else if ( $_REQUEST['action'] == 'logout' )
		{
			user_logout();
		}
		else if ( $_REQUEST['action'] == 'validate' ) // 3Xlogic 요청에 따른 cgi 추가
		{
			if (!isset($_REQUEST['id']) || !isset($_REQUEST['password']) ){	
				echo "invalid\r\n";
				exit;
			}
			if (!strlen($_REQUEST['id']) || !strlen($_REQUEST['password'])) {  
				echo "invalid\r\n";
				exit;
			}
			if ( user_validate($_REQUEST['id'],$_REQUEST['password']) == 0 )
			{
				echo "valid\r\n";
			}
			else
			{
				echo "invalid\r\n";
			}
		}
		else
			show_post_ng();

		exit;	
	}
	else if ( $_REQUEST['msubmenu'] == 'datetime' )
	{
		if ( $_REQUEST['action'] == 'view' )
		{
			datetime_view_post();
		}
		else if ( $_REQUEST['action'] == 'apply' )
		{
			if ( $_REQUEST['sync_type'] == 2 || $_REQUEST['sync_type'] == 1)  {
				if (!isset($_REQUEST['year']) || !isset($_REQUEST['mon']) || !isset($_REQUEST['day']) ||
					!isset($_REQUEST['hour']) || !isset($_REQUEST['min']) || !isset($_REQUEST['sec']) ) 
				{
					show_post_ng();
					return;
				}
				$_REQUEST['gmt'] = 12;
			}

			if (change_date() == 0 && change_date_date() == 0)
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
	else if ( $_REQUEST['msubmenu'] == 'time_format' ) {

		if ( $_REQUEST['action'] == 'view' ) {
			time_format_view();
			exit;
		}
		else if( $_REQUEST['action'] == 'apply' ) {
			if( change_time_format() == 0 ){
				$ipc_sock = new IPCSocket();
				$ipc_sock->Connection($GLOBALS['system_conf']->SystemDatetime, CMD_SET_TIME_FORMAT);
				if( $ipc_sock->dataInfo['ErrorCode']['value'] == APP_OK ){
					show_post_ok();
				}
				else {
					show_post_ng();
					echo 'error_code=' . $ipc_sock->dataInfo['ErrorCode']['value'];
				}
				exit;
			}
		}
	}
	else if ( $_REQUEST['msubmenu'] == 'timezone' )  // BY LAUDS : TIMEZONE SDK
	{
		if ( $_REQUEST['action'] == 'apply' )
		{
			if (change_timezone() == 0)	{
				$ipc_sock = new IPCSocket();
				$ipc_sock->Connection($GLOBALS['system_conf']->SystemDatetime, CMD_SET_DATETIME);
				if ($ipc_sock->dataInfo['ErrorCode']['value'] == APP_OK)
				{
					show_post_ok();
				}
				else
				{
					show_post_ng();
				}	
			} else {
				show_post_ng();
			}
		}
		else if ( $_REQUEST['action'] == 'view' )
		{
			timezone_view_post();
		}
		else
			show_post_ng();
		exit;
	}
	else if ( $_REQUEST['msubmenu'] == 'language' )  // by leo
	{
		if ( $_REQUEST['action'] == 'apply' )
		{
			if (change_timezone() == 0)	{
				$ipc_sock = new IPCSocket();
				$ipc_sock->Connection($GLOBALS['system_conf']->SystemDatetime, CMD_SET_LANGUAGE);
				if ($ipc_sock->dataInfo['ErrorCode']['value'] == APP_OK)
				{
					show_post_ok();
				}
				else
				{
					show_post_ng();
				}	
			} else {
				show_post_ng();
			}
		}
		else if ( $_REQUEST['action'] == 'view' )
		{
			view_language();
		}
		else
			show_post_ng();
		exit;
	}	
	else if ( $_REQUEST['msubmenu'] == 'device_info' )  // by leo
	{
		if ( $_REQUEST['action'] == 'view' )
		{
			echo $GLOBALS['system_caps']->getCapability(false);
		}		
		else if ( $_REQUEST['action'] == 'apply' )
		{
			if (change_system_device() == 0 )	{
				$ipc_sock = new IPCSocket();
				$ipc_sock->Connection($GLOBALS['system_conf']->DeviceInfo, CMD_SET_DEVICE_INFORMATION);
				if ($ipc_sock->dataInfo['ErrorCode']['value'] == APP_OK)
				{
					show_post_ok();
				}
				else
				{
					show_post_ng();
				}	
			} else {
				show_post_ng();
			}
		}
		else
			show_post_ng();
		exit;
	}
	else if ( $_REQUEST['msubmenu'] == 'config' )
	{
		if ( $_REQUEST['action'] == 'encrypt' )
		{
			encrypt_config();
		}
		else if ( $_REQUEST['action'] == 'download')
		{
			download_config();

			$ipc_sock = new IPCSocket();
			$ipc_sock->Connection(NULL, CMD_SYSTEM_DOWNLOAD_CONFIG);
			if ($ipc_sock->dataInfo['ErrorCode']['value'] == APP_OK)
			{
				return 0;
			}
			else
			{
				return -1;
			}  
		}
		else if ( $_REQUEST['action'] == 'upload' )
		{
			$config = upload_config();
			if($config == 0)
			{
				$ipc_sock = new IPCSocket();
				$ipc_sock->Connection(NULL, CMD_SYSTEM_UPLOAD_CONFIG);
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
			{
				if($config == -2)
				{
					echo 'Please enter correct password';
				}
				else if($config == -3)
				{
					echo 'Camera information does not match';
				}
				else if($config == -4)
				{
					echo 'Firmware version does not match';
				}
				else if($config == -5)
				{
					echo 'File Decrypt fail';
				}
				else
				{
					show_post_ng();
				}

			}

		}
		else
		{
			show_post_ng();
		}
		exit();
	}
	else if ( $_REQUEST['msubmenu'] == 'reset' )
	{
		if ( $_REQUEST['action'] == 'defaultset' )
		{
			$factorySet = new CFactoryDefault();
			if ( $_REQUEST['option'] == 0 )	//all reset
			{
				$factorySet->Type = 0;
				$ipc_sock = new IPCSocket();
				$ipc_sock->Connection($factorySet, CMD_SET_SYSTEM_FACTORY_DEFAULT);
				if ($ipc_sock->dataInfo['ErrorCode']['value'] == APP_OK)
				{
					show_post_ok();
					echo ("System will restart!");	
				}
				else
				{
					show_post_ng();
				}	
			}
			else if ( $_REQUEST['option'] == 1 ) //except network setting
			{
				$factorySet->Type = 1;
				$ipc_sock = new IPCSocket();
				$ipc_sock->Connection($factorySet, CMD_SET_SYSTEM_FACTORY_DEFAULT);
				if ($ipc_sock->dataInfo['ErrorCode']['value'] == APP_OK)
				{
					show_post_ok();
					echo ("System will restart!");	
				}
				else
				{
					show_post_ng();
				}	
			}
			else
				show_post_ng();
		}
		else if ( $_REQUEST['action'] == 'reboot' )
		{
			$ipc_sock = new IPCSocket();
			$ipc_sock->Connection(NULL, CMD_SYSTEM_REBOOT);
			if ($ipc_sock->dataInfo['ErrorCode']['value'] == APP_OK)
			{
				show_post_ok();
			}
			else
			{
				show_post_ng();
			}	
		}
		else if ( $_REQUEST['action'] == 'slave_reboot' )
		{
			exec("/root/slave_reset.sh > /dev/null &");
		}
		else if ( $_REQUEST['action'] == 'view' )
		{
			reset_status_view_post();
		}
		else
			show_post_ng();
		exit;
	}
	else if ( $_REQUEST['msubmenu'] == 'onvif' )
	{
		if ( $_REQUEST['action'] == 'apply' )
		{
	    	if(isset($_REQUEST['onvif_discovery']))
	    	{
		        if($_REQUEST['onvif_discovery']<0 || $_REQUEST['onvif_discovery']>1) return -1;
		        $GLOBALS['system_conf']->DeviceInfo->OnvifConf->discovery_mode = $_REQUEST['onvif_discovery']; 				  
		    	}
		    	if(isset($_REQUEST['onvif_auth']))
		    	{
		    	  if($_REQUEST['onvif_auth']<0 || $_REQUEST['onvif_auth']>2) return -1;
		    		$GLOBALS['system_conf']->DeviceInfo->OnvifConf->auth_mode =  $_REQUEST['onvif_auth'];	
		    	}		
			
				$ipc_sock = new IPCSocket();
				$ipc_sock->Connection($GLOBALS['system_conf']->DeviceInfo, CMD_SET_DEVICE_INFORMATION);
				if ($ipc_sock->dataInfo['ErrorCode']['value'] == APP_OK)
				{
					show_post_ok();	
				}
				else
				{
					show_post_ng();
				}
		}	
		else if ( $_REQUEST['action'] == 'view' )
		{
				echo "discovery_mode="	. 	 $GLOBALS['system_conf']->DeviceInfo->OnvifConf->discovery_mode. "\r\n";
				echo "auth_mode="	. 	 $GLOBALS['system_conf']->DeviceInfo->OnvifConf->auth_mode. "\r\n";
				
				
		}
		else
			show_post_ng();
		exit;			
	}	
	else if ( $_REQUEST['msubmenu'] == 'log' )
	{
		if ( $_REQUEST['action'] == 'view' )
		{
			echo '<meta http-equiv="Refresh" content="0; URL=setup_system_log.cgi">';
		}
		else if ( $_REQUEST['action'] == 'getlog' )
		{
			get_system_log($json=true);
		}
		else if ( $_REQUEST['action'] == 'backup' )
		{
			backup_log();
		}
		exit;
	}
	else if ( $_REQUEST['msubmenu'] == 'recovery_mode' )
	{

		if ( $_REQUEST['action'] == 'clear' )
		{
			$ipc_sock = new IPCSocket();
			$ipc_sock->Connection(NULL, CMD_CLEAR_RECOVERY_MODE);
			if ($ipc_sock->dataInfo['ErrorCode']['value'] == APP_OK) {
				show_post_ok();
			}
			else {
				show_post_ng();
			}
		}
		else {
			show_post_ng();
		}
		exit;
	} 
	else if ( $_REQUEST['msubmenu'] == 'led' )  // by sykim
	{
		if ( $_REQUEST['action'] == 'apply' )
		{
			if(!isset($_REQUEST['option']))
			{
				show_post_ng();
			}
			else
			{
				$systemledset = new CSystemLED();
				$systemledset->Type = $_REQUEST['option']; 
				$ipc_sock = new IPCSocket();
				$ipc_sock->Connection($systemledset, CMD_SET_LED_CONTROL);
				if ($ipc_sock->dataInfo['ErrorCode']['value'] == APP_OK)
				{
					show_post_ok();
				//	echo "led_control_option changed";
				}
				else
				{
					show_post_ng();
				}	
			}
		}
		else if ( $_REQUEST['action'] == 'view' )
		{
			echo "led_control=";
		}
		else
			show_post_ng();
		exit;
	}	
}
show_post_ng();
?>
