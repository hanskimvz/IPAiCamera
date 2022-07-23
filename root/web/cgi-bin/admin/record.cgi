<?
require('../_define.inc');
require('../class/socket.class');
require('../class/record.class');
require('../class/event.class');
require('../class/capability.class');

$shm_id = shmop_open(KEY_SM_SHARED_CONFIG, "a", 0, 0);
$record_conf = new CRecordConfiguration($shm_id);
$system_caps = new CCapability($shm_id);
$event_conf  = new CEventConfiguration($shm_id);
$get_oem = $system_caps->getOEM();

function record_list_get_json($option)
{
	/* PITS 0002038: [LM55] SD Card 제거 및 Unmount 후에도 Record List 출력됨. */
	date_default_timezone_set('UTC');		
	/* ------------------------------------------ */
	if( isset($_REQUEST['storage_index']) )
	{
		$index = $_REQUEST['storage_index'];
		$filepath = $GLOBALS['event_conf']->StorageDevices->Device[$index]->Extension->MountDirectory . "/index.db";
	}
	else
	{
		$filepath = "/sdcard/index.db";
		exec("df|grep mmcblk", $data, $retval);
		$mounted = $retval == 0 ? 1 : 0;
	}
	if( file_exists($filepath) == false || (isset($mounted) && $mounted == 0 )) {
		echo "[ ]";
		return ;
	}

	$fd = fopen($filepath, "r", true);
	while( false == flock($fd, LOCK_EX)){
		usleep(10000);
	}
	echo "[";
	while( !feof($fd) ) {
	  if(PHP_INT_MAX == 2147483647) // 32 bit
	  {
		$buffer = fread($fd, 23);
		}
		else // 64 bit
		{
		$buffer = fread($fd, 27);
		}
		if( $buffer != false ) {
			$data = "";
			if(PHP_INT_MAX == 2147483647) // 32 bit
			{
			  $data = unpack("I1key_l/I1key_h/I1start/I1event/I1duration/C1storage/C1protect/C1flag",$buffer); // check leo
			}
			else  // 64 bit
			{
			  $data = unpack("I1key_l/I1key_h/I1start/I1start_lower/I1event/I1duration/C1storage/C1protect/C1flag",$buffer);		  
			}
			$event = $data['event'];
			$data['event'] = "";

			//if( !($data['flag'] & 0x2 ) )
			//	continue;
			if( $data['flag'] != 3)  // 7 : error, 1 : recording
				continue;
			
			if($event == EVENT_MASK_CONTINOUS){
				$data['event'] .= "setup_continous";
			} else {
				if($event & EVENT_MASK_MOTION){
					$data['event'] .= "ON_EVENT_MOTION";
				} 
				else if($event & EVENT_MASK_SCHEDULE){
					$data['event'] .= "ON_EVENT_SCHEDULER";
				} 
				else if($event & EVENT_MASK_RELAY ){
					$data['event'] .= "ON_EVENT_RELAY";
				} 
				else if($event & EVENT_MASK_SENSOR_ALARM ){
					$data['event'] .= "ON_EVENT_SENSOR_ALARM";
				} 
				else if($event & EVENT_MASK_NETWORKDISCONNECTED){
					$data['event'] .= "ON_EVENT_NETWORK_DISCONNECTED";
				}
				else if($event & EVENT_MASK_SD_FULL ){
					$data['event'] .= "ON_EVENT_SD_FULL";
				}
				else if($event & EVENT_MASK_SD_FAILURE ){
					$data['event'] .= "ON_EVENT_SD_FAILURE";
				}
				else if($event & EVENT_MASK_IP_ADDR_CONFLICTED ){
					$data['event'] .= "ON_EVENT_IP_ADDR_CONFLICTED";
				}
				else if($event & EVENT_MASK_TEMPERATURE_CRITICAL ){
					$data['event'] .= "ON_EVENT_TEMPERATURE_CRITICAL";
				}
				else if($event & EVENT_MASK_ILLEGAL_LOGIN ){
					$data['event'] .= "ON_EVENT_ILLEGAL_LOGIN";
				}				
				//hdseo for thermal
				else if($event & EVENT_MASK_TEMPERATURE_DETECTED ){
					$data['event'] .= "ON_EVENT_TEMPERATURE_DETECTED";
				}	
				//hdseo for iNode
				else if($event & EVENT_MASK_CUSTOM_SNAP ){
					$data['event'] .= "ON_EVENT_CUSTOM_SNAP";
				}				
				else if($event & EVENT_MASK_PIR_DETECTED ){
					$data['event'] .= "ON_EVENT_PIR_DETECTED";
				}				
				else if($event & EVENT_MASK_SYS_INIT ){
					$data['event'] .= "ON_EVENT_SYS_INIT";
				}				
				// UDP Tech for VCA user event
				else				
				{
					$tempMask = EVENT_MASK_USER_EVENT1;
					for($i = 0; $i < 16; $i++)
					{
						if($event & $tempMask)
						{
							$data['event'] .= ON_EVENT_USER_EVENT1 + $i;
							break;
						}
						$tempMask = $tempMask << 1;
					}
				}
			}
			if( strlen($data['event']) == 0 )
				$data['event'] = "Unknown";
			if( $data['storage'] == 1) {
				$data['storage'] = "SDCARD";
			} else {
				$data['storage'] = "Unknown";
			}
			if( $option == 0 ){
				echo json_encode($data). ",\r\n";
			}
			else{
				$data['start'] = strftime( "%Y-%m-%d %H:%M:%S",$data['start']);
				echo json_encode($data). ",\r\n";		
			}    
		}
	}
	echo "]";
	while( false == flock($fd, LOCK_UN)){
		usleep(10000);
	}
	fclose($fd);
}

function change_record_enabled($index)
{
	if( !isset($_REQUEST['enabled'])) return 1;
	$GLOBALS['record_conf']->job_conf[$index]->enabled = $_REQUEST['enabled'];
	return 0;
}

function change_record_storage($index)
{
	if( !isset($_REQUEST['storage_type']) ) return 1;
	$GLOBALS['record_conf']->job_conf[$index]->storage_type = $_REQUEST['storage_type'];
	return 0;
}

function change_record_file_type($index)
{
	if(!isset($_REQUEST['file_type'])) return 1;
	$GLOBALS['record_conf']->job_conf[$index]->file_type = $_REQUEST['file_type'];
	return 0;
}

function change_record_continous($index)
{
	if( !isset($_REQUEST['continous']) ) return 1;
	$GLOBALS['record_conf']->job_conf[$index]->continous= $_REQUEST['continous'];
	return 0;
}

function change_record_pre($index)
{
	if( !isset($_REQUEST['pre_duration']) ) return 1;
	$GLOBALS['record_conf']->job_conf[$index]->pre_duration = $_REQUEST['pre_duration'];
	return 0;
}

function change_record_post($index)
{
	if( !isset($_REQUEST['post_duration']) ) return 1;
	$GLOBALS['record_conf']->job_conf[$index]->post_duration= $_REQUEST['post_duration'];
	return 0;
}
function change_record_storage_device($index)
{
	if( !isset($_REQUEST['storage_device']) ) return 1;
	$GLOBALS['record_conf']->job_conf[$index]->storage_device 
		= $_REQUEST['storage_device'];
	return 0;
}
function change_record()
{
	if( !isset($_REQUEST['index'] ) || ($_REQUEST['index']< 0 ||
		$_REQUEST['index'] > $GLOBALS['system_caps']->max_record) ){
		return 1;
	}
	$index = $_REQUEST['index'];

	
	$changed = 0;
	$changed += change_record_enabled($index);
	$changed += change_record_storage($index);
	$changed += change_record_file_type($index);
	$changed += change_record_continous($index);
	$changed += change_record_pre($index);
	$changed += change_record_post($index);
	$changed += change_record_storage_device($index);

	if( $changed == 7 ) return 1;
	
	$ipc_sock = new IPCSocket();
	$ipc_sock->Connection($GLOBALS['record_conf'], CMD_SET_RECORDING_JOB);
	if( $ipc_sock->dataInfo['ErrorCode']['value'] != APP_OK )
	{
		return 1;
	}	
	return 0;	
}
function download_record($path)
{
	if(file_exists($path)) {
		header('Content-Description: File Transfer');
		header('Content-Type:  multipart/form-data');
		header('Content-Disposition: attachment; filename="'.basename($path).'"');
		header('Content-Length: ' . filesize($path));
		readfile($path);
		exit;
	}   
}

//------------------------------------------------------------------------------------------------------
// 	Sdk
//------------------------------------------------------------------------------------------------------
header("Content-Type: text/plain");
ob_end_clean ();
if ( $_REQUEST['msubmenu'] == 'manage')
{
	if( isset($_REQUEST['action']) )
	{
		if( $_REQUEST['action'] == 'view')
			show_record_management($GLOBALS['record_conf']);
		else if( $_REQUEST['action'] == 'apply')
		{
			if( change_record() == 0 )
				show_post_ok();
			else
				show_post_ng();
		}
		else if( $_REQUEST['action'] == 'get')
			show_record_management($GLOBALS['record_conf'], true);
		else
			show_post_ng();
	}
	if( isset($_REQUEST['target_stream']) ) {
		$ipc_sock = new IPCSocket();
		$GLOBALS['record_conf']->target_stream->value = $_REQUEST['target_stream'];
		$ipc_sock->Connection($GLOBALS['record_conf']->target_stream, CMD_SET_RECORDING_CHANNEL);
		if( $ipc_sock->dataInfo['ErrorCode']['value'] != APP_OK ) {
			show_post_ng();
		} else {
			show_post_ok();
		}
		exit;
	}
	exit;
}
else if ($_REQUEST['msubmenu'] == 'list' )
{
	if( $_REQUEST['action'] == 'get')
	{
		record_list_get_json(0);
	}
	else if (  $_REQUEST['action'] == 'view')
	{
		record_list_get_json(1);
	}
	exit;
}
else if ($_REQUEST['msubmenu'] == 'export' )
{
	if( isset($_REQUEST['file']) && isset($_REQUEST['reason']) || isset($_REQUEST['key']) || isset($_REQUEST['path'] )) 
	{
	  if(strlen($_REQUEST['file']) > 255 || strlen($_REQUEST['reason']) > 32)
	  {
	  	show_post_ng();
	  	exit;
	  }
	  $exportFile = new CExportRecordFileRequest(); 
	  $exportFile->FileName = $_REQUEST['file'];
	  $exportFile->Reason = $_REQUEST['reason'];
		if( $GLOBALS['get_oem'] == 19){
			  $exportFile->Key = $_REQUEST['key'];
			  $exportFile->Path = $_REQUEST['path'];
		}
		$ipc_sock = new IPCSocket();
		$ipc_sock->Connection($exportFile, CMD_EXPORT_RECORDFILE);


		if( $ipc_sock->dataInfo['ErrorCode']['value'] != APP_OK ) {
			show_post_ng();
		} else {
			show_post_ok();
		}
		exit;
	}
	else
	{
		show_post_ng();
	}
	exit;
}
else if ($_REQUEST['msubmenu'] == 'download' )
{
	if(isset($_REQUEST['path'])){
		download_record($_REQUEST['path']);
	}
	else
	{
		show_post_ng();
	}
	exit;
}
show_post_ng();
?>
