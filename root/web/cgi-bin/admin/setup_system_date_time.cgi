<?
		require('../_define.inc');
		require('../class/system.class');
		require('../class/network.class');
		require('../class/socket.class');
		$shm_id = shmop_open(KEY_SM_SHARED_CONFIG, "a", 0, 0);
		$system_conf = new CSystemConfiguration();
		$network_conf = new CNetworkConfiguration();
		shmop_close($shm_id);
		
		function getsystmetimeInfo(){	
					echo "sync_type='".$GLOBALS['system_conf']->SystemDatetime->Type."';\r\n";
					echo "gmt='".$GLOBALS['system_conf']->SystemDatetime->TimeZoneIndex."';\r\n";
					echo "timezone='".trim($GLOBALS['system_conf']->SystemDatetime->TimeZone)."';\r\n";
					echo "ntp_server='".$GLOBALS['network_conf']->NTP->Index."'\r\n";
					echo "ntpurl='".trim($GLOBALS['network_conf']->NTP->Address)."'\r\n";
/*					$ipc_sock = new IPCSocket();
					$ipc_sock->Connection($GLOBALS['system_conf']->SystemDatetime, CMD_GET_DATETIME);	
					if ($ipc_sock->dataInfo['ErrorCode']['value'] == APP_OK)
					{
						printf("strtime='%04d/%02d/%02d %02d:%02d:%02d';\r\n", 
						$GLOBALS['system_conf']->SystemDatetime->SystemTime->year,
						$GLOBALS['system_conf']->SystemDatetime->SystemTime->mon, 
						$GLOBALS['system_conf']->SystemDatetime->SystemTime->day,
						$GLOBALS['system_conf']->SystemDatetime->SystemTime->hour, 
						$GLOBALS['system_conf']->SystemDatetime->SystemTime->min, 
						$GLOBALS['system_conf']->SystemDatetime->SystemTime->sec);	
						echo $GLOBALS['system_conf']->SystemDatetime->SystemTime->year ;
					}
					else
					{
						show_post_ng();
					}
*/				
		}

			
?>
<!DOCTYPE html>
<html>
	<head>
		<meta content="text/html; charset=utf-8" http-equiv="Content-Type">
		<title>date & time settings</title>
	</head>
	<body onload="onLoadPage();realtimeClock();">
		<div class="contentTitle"><span tkey="setup_system_datetime_config"></span></div>
		<div class="content2 low-margin">
			<label class="maintitle"><span tkey="setup_system_timezone_setup"></span></label>
			<label class="subtitle"><span tkey="setup_system_zone"></span></label>
			<div class="select extralong">
				<select id="selTimeZone" class="extralong">
<? if( ($GLOBALS['system_conf']->SystemOption & SYSTEM_OPTION_DW_EDGE) > 0 ) {
	$handle = popen("awk '! /#/ ' /usr/share/zoneinfo/zone.tab | awk '{ print $1 \" \" $3}'", "r");
	$index = 0;
	while( $line = fgets($handle) )
	{
		$line = str_replace("\n","",$line);
		printf("<option value='%d'>%s</option>\n" ,$index++, $line);
	}
	pclose($handle);
}
else {
?>
<!--				<option value=0>  (GMT-12) International Date Line West</option>
					<option value=1>  (GMT-11) Samoa, Coordinated Universal Time -11</option>
					<option value=2>  (GMT-10) Hawaii</option>
					<option value=3>  (GMT-09) Alaska</option>
					<option value=4>  (GMT-08) Pacific Time (US & Canada), Baja California </option>
					<option value=5>  (GMT-07) Mountain Time(US & Canada), Arizona</option>
					<option value=6> (GMT-06) Central Time(US & Canada), Mexico City</option>
					<option value=7> (GMT-05) Indiana (East), Estern Time (US & Canada)</option>
					<option value=8> (GMT-04) Atlantic Time(Canada), Cuiaba, Sangtiago</option>
					<option value=9> (GMT-03) Brasilia, Montevideo, Cayenne, Fortaleza</option>
					<option value=10> (GMT-02) Mid-Atlantic, Coordinated Universal Time -02</option>
					<option value=11> (GMT-01) Azores, Cape verde Is.</option>
					<option value=12> (GMT&ensp;00) Greenwich Mean Time, Lisbon, London, </option>
					<option value=13> (GMT+01) Madrid, Paris, Berlin, Rome, Vienna</option>
					<option value=14> (GMT+02) Sofia, Tallinn, Vilnius, Istanbuli,  Windhoek</option>
					<option value=15> (GMT+03) Kuwait, Baghdad, Moscow, St. Petersburg, </option>
					<option value=16> (GMT+04) Yerevan, Tbilisi, Port Louis, Kabul</option>
					<option value=17> (GMT+05) Karachi, Kolkata, New Delhi, Kathmandu</option>
					<option value=18> (GMT+06) Dhaka, Astana, Novosibirsk, Yangon</option>
					<option value=19> (GMT+07) Dhaka, Astana</option>
					<option value=20> (GMT+08) Beijing, Hong Kong, Singapore, Taipei, </option>
					<option value=21> (GMT+09) Seoul, Osaka, Tokyo</option>
					<option value=22> (GMT+10) Canberra, Melbourne, Sydney, Brisbane</option>
					<option value=23> (GMT+11) Magadan, Solomon Is., New Caledonia</option>
					<option value=24> (GMT+12) Coordinated Universal Time +12</option>
					<option value=25> (GMT+13) Nuku'alofa</option>
-->
<? } ?>
				</select>
			</div>
		</div>
		<center>
			<button id="btTimeZoneOK" type="submit" class="button"><span tkey="apply"></span></button>
		</center>
		<div class=content2>
			<label class="maintitle"><span tkey="setup_system_datetime_timeformat"></span></label>
			<label class="subtitle"><span tkey="setup_system_datetime_timeformat"></span></label>
			<div class="select">
				<select class="select" id="time_format">
					<option value=0>yy-mm-dd</option>
					<option value=1>mm/dd/yy</option>
				</select>
			</div><br>
			<div id="hourformat_div">
			<label class="subtitle"><span tkey="setup_system_datetime_hourformat"></span></label>
			<div class="select">
				<select class="select" id="hour_format">
					<option value=0>24H</option>
					<option value=1>12H</option>
				</select>
			</div></div>
		</div>
		<center>
			<button id="btDateFormat" class="button" tkey="apply"></button>
		</center>
		<div class="content2">
			<label class="maintitle"><span tkey="setup_system_currenttime"></span></label>
			<label class="subtitle"><span tkey="date_time"></span></label>
			<input id="sDate" type="text" class="third" readonly>
			<input id="sTime" type="text" class="third" readonly>
			<label class="maintitle"><span tkey="setup_system_newcameradatetime"></span></label>
			<input type="radio" id="camTime" name="rdCameraTime" value='1'>
			<label for="camTime"></label><span tkey="setup_system_sync_pc"></span><br>
			<label class="subtitle2"><span tkey="date_time"></span></label>
			<input id="pDate" type="text" class="third" readonly>
			<input id="pTime" type="text" class="third" readonly><br>
			<input type="radio" id="manualTime" name="rdCameraTime" value='2'>
			<label for="manualTime"></label><span tkey="setup_system_sync_manual"></span><br>
			<label class="subtitle2"><span tkey="setup_system_date"></span></label>
			<div class="select third">
				<select id="selYear" class="third">
				</select>
			</div>
			<div class="select third">
				<select id="selMonth" class="third">
				</select>
			</div>
			<div class="select third">
				<select id="selDay" class="third">
				</select>
			</div>
			<br>
			<label class="subtitle2"><span tkey="setup_system_time"></span></label>
			<div class="select third">
				<select id="selHour" class="third">
				</select>
			</div>
			<div class="select third">
				<select id="selMin" class="third">
				</select>
			</div>
			<div class="select third">
				<select id="selSec" class="third">
				</select>
			</div>
			<br>
			<input type="radio" id="nts" name="rdCameraTime" value='0'>
			<label for="nts"></label><span tkey="setup_system_sync_timeserver"></span><br>
			<label class="subtitle2"><span tkey="setup_system_ntp"></span></label>
			<div class="select">
				<select id="selNtpServer" onchange="onChangeNtpServer(this.value);" size="1">
				</select>
			</div>
			<button id="btsyncntp" class="button thin"><span tkey="Synchronize_now"></span></button><br>
			<label class="subtitle2"></label>
			<input id="txtManualAddress" type="text">
		</div>
		<center>
			<button id="btDateTimeOK" type="submit" class="button"><span tkey="apply"></span></button>
		</center>
		<script>
			var sync_type;
			var gmt;
			var ntp_server;
			var ntpurl;
			var strtime;
			<?
				getsystmetimeInfo(); 
			?>
			var timeFormat=<?echo $GLOBALS['system_conf']->SystemDatetime->TimeFormat?>;
			var hourFormat=<?echo $GLOBALS['system_conf']->SystemDatetime->HourFormat?>;
		</script>
		<script src="./setup_system_date_time.js"></script>
	</body>
</html>
