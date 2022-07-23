<?
ini_set('memory_limit', '1M');
require("./_define.inc");
require("./_upgrade.inc");
require("./class/system.class");
require("./class/socket.class");

$status = new CUploadStatus();

header("Content-Type: text/plain");
ob_end_clean();
if(isset($_REQUEST['cmd']))
{
	if( $_REQUEST['cmd'] == "progress")
	{
		$ipc_sock = new IPCSocket(UPGRADE_SOCKET_PATH);
		$ipc_sock->Connection($GLOBALS["status"], M_FTP_UPGRADE_STATUS);
		printf("%d/%d\r\n", $GLOBALS["status"]->Status,
			$GLOBALS["status"]->Value);
		exit;
	}
}
echo "NG";
?>
