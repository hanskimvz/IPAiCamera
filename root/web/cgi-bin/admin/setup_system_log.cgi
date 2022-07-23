<?
    require('../_define.inc');
    require('../class/system.class');
    require('../class/capability.class');
    // require('../class/network.class');

    $shm_id = shmop_open(KEY_SM_SHARED_CONFIG, "a", 0, 0);
    $system_conf = new CSystemConfiguration($shm_id);
    $system_caps = new CCapability($shm_id);
    shmop_close($shm_id);
    $get_oem = $system_caps->getOEM();


?>
<!DOCTYPE html>
<html>
<head>
	<meta http-equiv="Expires" content="Tue, 12 May 1962 1:00:00 GMT">
	<meta http-equiv="Pragma" content="no-cache">
	<meta http-equiv="Cache-Control" content="no-cache">
	<meta content="text/html; charset=utf-8" http-equiv="Content-Type">
	<meta http-equiv="X-UA-Compatible" content="IE=10" /> 	
	<meta name="google" content="notranslate" />
	<title>System Log Page</title>
	<noscript> </noscript>
</head>
<script>
</script>
<body oncontextmenu='return false;' ondragstart='return false;' onselectstart='return false;'>
	<div id="system_log">
		<div class="contentTitle"><span tkey="system_log"></span></div>
		<div class="content list">
			<label class="maintitle"><span tkey="system_log_filter"></span></label>
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
				<input type="checkbox" id="cType" name="filter">
				<label for="cType"></label>
				<span class="c_title"><span tkey="type"></span></span>
			</label>
			<div class="select">
				<select id="sType" disabled="true">
					<option value="all" tkey="log_type_all">All</option>
					<option value="events" tkey="log_type_events">Events</option>
					<option value="exceptions" tkey="log_type_exceptions">Exceptions</option>
					<option value="operations" tkey="log_type_operations">Operations</option>
					<option value="informations" tkey="log_type_informations">Informations</option>
				</select>
			</div><br>
			<label class="subtitle">
				<input type="checkbox" id="cSort" name="filter"/>
				<label for="cSort"></label>
				<span class="c_title" tkey="setup_sort"></span>
			</label>
			<div class="select">
				<select id="sSort" disabled="true">
					<option value="asc" tkey="setup_ascending"></option>
					<option value="dec" tkey="setup_decending"></option>
				</select>
			</div><br>
		</div>
		<center>
		<div id="log_button">
			<button id="refresh" class="button" tkey="setup_refresh"></button>
			<button id="filter" class="button" disabled="true" tkey="setup_filter"></button>
			<button id="backup_log" class="button" tkey="setup_backup" style = "display:inline;"></button>
		</div>
		</center>

		<div class="content">
			<label class="maintitle"><span tkey="system_log_list"></span></label>
			<div class="log_table">
				<table class="result_filed">
					<thead>
						<tr class="headline">
							<th width="30%"><span tkey="date_time" style="margin-right: 10px;"></span></th>
							<th width="45%"><span tkey="system_log_code" style="margin-right: 10px;"></span></th>
							<th width="15%"><span tkey="system_log_object" style="margin-right: 10px;"></span></th>
						</tr>
					</thead>
					<tbody id="log_table">
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
	</div>
</body>
<script src="/js/jquery1.11.1.min.js"></script>
<script src="/js/jqueryui.js"></script>
<script src="/js/page.js"></script>
<script>
	var userInfo = new Object();
	var data = new Array();
	<?
        if($GLOBALS['get_oem'] == 19 || $GLOBALS['get_oem'] == 20 || $GLOBALS['get_oem'] == 21)
        {
            $GLOBALS['system_conf']->Users->getAccessUserInfo_x("userInfo");
        }
        else
        {
            $GLOBALS['system_conf']->Users->getAccessUserInfo("userInfo");
        }
    ?>
    var timeFormat=<?echo $GLOBALS['system_conf']->SystemDatetime->TimeFormat?>;
    var hourFormat=<?echo $GLOBALS['system_conf']->SystemDatetime->HourFormat?>;

</script>
<script src="./setup_system_log.js"></script>
</html>
