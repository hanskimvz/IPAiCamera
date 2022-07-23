<?
require('../_define.inc');
require("../_upgrade.inc");
require('../class/system.class');
require('../class/socket.class');

$dev_info = new CDeviceInfomation();
$ipc_sock = new IPCSocket();
$ipc_sock->Connection($GLOBALS['dev_info'], CMD_GET_DEVICE_INFORMATION);

$product_name = $dev_info->ProductName;

define('CAPABILITY_JSON_PATH', '../capability.json');

function get_capability()
{
	$str = file_get_contents(CAPABILITY_JSON_PATH);
	$json =  json_decode($str, true);
	for($i=0; $i<count($json); $i++)
	{
		for($j=0; $j<count($json[$i]["model"]); $j++)
		{
			if($GLOBALS['product_name'] == $json[$i]["model"][$j])
			{
				/*
				   [20200513]  FIX ME
				   resolution capability 의 경우 STANLEY OEM 기준으로 정리되어 있음
				   추후, resolution은 json 파일에서 읽어오는 것이 아닌 pconf_etc 에서 채널 별로 읽어오는 작업 필요
				 */

				echo json_encode($json[$i]["capability"], JSON_PRETTY_PRINT);
			}
		}
	}
}
//------------------------------------------------------------------------------------------------------
//  Sdk
//------------------------------------------------------------------------------------------------------
header("Content-Type: text/plain");
ob_end_clean ();
if(isset($_REQUEST['msubmenu']))
{
	if ( $_REQUEST['msubmenu'] == 'cap' )
	{    
		if ( $_REQUEST['action'] == 'view' )
		{
			get_capability();
		}
	}
}
?>
