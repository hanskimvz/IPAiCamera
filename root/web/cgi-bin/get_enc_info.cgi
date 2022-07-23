<?
require('./_define.inc');
require('./class/system.class');
require('./class/socket.class');
$shm_id = shmop_open(KEY_SM_SHARED_CONFIG, "a", 0, 0);
$system_conf = new CSystemConfiguration($shm_id);
shmop_close($shm_id);

header("Content-Type: text/plain");
ob_end_clean ();
if(isset($_REQUEST['action'])) {
	if ( $_REQUEST['action'] == 'view' ) {
		echo "enc_ver=" . $GLOBALS['system_conf']->Security->SystemService->EncodeVersion. "\n";
		exit;
	} else if ( $_REQUEST['action'] == 'apply' ) {
		if( isset($_REQUEST['enc_ver']) ){
			$GLOBALS['system_conf']->Security->SystemService->EncodeVersion = $_REQUEST['enc_ver'];
	
			$ipc_sock = new IPCSocket();
			$ipc_sock->Connection($GLOBALS['system_conf']->Security->SystemService, CMD_SET_SECURITY_SERVICE);
			if ($ipc_sock->dataInfo['ErrorCode']['value'] == APP_OK ) {
				echo "OK";
			} else {
				echo "NG";
			}
			exit;
		}
	}
}
show_post_ng();
?>
