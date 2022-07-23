<?
require("../_define.inc");
require("../_upgrade.inc");
require("../class/system.class");
require("../class/socket.class");

$system_conf = new CSystemConfiguration();
$status = new CUploadStatus();

function ftp_upgrade_view_post()
{
	show_ftp($GLOBALS['system_conf']->FtpUpgrade, false);
}

function change_ftp_upgrade_server() 
{
	if( !isset($_REQUEST["address"]) ) return 1;
	$GLOBALS['system_conf']->FtpUpgrade->Server = $_REQUEST['address'];
	return 0;
}
function change_ftp_upgrade_directory() 
{
	if( !isset($_REQUEST["location"]) ) return 1;
	$GLOBALS['system_conf']->FtpUpgrade->Directory= $_REQUEST['location'];
	return 0;
}
function change_ftp_upgrade_port() 
{
	if( !isset($_REQUEST["port"]) ) return 1;
	$GLOBALS['system_conf']->FtpUpgrade->Port= $_REQUEST['port'];
	return 0;
}
function change_ftp_upgrade_username() 
{
	if( !isset($_REQUEST["id"]) ) return 1;
	$GLOBALS['system_conf']->FtpUpgrade->Username= $_REQUEST['id'];
	return 0;
}
function change_ftp_upgrade_password() 
{
	if( !isset($_REQUEST["password"]) ) return 1;
	$GLOBALS['system_conf']->FtpUpgrade->Password= $_REQUEST['password'];
	return 0;
}
function change_ftp_upgrade_autoupdate() 
{
	if( !isset($_REQUEST["autoupdate"]) ) return 1;
	$GLOBALS['system_conf']->FtpUpgrade->AutoUpdate= $_REQUEST['autoupdate'];
	return 0;
}
function change_ftp_upgrade_interval() 
{
	if( !isset($_REQUEST["interval"]) ) return 1;
	$GLOBALS['system_conf']->FtpUpgrade->Interval= $_REQUEST['interval'];
	return 0;
}
function change_ftp_upgrade() 
{
	if( change_ftp_upgrade_server()    < 0 ) return -1;
	if( change_ftp_upgrade_directory() < 0 ) return -1;
	if( change_ftp_upgrade_port()      < 0 ) return -1;
	if( change_ftp_upgrade_username()  < 0 ) return -1;
	if( change_ftp_upgrade_password()  < 0 ) return -1;
	if( change_ftp_upgrade_autoupdate()  < 0 ) return -1;
	if( change_ftp_upgrade_interval()  < 0 ) return -1;
	return 0;
}

header("Content-Type: text/plain");
ob_end_clean();
if(isset($_REQUEST['msubmenu']))
{
	if ($_REQUEST['msubmenu'] == 'ftp' ) 
	{
		if($_REQUEST['action'] == 'view') 
		{
			ftp_upgrade_view_post();
		}
		elseif( $_REQUEST['action'] == 'apply') // save ftp server information
		{ 
			if( change_ftp_upgrade() == 0 )
			{
				$ipc_sock = new IPCSocket();
				$ipc_sock->Connection($GLOBALS['system_conf']->FtpUpgrade, CMD_SET_FTP_UPGRADE);
				if ($ipc_sock->dataInfo['ErrorCode']['value'] == APP_OK)
				{
					show_post_ok();
					exit;
				}
			}
			show_post_ok();
		}
		elseif( $_REQUEST['action'] == 'upgrade') // start get new firmware
		{
			$ipc_sock = new IPCSocket(UPGRADE_SOCKET_PATH);
			$ipc_sock->Connection($GLOBALS["status"], M_FTP_UPGRADE_DOWNLOAD_START);
			if ($ipc_sock->dataInfo['ErrorCode']['value'] == APP_OK)
			{
				printf("%d/%d\r\n", $GLOBALS["status"]->Status, $GLOBALS["status"]->Value);
			}
			else
			{
				show_post_ng();
			}
		}
		elseif( $_REQUEST['action'] == 'status')
		{
			;
		}
		else if($_REQUEST['action'] == 'check') // progress & status 
		{
			$ipc_sock = new IPCSocket(UPGRADE_SOCKET_PATH);
			$ipc_sock->Connection($GLOBALS["status"], M_FTP_UPGRADE_FIRMWARE_CHECK);
			printf("%d/%d\r\n", $GLOBALS["status"]->Status, $GLOBALS["status"]->Value);
		}
		exit;
	}
}
show_post_ng();
?>
