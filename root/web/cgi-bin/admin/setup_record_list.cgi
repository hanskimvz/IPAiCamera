<?
require('../_define.inc');
require('../class/system.class');
require('../class/capability.class');
require('../class/event.class');
// require('../class/network.class');

$shm_id = shmop_open(KEY_SM_SHARED_CONFIG, "a", 0, 0);
$system_conf = new CSystemConfiguration($shm_id);
$system_caps = new CCapability($shm_id);
$event_conf = new CEventConfiguration($shm_id);
shmop_close($shm_id);
$get_oem = $system_caps->getOEM();
?>
<!DOCTYPE html>
<html>
<body oncontextmenu='return false;' ondragstart='return false;' onselectstart='return false;'>
	<div id="recording">
		<div class="contentTitle"><span tkey="setup_record_list"></span></div>
		<div id='storages' class='content'>
			<label class='subtitle'><span tkey='storage'></span></label>
			<div class='select'>
				<select id='storage_index'></select>	
			</div>
		</div>
		<div class="content list">
			<label class="maintitle"><span tkey="setup_filter"></span></label>
			<label class="subtitle">
				<input type="checkbox" id="cDate" name="filter"/>
				<label for="cDate"></label>
				<span class="c_title" tkey="setup_date"></span>
			</label>
			<input type="text" id="dFromDate" disabled="true" />~
			<input type="text" id="dToDate" disabled="true"/><br>
			<label class="subtitle">
				<input type="checkbox" id="cTime" name="filter" />
				<label for="cTime"></label>
				<span class="c_title"><span tkey="setup_time"></span>
			</label>
			<div class="select quarter">
				<select id="sFromHour" class="quarter" disabled="true">
				</select>
			</div>
			<div class="select quarter">
				<select id="sFromMin" class="quarter" disabled="true">
				</select>
			</div>
			<div class="select quarter">
				<select id="sFromSec" class="quarter" disabled="true">
				</select>
			</div>&nbsp;~&nbsp;
			<div class="select quarter">
				<select id="sToHour" class="quarter" disabled="true">
				</select>
			</div>
			<div class="select quarter">
				<select id="sToMin" class="quarter" disabled="true">
				</select>
			</div>
			<div class="select quarter">
				<select id="sToSec" class="quarter" disabled="true">
				</select>
			</div><br>
			<label class="subtitle">
				<input type="checkbox" id="cEvent" name="filter">
				<label for="cEvent"></label>
				<span class="c_title"><span tkey="setup_event"></span></span>
			</label>
			<div class="select">
				<select id="sEvent" disabled="true">
					<option value="all" tkey="setup_all"></option>
					<option value="On Continous" tkey="setup_record_continous"></option>
					<option value="On Motion" tkey="setup_motion"></option>
<? if ( $get_oem != 2) { ?>
<? if ( ($get_oem == 11) || ($get_oem == 25) ) { ?>
					<option value="On Schedule" tkey="setup_event_recurrences"></option>
<? } else { ?>
					<option value="On Schedule" tkey="setup_schedule"></option>
<? } ?>
<? } ?>
					<option value="On Sensor Alarm" tkey="setup_sensor_alarm"></option>
					<option value="Network Disconnected" tkey="setup_network_disconnected"></option>
					<option value="Temperature Critical" tkey="setup_temperature_critical"></option>
					<option value="Illegal login detected" tkey="setup_illegal_login"></option>
					<option value="Temperature Detected" tkey="setup_temperature_detected"></option>
					// Only Stanley use iNode func.
<? if ( $get_oem == 19) { ?>
					<option value="Custum Event Detected" tkey="setup_custom_event_detected"></option>
<? } ?>
<? if ( $get_oem == 2) { ?>
					<option value="System Initialize" tkey="setup_system_initialize"></option>
<? } ?>
				</select>
			</div><br>
			<label class="subtitle">
				<input type="checkbox" id="cStorage" name="filter"/>
				<label for="cStorage"></label>
				<span class="c_title" tkey="setup_record_memory"></span>
			</label>
			<div class="select">
				<select id="sStorage" disabled="true">
					<option value="all" tkey="setup_all">ALL</option>
					<option value="SDCARD" tkey="setup_sdcard">SDCard</option>
				</select>
			</div><br>
			<label class="subtitle">
				<input type="checkbox" id="cSort" name="filter"/>
				<label for="cSort"></label>
				<span class="c_title" tkey="setup_sort"></span>
			</label>
			<div class="select">
				<select id="sSort" disabled="true">
					<option value="asc" tkey="setup_ascending">Ascending</option>
					<option value="dec" tkey="setup_decending">Decending</option>
				</select>
			</div><br>
		</div>
		<center>
			<button id="refresh" class="button"><span tkey="setup_refresh"></span></button>
			<button id="filter" class="button" disabled="true"><span tkey="setup_filter"></span></button>
		</center>
		<div class="content">
			<label class="maintitle"><span tkey="setup_event"></span></label>
			<div class="result_table">
				<table class="result_filed">
					<thead class="record_thead">
						<tr class="headline">
							<th class="qt"><span tkey="setup_day"></span></th>
							<th class="qt"><span tkey="setup_time"  ></span></th>
							<th class="qt"><span tkey="setup_duration"  class="sb_margin_6"></span></th>
							<th class="qt"><span tkey="setup_event"  ></span></th>
						</tr>
					</thead>
					<tbody id="result_table">
					</tbody>
				</table>
			</div>
			<div id="pages">
				<div class="left">
					<button id="first_page" class="button"> << </button>
					<button id="prev_page" class="button"> < </button>
				</div>
				<div id="page_list"></div>
				<div class="right">
					<button id="next_page" class="button"> > </button>
					<button id="last_page" class="button"> >> </button>
				</div>
			</div>
		</div>
		<center>
			<button id="play" class="button"><span tkey="setup_play"></span></button>
			<!-- <button id="remove" class="button"><span tkey="setup_remove"></span></button> -->
			<!-- <button id="properties" class="button"><span tkey="setup_properties"></span></button> -->
			<button id="download" class="button"><span tkey="setup_download"></span></button>
		</center>
	</div>
	<div id="record_video" class="record_view">
		<div class="contentTitle" tkey="setup_record_list">Recording Video</div>
		<object type='application/x-vlc-plugin' pluginspage='http://www.videolan.org' \
		version='VideoLAN.VLCPlugin.2' id='vlc' width='512px' \
		height='288px' align='center' vspace='0' events='True' VIEWASTEXT>
		<param name='MRL' value='' />
		<param name='controls' value='true' /> 
		<param name='toolbar' value='false' />
		<param name='mute' value='true' />
		<param name='AutoLoop' value='false' />
		<!--
		<param name='ShowDisplay' value='true' />
		<param name='AutoPlay' value='true' />
		<param name='StartTime' value='0' />
		<param name='branding' value='true' />
		<param name='windowless' value='true'/>--!></object>
		<br><br>
		<div class="content">
			<label class="maintitle"><span tkey="setup_recording_video"></span></label>
			<label class="subtitle"><span tkey="setup_record_token"></span></label>
			<span id='p_token'></span><br>
			<label class="subtitle"><span tkey="setup_status"></span></label>
			<span id='p_status'></span><br>
			<label class="subtitle"><span tkey="setup_starttime"></span></label>
			<span id='p_starttime'></span><br>
			<label class="subtitle"><span tkey="setup_endtime"></span></label>
			<span id='p_endtime'></span><br>
			<label class="subtitle"><span tkey="setup_record_recordtime"></span></label>
			<span id='p_recordingtime'></span><br>
		</div>
		<button id="replay" class="button"><span tkey="setup_replay"></span></button>
		<button id="back" class="button"><span tkey="setup_back"></span></button>
		</div>
		<div id="download_video" style="display:none;">
			<div class="contentTitle" tkey="setup_record_list">Recording Video</div>
			<div class="content">
				<label class="subtitle2">Download purpose</label>
				<input id="download_purpose" type="text" maxlength="32" class="inputText">(max : 32)<br>
				<label class="subtitle2">Backup key</label>
				<input id="download_key" type="password" maxlength="32" class="inputText">(max : 32)<br>
			</div>
			<center>
				<button id="btOK" class="button" ><span tkey="apply" ></span></button>
				<button class="button" id="cancel"><span tkey="setup_cancel"></span></button>
			</center>
		</div>
		<iframe id="forDownload"></iframe>
</body>
<script src="/js/jquery1.11.1.min.js"></script>
<script src="/js/jqueryui.js"></script>
<script src="/js/page.js"></script>
<script>
	var userInfo = new Object();
	var data = new Array();
    var gmt;
	<?
	if($GLOBALS['get_oem'] == 19 || $GLOBALS['get_oem'] == 20 || $GLOBALS['get_oem'] == 21)
	{
		$GLOBALS['system_conf']->Users->getAccessUserInfo_x("userInfo");
	}
	else
	{
		$GLOBALS['system_conf']->Users->getAccessUserInfo("userInfo");
	}

	echo "gmt='".$GLOBALS['system_conf']->SystemDatetime->TimeZoneIndex."';\r\n";

	?>
    var timeFormat=<?echo $GLOBALS['system_conf']->SystemDatetime->TimeFormat?>;
    var hourFormat=<?echo $GLOBALS['system_conf']->SystemDatetime->HourFormat?>;
	var mStorageDeviceConf = <? $GLOBALS['event_conf']->StorageDevices->getStorageDevciesConfig(0, true); ?>;
</script>
<script src="./setup_record_list.js"></script>
</html>
