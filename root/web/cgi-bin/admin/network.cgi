<?
require('../_define.inc');
require('../class/system.class');
require('../class/capability.class');
require('../class/network.class');
require('../class/socket.class');

$shm_id = shmop_open(KEY_SM_SHARED_CONFIG, "a", 0, 0);
$system_conf = new CSystemConfiguration($shm_id);
$system_caps = new CCapability($shm_id);
$net_conf = new CNetworkConfiguration($shm_id);
shmop_close($shm_id);
//--- ip
function ip_view_post()
{
	echo "ip_type="			.$GLOBALS['net_conf']->IPv4->Type."\r\n";
	echo "mac="				.trim($GLOBALS['net_conf']->HwAddress)."\r\n";
	echo "ip="				.trim(($GLOBALS['net_conf']->IPv4->Type == 0)?$GLOBALS['net_conf']->IPv4->StaticIpAddr:$GLOBALS['net_conf']->IPv4->DynamicIpAddr)."\r\n";
	echo "sm="				.trim($GLOBALS['net_conf']->IPv4->SubnetMask)."\r\n";
	echo "gw="				.trim($GLOBALS['net_conf']->IPv4->Gateway)."\r\n";
	echo "dns_pre="				.trim(($GLOBALS['net_conf']->DNS->Type == 0)?$GLOBALS['net_conf']->DNS->DNSManualAddr0:$GLOBALS['net_conf']->DNS->DNSDynamicAddr0)."\r\n";
	echo "dns_alt="				.trim(($GLOBALS['net_conf']->DNS->Type == 0)?$GLOBALS['net_conf']->DNS->DNSManualAddr1:$GLOBALS['net_conf']->DNS->DNSDynamicAddr1)."\r\n";
	echo "web_port="		.$GLOBALS['net_conf']->Protocols->Protocol[0]->Port."\r\n";
	echo "https_port="		.$GLOBALS['net_conf']->Protocols->Protocol[2]->Port."\r\n";
	echo "control_port="	."0"."\r\n";
	echo "video_port="		."0"."\r\n";
	echo "at_port="			."0"."\r\n";
	echo "ar_port="			."0"."\r\n";
	echo "rtsp_port="		.$GLOBALS['net_conf']->Protocols->Protocol[1]->Port."\r\n";
	echo "ipv6_enable="		."0"."\r\n";
	{
		exec("ifconfig eth0 |grep 'inet6 addr'", $ret);
		if ( count($ret) > 0 )
		{
			$ret[0] = str_replace(" ", "", $ret[0]);
			$spos = strpos($ret[0], ":");
			$epos = strpos($ret[0], "/");
			$addr = substr($ret[0], $spos+1, $epos-$spos-1);
		}
		else
		{
			$addr = "::1";
		}
		echo "ipv6_addr="	.$addr."\r\n";
	}
}

//---
function CheckIP()
{
	if (!isset($_REQUEST['ip'])) {
		$ip_addr = ($GLOBALS['net_conf']->IPv4->Type == 0)?$GLOBALS['net_conf']->IPv4->StaticIpAddr:$GLOBALS['net_conf']->IPv4->DynamicIpAddr;
	} else {
		$ip_addr = $_REQUEST['ip'];
	}
	if (!isset($_REQUEST['gw'])) {
		$gw_addr = $GLOBALS['net_conf']->IPv4->Gateway;
	} else {
		$gw_addr = $_REQUEST['gw'];
	}
	if (!isset($_REQUEST['sm'])) {
		$sm_addr = $GLOBALS['net_conf']->IPv4->SubnetMask;
	} else {
		$sm_addr = $_REQUEST['sm'];
	}
	
	$ipArray 	= explode(".", $ip_addr);
	$smArray 	= explode(".", $sm_addr);
	$gwArray 	= explode(".", $gw_addr);
	
	if (count($ipArray) != 4 || count($smArray) != 4 || count($gwArray) != 4)
		return false;

	$ip_num 		= (($ipArray[0]&0xFF)<<24) + (($ipArray[1]&0xFF)<<16) + (($ipArray[2]&0xFF)<<8) + (($ipArray[3]&0xFF)<<0);
	$gw_num 		= (($gwArray[0]&0xFF)<<24) + (($gwArray[1]&0xFF)<<16) + (($gwArray[2]&0xFF)<<8) + (($gwArray[3]&0xFF)<<0);
	$sm_num 		= (($smArray[0]&0xFF)<<24) + (($smArray[1]&0xFF)<<16) + (($smArray[2]&0xFF)<<8) + (($smArray[3]&0xFF)<<0);
	$not_sm_num 	= (((-$smArray[0]-1)&0xFF)<<24) + (((-$smArray[1]-1)&0xFF)<<16) + (((-$smArray[2]-1)&0xFF)<<8) + (((-$smArray[3]-1)&0xFF)<<0);
	
	$thisSegment = $ipArray[0];
	
	if($thisSegment<1 || $thisSegment>223)	return false;

	for($i=1; $i<4; $i++) {
		$thisSegment = $ipArray[$i];
		if($thisSegment>255)	return false;
	}

	$thisSegment = $gwArray[0];
	if($thisSegment<1 || $thisSegment>223)	return false;

	for($i=1; $i<4; $i++) {
		$thisSegment = $gwArray[$i];
		if($thisSegment>255)	return false;
	}

	for($i=0; $i<4; $i++) {
		$thisSegment = $smArray[$i];
		if($thisSegment>255)	return false;
	}

	for($i=0; $i<32; $i++) {
		$token = 1<<$i;
		if(($sm_num & $token)>0) break;
	}

	for($i++; $i<32; $i++) {
		$token = 1<<$i;
		if(($sm_num & $token)==0)	return false;
	}

	if($ip_num==$gw_num)	return false;

	if((($ip_num & $not_sm_num)==$not_sm_num) || (($ip_num&$not_sm_num)==0) || (($ip_num&$sm_num)==0)) {
		return false;
	}

	if((($gw_num&$not_sm_num)==$not_sm_num) || (($gw_num&$not_sm_num)==0) || (($gw_num&$sm_num)==0)) {
		return false;
	}

	if(($ip_num&$sm_num) != ($gw_num&$sm_num)) {
		return false;
	}

	return true;
}
function CheckPortDuplicate()
{
	if (!isset($_REQUEST['web_port'])) {
		$web_port = $GLOBALS['net_conf']->Protocols->Protocol[0]->Port;
	} else {
		$web_port = $_REQUEST['web_port'];
	}
	if (!isset($_REQUEST['control_port'])) {
		$control_port = "0";
	} else {
		$control_port = $_REQUEST['control_port'];
	}
	if (!isset($_REQUEST['video_port'])) {
		$video_port = "0";
	} else {
		$video_port = $_REQUEST['video_port'];
	}
	if (!isset($_REQUEST['at_port'])) {
		$at_port = "0";
	} else {
		$at_port = $_REQUEST['at_port'];
	}
	if (!isset($_REQUEST['ar_port'])) {
		$ar_port = "0";
	} else {
		$ar_port = $_REQUEST['ar_port'];
	}
	if (!isset($_REQUEST['https_port'])) {
		$https_port = $GLOBALS['net_conf']->Protocols->Protocol[2]->Port;
	} else {
		$https_port = $_REQUEST['https_port'];
	}
	if (!isset($_REQUEST['rtsp_port'])) {
		$rtsp_port = $GLOBALS['net_conf']->Protocols->Protocol[1]->Port;
	} else {
		$rtsp_port = $_REQUEST['rtsp_port'];
	}
	
	if ($web_port == $control_port)			return false;
	else if ($web_port == $video_port)		return false;
	else if ($web_port == $at_port)			return false;
	else if ($web_port == $ar_port)			return false;
	else if ($web_port == $https_port)		return false;
	else if ($web_port == $rtsp_port)		return false;
	else if ($control_port == $video_port)	return false;
	else if ($control_port == $at_port)		return false;
	else if ($control_port == $ar_port)		return false;
	else if ($control_port == $https_port)	return false;
	else if ($control_port == $rtsp_port)	return false;
	else if ($video_port == $at_port)		return false;
	else if ($video_port == $ar_port)		return false;
	else if ($video_port == $https_port)	return false;
	else if ($video_port == $rtsp_port)		return false;
	else if ($at_port == $ar_port)			return false;
	else if ($at_port == $https_port)		return false;
	else if ($at_port == $rtsp_port)		return false;
	else if ($ar_port == $https_port)		return false;
	else if ($ar_port == $rtsp_port)		return false;
	else if ($https_port == $rtsp_port)		return false;
	
	return true;
}
//---------
function change_hostname()
{
	if (!isset($_REQUEST['hostname'])) return 1;
	if (strlen($_REQUEST['hostname']) > 30) return -1;

	$GLOBALS['system_conf']->DeviceInfo->OnvifConf->hostname  = $_REQUEST['hostname'];
	return 0;
}

function change_ip_iptype()
{
	if (!isset($_REQUEST['ip_type'])) return 1;
	if ($_REQUEST['ip_type'] < 0 || $_REQUEST['ip_type'] > 1) return -1;
	
	$GLOBALS['net_conf']->IPv4->Type = $_REQUEST['ip_type'];
	return 0;
}

function change_ip_ipaddr()
{
	if (!isset($_REQUEST['ip'])) return 1;
	if (strlen($_REQUEST['ip']) > 15) return -1;
	
	$GLOBALS['net_conf']->IPv4->StaticIpAddr = $_REQUEST['ip'];
	return 0;
}

function change_ip_subnet()
{
	if (!isset($_REQUEST['sm'])) return 1;
	if (strlen($_REQUEST['sm']) > 15) return -1;
	
	$GLOBALS['net_conf']->IPv4->SubnetMask = $_REQUEST['sm'];
	return 0;
}

function change_ip_gateway()
{
	if (!isset($_REQUEST['gw'])) return 1;
	if (strlen($_REQUEST['gw']) > 15) return -1;

	$GLOBALS['net_conf']->IPv4->Gateway = $_REQUEST['gw'];
	return 0;
}

function change_mtu()
{
	if (!isset($_REQUEST['mtu'])) return 1;
	if ($_REQUEST['mtu'] < 1072 || $_REQUEST['mtu'] > 1500) return -1;

	$GLOBALS['net_conf']->MTUSetting->Value = $_REQUEST['mtu'];
	return 0;
}

function change_ip_dns()
{
	if(isset($_REQUEST['dns']))
	{
		if (strlen($_REQUEST['dns']) > 15) return -1;
		$GLOBALS['net_conf']->DNS->DNSManualAddr0 = $_REQUEST['dns'];
	}
	if(isset($_REQUEST['dns_pre']))
	{
		if (strlen($_REQUEST['dns_pre']) > 15) return -1;
		$GLOBALS['net_conf']->DNS->DNSManualAddr0 = $_REQUEST['dns_pre'];
	}	
	if(isset($_REQUEST['dns_alt']))
	{
		if (strlen($_REQUEST['dns_alt']) > 15) return -1;
		$GLOBALS['net_conf']->DNS->DNSManualAddr1 = $_REQUEST['dns_alt'];
	}	
	return 0;
}
function change_ip_webport()
{
	if (!isset($_REQUEST['web_port'])) return 1;
	if ($_REQUEST['web_port'] != 80 && ($_REQUEST['web_port'] < 1025 || $_REQUEST['web_port'] > 60000)) return -1;
	
	$GLOBALS['net_conf']->Protocols->Protocol[0]->Port = $_REQUEST['web_port'];
	return 0;
}
function change_ip_https_port()
{
	if (!isset($_REQUEST['https_port'])) return 1;
	if ($_REQUEST['https_port'] != 443 && ($_REQUEST['https_port'] < 1025 || $_REQUEST['https_port'] > 60000)) return -1;
	
	$GLOBALS['net_conf']->Protocols->Protocol[2]->Port = $_REQUEST['https_port'];
	return 0;
}
function change_ip_https_enabled()
{
	if (!isset($_REQUEST['https_enabled'])) return 1;
	$GLOBALS['net_conf']->Protocols->Protocol[2]->Enabled = $_REQUEST['https_enabled'];
	return 0;
}
function change_ip_controlport()
{
	if (!isset($_REQUEST['control_port'])) return 1;
	if ($_REQUEST['control_port'] < 1025 || $_REQUEST['control_port'] > 60000) return -1;

	return 0;
}
function change_ip_videoport()
{
	if(!isset($_REQUEST['video_port'])) return 1;
	if($_REQUEST['video_port'] < 1025 || $_REQUEST['video_port'] > 60000) return -1;
	
	return 0;
}

function change_ip_atransport()
{
	if(!isset($_REQUEST['at_port'])) return 1;
	if($_REQUEST['at_port'] < 1025 || $_REQUEST['at_port'] > 60000) return -1;

	return 0;
}

function change_ip_arecvport()
{
	if(!isset($_REQUEST['ar_port'])) return 1;
	if($_REQUEST['ar_port'] < 1025 || $_REQUEST['ar_port'] > 60000) return -1;

	return 0;
}

function change_ip_rtspport()
{
	if(!isset($_REQUEST['rtsp_port'])) return 1;
	if ($_REQUEST['rtsp_port'] != 554 && ($_REQUEST['rtsp_port'] < 1025 || $_REQUEST['rtsp_port'] > 60000)) return -1;
	
	$GLOBALS['net_conf']->Protocols->Protocol[1]->Port = $_REQUEST['rtsp_port'];
	return 0;
}

function change_ip_ipv6()
{
	if (!isset($_REQUEST['ipv6_enable'])) return 1;
	if ($_REQUEST['ipv6_enable'] < 0 || $_REQUEST['ipv6_enable'] > 1) return -1;
	
	return 0;
}

function change_rtp_timeout()
{
	if (!isset($_REQUEST['rtp_timeout'])) return 1;
	if ($_REQUEST['rtp_timeout'] != 0  && ($_REQUEST['rtp_timeout'] < 30 || $_REQUEST['rtp_timeout'] > 120)) return -1;
	
	return 0;
}

function change_ip()
{
	if (change_ip_iptype() < 0) return -1;
	if (change_ip_ipaddr() < 0) return -1;
	if (change_ip_subnet() < 0) return -1;
	if (change_ip_gateway() < 0) return -1;
	if (change_ip_dns() < 0) return -1;
	if(change_mtu() < 0) return -1;
	if (change_ip_webport() < 0) return -1;
	//if (change_ip_controlport() < 0) return -1;
	//if (change_ip_videoport() < 0) return -1;
	//if (change_ip_atransport() < 0) return -1;
	//if (change_ip_arecvport() < 0) return -1;
	if (change_ip_rtspport() < 0) return -1;
	if (change_ip_ipv6() < 0) return -1;
	if (change_ip_https_port() < 0) return -1;
	if (change_ip_https_enabled() < 0 ) return -1;
	
	return 0;
}
//--- zeroconfig
function zeroconfig_view_post()
{
		echo "zeroconfig_enable="	.$GLOBALS['net_conf']->ZeroConfig->Enabled."\r\n";		
		echo "zeroconfig_id="		.trim($GLOBALS['net_conf']->ZeroConfig->InterfaceToken)."\r\n";
		echo "zeroconfig_addr="		.trim($GLOBALS['net_conf']->ZeroConfig->Addr)."\r\n";
	
}
function change_zeroconfig_enable()
{
	if (!isset($_REQUEST['zeroconfig_enable'])) return 1;
	if ($_REQUEST['zeroconfig_enable'] < 0 || $_REQUEST['zeroconfig_enable'] > 2) return -1;
	
	$GLOBALS['net_conf']->ZeroConfig->Enabled = $_REQUEST['zeroconfig_enable'];
	return 0;
}
function change_zeroconfig_id()
{
	if (!isset($_REQUEST['zeroconfig_id'])) return 1;
	if ($GLOBALS['net_conf']->ZeroConfig->Enabled != 1) return 1;
	
	$GLOBALS['net_conf']->ZeroConfig->InterfaceToken = $_REQUEST['zeroconfig_id'];
	return 0;
}
function change_zeroconfig_addr()
{
	if (!isset($_REQUEST['zeroconfig_addr'])) return 1;
	if ($GLOBALS['net_conf']->ZeroConfig->Enabled != 1) return 1;
	
	$GLOBALS['net_conf']->ZeroConfig->Addr = $_REQUEST['zeroconfig_addr'];
	return 0;
}

function change_zeroconfig()
{
	if (change_zeroconfig_enable() < 0) return -1;
	if (change_zeroconfig_id() < 0) return -1;
	if (change_zeroconfig_addr() < 0) return -1;
	
	return 0;
}
//--- snmp
function snmp_view_post()
{
	echo "Enabled_V1="			.$GLOBALS['net_conf']->SnmpSetting->Snmpv1->Enabled_V1."\r\n";		
	echo "Enabled_V2="			.$GLOBALS['net_conf']->SnmpSetting->Snmpv2->Enabled_V2."\r\n";
	echo "RoComName="			.trim($GLOBALS['net_conf']->SnmpSetting->Snmpv2->RoComName)."\r\n";
	echo "RwComName="			.trim($GLOBALS['net_conf']->SnmpSetting->Snmpv2->RwComName)."\r\n";
	echo "Enabled_Trap="		.$GLOBALS['net_conf']->SnmpSetting->Snmpv2->Enabled_Trap."\r\n";
	echo "TrapServer="			.trim($GLOBALS['net_conf']->SnmpSetting->Snmpv2->TrapServer)."\r\n";
	echo "TrapComName="			.trim($GLOBALS['net_conf']->SnmpSetting->Snmpv2->TrapComName)."\r\n";

	echo "RoEnabled_V3="		.$GLOBALS['net_conf']->SnmpSetting->Snmpv3->RoEnabled_V3."\r\n";
	echo "RoUserName="			.trim($GLOBALS['net_conf']->SnmpSetting->Snmpv3->RoUserName)."\r\n";
	echo "RoSecuLevel="			.$GLOBALS['net_conf']->SnmpSetting->Snmpv3->RoSecuLevel."\r\n";
	echo "RoAuthAlg="			.$GLOBALS['net_conf']->SnmpSetting->Snmpv3->RoAuthAlg."\r\n";
	echo "RoAuthName="			.trim($GLOBALS['net_conf']->SnmpSetting->Snmpv3->RoAuthName)."\r\n";
	echo "RoPriAlg="			.$GLOBALS['net_conf']->SnmpSetting->Snmpv3->RoPriAlg."\r\n";
	echo "RoPriName="			.trim($GLOBALS['net_conf']->SnmpSetting->Snmpv3->RoPriName)."\r\n";


	echo "RwEnabled_V3="		.$GLOBALS['net_conf']->SnmpSetting->Snmpv3->RwEnabled_V3."\r\n";
	echo "RwUserName="			.trim($GLOBALS['net_conf']->SnmpSetting->Snmpv3->RwUserName)."\r\n";
	echo "RwSecuLevel="			.$GLOBALS['net_conf']->SnmpSetting->Snmpv3->RwSecuLevel."\r\n";
	echo "RwAuthAlg="			.$GLOBALS['net_conf']->SnmpSetting->Snmpv3->RwAuthAlg."\r\n";
	echo "RwAuthName="			.trim($GLOBALS['net_conf']->SnmpSetting->Snmpv3->RwAuthName)."\r\n";
	echo "RwPriAlg="			.$GLOBALS['net_conf']->SnmpSetting->Snmpv3->RwPriAlg."\r\n";
	echo "RwPriName="			.trim($GLOBALS['net_conf']->SnmpSetting->Snmpv3->RwPriName)."\r\n";

}
function change_snmp()
{
	$Snmpv1 = $GLOBALS['net_conf']->SnmpSetting->Snmpv1;
	if(isset($_REQUEST['Enabled_V1'])){	
		if($_REQUEST['Enabled_V1'] < 0 || $_REQUEST['Enabled_V1'] > 1)	return -1;
		$Snmpv1->Enabled_V1 = $_REQUEST['Enabled_V1'];
	}
	
	$Snmpv2 = $GLOBALS['net_conf']->SnmpSetting->Snmpv2;
	if(isset($_REQUEST['Enabled_V2'])){	
		if($_REQUEST['Enabled_V2'] < 0 || $_REQUEST['Enabled_V2'] > 1)	return -1;
		$Snmpv2->Enabled_V2 = $_REQUEST['Enabled_V2'];
	}
	if(isset($_REQUEST['RoComName'])){			
		 $Snmpv2->RoComName = $_REQUEST['RoComName'];
	}
	if(isset($_REQUEST['RwComName'])){			
		 $Snmpv2->RwComName = $_REQUEST['RwComName'];
	}
	if(isset($_REQUEST['Enabled_Trap'])){			
		 $Snmpv2->Enabled_Trap = $_REQUEST['Enabled_Trap'];
	}
	if(isset($_REQUEST['TrapServer'])){			
		 $Snmpv2->TrapServer = $_REQUEST['TrapServer'];
	}	
	if(isset($_REQUEST['TrapComName'])){			
		 $Snmpv2->TrapComName = $_REQUEST['TrapComName'];
	}	
			
	$Snmpv3 = $GLOBALS['net_conf']->SnmpSetting->Snmpv3;
	if(isset($_REQUEST['RoEnabled_V3'])){	
		if($_REQUEST['RoEnabled_V3'] < 0 || $_REQUEST['RoEnabled_V3'] > 1)	return -1;
		$Snmpv3->RoEnabled_V3 = $_REQUEST['RoEnabled_V3'];
	}
	if(isset($_REQUEST['RoUserName'])){			
		 $Snmpv3->RoUserName = $_REQUEST['RoUserName'];
	}
	if(isset($_REQUEST['RoSecuLevel'])){	
		if($_REQUEST['RoSecuLevel'] < 0 || $_REQUEST['RoSecuLevel'] > 2)	return -1;
		$Snmpv3->RoSecuLevel = $_REQUEST['RoSecuLevel'];
	}
	if(isset($_REQUEST['RoAuthAlg'])){	
		if($_REQUEST['RoAuthAlg'] < 0 || $_REQUEST['RoAuthAlg'] > 1)	return -1;
		$Snmpv3->RoAuthAlg = $_REQUEST['RoAuthAlg'];
	}
	if(isset($_REQUEST['RoAuthName'])){
		 $Snmpv3->RoAuthName = $_REQUEST['RoAuthName'];
	}   
	if(isset($_REQUEST['RoPriAlg'])){	
		if($_REQUEST['RoPriAlg'] < 0 || $_REQUEST['RoPriAlg'] > 1)	return -1;
		$Snmpv3->RoPriAlg = $_REQUEST['RoPriAlg'];
	}   	
	if(isset($_REQUEST['RoPriName'])){			
		 $Snmpv3->RoPriName = $_REQUEST['RoPriName'];
	}
	
	if(isset($_REQUEST['RwEnabled_V3'])){	
		if($_REQUEST['RwEnabled_V3'] < 0 || $_REQUEST['RwEnabled_V3'] > 1)	return -1;
		$Snmpv3->RwEnabled_V3 = $_REQUEST['RwEnabled_V3'];
	}
	if(isset($_REQUEST['RwUserName'])){
		 $Snmpv3->RwUserName = $_REQUEST['RwUserName'];
	} 
	if(isset($_REQUEST['RwSecuLevel'])){	
		if($_REQUEST['RwSecuLevel'] < 0 || $_REQUEST['RwSecuLevel'] > 2)	return -1;
		$Snmpv3->RwSecuLevel = $_REQUEST['RwSecuLevel'];
	}
	if(isset($_REQUEST['RwAuthAlg'])){	
		if($_REQUEST['RwAuthAlg'] < 0 || $_REQUEST['RwAuthAlg'] > 1)	return -1;
		$Snmpv3->RwAuthAlg = $_REQUEST['RwAuthAlg'];
	}  
	if(isset($_REQUEST['RwAuthName'])){
		 $Snmpv3->RwAuthName = $_REQUEST['RwAuthName'];
	}  
	if(isset($_REQUEST['RwPriAlg'])){	
		if($_REQUEST['RwPriAlg'] < 0 || $_REQUEST['RwPriAlg'] > 1)	return -1;
		$Snmpv3->RwPriAlg = $_REQUEST['RwPriAlg'];
	} 
	if(isset($_REQUEST['RwPriName'])){
		 $Snmpv3->RwPriName = $_REQUEST['RwPriName'];
	}  

	return 0;
}

//--- upnp
function upnp_view_post()
{
		echo "upnp_enable="			.$GLOBALS['net_conf']->UpnpSetting->Enabled."\r\n";		
		echo "upnp_friendlyname="	.trim($GLOBALS['net_conf']->UpnpSetting->FriendlyName)."\r\n";
}
function change_upnp_enable()
{
	if (!isset($_REQUEST['upnp_enable'])) return 1;
	if ($_REQUEST['upnp_enable'] < 0 || $_REQUEST['upnp_enable'] > 2) return -1;
	
	$GLOBALS['net_conf']->UpnpSetting->Enabled = $_REQUEST['upnp_enable'];
	return 0;
}   

function change_upnp_friendlyname()
{
	if (!isset($_REQUEST['upnp_friendlyname'])) return 1;
	if ($GLOBALS['net_conf']->UpnpSetting->Enabled != 1) return 1;
	if (strlen($_REQUEST['upnp_friendlyname']) > 30) return -1;
	
	$GLOBALS['net_conf']->UpnpSetting->FriendlyName = $_REQUEST['upnp_friendlyname'];
	return 0;
}

function change_upnp()
{
	if (change_upnp_enable() < 0) return -1;
	if (change_upnp_friendlyname() < 0) return -1;
	
	return 0;
}

//--- ddns
function ddns_view_post()
{
	echo "ddns_enable="			.$GLOBALS['net_conf']->DDNS->Enabled."\r\n";
	echo "ddns_type="			.$GLOBALS['net_conf']->DDNS->Type."\r\n";
	echo "ddns_hostname="	.trim($GLOBALS['net_conf']->DDNS->HostName)."\r\n";
	echo "ddns_username="	.trim($GLOBALS['net_conf']->DDNS->UserId)."\r\n";
	echo "ddns_password="	.trim($GLOBALS['net_conf']->DDNS->Password)."\r\n";
	echo "ddns_service="	.trim($GLOBALS['net_conf']->DDNS->ServiceAddr)."\r\n";
}
function change_ddns_enable()
{
	if (!isset($_REQUEST['ddns_enable'])) return 1;
	if ($_REQUEST['ddns_enable'] < 0 || $_REQUEST['ddns_enable'] > 1) return -1;
	
	$GLOBALS['net_conf']->DDNS->Enabled = $_REQUEST['ddns_enable'];
	
	return 0;
}

function change_ddns_ddnstype()
{
	if (!isset($_REQUEST['ddns_type'])) return 1;
	if ($_REQUEST['ddns_type'] < 1 || $_REQUEST['ddns_type'] > 2) return -1;
	
	$GLOBALS['net_conf']->DDNS->Type = $_REQUEST['ddns_type'];
	
	return 0;
}

function change_ddns_service()
{
	if (!isset($_REQUEST['ddns_service'])) return 1;
	if ($_REQUEST['ddns_service'] < 1 || $_REQUEST['ddns_service'] > 2) return -1;
	
	$GLOBALS['net_conf']->DDNS->ServiceAddr = $_REQUEST['ddns_service'];
	return 0;
}

function change_ddns_hostname()
{
	if (!isset($_REQUEST['ddns_hostname'])) return 1;
	if ($GLOBALS['net_conf']->DDNS->Enabled != 1) return 1;
	if (strlen($_REQUEST['ddns_hostname']) > 62) return -1;
	
	$GLOBALS['net_conf']->DDNS->HostName = $_REQUEST['ddns_hostname'];
	return 0;
}

function change_ddns_username()
{
	if (!isset($_REQUEST['ddns_username'])) return 1;
	if ($GLOBALS['net_conf']->DDNS->Enabled != 1) return 1;
	if (strlen($_REQUEST['ddns_username']) > 30) return -1;
	
	$GLOBALS['net_conf']->DDNS->UserId = $_REQUEST['ddns_username'];
	return 0;
}

function change_ddns_password()
{
	if (!isset($_REQUEST['ddns_password'])) return 1;
	if ($GLOBALS['net_conf']->DDNS->Enabled != 1) return 1;
	if (strlen($_REQUEST['ddns_password']) > 30) return -1;
	
	$GLOBALS['net_conf']->DDNS->Password = $_REQUEST['ddns_password'];
	return 0;
}


function change_ddns()
{
	if (change_ddns_enable() < 0) return -1;
	if (change_ddns_ddnstype() < 0) return -1;
	if (change_ddns_hostname() < 0) return -1;
	if (change_ddns_username() < 0) return -1;
	if (change_ddns_password() < 0) return -1;
//	if (change_ddns_service() < 0) return -1;
	
	return 0;
}

//--- https
function https_view_post()
{
	echo "conn_mode="	."0"."\r\n";
}

function change_https_conn_mode()
{
	if (!isset($_REQUEST['conn_mode'])) return 1;
	if ( $GLOBAL['https_conf']['mode'] == $_REQUEST['conn_mode'] ) return 1;


	return 0;
}

function change_https()
{
	if (change_https_conn_mode() < 0) return -1;
	return 0;
}

//--- snmp

function change_snmp_username()
{
	if (!isset($_REQUEST['username'])) return 1;
	if ( strlen($_REQUEST['username']) > 30 ) return -1;
	

	return 0;
}
function change_snmp_authpass()
{
	if (!isset($_REQUEST['authpass'])) return 1;
	if ( strlen($_REQUEST['authpass']) > 30 || strlen($_REQUEST['authpass']) < 8 ) return -1;
	

	return 0;
}
function change_snmp_privpass()
{
	if (!isset($_REQUEST['privpass'])) return 1;
	if ( strlen($_REQUEST['privpass']) > 30 || strlen($_REQUEST['privpass']) < 8 ) return -1;
	

	return 0;
}
function change_snmp_snmpstate()
{
	if (!isset($_REQUEST['snmpstate'])) return 1;
	if ( $_REQUEST['snmpstate'] > 1 || $_REQUEST['snmpstate'] < -1)	return -1;
	

	return 0;
		
}


//--- srtp
function srtp_view_post()
{
		echo "srtp_enable="			.$GLOBALS['net_conf']->SRTPSetting->Enabled."\r\n";		
		echo "srtp_protection_profile="			.$GLOBALS['net_conf']->SRTPSetting->Protection_profile."\r\n";	
		echo "srtp_master_key="	.trim($GLOBALS['net_conf']->SRTPSetting->Master_key)."\r\n";
		echo "srtp_salt_key="	.trim($GLOBALS['net_conf']->SRTPSetting->Salt_key)."\r\n";
}
function change_srtp_enable()
{
	if (!isset($_REQUEST['srtp_enable'])) return 1;
	if ($_REQUEST['srtp_enable'] < 0 || $_REQUEST['srtp_enable'] > 1) return -1;
	
	$GLOBALS['net_conf']->SRTPSetting->Enabled = $_REQUEST['srtp_enable'];
	return 0;
}   
function change_srtp_protection_profile()
{
	if (!isset($_REQUEST['srtp_protection_profile'])) return 1;
	if ($_REQUEST['srtp_protection_profile'] < 0 || $_REQUEST['srtp_protection_profile'] > 3) return -1;
	
	$GLOBALS['net_conf']->SRTPSetting->Protection_profile = $_REQUEST['srtp_protection_profile'];
	return 0;
}   
function change_srtp_master_key()
{
	if (!isset($_REQUEST['srtp_master_key'])) return 1;
	if ($GLOBALS['net_conf']->SRTPSetting->Enabled != 1) return 1;
	if (strlen($_REQUEST['srtp_master_key']) != 32 && strlen($_REQUEST['srtp_master_key']) != 0) return -1;
	
	$GLOBALS['net_conf']->SRTPSetting->Master_key = $_REQUEST['srtp_master_key'];
	return 0;
}
function change_srtp_salt_key()
{
	if (!isset($_REQUEST['srtp_salt_key'])) return 1;
	if ($GLOBALS['net_conf']->SRTPSetting->Enabled != 1) return 1;
	if (strlen($_REQUEST['srtp_salt_key']) != 28 && strlen($_REQUEST['srtp_salt_key']) != 0) return -1;
	
	$GLOBALS['net_conf']->SRTPSetting->Salt_key = $_REQUEST['srtp_salt_key'];
	return 0;
}
function change_srtp()
{
	if (change_srtp_enable() < 0) return -1;
	if (change_srtp_protection_profile() < 0) return -1;
	if (change_srtp_master_key() < 0) return -1;
	if (change_srtp_salt_key() < 0) return -1;

	return 0;
}
//////////////////////
/*function change_snmp()
{
	if (change_snmp_username() < 0) return -1;
	if (change_snmp_authpass() < 0) return -1;
	if (change_snmp_privpass() < 0) return -1;
	if (change_snmp_snmpstate() < 0) return -1;		//_BY_JGKO_20130612_SNMP_ON_OFF 

	return 0;
}*/
/////////////// rtsp ///////////
function view_rtsp()
{
	echo "rtsp_port="		.$GLOBALS['net_conf']->Protocols->Protocol[1]->Port."\r\n";
	echo "rtp_timeout="		."0"."\r\n";
}

function change_rtsp()
{
	if (change_rtp_timeout() < 0) return -1;
	if (change_ip_rtspport() < 0) return -1;

	return 0;
}

//------------------------------------------------------------------------------------------------------
// 	Html
//------------------------------------------------------------------------------------------------------
if(isset($_REQUEST['submenu']))
{
if ( $_REQUEST['submenu'] == 'ip' )
{
	if ( $_REQUEST['action'] == 'view' )
	{
		echo '<meta http-equiv="Refresh" content="0; URL=setup_network_tcp_ip.cgi">';
	}
	else if ( $_REQUEST['action'] == 'apply' )
	{
		change_ip();

		$ipc_sock = new IPCSocket();
		$ipc_sock->Connection($GLOBALS['net_conf'], CMD_SET_NETWORK_CONFIGURATION);
		if ($ipc_sock->dataInfo['ErrorCode']['value'] == APP_OK) {
			show_post_ok();
		} else {
			show_post_ng();
			echo "\r\nresult: ".$ipc_sock->dataInfo['ErrorCode']['value']."\r\n";
		}	
	}
	exit;
}
else if ( $_REQUEST['submenu'] == 'ddns' )
{
	if ( $_REQUEST['action'] == 'view' )
	{
		echo '<meta http-equiv="Refresh" content="0; URL=setup_network_ddns.cgi">';
	}
	else if ( $_REQUEST['action'] == 'apply' )
	{
		change_ddns();
  	$ipc_sock = new IPCSocket();
    $ipc_sock->Connection($GLOBALS['net_conf'], CMD_SET_NETWORK_CONFIGURATION);
    if ($ipc_sock->dataInfo['ErrorCode']['value'] == APP_OK)
    {
    	show_post_ok();
    }
    else
    {
      show_post_ng();
    }	
	}
	exit;
}
else if ( $_REQUEST['submenu'] == 'https' )
{
	if ( $_REQUEST['action'] == 'view' )
	{
		echo '<meta http-equiv="Refresh" content="0; URL=setup_network_https.cgi">';
	}
	else if ( $_REQUEST['action'] == 'apply' )
	{
		change_https();
  	$ipc_sock = new IPCSocket();
    $ipc_sock->Connection($GLOBALS['net_conf'], CMD_SET_NETWORK_CONFIGURATION);
    if ($ipc_sock->dataInfo['ErrorCode']['value'] == APP_OK)
    {
    	show_post_ok();
    }
    else
    {
      show_post_ng();
    }	
	}
	else if ( $_REQUEST['action'] == 'install' )
	{
		//check
		if (isset($_REQUEST['state'])) {
			//$cert_flag = $_REQUEST['state'];
			//$https_conf['cert_flag'] = $cert_flag;
			//shm_update_i(OFFSET_SYSTEM+59, $cert_flag);

			if (isset($_REQUEST['cname'])) {
			//	$cert_name = $_REQUEST['cname'];
			//	$https_conf['cert_name'] = $cert_name;
			//	shm_update_a41(OFFSET_SYSTEM+63, $cert_name);
			}
		}

		//send_command(M_CGI_CHANGE_HTTPS, 0, 0, 0, 0);

		echo '<meta http-equiv="Refresh" content="0; URL=setup_network_https.cgi">';
	}
	else if ( $_REQUEST['action'] == 'remove' )
	{
		//exec("rm -rf /mnt/nand/user.pem", $ret);
		usleep(100000);

		//$GLOBAL['https_conf']['cert_flag'] = 0;
		//shm_update_i(OFFSET_SYSTEM+59, 0);
		
		//$GLOBAL['https_conf']['cert_name'] = "";
		//shm_update_i(OFFSET_SYSTEM+63, $GLOBAL['https_conf']['cert_name']);
		
		//send_command(M_CGI_CHANGE_HTTPS, 0, 0, 0, 0);
		
	}
	exit;
}/*
else if ( $_REQUEST['submenu'] == 'snmp' )
{
	if ( $_REQUEST['action'] == 'view' )
	{
		echo '<meta http-equiv="Refresh" content="0; URL=setup_network_snmp.cgi">';
	}
	else if ( $_REQUEST['action'] == 'apply' )
	{
	change_snmp();
  	$ipc_sock = new IPCSocket();
    $ipc_sock->Connection($GLOBALS['net_conf'], CMD_SET_NETWORK_CONFIGURATION);
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
		show_post_ng();

	exit;
}*/
else if ( $_REQUEST['submenu'] == 'rtsp' )
{
	if ( $_REQUEST['action'] == 'view' )
	{
//		echo '<meta http-equiv="Refresh" content="0; URL=setup_network_snmp.cgi">';
	}
	else if ( $_REQUEST['action'] == 'apply' )
	{
		change_rtsp();
  	$ipc_sock = new IPCSocket();
    $ipc_sock->Connection($GLOBALS['net_conf'], CMD_SET_NETWORK_CONFIGURATION);
    if ($ipc_sock->dataInfo['ErrorCode']['value'] == APP_OK)
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
//------------------------------------------------------------------------------------------------------
// 	Sdk
//------------------------------------------------------------------------------------------------------
header("Content-Type: text/plain");
ob_end_clean ();
if(isset($_REQUEST['msubmenu']))
{
if ( $_REQUEST['msubmenu'] == 'ip' )
{
	if ( $_REQUEST['action'] == 'view' )
	{
		ip_view_post();
	}
	else if ( $_REQUEST['action'] == 'apply' )
	{
/*		if (CheckIP() == false || CheckPortDuplicate() == false)
		{
			show_post_ng();
			exit;
		}*/
		  $return_value = APP_NONE;
      if(change_hostname() == 0)
      {
 				$ipc_sock = new IPCSocket();
				$ipc_sock->Connection($GLOBALS['system_conf']->DeviceInfo, CMD_SET_DEVICE_INFORMATION);
				$return_value = $ipc_sock->dataInfo['ErrorCode']['value'];
				if ($ipc_sock->dataInfo['ErrorCode']['value'] != APP_OK)
				{
				  show_post_ng();
				  exit;
				}
      }
		
		  if(change_ip() == 0)
		  {
  	  	$ipc_sock = new IPCSocket();
  	    $ipc_sock->Connection($GLOBALS['net_conf'], CMD_SET_NETWORK_CONFIGURATION);
  	    if ($ipc_sock->dataInfo['ErrorCode']['value'] == APP_OK)
  	    {
  	    	show_post_ok();
  	    }
  	    else if ($ipc_sock->dataInfo['ErrorCode']['value'] == APP_NONE)
  	    {
     	    if ($return_value  == APP_OK)
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
      else
      {
  	    if ($return_value  == APP_OK)
  	    {
  	    	show_post_ok();
  	    }
      }
	}
	else if ( $_REQUEST['action'] == 'get_dns' )
	{
		$fp = fopen("/etc/resolv.conf", "r");

		$i = 0;
		while(!feof($fp)){
			if($i < 2) {
				$line = fgets($fp);
				if ( strlen($line) > 0 ) {
					$word = explode(' ', $line);
					$dns[$i] = str_replace("\n", "", $word[1]);
				} else {
					$dns[$i] = "";
				}
				$i++;
			} else {
				break;
			}
		}

		fclose($fp);

		$response['dns_pre'] = $dns[0];
		$response['dns_alt'] = $dns[1];

		echo json_encode( $response );
	}
	else
		show_post_ng();
	
	exit;
}
else if ( $_REQUEST['msubmenu'] == 'zeroconfig' )
{
	if ( $_REQUEST['action'] == 'view' )
	{
		zeroconfig_view_post();
	}
	else if ( $_REQUEST['action'] == 'apply' )
	{
	    change_zeroconfig();
    	$ipc_sock = new IPCSocket();
	    $ipc_sock->Connection($GLOBALS['net_conf'], CMD_SET_NETWORK_CONFIGURATION);
		
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
		show_post_ok();
	
	exit;
}
else if ( $_REQUEST['msubmenu'] == 'upnp' )
{
	if ( $_REQUEST['action'] == 'view' )
	{
		upnp_view_post();
	}
	else if ( $_REQUEST['action'] == 'apply' )
	{
	    change_upnp();
    	$ipc_sock = new IPCSocket();
	    $ipc_sock->Connection($GLOBALS['net_conf'], CMD_SET_NETWORK_CONFIGURATION);
		
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
		show_post_ok();
	
	exit;
}
else if ( $_REQUEST['msubmenu'] == 'snmp' )
{
	if ( $_REQUEST['action'] == 'view' )
	{
		snmp_view_post();
	}
	else if ( $_REQUEST['action'] == 'apply' )
	{   
	    change_snmp();
    	$ipc_sock = new IPCSocket();
	    $ipc_sock->Connection($GLOBALS['net_conf'], CMD_SET_NETWORK_CONFIGURATION);
		
	    if ($ipc_sock->dataInfo['ErrorCode']['value'] == APP_OK)
	    {
    		show_post_ok();
	    }
	    else
	    {
	   		show_post_ng();
	    }	
	     echo "result : ".$ipc_sock->dataInfo['ErrorCode']['value'];		
	}
	else
		show_post_ng();
	
	exit;
}
else if ( $_REQUEST['msubmenu'] == 'ddns' )
{
	if ( $_REQUEST['action'] == 'view' )
	{
		ddns_view_post();
	}
	else if ( $_REQUEST['action'] == 'apply' )
	{
	  change_ddns();
  	$ipc_sock = new IPCSocket();
    $ipc_sock->Connection($GLOBALS['net_conf'], CMD_SET_NETWORK_CONFIGURATION);
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
		show_post_ng();
	
	exit;
}
else if ( $_REQUEST['msubmenu'] == 'srtp' )
{
	if ( $_REQUEST['action'] == 'view' )
	{
		srtp_view_post();
	}
	else if ( $_REQUEST['action'] == 'apply' )
	{
	  	change_srtp();
		$ipc_sock = new IPCSocket();
		$ipc_sock->Connection($GLOBALS['net_conf']->SRTPSetting, CMD_SET_SRTP);
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
		show_post_ng();
	
	exit;
}
else if ( $_REQUEST['msubmenu'] == 'https' )
{
	if ( $_REQUEST['action'] == 'view' )
	{
		https_view_post();
	}
	else if ( $_REQUEST['action'] == 'apply' )
	{
		show_post_ng();
	}
	else
		show_post_ng();
	
	exit;
}
else if ( $_REQUEST['msubmenu'] == 'rtsp' )
{
	if ( $_REQUEST['action'] == 'view' )
	{
		view_rtsp();
	}
	else if ( $_REQUEST['action'] == 'apply' )
	{
		if (CheckPortDuplicate() == false)
		{
			show_post_ng();
			exit;
		}
		change_rtsp();
		$ipc_sock = new IPCSocket();
		$ipc_sock->Connection($GLOBALS['net_conf'], CMD_SET_NETWORK_CONFIGURATION);
		if ($ipc_sock->dataInfo['ErrorCode']['value'] == APP_OK)
		{
			show_post_ok();
		}
		else
		{
			show_post_ng();
		}				
	}
	else if ( $_REQUEST['action'] == 'session_info' )
	{
		$shm_id = shmop_open(KEY_SM_RTSP_CONNECTIONS, "a", 0, 0);
		if (!$shm_id) exit;
		
		$data = shmop_read($shm_id, 0, 4);
		$rtsp_connections = unpack("i1count", $data);

		$index = 0;
		if ($rtsp_connections['count'] > 0)
		{
			for($i=0; $i<20; $i++)
			{
				$data = shmop_read($shm_id, 4 + ($i)*16, 16);
				$rtsp_connections[$index] = unpack("i1sock/i1addr/i1port/i1type", $data);
				$type = ($rtsp_connections[$index]['type'] == 0) ? "TCP" : "UDP";
				if ( $rtsp_connections[$index]['sock'] >= 0)
				{
					echo $index.' '.long2ip($rtsp_connections[$index]['addr']).' '.$rtsp_connections[$index]['port'].' '.$type."\r\n";
					$index++;
				}
			}
			echo $index."\r\n";
		}

		shmop_close($shm_id);	
	}
	else
		show_post_ng();

	exit;
}
}

show_post_ng();

?>
