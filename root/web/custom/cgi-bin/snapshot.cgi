<?
require('../../cgi-bin/_define.inc');
require('../../cgi-bin/class/socket.class');

function customsnap_event()
{
	$ipc_sock = new IPCSocket();
	$ipc_sock->Connection(NULL, CMD_CUSTOM_SNAP);
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
if(isset($_REQUEST['action']))
{
	if ( $_REQUEST['action'] == 'customsnap' )
	{
		if ( customsnap_event() == 0 )
		{
			show_post_ok();
		}
		else
		{
			show_post_ng();
		}	
		exit;
	}
	else
		show_post_ng();
}

?>