<?
require('../_define.inc');
require('../class/system.class');
require("../class/event.class");
$shm_id = shmop_open(KEY_SM_SHARED_CONFIG, "a", 0, 0);
$event_conf = new CEventConfiguration($shm_id);
$system_conf = new CSystemConfiguration($shm_id);
?>
<html>
<head>
	<title>Storage Configuration</title>
</head> 
<body oncontextmenu="return false" onselectstart="return false"  ondragstart="return false">
	<!-- default list page 	 -->
	<div>
		<div class="contentTitle"><span tkey="setup_storage_config"></span>
			<div class="contentNotice">
				<span class="caution" tkey="setup_notice"></span>
				<ul class="padding_left30">
					<li><span tkey="storage_for_sdcard_message1"></span></li>
				</ul>
			</div> 
		</div>
		<div  id="storage_list" class="content">
			<label class="maintitle"><span tkey="setup_storage_list"></span></label>
			<div class="result_table">
				<table class="result_filed">
					<thead>
						<tr class="headline">
							<th><span tkey="setup_name"></span></th>
							<th><span tkey="setup_mounted"></span></th>
							<th><span tkey="setup_size"></span></th>
							<th><span tkey="setup_storage_usedsize"></span></th>
							<th><span tkey="setup_storage_available"></span></th>
						</tr>
					</thead>
					<tbody class="items_5" id="result_table">
					</tbody>
				</table>
			</div>
		</div>
		<div id="storage_infomation">
			<div class="content">
				<label id="sd_type" class="maintitle"></label>

				<label class="subtitle"><span tkey="setup_storage_size"></span></label>
				<span id="sd_size"></span><br>

<? if( ($GLOBALS['system_conf']->SystemOption & SYSTEM_OPTION_DW_EDGE) > 0 ) {
}
else {
?>
				<label class="subtitle"><span tkey="setup_auto_delete"></span></label>
				<div class="select">
					<select id="auto_delete">
						<option value="0" tkey="setup_none"></option>
						<option value="1" tkey="setup_1day"></option>
						<option Value="2" tkey="setup_7days"></option>
						<option Value="3" tkey="setup_15days"></option>
						<option Value="4" tkey="setup_1month"></option>
					</select>
				</div><br>

				<label class="subtitle"><span tkey="setup_overwrite"></span></label>
				<input id="sd_over_write_off" name="over_write" type="radio" value="0" autocomplete='off'>
				<label for="sd_over_write_off"></label><span tkey="off"></span>
				<input id="sd_over_write_on" name="over_write" type="radio" value="1" autocomplete='off'>
				<label for="sd_over_write_on"></label><span tkey="on"></span><br>
<? }?>

				<label class="subtitle"><span tkey="setup_unmount"></span></label>
				<button id="unmount" name="control" class="button thin half" tkey="setup_unmount"></button><br>

				<label class="subtitle"><span tkey="setup_format"></span></label>
				<button id="format" name="control"  class="button thin half" tkey="setup_format_clear"></button>
				<span class="contentNotice" id="sd_status"></span><br>
			</div>
<? if( ($GLOBALS['system_conf']->SystemOption & SYSTEM_OPTION_DW_EDGE) > 0 ) {
}
else {
?>
			<center>
				<button id="save" name="control" class="button" tkey="setup_storage_apply"></button>
				<button id="cancel" class="button" tkey="setup_storage_cancel"></button>
			</center>
<? }?>
		</div>
	</div>
	<script>
		var mStorageDeviceConf = <? $GLOBALS['event_conf']->StorageDevices->getStorageDevciesConfig(0, true); ?>
 	</script>
	<script src="./setup_event_storage.js"></script>
</body>
</html>
