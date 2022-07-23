
<?
require('../_define.inc');
require('../class/capability.class');
require('../class/network.class');
require('../class/system.class');
$shm_id      = shmop_open(KEY_SM_SHARED_CONFIG, "a", 0, 0);
$system_caps = new CCapability($shm_id);
$system_conf = new CSystemConfiguration($shm_id);
$net_conf    = new CNetworkConfiguration($shm_id);
$cert   = $system_conf->Security->Certificates;
shmop_close($shm_id);
?>
<!DOCTYPE html>
<html>
	<body>
		<div class="contentTitle">
			<span tkey="https_configuration"></span>
			<div class="contentNotice margin_top_10">
				<span class="caution" tkye="setup_notice"></span>
				<ul class="padding_left30">
					<li><span tkey="setup_msg_https_certificate_msg"></span></li>
				</ul>
			</div> 
		</div>
		<div class="content">
			<label class="maintitle" tkey="Certificates"></label>
			<label class="subtitle" tkey="Certificate"></label>
			<div class="select">
				<select id="certList">
					<option value="0" tkey="setup_none">NONE</option>
				</select>
			</div>
		</div>
		<div class="content">
			<label class="maintitle" tkey="setup_https_connect_policy"></label>
			<label class="subtitle">WEB</label>	
			<div class="select">
				<select name="connect_policy" id="admin_policy"></select>
			</div><br>
			<!-- 
			<label class="subtitle" tkey="Operator"></label>	
			<div class="select">
				<select name="connect_policy" id="operator_policy"></select>
			</div><br>
			<label class="subtitle" tkey="Viewer"></label>	
			<div class="select">
				<select name="connect_policy" id="viewer_policy"></select>
			</div><br>
			-->
			<label class="subtitle">ONVIF</label>	
			<div class="select">
				<select name="protocol_policy" id="onvif_policy"></select>
			</div><br>		
			<label class="subtitle">RTSP OVER HTTP</label>	
			<div class="select">
				<select name="protocol_policy" id="rtsp_policy"></select>
			</div><br>		
		</div>
<? if ( $system_caps->getOEM() == 12) { ?>			
<? if( $GLOBALS['system_conf']->Security->Https->ConnectionPolicy[0]->value == 1 || $GLOBALS['system_conf']->Security->Https->ConnectionPolicy[3]->value == 1 || $GLOBALS['system_conf']->Security->Https->ConnectionPolicy[4]->value == 1) { ?>	
		<label class="caution" id="core_caution">The live video viewed in the browser will use RTSP over TCP. This data maybe un-encrypted</label>
<? } ?>			
<? } ?>				
		<center>
			<button id="btnApply"class="button" tkey="apply"></button>
		</center>
	</body>
	<script>
		var certInfo= <? show_certificates($GLOBALS['cert']->Certificate, true);?>;
		var httpsInfo = <? show_https($GLOBALS['system_conf']->Security->Https, true); ?>;
		var APP_ERR_USED_CERTIFICATE = <? echo APP_ERR_USED_CERTIFICATE ?>;
		var APP_ERR_INCOMPLETE_CONFIGURATION = <? echo APP_ERR_INCOMPLETE_CONFIGURATION ?>;
	</script>
	<script src="./setup_security_https.js"></script>
</html>
