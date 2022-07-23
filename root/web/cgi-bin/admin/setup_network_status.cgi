<?
require('../_define.inc');
require('../class/network.class');
require('../class/capability.class');

$net_conf = new CNetworkConfiguration();
$system_caps = new CCapability();
$get_oem = $system_caps->getOEM();
//--- ip
function getNetworkInfo($name)
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

	echo $name ."=". json_encode($data) . ";\r\n";
}
function getoemInfo($name)
{
	$data['oem'] = $GLOBALS['get_oem'];
	echo $name ."=\"". $data['oem'] . "\";\r\n";
}
?>

<!DOCTYPE html>
<html>
	<head>
		<title>NETWORK status</title>
		<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
	</head>
	<body oncontextmenu="return false" onselectstart="return false"  ondragstart="return false">
		<div class="contentTitle" tkey="setup_network_status">NETWORK status</div>
		<div class="content">
			<table id="info">
				<tr>
					<th width="150"><span tkey="setup_mac_address"></span></th>
					<td id="mac"></td>
				</tr>
				<tr>
					<th><span tkey="setup_ipaddress"></span></th>
					<td id="ip"></td>
				</tr>
				<tr>
					<th><span tkey="setup_subnet_mask"></span></th>
					<td id="subnetmask"></td>
				</tr>
				<tr>
					<th><span tkey="setup_default_gateway"></span></th>
					<td id="gateway"></td>
				</tr>
				<tr>
					<th><span tkey="setup_preferred_dnsserver"></span></th>
					<td id="dns_pre"></td>
				</tr>  
				<tr>
					<th><span tkey="setup_alternate_dnsserver"></span></th>
					<td id="dns_alt"></td>
				</tr>
				<tr>
					<th><span tkey="setup_http_port"></span></th>
					<td id="web_port"></td>
				</tr>
				<tr name="SYSTEM_OPTION_UI_FIXED_DATE_20160504"> 
					<th tkey="setup_https_port"></th>
					<td id="https_port"></td>
				</tr>
				<tr>
					<th><span tkey="setup_rtsp_port"></span></th>
					<td id="rtsp_port"></td>
				</tr>
				<tr name="IV_MTU">
					<th><span>MTU</span></th>
					<td id="mtu"></td>
				</tr>				
			</table>
		</div>
		<script type="text/javascript">
			var NetworkInfo = {};
			var oemInfo;
			<?  getNetworkInfo("NetworkInfo"); ?>
			<?  getoemInfo("oemInfo"); ?>
			$(document).ready( function() {
				if( (systemOption & SYSTEM_OPTION_UI_FIXED_DATE_20160504) == 1 ){
					$("[name=SYSTEM_OPTION_UI_FIXED_DATE_20160504]").remove();
				}
				if(oemInfo != 12) {
					$("[name=IV_MTU]").remove();
				}
				initLanguage();
				for( id in NetworkInfo) {
					if( NetworkInfo.hasOwnProperty(id) ) {
						$("#"+ id).html(NetworkInfo[id]);
					} else {
						console.log("false", id);
					}
				}
			});    
		</script>
	</body>
</html>
