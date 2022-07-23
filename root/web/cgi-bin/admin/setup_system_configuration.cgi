<?
require('../_define.inc');
require('../class/system.class');
require('../class/capability.class');

$shm_id		= shmop_open(KEY_SM_SHARED_CONFIG, "a", 0, 0);
$system_caps = new CCapability($shm_id);
shmop_close($shm_id);
$get_oem = $system_caps->getOEM();
?>
<!DOCTYPE html>
<html>
	<head>
		<meta content="text/html; charset=utf-8" http-equiv="Content-Type">
	</head>
	<body>
		<div class="contentTitle">
			<span tkey="setup_system_configuration"></span>
			<div class="contentNotice margin_top_10">
				<span class="caution" tkye="setup_notice"></span>
				<ul class="padding_left30">
					<li><span tkey="setup_system_confbackup_message1"></span></li>
					<li><span tkey="setup_system_confbackup_message2"></span></li>
<? if ( $get_oem == 2) { ?>					
					<span tkey="setup_system_confbackup_message3_dw"></span>
<? } else { ?>
					<span tkey="setup_system_confbackup_message3"></span>
<? } ?>
				</ul>
			</div> 
		</div> 
		<div class="content">
			<label class="subtitle">Mode</label>
			<input type="radio" name="config" value="1" id="config_download">
			<label for="config_download"></label><span tkey="setup_download"></span>
			<input type="radio" name="config" value="0" id="config_upload" checked>
			<label for="config_upload"></label><span tkey="setup_upload"></span><br>
			<label class="subtitle">Backup Key</label>
			<input id="backup_key" type="password" onfocus="this.value=''"><br>
			<div id="file_div" style="display;">
				<div class="subtitle bottom_5">Select File</div>
				<div id="file" class="filebox disign_sel"> 
					<input type="file" name="FileInput" id="FileInput" />
					<label for="FileInput" tkey="setup_system_selectfile" >Select File</label>
				</div>
				<br><label id="file_Info" style="margin-left:140px;display:none;"></label>
				<br><label id="file_status" style="margin-left:140px;display:none;"></label>
			</div>
		</div>
		<center>
			<button id="btOK" class="button"><span tkey="apply"></span></button>
		</center>
	</body>
	<script src="./setup_system_configuration.js"></script>
</html>
