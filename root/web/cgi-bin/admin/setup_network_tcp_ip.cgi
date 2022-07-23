<?
require('../_define.inc');
require('../class/network.class');
require('../class/system.class');

$system_conf = new CSystemConfiguration();
$net_conf = new CNetworkConfiguration();

//--- ip
function getNetworkInfo($name)
{	
	echo $name."['hostname']='"			.trim($GLOBALS['system_conf']->DeviceInfo->OnvifConf->hostname)."';\r\n";
	echo $name."['ip_type']="			.$GLOBALS['net_conf']->IPv4->Type."\r\n";
	echo $name."['mac']='"				.trim($GLOBALS['net_conf']->HwAddress)."';\r\n";
	echo $name."['ip']='"				.trim(($GLOBALS['net_conf']->IPv4->Type == 0)?$GLOBALS['net_conf']->IPv4->StaticIpAddr:$GLOBALS['net_conf']->IPv4->DynamicIpAddr)."';\r\n";
	echo $name."['ip_static']='"		.trim($GLOBALS['net_conf']->IPv4->StaticIpAddr)."';\r\n";
	echo $name."['ip_dynamic']='"		.trim($GLOBALS['net_conf']->IPv4->DynamicIpAddr)."';\r\n";
	echo $name."['sm']='"				.trim($GLOBALS['net_conf']->IPv4->SubnetMask)."';\r\n";
	echo $name."['gw']='"				.trim($GLOBALS['net_conf']->IPv4->Gateway)."';\r\n";
	echo $name."['mtu']='"				.trim($GLOBALS['net_conf']->MTUSetting->Value)."';\r\n";
	echo $name."['dns_pre']='"				.trim(($GLOBALS['net_conf']->DNS->Type == 0)?$GLOBALS['net_conf']->DNS->DNSManualAddr0:$GLOBALS['net_conf']->DNS->DNSDynamicAddr0)."';\r\n";
	echo $name."['dns_alt']='"				.trim(($GLOBALS['net_conf']->DNS->Type == 0)?$GLOBALS['net_conf']->DNS->DNSManualAddr1:$GLOBALS['net_conf']->DNS->DNSDynamicAddr1)."';\r\n";
	echo $name."['web_port']="		.$GLOBALS['net_conf']->Protocols->Protocol[0]->Port.";\r\n";
	//echo $name."['https_enabled']="		.$GLOBALS['net_conf']->Protocols->Protocol[2]->Enabled.";\r\n";
	echo $name."['https_port']="		.$GLOBALS['net_conf']->Protocols->Protocol[2]->Port.";\r\n";
	echo $name."['control_port']="	."0".";\r\n";
	echo $name."['video_port']="		."0".";\r\n";
	echo $name."['at_port']="			."0".";\r\n";
	echo $name."['ar_port']="			."0".";\r\n";
	echo $name."['rtsp_port']="		.$GLOBALS['net_conf']->Protocols->Protocol[1]->Port.";\r\n";
	echo $name."['ipv6_enable']="		."0".";\r\n";

}
?>

<!DOCTYPE html>
<html>
	<head>
		<meta content="text/html; charset=utf-8" http-equiv="Content-Type">

		<title>network settings</title>

	</head>

	<body onload="onLoadPage();" oncontextmenu="return false" onselectstart="return false"  ondragstart="return false">
		<div class="contentTitle"><span tkey="Network_Settings"></span></div>
		<div class="content">
			<label class="subtitle"><span tkey="setup_network_hostname"></span></label>
			<input id="hostname" type="text"><br>		
		</div>
		<div class="content">
			<label class="maintitle"><span tkey="setup_network_type"></span></label>
			<input id='static' type="radio" value=0 name="ip_type">
			<label for="static"></label><span tkey="static"></span>
			<input id="dhcp" type="radio" value=1 name="ip_type">
			<label for="dhcp"></label><span tkey="dynamic"></span>
		</div>
		<div class="content" >
		<div id="static_ip_setting" >
			<label class="maintitle"><span tkey="ipsetup"></span></label>
			<label class="subtitle"><span tkey="setup_ipaddress"></span></label>
			<input id="ip" type="text"><br>

			<label class="subtitle"><span tkey="setup_subnet_mask"></span></label>
			<input id="sm" type="text"><br>

			<label class="subtitle"><span tkey="setup_default_gateway"></span></label>
			<input id="gw" type="text"><br>

			<label class="subtitle"><span tkey="setup_preferred_dnsserver"></span></label>
			<input id="dns_pre" type="text"><br>

			<label class="subtitle"><span tkey="setup_alternate_dnsserver"></span></label>
			<input id="dns_alt" type="text"><br>
			
	  </div>
		</div>
		<div class="content" id= "network_port">
			<label class="maintitle"><span tkey="portsetup"></span></label>
			
			<label  class="subtitle"><span tkey="setup_http_port"></span></label>
			<input id="web_port" type="text" class="short" ><span tkey="http_defalut_text" ></span><br>	
<? if( ($GLOBALS['system_conf']->SystemOption & SYSTEM_OPTION_UI_FIXED_DATE_20160504) == 0) { ?>			
			<label class="subtitle" tkey="setup_https_port"></label>
			<input id="https_port" type="text" class="short" ><span tkey="https_defalut_text"></span><br>
<? } ?>			
		  	<!-- 
		    <div id= "TBD">
				<label class="subtitle">HTTPS Port</label>
				<input id="https_port" type="text" class="inputText">(TBD)<br>	
				
				<label class="subtitle">Control Port</label>
				<input id="control_port" type="text" class="inputText">(TBD)<br>
					
				<label class="subtitle">Video Port</label>
				<input id="video_port" type="text" class="inputText">(TBD)<br>
				
				<label class="subtitle">Audio Transmit Port</label>
				<input id="at_port" type="text" class="inputText">(TBD)<br>
				
				<label class="subtitle">Audio Receive Port</label>
				<input id="ar_port" type="text" class="inputText">(TBD)<br>
			</div>	 
			-->
			<label class="subtitle"><span tkey="setup_rtsp_port"></span></label>
			<input id="rtsp_port" type="text" class="short" ><spane tkey="rtsp_defalut_text"></span>br>
			
		</div>
		<div class="content" id= "mtu_setting">
		  <label class="maintitle"><span>MTU Setup</span></label>
			<label class="subtitle"><span>MTU</span></label>
			<input id="mtu" type="text" class="short"><span tkey="mtu_default_text" ></span><br>				
		</div>		
		<!--
		<div class="content">
			<label class="maintitle"><span tkey="setup_https"></span></label>
			<label class="subtitle"><span tkey="setup_enable"></span></label> 
			<input id='https_on' type="radio" value=1 name="https_enabled">
			<label for="https_on"></label><span tkey="on"></span>
			<input id="https_off" type="radio" value=0 name="https_enabled">
			<label for="https_off"></label><span tkey="off"></span><br>
		</div>
		-->
		<!-- div class="content">
		<label class="maintitle" colspan="2">IPv6 Setting</label>
				<input type="checkbox" id="ip6" name="chkIPv6" value="1" ></td>
				<label for="ip6"></label><span></span>Enable<br>
		</div> -->
   
		<center>
			<button id="btOK" class="button" ><span tkey="apply"></span></button>
		</center>
		<script type="text/javascript">
			var NetworkInfo = new Object();
		<? 
				getNetworkInfo("NetworkInfo"); 
		?>
		</script>
		<script src="./setup_network_tcp_ip.js"></script>
	</body>
</html>
