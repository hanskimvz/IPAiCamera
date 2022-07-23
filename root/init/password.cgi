<?
require('./_define.inc');
require('./class/system.class');
require('./class/socket.class');
$system_conf = new CSystemConfiguration($shm_id);

function user_change_pass($index)
{
	$strongRegex = '/^(?=.{12,})(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])(?=.*[\W_]).*$/';
	$goodRegex = '/^(?=.{8,})(((?=.*[A-Z])(?=.*[a-z])(?=.*[\W_]))|((?=.*[A-Z])(?=.*[0-9])(?=.*[\W_]))|((?=.*[a-z])(?=.*[0-9])(?=.*[\W_]))|((?=.*[A-Z])(?=.*[a-z])(?=.*[0-9]))).*$/';
	$weakRegex   = '/^(?=.{8,})(((?=.*[A-Z])(?=.*[a-z]))|((?=.*[A-Z])(?=.*[0-9]))|((?=.*[a-z])(?=.*[0-9]))|((?=.*[A-Z])(?=.*[\W_]))|((?=.*[a-z])(?=.*[\W_]))|((?=.*[0-9])(?=.*[\W_]))).*$/';

	if (!isset($_REQUEST['pass'])) return 1;
	  if (strlen($_REQUEST['pass']) < 8) return -1;
	if (strlen($_REQUEST['pass']) > 30) return -1;

	if(preg_match($strongRegex, $_REQUEST['pass'])){
		;
	}
	else if(preg_match($goodRegex, $_REQUEST['pass'])){
		;
	}
	else {
		//       return -1;
	}
	$GLOBALS['system_conf']->Users->User[$index]->Password = $_REQUEST['pass'];
	return 0;
}
function user_modify($index)
{
//	if (user_change_name($index) < 0)   return -1;
//	if (user_change_auth($index) < 0)   return -1;
	if (user_change_pass($index) < 0)   return -1;

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
header("Content-Type: text/plain");
ob_end_clean ();
if(isset($_REQUEST['msubmenu']))
{
	if ( $_REQUEST['msubmenu'] == 'users' )
	{
		if ( $_REQUEST['action'] == 'modify' )
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

	}
}
?>
