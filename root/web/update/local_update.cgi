<?
require("../cgi-bin/_define.inc");
require("../cgi-bin/_upgrade.inc");
require("../cgi-bin/class/system.class");
require("../cgi-bin/class/socket.class");

$status = new CUploadStatus();

//------------------------------------------------------------------------------------------------------
// 	Html
//------------------------------------------------------------------------------------------------------
header("Content-Type: text/plain");
ob_end_clean();
if($_SERVER['REMOTE_ADDR'] == '127.0.0.1' || $_SERVER['REMOTE_ADDR'] == $_SERVER['SERVER_ADDR'])
{
	if(isset($_REQUEST['submenu']))
	{
		if ( $_REQUEST['submenu'] == 'upgrade' )
		{
			if ( $_REQUEST['action'] == 'start' )
			{
				$dir = "/firmware/";
				$newfile = "upgrade.img";
				if( file_exists(($dir.$newfile)) ) 
				{
					$uploadRequest = new CUploadRequest();
					$ipc_sock = new IPCSocket();
					$ipc_sock->Connection($uploadRequest, CMD_SYSTEM_UPDATE_READY);

					if ($ipc_sock->dataInfo['ErrorCode']['value'] == APP_OK)
					{
						$ipc_sock = new IPCSocket(UPGRADE_SOCKET_PATH);
						$ipc_sock->Connection($GLOBALS["status"],M_UPGRADE_START_KBM);
						if($GLOBALS["status"]->Status != 1)
						{
							http_response_code(406);
						}
						show_post_ok();
					}
					else
					{
					http_response_code(406);
					} 
				}
				else
				{
					http_response_code(406);
				}
			}
			exit;
		}
	}
}
else
{
	header("HTTP/1.0 406 Not Acceptable");
}

//------------------------------------------------------------------------------------------------------
// 	Sdk
//------------------------------------------------------------------------------------------------------
header("Content-Type: text/plain");

?>
