<?
ini_set('memory_limit', '1M');
require("../_define.inc");
require("../_upgrade.inc");
require("../class/system.class");
require("../class/socket.class");

$status = new CUploadStatus();

//------------------------------------------------------------------------------------------------------
// 	Html
//------------------------------------------------------------------------------------------------------
header("Content-Type: text/plain");
ob_end_clean();
if(isset($_REQUEST['submenu']))
{
	if ( $_REQUEST['submenu'] == 'upgrade' )
	{
		if ( $_REQUEST['action'] == 'status' )
		{
			$ipc_sock = new IPCSocket(UPGRADE_SOCKET_PATH);
			$ipc_sock->Connection($GLOBALS["status"], M_UPGRADE_STATUS);
			echo "status=".$GLOBALS["status"]->Status."\r\n";
			echo "progress=".$GLOBALS["status"]->Value."\r\n";
		}
		else if ( $_REQUEST['action'] == 'check_end' )// 파일 저장 완료 상태
		{
			$dir = "/firmware/";
			$newfile = "upgrade.img";
			$newfile_ver2 = "lnx.img";
			
			if( file_exists(($dir.$newfile)) || file_exists(($dir.$newfile_ver2)) )
			{
				echo ("0");
			}
			else
			{
				echo ("1");
			}
		}
		else if ( $_REQUEST['action'] == 'check' )// 딴넘이 하는지
		{
			$dir = "/firmware/";
			$newfile = "upgrade.img";
			
			$exec = exec('du -a /tmp/lighttpd-*');
		
			$ipc_sock = new IPCSocket(UPGRADE_SOCKET_PATH);
			$ipc_sock->Connection($GLOBALS["status"], M_FTP_UPGRADE_STATUS);
			if( $exec || $GLOBALS["status"]->Status == 2)
			{
				echo ("1");
			}
			else
			{
				if( file_exists(($dir.$newfile)) )
				{
					if (!unlink($dir.$newfile))
					{
					   exec('rm -rf /firmware/upgrade.img');
					}
				}
				echo ("0");
			}
		}
		else if ( $_REQUEST['action'] == 'slave_reboot' )
		{
			exec("/root/slave_reset.sh > /dev/null &");
		}
		exit;
	}
}

//------------------------------------------------------------------------------------------------------
// 	Sdk
//------------------------------------------------------------------------------------------------------
header("Content-Type: text/plain");

?>
