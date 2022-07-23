<?
require('../_define.inc');
require("../class/event.class");
$shm_id = shmop_open(KEY_SM_SHARED_CONFIG, "a", 0, 0);
$event_conf = new CEventConfiguration($shm_id);
?>
<!DOCTYPE html>
<html>
<head>
	<title>Action Rule Contfiguration</title>
	<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
</head>
<body  oncontextmenu="return false" onselectstart="return false"  ondragstart="return false">
	<div class="contentTitle"><span tkey="setup_record_config"></span></div>
	<div id="record_index">
		<div class="content">
			<label class="maintitle"><span tkey="setup_record_setup"></span></label>
			<label class="subtitle"><span tkey="setup_record_stream"></span></label>
			<div class="select">
				<select id="target_stream">
                    <option value='-1' tkey="setup_none"></option>
					<option value='0' tkey="setup_main_stream"></option>
					<option value='1' tkey="setup_sub_stream"></option>
				</select>
			</div>
		</div>
		<center>
			<button class="button" id="save_global_setting"><span tkey="setup_save"></span></button>
		</center>
		<div class="content">
			<label class="maintitle"><span tkey="setup_record_list"></span></label>
			<div class="result_table">
				<table class="result_filed">
					<thead>
						<tr class="headline">
							<th id="th1"><span tkey="setup_name"></span></th>
							<th id="th2"><span tkey="setup_record_enabled"></span></th>
							<th id="th3"><span tkey="setup_record_filetype"></span></th>
							<th id="th4"><span tkey="setup_record_storage"></span></th>
							<th id="th5"><span tkey="setup_record_continous"></span>
							</th>
						</tr>
					</thead>
					<tbody class="items_5" id="result_table">
					</tbody>
				</table>
			</div>
		</div>
		<center>
			<button id="modify" class="button"><span tkey="setup_modify"></span></button>
			<!-- <button id="add" class="button"><span tkey="setup_add"></span></button> 
			<button id="delete" class="button"><span tkey="setup_delete"></span></button> -->
		</center>
	</div>
	<div id="record_add_modify">
		<div class="content">
			<label class="maintitle"><span tkey="setup_record_setting"></span></label>
			<label class="subtitle"><span tkey="setup_record_enabled"></span></label>
			<input type="radio" id="enabled_off" name="enabled" value="0">
			<label for="enabled_off"></label><span class="c_title"><span tkey="off"></span></span>
			<input type="radio" id="enabled_on" name="enabled" value="1">
			<label for="enabled_on"></label><span class="c_title"><span tkey="on"></span></span><br>
<!--
			<label class="subtitle"><span tkey="setup_record_streamid"></span></label>
			<div class="select">
				<select id='stream_id'>
					<option value="0">channel 1</option>
					<option value="1">channel 2</option>
				</select>
			</div><br>
-->
			<label class='subtitle'><span tkey="setup_storage_device"></span></label>
			<div class='select'>
				<select id='storage_device'>
				</select>
			</div><br>
			<label class='subtitle'><span tkey="setup_record_filetype"></span></label>
			<div class='select'>
				<select id='file_type'>
					<option value='0'>TS</option>
					<option value='1'>MP4</option>
				</select>
			</div><br>
			<label class='subtitle'><span tkey="setup_record_storage"></span></label>
			<div class='select'>
<!--
				<select id='storage_type'>
					<option value='1' tkey="setup_sdcard">SD Card</option>
				</select>
-->
				<input type="text" id="storage_type" disabled/>
			</div><br>
			<label class="subtitle"><span tkey="setup_record_continous"></span></label>
			<input type="radio" id="continous_off" name="continous" value="0">
			<label for="continous_off"></label><span class="c_title" tkey="off"></span>
			<input type="radio" id="continous_on" name="continous" value="1">
			<label for="continous_on"></label><span class="c_title" tkey="on"></span><br>
			<label class='subtitle'><span tkey="setup_record_preduration"></span></label>
			<input type='number' id='pre_duration' class='third'>[ 0 ~ 5 ]<br>
			<label class='subtitle'><span tkey="setup_record_postduration"></span></label>
			<input type='number' id='post_duration' class='third'>[ 1 ~ 240 ]<br>
		</div>
		<center>
			<button class="button" id="save"><span tkey="setup_save"></span></button>
			<button class="button" id="cancel"><span tkey="setup_cancel"></span></button>
		</center>	
	</div>
	<script>
		var mStorageDeviceConf = <? $GLOBALS['event_conf']->StorageDevices->getStorageDevciesConfig(0, true); ?>
	</script>
	<script src="./setup_record_management.js"></script>
</body>
</html>
