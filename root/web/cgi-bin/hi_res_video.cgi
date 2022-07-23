<?
ini_set('memory_limit', '4M');
include('_define.inc');
include('./class/socket.class');
include('./class/system.class');

if(isset($_REQUEST['action'])) 
{
	if ( $_REQUEST['action'] == 'apply' )
	{
		if(isset($_REQUEST['mode']))
		{
			$HrImgMode = new CHRImage();
			$HrImgMode->Mode = $_REQUEST['mode'];
			$ipc_sock = new IPCSocket();
			$ipc_sock->Connection($HrImgMode, CMD_SET_HR_IMAGE);
			if ($ipc_sock->dataInfo['ErrorCode']['value'] == APP_OK)
			{
				show_post_ok();
			}
			else
			{
				show_post_ng();
			}
		}
		else
		{
			show_post_ng();
		}
	}
}
else
{
	$image;
	$ipc_sock = new IPCSocket();
	$image = $ipc_sock->Connection(NULL, CMD_GET_HR_IMAGE, 0);
	if ($ipc_sock->dataInfo['ErrorCode']['value'] == APP_OK)
	{
		header("Content-Type: image/jpeg");
		header("Content-Length: ". strlen($image));

		echo $image; 	
	}
	else
	{
		$file = "/root/web/images/encrypted.jpg";
		is_file($file) or die ("File: $file does not exist.");

		header("Content-Type: image/jpeg");
		header("Content-Length: ". filesize($file));

		readfile($file);
	}
}
?>

