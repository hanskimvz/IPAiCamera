<?
ini_set('memory_limit', '2M');
include('_define.inc');
//require('./class/image.class');
include('./class/socket.class');

$image;
$ipc_sock = new IPCSocket();
$snapimage_id = 0;
if ( isset($_REQUEST['id']) )
{
	$snapimage_id = $_REQUEST['id'];
}
$image = $ipc_sock->Connection(NULL, CMD_GET_SNAPSHOT_IMAGE, $snapimage_id);
if ($ipc_sock->dataInfo['ErrorCode']['value'] == APP_OK)
{
  header("Content-Type: image/jpeg");
  header("Content-Length: ". strlen($image));
  echo $image; 	
}
else if ($ipc_sock->dataInfo['ErrorCode']['value'] == APP_ERR_ENCRYPTED_VIDEO)
{
	$file = "/root/web/images/encrypted.jpg";
	is_file($file) or die ("File: $file does not exist.");

	header("Content-Type: image/jpeg");
	header("Content-Length: ". filesize($file));

	readfile($file);
}
?>
