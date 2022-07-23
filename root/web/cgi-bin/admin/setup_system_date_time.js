

var menu = getLanguage("Date&Time_Settings");
var ntp_server_name = new Array(
	'time-a.nist.gov', 'time-b.nist.gov',
	 'utcnist.colorado.edu', 'time.google.com',
	'pool.ntp.org', 'Manual'
);
var diffTime_sub ;
var timeout ;
function getSystime_sub(input)
{
	systime = new Date(input).getTime();
	diffTime_sub = systime - new Date().getTime();
	if(typeof(systime) != 'undefined') 
	{
		diffTime_sub = systime - new Date().getTime();
	}
	clearTimeout(timeout);
	timeout = setTimeout(refreshTime_sub, 15000);
}

function refreshTime_sub()
{
	$.ajax({
		url: "/cgi-bin/result",
		data: {
			"msubmenu"      : "event",
			"action"        : "view"
		}
	,async : false 
	,success: function(ret){		
		console.log(ret);
		var tmp = ret.trim().split('\n');

		for( var i=0 ; i < tmp.length ; i++){
			if( tmp[i].split('=')[0].trim() == "system_time" ){		
				var tmp2 = tmp[i].split('=')[1];  
				try {
					if(tmp2.length > 0)
					{
						getSystime_sub(tmp2);
					}
				} catch (e){
					console.log(e);
				}
			}
		}
      }
	});
}

function updateTime()
{
	if( $(".select_minor").attr("id") != "Date_Time_Settings" ) return;
	var pTime = new Date();
	var now ;
	if( diffTime_sub == undefined )	  now   = pTime.valueOf() ;
	else now   = pTime.valueOf() + diffTime_sub;  

	var sTime  = new Date(now);

	var sDateTime = getTimeStamp(sTime, false).split(" ");
	$("#sDate").val(sDateTime[0]);
	$("#sTime").val(sDateTime[1]);
	var pDateTime = getTimeStamp(pTime, false).split(" ");
	$("#pDate").val(pDateTime[0]);
	$("#pTime").val(pDateTime[1]);
	setTimeout(updateTime, 1000);
}

function onLoadPage()
{
	initUI();
	initValue();
	initEvent();
	updateTime();
	clearTimeout(timeout);
	refreshTime_sub();
	updateTime();
}
function initUI()
{
	//Add ntpServerList
	var max = ntp_server_name.length;
	var index = max-1;
	for(var i = 0 ; i < max ; i++)
	{
		if(i==5 && capInfo["oem"] == 12)
		{
			$("#selNtpServer").append("<option value=" +  i + ">Server Address</option>");
		}
		else
		{
			$("#selNtpServer").append("<option value=" +  i + ">"+ ntp_server_name[i] +"</option>");
		}
	}
	if(ntp_server < 0 || ntp_server > 5)
	  index = 0;
	else  
	  index = ntp_server;

	$("#selNtpServer").val(index);
    console.log("index= "+index+"\nntp_server_name[index]: "+ntp_server_name[index]+"\nntpurl: "+ntpurl);
	if ( ntp_server_name[index] == "Manual" )
	{
		$("#txtManualAddress").removeAttr("disabled");
		$("#txtManualAddress").removeAttr("readonly");
		$("#txtManualAddress").val(ntpurl);
	} else {
		$("#txtManualAddress").attr("disabled", "true");
		$("#txtManualAddress").attr("readonly", "true");
	}

	$("#selTimeZone").append("<option value = 0 tkey='setup_gmt0'></option>");
	$("#selTimeZone").append("<option value = 1 tkey='setup_gmt1'></option>");
	$("#selTimeZone").append("<option value = 2 tkey='setup_gmt2'></option>");
	$("#selTimeZone").append("<option value = 26 tkey='setup_gmt26'></option>");
	$("#selTimeZone").append("<option value = 3 tkey='setup_gmt3'></option>");
	$("#selTimeZone").append("<option value = 4 tkey='setup_gmt4'></option>");
	$("#selTimeZone").append("<option value = 5 tkey='setup_gmt5'></option>");
	$("#selTimeZone").append("<option value = 6 tkey='setup_gmt6'></option>");
	$("#selTimeZone").append("<option value = 7 tkey='setup_gmt7'></option>");
	$("#selTimeZone").append("<option value = 8 tkey='setup_gmt8'></option>");
	$("#selTimeZone").append("<option value = 27 tkey='setup_gmt27'></option>");	
	$("#selTimeZone").append("<option value = 9 tkey='setup_gmt9'></option>");
	$("#selTimeZone").append("<option value = 10 tkey='setup_gmt10'></option>");
	$("#selTimeZone").append("<option value = 11 tkey='setup_gmt11'></option>");
	$("#selTimeZone").append("<option value = 12 tkey='setup_gmt12'></option>");
	$("#selTimeZone").append("<option value = 13 tkey='setup_gmt13'></option>");
	$("#selTimeZone").append("<option value = 14 tkey='setup_gmt14'></option>");
	$("#selTimeZone").append("<option value = 15 tkey='setup_gmt15'></option>");
	$("#selTimeZone").append("<option value = 28 tkey='setup_gmt28'></option>");	
	$("#selTimeZone").append("<option value = 16 tkey='setup_gmt16'></option>");
	$("#selTimeZone").append("<option value = 29 tkey='setup_gmt29'></option>");
	$("#selTimeZone").append("<option value = 17 tkey='setup_gmt17'></option>");
	$("#selTimeZone").append("<option value = 30 tkey='setup_gmt30'></option>");
	$("#selTimeZone").append("<option value = 31 tkey='setup_gmt31'></option>");
	$("#selTimeZone").append("<option value = 18 tkey='setup_gmt18'></option>");
	$("#selTimeZone").append("<option value = 32 tkey='setup_gmt32'></option>");
	$("#selTimeZone").append("<option value = 19 tkey='setup_gmt19'></option>");
	$("#selTimeZone").append("<option value = 20 tkey='setup_gmt20'></option>");
	$("#selTimeZone").append("<option value = 33 tkey='setup_gmt33'></option>");
	if( capInfo['oem'] == 8)
		$("#selTimeZone").append("<option value = 21 tkey='setup_gmt21_1'></option>");
	else
		$("#selTimeZone").append("<option value = 21 tkey='setup_gmt21'></option>");
	$("#selTimeZone").append("<option value = 34 tkey='setup_gmt34'></option>");	
	$("#selTimeZone").append("<option value = 22 tkey='setup_gmt22'></option>");	
	$("#selTimeZone").append("<option value = 35 tkey='setup_gmt35'></option>");	
	$("#selTimeZone").append("<option value = 23 tkey='setup_gmt23'></option>");
	$("#selTimeZone").append("<option value = 24 tkey='setup_gmt24'></option>");
	$("#selTimeZone").append("<option value = 36 tkey='setup_gmt36'></option>");	
	$("#selTimeZone").append("<option value = 25 tkey='setup_gmt25'></option>");	
	if(gmt == -1)
	{
	  var user_define_timezone = "<option value = -1> " + timezone + " </option>";
	  $("#selTimeZone").append(user_define_timezone);
	}
	if(TimerId == 0)
		TimerId = updateTime();
	else{
		clearTimeout(TimerId);
		TimerId = updateTime();
	}
	if( capInfo['oem'] == 11 || capInfo['oem'] == 13 || capInfo['oem'] == 25 || capInfo['oem'] == 24 )
		$("#time_format").append("<option value=2>dd/mm/yy</option>");
	if( capInfo['oem'] != 2) // DW hour format
		$("#hourformat_div").css("display","none");
	if( capInfo['oem'] != 12)
		$("#btsyncntp").css("display","none");
	if ( sync_type == 0) {
		$('#btsyncntp').prop("disabled", false);
	} else {
		$('#btsyncntp').prop("disabled", true);
	}

}
function initValue()
{
	function onLoadOption(obj, min, max)
	{
		if(min < max )
		{
			var start = min;
			var end = max;
		} else {
			var start = max;
			var end = end;
		}
		for(var i = start ; i <= end  ; i++)
		{
			if( Number(i) < 10 ) i = "0" + i.toString();
			obj.append("<option value=" + i +">" + i + "</option>");
		}

	}
	$("#selTimeZone").val(gmt);
	onLoadOption( $("#selYear"), 2005, 2030);
	onLoadOption( $("#selMonth"), 1, 12);
	onLoadOption( $("#selDay"), 1, 31);
	onLoadOption( $("#selHour"), 0, 23);
	onLoadOption( $("#selMin"), 0, 59);
	onLoadOption( $("#selSec"), 0, 59);
	$("input:radio[name=rdCameraTime]:radio[value=" + sync_type + "]").attr('checked', 'true');
	$("select#time_format").val(timeFormat);
	$("select#hour_format").val(hourFormat);
}

function initEvent()
{
	menu = getLanguage("setup_system_datetime_config");
	var  pop_msg ="";

	$("#selNtpServer").bind("change", function(){
			if ( $("#selNtpServer").val() == 5 )
			{
				$("#txtManualAddress").removeAttr("disabled");
				$("#txtManualAddress").removeAttr("readonly");
				$("#txtManualAddress").val(ntpurl);
			} else {
				$("#txtManualAddress").attr("disabled", "true");
				$("#txtManualAddress").attr("readonly", "true");
			}
	});
	$("#btTimeZoneOK").bind("click", function(){
		$.ajax({
			type:       "get",
			url:        "/cgi-bin/admin/system.cgi?msubmenu=timezone&action=apply",
			msubmenu:   "system",
			action:     "apply",
			data:       { gmt :$("#selTimeZone").val() },
			success: function(response){
				console.log(response);
				var data = response.trim();
				if(data == "OK")
				{
					pop_msg = getLanguage("setup_system_timezone_setup");
					settingSuccess(pop_msg);
					refreshMenuContent();
				} else {
					pop_msg = getLanguage("setup_system_timezone_setup"); 
					settingFail(pop_msg);
				}
			}
		});
	});
	$("#btDateFormat").click(function(){
		var _timeFormat = $("select#time_format").val(),
			_hourFormat = $("select#hour_format").val(),
			param = {
				msubmenu : "time_format",
				action   : "apply"
			},
			changed = false;
		if( timeFormat != _timeFormat ) {
			param['format']= _timeFormat;
			changed = true;
		}
		if( hourFormat != _hourFormat ) {
			param['hourformat']= _hourFormat;
			changed = true;
		}
		if( changed == false ){
			settingFail(getLanguage('setup_system_datetime_timeformat'),
					getLanguage("msg_nothing_changed"));
			return ;
		}
		$.ajax({
			type:   'get',
			url:    'system.cgi',
			data:   param,
			success: function(response){
				var data = response.trim();
				if ( data == "OK"){
					settingSuccess(menu);
					refreshMenuContent();

				} else {
					settingFail(menu);
				}
			}
		});
	});
	$("#btDateTimeOK").bind("click", function(){
		var getMode = $("input:radio[name=rdCameraTime]:checked").val(),
			data = null;
		if( getMode == 1 ) // sync
		{
			var dt = new Date();
			data = "sync_type=1";
			data += "&year=" + dt.getFullYear();
			data += "&mon=" +  Number(dt.getMonth()+1);
			data += "&day=" +  dt.getDate();
			data += "&hour=" + dt.getHours();
			data += "&min=" +  dt.getMinutes();
			data += "&sec=" +  dt.getSeconds();
		} else if ( getMode == 2) {
			data = "sync_type=2";
			data += "&year=" + $("#selYear").val();
			data += "&mon=" + $("#selMonth").val();
			data += "&day=" + $("#selDay").val();
			data += "&hour=" + $("#selHour").val();
			data += "&min=" + $("#selMin").val();
			data += "&sec=" + $("#selSec").val();
		} else if (getMode == 0){
			data = "sync_type=0";
			if ( ntp_server_name[$("#selNtpServer").val()] == "Manual" )
			{
			  data += "&ntp_server=" + $("#selNtpServer").val();
				data += "&ntpurl=" + $("#txtManualAddress").val();
			}
			else
			{
				data += "&ntp_server=" + $("#selNtpServer").val();
				data += "&ntpurl=" + ntp_server_name[$("#selNtpServer").val()];
			}
		}
		if(data === null){
			pop_msg = getLanguage("msg_nothing_changed");
			settingFail(menu, pop_msg);
			return;
		} else {
			console.log(data);
			$.ajax({
				type:   'get',
				url:    '/cgi-bin/admin/system.cgi?msubmenu=datetime&action=apply',
				data:   data,
				success: function(response){
					var data = response.trim();
					if ( data == "OK"){
						settingSuccess(menu);
//						opener.location.reload(true);  
//						VLCManager.doGo();
						refreshMenuContent();
						
					} else {
						settingFail(menu);
					}
				}
			});
		}
	});
	$("#btsyncntp").bind("click", function(){
		data = "sync_type=0";
		if ( ntp_server_name[$("#selNtpServer").val()] == "Manual" )
		{
			data += "&ntp_server=" + $("#selNtpServer").val();
			data += "&ntpurl=" + $("#txtManualAddress").val();
		}
		else
		{
			data += "&ntp_server=" + $("#selNtpServer").val();
			data += "&ntpurl=" + ntp_server_name[$("#selNtpServer").val()];
		}
		$.ajax({
			type:   'get',
			url:    '/cgi-bin/admin/system.cgi?msubmenu=datetime&action=apply',
			data:   data,
			success: function(response){
				var data = response.trim();
				if ( data == "OK"){
					pop_msg = getLanguage("Synchronize_now");
					settingSuccess(pop_msg);
					refreshMenuContent();
				} else {
					settingFail(menu);
				}
			}
		});
	});
	$("[name=rdCameraTime]").change(function ( obj ) {
		if ( this.value == 0) {
			$('#btsyncntp').prop("disabled", false);
		}
		else {
			$('#btsyncntp').prop("disabled", true);
		}
	});
}
$(document).ready( function() {
	onLoadPage();
});
