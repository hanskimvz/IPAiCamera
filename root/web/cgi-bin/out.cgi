<?
require('_define.inc');
require('./class/socket.class');

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

header("Content-Type: text/plain");
ob_end_clean ();
if(isset($_REQUEST['msubmenu']))
{
	if ( $_REQUEST['msubmenu'] == 'users' )
	{
		if ( $_REQUEST['action'] == 'logout' )
		{
			user_logout();
		}
		else
			show_post_ng();

		exit;
	}
}
show_post_ng();

?>
