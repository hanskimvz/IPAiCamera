<?
require('../_define.inc');
require('../class/media.class');
require('../class/capability.class');
require('../class/socket.class');
require('../class/system.class');

$shm_id      = shmop_open(KEY_SM_SHARED_CONFIG, "a", 0, 0);
$system_caps = new CCapability($shm_id);
$media_conf  = new CMediaConfiguration($shm_id);
$system_conf = new CSystemConfiguration($shm_id);
shmop_close($shm_id);

$fish_conf = $media_conf->ProfileConfig->VideoSourceConfiguration->Extension->FishEyeConf;

function cali_center_view_post()
{
	echo "finded="      . $GLOBALS['fish_conf']->CaliCenter->finded . "\r\n";
	echo "pos_x="       . $GLOBALS['fish_conf']->CaliCenter->pos_x  . "\r\n";
	echo "pos_y="       . $GLOBALS['fish_conf']->CaliCenter->pos_y  . "\r\n";
	echo "radius="      . $GLOBALS['fish_conf']->CaliCenter->radius . "\r\n";
	return 0;
}
function fisheye_view_post()
{
	echo "mount_type="  . $GLOBALS['fish_conf']->MountType          . "\r\n";
	echo "source_type=" . $GLOBALS['fish_conf']->SourceType         . "\r\n";
	return 0;
}

function change_fisheye_mount_type(){
	if(!isset($_REQUEST['mount_type'])) return 1;
	$GLOBALS['fish_conf']->MountType = $_REQUEST['mount_type'];	
	return 0;
}
function change_fisheye_source_type(){
	if(!isset($_REQUEST['source_type'])) return 1;
	$GLOBALS['fish_conf']->SourceType = $_REQUEST['source_type'];	
	return 0;
}
function change_fisheye(){
	if( change_fisheye_mount_type() < 0 ) return -1;
	if( change_fisheye_source_type() < 0 ) return -1;
	return 0;
}
function set_cali_center(){
	$GLOBALS["system_conf"]->DeviceInfo->FisheyeInputOffset->x = $GLOBALS['media_conf']->ProfileConfig->VideoSourceConfigurations->Config[0]->Extension->FishEyeConf->CaliCenter->pos_x;
	$data = $GLOBALS['system_conf']->DeviceInfo->FisheyeInputOffset;
	$ipc_sock = new IPCSocket();
	$ipc_sock->Connection($data, CMD_SET_FISHEYE_BUFFER_OFFSET);
	if ( $ipc_sock->dataInfo['ErrorCode']['value'] != APP_OK) {
		show_post_ng();
	}
	return 0;
}

header("Content-Type: text/plain");
ob_end_clean ();
if ( $_REQUEST['msubmenu'] == 'cali_center')
{
	if( isset($_REQUEST['action']) )
	{
		if( $_REQUEST['action'] == 'view'){
			if( cali_center_view_post() != 0)
				show_post_ng();
		} else if( $_REQUEST['action'] == 'run') {
			$ipc_sock = new IPCSocket();
			$ipc_sock->Connection(NULL, CMD_SET_FISH_CENTER);
			if( $ipc_sock->dataInfo['ErrorCode']['value'] != APP_OK )
				show_post_ng();
			else
				show_post_ok();
			exit;
		} else if( $_REQUEST['action'] == 'default') {
			//todo
		} else if( $_REQUEST['action'] == 'set') {               // set fisheye center
			$ipc_sock = new IPCSocket();
			$ipc_sock->Connection($GLOBALS['fish_conf'], CMD_SET_FISH_CENTER);
			if( $ipc_sock->dataInfo['ErrorCode']['value'] != APP_OK )
				show_post_ng();
			else{
				show_post_ok();
			}
			exit;
		} else if( $_REQUEST['action'] == 'get') {               // get fisheye centerpos
			$ipc_sock = new IPCSocket();
			$ipc_sock->Connection($GLOBALS['fish_conf'], CMD_GET_FISHEYE_CONFIG);
			if( $ipc_sock->dataInfo['ErrorCode']['value'] != APP_OK ){
//				show_post_ng();
			}else{
//				show_post_ok();
				$GLOBALS['media_conf']->getFisheyeInformation(NULL, 1);
			}
			exit;
		} else if( $_REQUEST['action'] == 'default') {
			//todo
		} else if( $_REQUEST['action'] == 'apply') {
			$ipc_sock = new IPCSocket();
			$ipc_sock->Connection($GLOBALS['fish_conf'], CMD_SET_FISH_CENTER);
			if( $ipc_sock->dataInfo['ErrorCode']['value'] != APP_OK )
				show_post_ng();
			else{
				if(set_cali_center() == 0){
					show_post_ok();
				}
			}
		}		
	}
	exit;
}
else if( $_REQUEST['msubmenu'] == 'fisheye')
{
	if( isset($_REQUEST['action']) )
	{
		if( $_REQUEST['action'] == 'view'){
			if( fisheye_view_post != 0){
				show_post_ng();
			}
		}
		else if( $_REQUEST['action'] == 'apply')
		{
			if( change_fisheye() == 0) {
				$ipc_sock = new IPCSocket();
				$ipc_sock->Connection($GLOBALS['fish_conf'], CMD_SET_FISHEYE_CONFIG);
				if( $ipc_sock->dataInfo['ErrorCode']['value'] != APP_OK ){
					show_post_ng();
					echo "ErrorCode=" . $ipc_sock->dataInfo['ErrorCode']['value']."\r\n";
				} else {
					show_post_ok();
				}
			} else { 
				show_post_ng();
				exit;
			}
		}
	}
	exit;
}
?>
