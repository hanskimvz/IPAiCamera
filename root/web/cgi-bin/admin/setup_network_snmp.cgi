<?
require('../_define.inc');
require('../class/network.class');

$net_conf = new CNetworkConfiguration();

//--- ip
function getsnmpInfo($name)
{	
	echo $name."['Enabled_V1']="	.$GLOBALS['net_conf']->SnmpSetting->Snmpv1->Enabled_V1."\r\n";
	
	echo $name."['Enabled_V2']="	.$GLOBALS['net_conf']->SnmpSetting->Snmpv2->Enabled_V2."\r\n";
	echo $name."['RoComName']='"	.trim($GLOBALS['net_conf']->SnmpSetting->Snmpv2->RoComName)."';\r\n";
	echo $name."['RwComName']='"	.trim($GLOBALS['net_conf']->SnmpSetting->Snmpv2->RwComName)."';\r\n";
	
	echo $name."['Enabled_Trap']="	.$GLOBALS['net_conf']->SnmpSetting->Snmpv2->Enabled_Trap."\r\n";
	echo $name."['TrapServer']='"	.trim($GLOBALS['net_conf']->SnmpSetting->Snmpv2->TrapServer)."';\r\n";
	echo $name."['TrapComName']='"	.trim($GLOBALS['net_conf']->SnmpSetting->Snmpv2->TrapComName)."';\r\n";
		
	echo $name."['RoEnabled_V3']="	.$GLOBALS['net_conf']->SnmpSetting->Snmpv3->RoEnabled_V3."\r\n";	
	echo $name."['RoUserName']='"	.trim($GLOBALS['net_conf']->SnmpSetting->Snmpv3->RoUserName)."';\r\n";
	echo $name."['RoSecuLevel']="	.$GLOBALS['net_conf']->SnmpSetting->Snmpv3->RoSecuLevel."\r\n";
	echo $name."['RoAuthAlg']='"	.trim($GLOBALS['net_conf']->SnmpSetting->Snmpv3->RoAuthAlg)."';\r\n";
	echo $name."['RoAuthName']='"	.trim($GLOBALS['net_conf']->SnmpSetting->Snmpv3->RoAuthName)."';\r\n";
	echo $name."['RoPriAlg']='"		.trim($GLOBALS['net_conf']->SnmpSetting->Snmpv3->RoPriAlg)."';\r\n";
	echo $name."['RoPriName']='"	.trim($GLOBALS['net_conf']->SnmpSetting->Snmpv3->RoPriName)."';\r\n";
	
	echo $name."['RwEnabled_V3']="	.$GLOBALS['net_conf']->SnmpSetting->Snmpv3->RwEnabled_V3."\r\n";	
	echo $name."['RwUserName']='"	.trim($GLOBALS['net_conf']->SnmpSetting->Snmpv3->RwUserName)."';\r\n";
	echo $name."['RwSecuLevel']="	.$GLOBALS['net_conf']->SnmpSetting->Snmpv3->RwSecuLevel."\r\n";
	echo $name."['RwAuthAlg']='"	.trim($GLOBALS['net_conf']->SnmpSetting->Snmpv3->RwAuthAlg)."';\r\n";
	echo $name."['RwAuthName']='"	.trim($GLOBALS['net_conf']->SnmpSetting->Snmpv3->RwAuthName)."';\r\n";
	echo $name."['RwPriAlg']='"		.trim($GLOBALS['net_conf']->SnmpSetting->Snmpv3->RwPriAlg)."';\r\n";
	echo $name."['RwPriName']='"	.trim($GLOBALS['net_conf']->SnmpSetting->Snmpv3->RwPriName)."';\r\n";
}

?>
<!DOCTYPE html>
<html>
	<head>
		<meta content="text/html; charset=utf-8" http-equiv="Content-Type">
		<title>SNMP CONFIGURATION</title>
	</head>

	<body onload="onLoadPage();" oncontextmenu="return false" onselectstart="return false"  ondragstart="return false">
		<div class="contentTitle" tkey="setup_snmp_config">SNMP configuration</div>
		<div class="snmp content height21">		
			<label class="maintitle">SNMP v1/v2c</label>	
			<label class="subtitle"><span tkey="SNMPv1"></span></label>
			<input type="radio" value="0" name="Enabled_V1"  id="Enabled_V1_1" > <label for="Enabled_V1_1"></label><span tkey="off"></span>
			<input type="radio" value="1" name="Enabled_V1"  id="Enabled_V1_2" > <label for="Enabled_V1_2" ></label> <span tkey="on"></span><br>
			
			<label class="subtitle"><span tkey="SNMPv2c"></span></label>
			<input type="radio" value="0" name="Enabled_V2"  id="Enabled_V2_1" > <label for="Enabled_V2_1"></label><span tkey="off"></span>
			<input type="radio" value="1" name="Enabled_V2"  id="Enabled_V2_2" > <label for="Enabled_V2_2" ></label> <span tkey="on"></span><br>
						
			<label class="subtitle" tkey="snmp_readcomm"><span>Read ommunity</span></label>
			<input id="RoComName" type="text" maxlength="30" class="inputText"><br>			
			<label class="subtitle" tkey="snmp_writecomm"><span>Write community</span></label>
			<input id="RwComName" type="text" maxlength="30" class="inputText"><br>	

			<label class="subtitle"><span tkey="SnmpTrap"></span></label>
			<input type="radio" value="0" name="Enabled_Trap"  id="Enabled_Trap_1" > <label for="Enabled_Trap_1"></label><span tkey="off"></span>
			<input type="radio" value="1" name="Enabled_Trap"  id="Enabled_Trap_2" > <label for="Enabled_Trap_2" ></label> <span tkey="on"></span><br>				
			<label class="subtitle" tkey="TrapAddress"><span></span></label>
			<input id="TrapServer" type="text" maxlength="30" class="inputText"><br>	
			<label class="subtitle" tkey="TrapCommunity"><span>Write community</span></label>
			<input id="TrapComName" type="text" maxlength="30" class="inputText" tkey="ASD"><br>		
		</div>
		
		<div class="snmp content height21" >
			<label class="maintitle">SNMP v3 </label>
			<label class="subtitle"><span tkey="setup_relay_out_mode"></span></label>
			<div class="select">
				<select id="Snmpv3mode"> 
					<option value="0" tkey="read">Read</option>
					<option value="1" tkey="read_write">Read/Write</option>
				</select>
			</div><br>
		</div>
			
		<div class="snmp content height21" >	
			<div id="ROSNMP3_CONTENTS">			
				<label class="subtitle"><span tkey="setup_motion_activation"></span></label>
				<input type="radio" value="0" name="RoEnabled_V3"  id="RoEnabled_V3_1" > <label for="RoEnabled_V3_1"></label><span tkey="off"></span>
				<input type="radio" value="1" name="RoEnabled_V3"  id="RoEnabled_V3_2" > <label for="RoEnabled_V3_2"></label><span tkey="on"></span><br>

				<label class="subtitle" tkey="read_name">Read Username</label>
				<input id="RoUserName" type="text" maxlength="30" class="inputText"><br>
				<label class="subtitle" tkey="snmp_securitylevel">Security Level</label>
				<div class="select">
					<select id="RoSecuLevel"> 
						<option value="0" tkey="no_auto_priv" >no auth, no priv</option>
						<option value="1" tkey="auto_nopriv"> auth, no priv</option>
						<option value="2" tkey="auto_priv"> auth, priv</option>
					</select>
				</div><br>
				<label class="subtitle" tkey="snmp_Authentication">Authentication Algorithm</label>
				<div class="select">
					<select id="RoAuthAlg"> 
						<option value="0">MD5</option>
						<option value="1">SHA</option>
					</select>
				</div><br>
				<label class="subtitle" tkey="snmp_Authentication_pass">Authentication Password</label>
				<input id="RoAuthName" type="text" maxlength="30" class="inputText"><br>			
				<div id="Ro_Private_Key">
					<label class="subtitle" tkey="snmp_Private_Key">Private-Key Algorithm</label>
					<div class="select">
						<select id="RoPriAlg"> 
							<option value="0">DES</option>
							<option value="1">AES</option>
						</select>
					</div><br>
					<label class="subtitle" tkey="snmp_Private_pass">Private-Key Password</label>
					<input id="RoPriName" type="text" maxlength="30" class="inputText"><br>
				</div>
			</div>
			<div id="RWSNMP3_CONTENTS">
				<label class="subtitle"><span tkey="setup_motion_activation"></span></label>
				<input type="radio" value="0" name="RwEnabled_V3"  id="RwEnabled_V3_1" > <label for="RwEnabled_V3_1"></label><span tkey="off"></span>
				<input type="radio" value="1" name="RwEnabled_V3"  id="RwEnabled_V3_2" > <label for="RwEnabled_V3_2"></label><span tkey="on"></span><br>
				
				<label class="subtitle" tkey="write_name">Write/Rread Username</label>
				<input id="RwUserName" type="text" maxlength="30" class="inputText"><br>
				<label class="subtitle" tkey="snmp_securitylevel">Security Level</label>
				<div class="select">
					<select id="RwSecuLevel"> 
						<option value="0" tkey="no_auto_priv">no auth, no priv</option>
						<option value="1" tkey="auto_nopriv"> auth, no priv</option>
						<option value="2" tkey="auto_priv"> auth, priv</option>
					</select>
				</div><br>
				<label class="subtitle" tkey="snmp_Authentication">Authentication Algorithm</label>
				<div class="select">
					<select id="RwAuthAlg"> 
						<option value="0">MD5</option>
						<option value="1">SHA</option>
					</select>
				</div><br>
				<label class="subtitle" tkey="snmp_Authentication_pass">Authentication Password</label>
				<input id="RwAuthName" type="text" maxlength="30" class="inputText"><br>
				
				<label class="subtitle" tkey="snmp_Private_Key">Private-Key Algorithm</label>
				<div class="select">
					<select id="RwPriAlg"> 
						<option value="0">DES</option>
						<option value="1">AES</option>
					</select>
				</div><br>
				<label class="subtitle" tkey="snmp_Private_pass">Private-Key Password</label>
				<input id="RwPriName" type="text" maxlength="30" class="inputText"><br>
			</div>			
		</div>			
		</div>
		<center>
			<button id="btOK" class="button" tkey="apply">Apply</button>
		</center>

		<script>
			var SnmpInfo = new Object();
		<? 
				getsnmpInfo("SnmpInfo"); 
		?>
		</script>
		<script src="./setup_network_snmp.js"></script>
	</body>
</html>
