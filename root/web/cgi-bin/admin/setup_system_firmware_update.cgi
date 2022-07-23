<html>
<head>
<? if(preg_match('/msie [1-10]/',$_SERVER['HTTP_USER_AGENT']) == false &&
      preg_match('/Trident\/[4-6]/',$_SERVER['HTTP_USER_AGENT']) == false) { ?>  
<meta http-equiv="x-ua-compatible" content="IE=10">
<? }  ?>
<title>FIRMWARE UPDATE</title>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
</head>
<body oncontextmenu="return false" ondragstart="return false">
	<form action="./code_update" method="post" enctype="multipart/form-data" id="MyUploadForm">
		<div class="contentTitle update"><span tkey="setup_system_update_config"></span>
			<div class="contentNotice margin_top_10">
				<span class="caution" tkye="setup_notice"></span>
				<ul class="padding_left30">
					<li><span tkey="setup_system_update_message1"></span></li>
					<li><span tkey="setup_system_update_message2"></span></li>
					<li><span tkey="setup_system_update_message3"></span></li>
				</ul>
			</div> 
		</div>
		<div class="content marginjpn1">
			<div class="maintitle"><span tkey="setup_system_version_infomation"></span></div>
			<div class="subtitle"><span tkey="setup_system_system"></span></div>
			<label id="fwInfo"></label><br>
			<div id = "camera_ver" style="display:none;">
				<div class="subtitle"><span tkey="setup_camera"></span></div>
				<label id="camInfo"></label><br>
			</div>
			<div id = "motion_isp" style="display:none;">
				<div class="subtitle"><span tkey="motionfw"></span></div>
				<label id="motionInfo"></label><br>
				<div class="subtitle"><span tkey="ispfw"></span></div>
				<label id="ispInfo"></label><br>
			</div>
			<div id = "Hardware_Revision" style="display:none;">
				<div class="subtitle">Hardware Revision</div>
				<label id="hwInfo"></label><br>
			</div>
		</div>
		<div class="content">
			<div class="maintitle"><span tkey="setup_system_webupdate"></span></div>
			<div class="subtitle bottom_5"><span tkey="setup_system_firmwarefile"></span></div>
			<div id="file" class="filebox disign_sel">			
			<input type="file" name="FileInput" id="FileInput" />
			<label for="FileInput" tkey="setup_system_selectfile" >Select File</label>
			</div><br>
			<label id="fwfileInfo" style="display:none;"></label>
			<label id="fw_status"></label>
			<div id="progressbox" >
				<div id="progressbar" class="stripes"></div >
				<div id="progress_text"></div>
				<div id="statustxt">0%</div>
			</div>
		</div>
		<center>
			<!--<input type="submit" class="button" id="submit-btn" value="Start F/W update" tkey="setup_system_startfwupdate" disabled /> -->
			<button class="button long" id="submit-btn" disabled><span tkey="setup_system_startfwupdate"></span></button>
		</center>	
	</form>
		<div id="DW" class="VCAFTP">
			<div class="content">
				<div class="maintitle" id="ftpinfomain" tkey="setup_ftp_user_info">FTP user information</div>
				<div id="activation_ui" class="showonlyvca">
					<label class="subtitle"><span tkey="autoup_activation"></span></label>
					<input type="radio" name="autoupdate" value=0 id="autoup_enabled_off"><label for="autoup_enabled_off"></label> <span tkey="off"></span>
					<input type="radio" name="autoupdate" value=1 id="autoup_enabled_on"><label for="autoup_enabled_on"></label><span tkey="on"></span><br>
				</div>
				<div class="subtitle" tkey="setup_ftp_serveraddress">ftp address</div>
				<input id="address" type="text"><br>
				<div class="subtitle" tkey="setup_ftp_port">port</div>
				<input id="port" type="text"><br>
				<div class="subtitle" tkey="setup_user_id">ID</div>
				<input id="id" type="text"><br>
				<div class="subtitle" tkey="setup_user_passwd" >password</div>
				<input id="password" type="password"><br>
				<div class="subtitle" tkey="setup_upload_path">location</div>
				<input id="location" type="text"><br>
				<div class="showonlyvcain subtitle" tkey="setup_autoup_interval">Check interval</div>
				<input id="interval" class="showonlyvcain" type="text"><label for="interval" class="showonlyvcain"><span tkey="setup_hours"></span> (1-720)</label><br>
				<!-- <div id="ftp_progressbox" style="display: none">
					<div class="subtitle">Status</div>
					<label id="fw_status"></label><br>
					<div id="ftp_progress_box" class="progress-bar stripes">
						<span id="ftp_progressbar" style="width:0%"></span>
					</div>
				</div> -->
				<div id="ftp_progressbox" >
					<div id="ftp_progressbar" class="stripes"></div >
					<div id="ftp_progress_text"></div>
					<div id="ftp_statustxt">0%</div>
				</div>
			</div>
			<center>
				<button id="save" class="button" tkey="setup_save">save</button>
				<button id="cancle" class="button" tkey="setup_cancel">cancel</button>
				<button id="upgrade" class="button" value="check" tkey="check">check</button>
			</center>
			</div>
		</div>
	</div>
</body>
<script>
	var fwInfo,fwInfo2;
	var camInfo;
    var ivfwInfo;
    var jcifwInfo;
<?
require("../_define.inc");
require("../class/system.class");
require("../class/capability.class");
$system_conf = new CSystemConfiguration();
$system_caps = new CCapability();
?>
    var capInfo = <? $GLOBALS['system_caps']->getCapability() ?>;
<?
printf("var MAX_FW_SIZE=%d;\r\n", MAX_FW_SIZE);
printf("var MAX_CV22_FW_SIZE=%d;\r\n", MAX_CV22_FW_SIZE);
	
	echo "fwInfo='". trim($system_conf->DeviceInfo->BuildVersion)."_". trim($system_conf->DeviceInfo->FirmwareVersion)."';\r\n;";
	echo "fwInfo2='". trim($system_conf->DeviceInfo->FirmwareVersion)."_". trim($system_conf->DeviceInfo->BuildVersion)."';\r\n;";
    echo "ivfwInfo='".trim($system_conf->DeviceInfo->FirmwareVersion)."';\r\n;";
    echo "jcifwInfo='".trim($system_conf->DeviceInfo->FirmwareVersion)."';\r\n;";
	echo "camInfo='". trim($system_conf->DeviceInfo->ModuleVersion) ."';\r\n;";
?>
	var ftpInfo = <? show_ftp($GLOBALS['system_conf']->FtpUpgrade); ?>;
</script>
<script type="text/javascript" src="/js/jquery.form.min.js"></script>
<script type="text/javascript" src="./setup_system_firmware_update.js"></script>
</html>
