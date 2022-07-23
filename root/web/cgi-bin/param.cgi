<?
// modified by Hans Kim
// compatible with IPN

if(!isset($_GET['action'])){
	$_GET['action'] = 'list';
}
if (!in_array($_GET['action'], [ 'list', 'update'] )) {
	echo "Failed" ;
}
if (!isset($_GET['group'])) {
	$_GET['group'] = 'all';
}

// header("Content-type:text/plain");
require('./_define.inc');

require('./class/system.class');
require('./class/network.class');
// require('./class/socket.class');
// require('./class/capability.class');
// require('./class/media.class');
// require('./class/ptz.class');

$shm_id = shmop_open(KEY_SM_SHARED_CONFIG, "a", 0, 0);
$system_conf = new CSystemConfiguration($shm_id);
// $system_caps = new CCapability($shm_id);
// $media_conf  = new CMediaConfiguration($shm_id);
// $profile_conf = new CProfileConfiguration($shm_id);
shmop_close($shm_id);
// print "<pre>"; print_r($GLOBALS['system_conf']); print "</pre>";
$net_conf = new CNetworkConfiguration();

// exit();

function getNetworkInfo($name, $stream)
{	
	$data['ip_type']      = $GLOBALS['net_conf']->IPv4->Type;
	$data['mac']          = trim($GLOBALS['net_conf']->HwAddress);

	$data['subnetmask']   = trim($GLOBALS['net_conf']->IPv4->SubnetMask);
	$data['gateway']      = trim($GLOBALS['net_conf']->IPv4->Gateway);
	$data['mtu']      = trim($GLOBALS['net_conf']->MTUSetting->Value);
	$data['web_port']     = $GLOBALS['net_conf']->Protocols->Protocol[0]->Port;
	$data['https_port']   = $GLOBALS['net_conf']->Protocols->Protocol[2]->Port;
	$data['control_port'] = 0;
	$data['video_port']   = 0;
	$data['at_port']      = 0;
	$data['ar_port']      = 0;
	$data['rtsp_port']    = $GLOBALS['net_conf']->Protocols->Protocol[1]->Port;
	$data['ipv6_enable']  = 0;

	if ($GLOBALS['net_conf']->IPv4->Type == 0 ){
		$data['ip']       = trim($GLOBALS['net_conf']->IPv4->StaticIpAddr);
	} else {
		$data['ip']       = trim($GLOBALS['net_conf']->IPv4->DynamicIpAddr);
	}
	if($GLOBALS['net_conf']->DNS->Type == 0)
	{
		$data['dns_pre']  = trim($GLOBALS['net_conf']->DNS->DNSManualAddr0);
		$data['dns_alt']  = trim($GLOBALS['net_conf']->DNS->DNSManualAddr1);	
	}
	else
	{
		$data['dns_pre']  = trim($GLOBALS['net_conf']->DNS->DNSDynamicAddr0);
		$data['dns_alt']  = trim($GLOBALS['net_conf']->DNS->DNSDynamicAddr1);
	}
	echo "Server.RTSP.S0.Unicast.RTP0.url=rtsp://" . $data['ip'] . ":" . $data['rtsp_port'] . "/" . $stream . "\r\n\r\n0\r\n\r\n";
}

if ((isset($_GET["action"]) && $_GET["action"] == "list") && (isset($_GET["group"]) && strcasecmp($_GET["group"],"Server.RTSP.S0.Unicast.RTP0.url") == 0)) {
	getNetworkInfo("NetworkInfo", "ufirststream");
}else if ((isset($_GET["action"]) && $_GET["action"] == "list") && (isset($_GET["group"]) && strcasecmp($_GET["group"],"Server.RTSP.S0.Unicast.RTP1.url") == 0)) {
	getNetworkInfo("NetworkInfo", "usecondstream");
}else if (isset($_GET["action"]) && $_GET["action"] == "update" && isset($_GET["group"]) && strcasecmp($_GET["group"],"AudioIn.Ch0") == 0) {
        echo "#200|OK|update|AudioIn.Ch0|enable volume ";
}
else if (isset($_GET["action"]) && $_GET["action"] == "update" && isset($_GET["group"]) && strcasecmp($_GET["group"],"AudioOut.Ch0") == 0) {
        echo "#200|OK|update|AudioOut.Ch0|enable ";
}
else if (isset($_GET["action"]) && $_GET["action"] == "update" && isset($_GET["group"]) && strcasecmp($_GET["group"],"AudioOut.Ch1") == 0) {
        echo "#200|OK|update|AudioOut.Ch1|enable ";
}
else {
	echo "Failed!";
}
?>

