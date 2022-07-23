var MAX_NUM_ITEM = Number(20);
var MAX_NUM_PAGE = Number(10);
var START_PAGE_NUM;
var AMOUNT_OF_PAGE;
var AMOUNT_OF_CONTENTS;
var SELECT_PAGE;
var data;
var initdata = new Object();
var format = "yy-mm-dd";
if( timeFormat == 1 ){
	format = "mm/dd/yy";
}
else if( timeFormat == 2 ){
	format = "dd/mm/yy";
}

var operation_code = [
	"LOG_SET_DEVICE_INFORMATION",
	"LOG_SET_USERS"              ,
	"LOG_ADD_USER"               ,
	"LOG_DEL_USER"               ,
	"LOG_SET_USER"               ,	
	"LOG_SET_DATETIME"           ,
	"LOG_SET_IO_CONFIGURATION"         ,
	"LOG_SET_RELAY_OUTPUT_STATE"       ,
	"LOG_SET_OSD"           ,
	"LOG_SET_SYSTEM_FACTORY_DEFAULT" ,
	"LOG_SYSTEM_REBOOT"          ,
	"LOG_SET_NETWORK_CONFIGURATION"    ,
	"LOG_SET_EVENT_CONFIGURATION"     ,
	"LOG_SET_CHANNEL_CONFIGURATION",	
	"LOG_SET_VIDEO_ENCODE_CONFIGURATION"     ,		
	"LOG_SET_PROFILES"                  ,
	"LOG_SET_PROFILE_CONFIGURATION"    , 
	"LOG_ADD_PROFILE"                  ,
	"LOG_DEL_PROFILE"                  ,
	"LOG_SET_PROFILE"                  ,
	"LOG_START_MULTICAST_STREAMING"    ,
	"LOG_STOP_MULTICAST_STREAMING"     ,
	"LOG_SET_SYNCHRONIZATION_POINT"     ,
	"LOG_DEL_RTSP_CONNECTION"      ,
	"LOG_SYSTEM_UPGRADE"		,
	"LOG_SET_CAMERA_SETUP",
	"LOG_SET_NTP_SYNC",
	"LOG_SET_CAMERA_DEAFULT",
	"LOG_SET_SETUP_INI",
	"LOG_TEST_FTP",
	"LOG_TEST_SMTP",
	"LOG_SET_CAMERA_RESTORE", 
	"LOG_ADD_RECORDING_JOB",
	"LOG_SET_RECORDING_JOB",
	"LOG_DEL_RECORDING_JOB",
	"LOG_ADD_EVENT_CONF",
	"LOG_SET_EVENT_CONF",
	"LOG_DEL_EVENT_CONF",
	"LOG_ADD_ACTION_RULE",
	"LOG_SET_ACTION_RULE",
	"LOG_DEL_ACTION_RULE",
	"LOG_SET_FORMAT_SDCARD",
	"LOG_SET_UNMOUNT_SDCARD",
	"LOG_SET_FTP_UPGRADE",
	"LOG_START_FTP_UPGRADE",
	"LOG_PTZ_MOVE",
	"LOG_PTZ_ARROW",
	"LOG_PTZ_ZOOM",
	"LOG_PTZ_POSITION_MOVE",
	"LOG_PTZ_STOP",
	"LOG_PTZ_SET_SPEED",
	"LOG_FOCUS_MOVE",
	"LOG_FOCUS_POSITION_MOVE",
	"LOG_IRIS_MOVE",
	"LOG_IRIS_POSITION_MOVE",	
	"LOG_SET_FOCUS_MODE",	
	"LOG_SET_RECORDING_CHANNEL",
	"LOG_SET_VIDEO_QPROI",
	"LOG_SET_SMART_LBR",
	"LOG_SET_IMAGING_SETTINGS",
	"LOG_SET_PRIVACY_MASK",
	"LOG_ADD_CAMERA_PROFILES", 
	"LOG_MODIFY_CAMERA_PROFILES",
	"LOG_APPLY_CAMERA_PROFILES",
	"LOG_DELETE_CAMERA_PROFILES",
	"LOG_ADD_STREAM_CLIENT",
	"LOG_SET_LANGUAGE",
	"LOG_SET_SECURITY_SERVICE",
	"LOG_SET_SECURITY_IP_FILTER",
	"LOG_ADD_SECURITY_IP_FILTER_ADDR",
	"LOG_DEL_SECURITY_IP_FILTER_ADDR",
	"LOG_DEL_ALL_SECURITY_IP_FILTER_ADDR",
	"LOG_SET_IEEE_8021X",
	"LOG_ADD_SELF_SIGNED_CERT",
	"LOG_DEL_CERTIFICATE",
	"LOG_CREATE_CSR",	
	"LOG_INSTALL_CERTIFICATE",	
	"LOG_INSTALL_CA",	
	"LOG_DEL_CA",	
	"LOG_SET_HTTPS",	
	"LOG_SET_RTSP_AUTHENTICATION",	
	"LOG_EXPORT_RECORDFILE",	
	"LOG_SET_PRESET",
	"LOG_REMOVE_PRESET",
	"LOG_SET_PRESET_TOUR",
	"LOG_REMOVE_PRESET_TOUR",
	"LOG_SET_HOME_POSITION",
	"LOG_NOTIRY_FAIL_LOGIN",
	"LOG_NOTIRY_SUCCESS_LOGIN",
	"LOG_NOTIRY_USER_LOGOUT",
	"LOG_END_CODE",
	]
if(capInfo["oem"] == 11 || capInfo["oem"] == 25){
	var event_code = [
		"ON_SYSTEM_INIT",	// 1
		"ON_SYSTEM_TERMINATE",
		"ON_INITIALIZED_NETWORK",
		"ON_CHANGED_PROFILE",
		"ON_CHANGED_PROFILECONFIG",
		"ON_CHANGED_ENCODER",
		"ON_CHANGED_IP",
		"ON_CHANGE_DATETIME",
		"ON_CHANGE_USERINFO",
		"ON_REBOOTING_SYSTEM",
		"ON_REBOOT_RTSP_SERVER",
		//----------------------------------//
		"ON_EVENT_BASE",	//12
		"ON_EVENT_MOTION",
		"ON_EVENT_RECURRENCES",
		"ON_EVENT_SENSOR_ALARM",
		"ON_EVENT_RELAY",
		"ON_EVENT_NETWORK_DISCONNECTED",
		"ON_EVENT_SD_FULL",
		"ON_EVENT_SD_FAILURE",
		"ON_EVENT_IP_ADDR_CONFLICTED",
		"ON_EVENT_TEMPERATURE_CRITICAL",
		"ON_EVENT_ILLEGAL_LOGIN",	
		"ON_EVENT_USER_EVENT1",
		"ON_EVENT_USER_EVENT2",
		"ON_EVENT_USER_EVENT3",
		"ON_EVENT_USER_EVENT4",
		"ON_EVENT_USER_EVENT5",
		"ON_EVENT_USER_EVENT6",
		"ON_EVENT_USER_EVENT7",
		"ON_EVENT_USER_EVENT8",
		"ON_EVENT_USER_EVENT9",
		"ON_EVENT_USER_EVENT10",
		"ON_EVENT_USER_EVENT11",
		"ON_EVENT_USER_EVENT12",
		"ON_EVENT_USER_EVENT13",
		"ON_EVENT_USER_EVENT14",
		"ON_EVENT_USER_EVENT15",
		"ON_EVENT_USER_EVENT16",
		"ON_EVENT_TEMPERATURE_DETECTED", //hdseo for thermal
		"ON_EVENT_CUSTOM_SNAP", //hdseo for iNode
		"ON_EVENT_PIR_DETECTED", 
		"ON_EVENT_SYS_INIT",		// cmlee
		"ON_EVENT_END",
		]
}else{	
	var event_code = [
		"ON_SYSTEM_INIT",	// 1
		"ON_SYSTEM_TERMINATE",
		"ON_INITIALIZED_NETWORK",
		"ON_CHANGED_PROFILE",
		"ON_CHANGED_PROFILECONFIG",
		"ON_CHANGED_ENCODER",
		"ON_CHANGED_IP",
		"ON_CHANGE_DATETIME",
		"ON_CHANGE_USERINFO",
		"ON_REBOOTING_SYSTEM",
		"ON_REBOOT_RTSP_SERVER",
		//----------------------------------//
		"ON_EVENT_BASE",	//12
		"ON_EVENT_MOTION",
		"ON_EVENT_SCHEDULER",
		"ON_EVENT_SENSOR_ALARM",
		"ON_EVENT_RELAY",
		"ON_EVENT_NETWORK_DISCONNECTED",
		"ON_EVENT_SD_FULL",
		"ON_EVENT_SD_FAILURE",
		"ON_EVENT_IP_ADDR_CONFLICTED",
		"ON_EVENT_TEMPERATURE_CRITICAL",
		"ON_EVENT_ILLEGAL_LOGIN",	
		"ON_EVENT_USER_EVENT1",
		"ON_EVENT_USER_EVENT2",
		"ON_EVENT_USER_EVENT3",
		"ON_EVENT_USER_EVENT4",
		"ON_EVENT_USER_EVENT5",
		"ON_EVENT_USER_EVENT6",
		"ON_EVENT_USER_EVENT7",
		"ON_EVENT_USER_EVENT8",
		"ON_EVENT_USER_EVENT9",
		"ON_EVENT_USER_EVENT10",
		"ON_EVENT_USER_EVENT11",
		"ON_EVENT_USER_EVENT12",
		"ON_EVENT_USER_EVENT13",
		"ON_EVENT_USER_EVENT14",
		"ON_EVENT_USER_EVENT15",
		"ON_EVENT_USER_EVENT16",
		"ON_EVENT_TEMPERATURE_DETECTED", //hdseo for thermal
		"ON_EVENT_CUSTOM_SNAP", //hdseo for iNode
		"ON_EVENT_PIR_DETECTED", 
		"ON_EVENT_SYS_INIT",		// cmlee
		"ON_EVENT_END",
		]
}
function pad(n, width, z) {
  z = z || '0';
  n = n + '';
  return n.length >= width ? n : new Array(width - n.length + 1).join(z) + n;
}
function makeEvetCode(type, code, value, num) {
	var event_text = "";
	if(type == 2)
	{
		event_text = getLanguage(operation_code[code -1]);
	}
	else
	{
	if(code == 13 ||  // ON_EVENT_MOTION
	code == 15 ||     // ON_EVENT_SENSOR_ALARM
	code == 39 ||     // ON_EVENT_TEMPERATURE_DETECTED
	code == 40 ||     // ON_EVENT_CUSTOM_SNAP
	code == 41 ||     // ON_EVENT_PIR_DETECTED
	code == 42 ||     // ON_EVENT_SYS_INIT
	code == 16 )      // ON_EVENT_RELAY
	{
		if(code == 13)
		{
			if(value == 1)
			{
				event_text = getLanguage(event_code[code -1]) + " : " + (num + 1) + " : " + getLanguage("EVENT_ON");
			}
			else
			{
				event_text = getLanguage(event_code[code -1])  + " : " + (num + 1) + " : " + getLanguage("EVENT_OFF");
			}
		}
		else if(code == 23 || code == 40)
		{
				event_text = getLanguage(event_code[code -1]) + " : " + (value) + " : " + getLanguage("EVENT_ON");
		}
		else if(code == 39)
		{
			event_text = getLanguage(event_code[code -1]) + " : " + (num + 1) + " : " + (value) + " : " + getLanguage("EVENT_ON");
		}
		else
		{
			if(value == 1)
			{
				event_text = getLanguage(event_code[code -1])  + " : " + (num + 1) + " : " + getLanguage("EVENT_ON");
			}
			else
			{
				event_text = getLanguage(event_code[code -1])  + " : " + (num + 1) + " : " + getLanguage("EVENT_OFF");
			}		
		}
	}
	else
	{
		event_text = getLanguage(event_code[code -1]);
	}
	}
	
	return event_text;
}
function makeObjectToIP(object)
{
	if(object == 0)
	{
		return "system";
	}
	else
	{	
		var ip=(object%256 >= 0) ? (object%256) : ((object%256) + 256) ;
		for (var i=1;i<=3;i++)
		{
		  object=Math.floor(object/256);
		  ip=(object%256 >= 0) ? (object%256)+'.'+ip : ((object%256) + 256)+'.'+ip;
		}
		return ip; // As string
	}
}

function filterData( option ) {
	if( option == 1){
		$.extend(true, data ,getInformation("log_list"));
		$.extend(true, initdata ,data);
	}
	if( option == 2){
		$.extend(true, data ,initdata);
	}
	function timeToInt(hours, mins, secs){
		return (Number(hours) * 3600 + Number(mins) * 60 + Number(secs));
	}
	var mType = $("#sType").val();
	var regex;
	var mSort = $("#sSort").val();
	var mFromDate;
	var mToDate;
	var mFromTime;
	var mToTime;
	var date;
	var time;
	var tmp;

	var checkDate = $("#cDate").is(":checked"); 
	var checkTime = $("#cTime").is(":checked");
	var checkType = $("#cType").is(":checked");
	var checkSort = $("#cSort").is(":checked");
	if( mType == "events"){
		regex = 0;
	} else if( mType == "exceptions"){
		regex = 1;
	} else if( mType == "operations"){
		regex = 2;
	} else if( mType == "informations"){
		regex = 3;
	} else {
		regex = 4;
	}

	if( $("#dFromDate").val() == 0 && $("#dToDate").val() == 0) {
		checkDate = false;	
	}

	if( checkDate ){

        if(timeFormat == 0)
        {
            var mFromDate_split = $("#dFromDate").val().split('-');
            var mToDate_split = $("#dToDate").val().split('-');
            mFromDate = new Date(mFromDate_split[0]+'/'+mFromDate_split[1]+'/'+mFromDate_split[2]);
            mToDate = new Date(mToDate_split[0]+'/'+mToDate_split[1]+'/'+mToDate_split[2]);
        }
        else if(timeFormat == 1)
        {
            var mFromDate_split = $("#dFromDate").val().split('/');
            var mToDate_split = $("#dToDate").val().split('/');
            mFromDate = new Date(mFromDate_split[2]+'/'+mFromDate_split[0]+'/'+mFromDate_split[1]);
            mToDate = new Date(mToDate_split[2]+'/'+mToDate_split[0]+'/'+mToDate_split[1]);
        }
        else
        {
            var mFromDate_split = $("#dFromDate").val().split('/');
            var mToDate_split = $("#dToDate").val().split('/');
            mFromDate = new Date(mFromDate_split[2]+'/'+mFromDate_split[1]+'/'+mFromDate_split[0]);
            mToDate = new Date(mToDate_split[2]+'/'+mToDate_split[1]+'/'+mToDate_split[0]);
        }

	}
	if( checkTime ) {
		mFromTime = timeToInt($("#sFromHour").val(), $("#sFromMin").val(), $("#sFromSec").val());
		mToTime = timeToInt($("#sToHour").val(), $("#sToMin").val(), $("#sToSec").val());
	}
	if( checkSort ){
		mSort = $("#sSort").val();
	} else {
		mSort = "desc";
	}

	var newData = new Array();
	var insert;
	for( var i=0 ; i < data.length ; i++) {
		insert = true;
		if( checkDate ) {
			date = new Date(Number(data[i]['year']+1900) + "/" + Number(data[i]['month']+1) + "/" + Number(data[i]['day']));
			insert = (mFromDate <= date && mToDate >= date);
		}
		if( insert && checkTime ) {
			time = timeToInt( data[i]['hour'], data[i]['min'], data[i]['sec']);
            insert = ( mFromTime <= time && mToTime >= time);
		}
		if( insert && checkType ) {
			if( mType == "all") {
				insert = true;
			} else {
				insert = (regex == data[i]['type']) ? true : false;
			}
		}
		if( insert ) {
			if( mSort == "asc") {
				newData.unshift(data[i]);
			} else {
				newData.push(data[i]);
			}
		}
	}
	data = newData;
	//delete newdata;
	AMOUNT_OF_CONTENTS = data.length;
	AMOUNT_OF_PAGE = Math.ceil(AMOUNT_OF_CONTENTS / MAX_NUM_ITEM);
	SELECT_PAGE = 1;
	START_PAGE_NUM = 1;
}

function setPageInfo() {
	$("#page_list").find("*").remove();	
	$("#page_list").text("");

	var content="";
	for( var i = START_PAGE_NUM ; i < START_PAGE_NUM + MAX_NUM_PAGE && i <= AMOUNT_OF_PAGE ;  i++ ) {
		content += "<label class='page_num' id='page_" + i + "'> " + i + " </label>";
	}
	$("#page_list").append(content);

	if( $("#page_list").find(".page_num").length == 0 ) {
		$("#log_table").find(".list_items").remove();
		return false;
	}
	return true;
}
function initUI() {
/*
	if( capInfo['oem'] == 1){
		$("#backup_log").css("display","inline");
	}
*/
	$("#ui-datepicker-div").remove();
	$("#dFromDate").datepicker({
		defaultDate: "+1w",
		showButtonPanel: true,
		dateFormat: format,
		setDate: new Date(),
		onClose: function( selectedDate ) {
			$( "#dToDate" ).datepicker( "option", "minDate", selectedDate );
		}
	});
	$("#dToDate").datepicker({
		defaultDate: "+1w",
		showButtonPanel: true,
		dateFormat: format,
		maxDate: "+0D",
		setDate: new Date(),	
		onClose: function( selectedDate ) {
			$( "#dFromDate" ).datepicker( "option", "maxDate", selectedDate );
		}
	});
	for(var i=0 ; i < 24 ; i++ ){
		$("#sFromHour").append("<option val=" + i + ">"+i +"</option>")
		$("#sToHour").append("<option val=" + i + ">"+i +"</option>")
	}
	for(var i=0 ; i < 60 ; i++ ){
		$("#sFromMin").append("<option val=" + i + ">"+i +"</option>")
		$("#sToMin").append("<option val=" + i + ">"+i +"</option>")
	}
	for(var i=0 ; i < 60 ; i++ ){
		$("#sFromSec").append("<option val=" + i + ">"+i +"</option>")
		$("#sToSec").append("<option val=" + i + ">"+i +"</option>")
	}
	setPageInfo();

	if( true ) {
		$("#remove").prop("disabled", true);
		$("#properties").prop("disabled", true);
	}
}
function setEventForPageItem() {
	$(".page_num").click(function(e) {
		var range;
		var content;
		var datatime = "";

		$(".page_num_active").removeClass("page_num_active");
		$("#" + e.delegateTarget.id).addClass("page_num_active");
		SELECT_PAGE = Number($("#" + e.delegateTarget.id).text().trim());
		range = SELECT_PAGE * MAX_NUM_ITEM;
		$(".list_items").remove();
		// input the list
		content = "";
		// data[i]['time'], data[i]['type'], data[i]['code'], data[i]['value'], data[i]['id'],
		for(var i=range-MAX_NUM_ITEM ; i < range && i < AMOUNT_OF_CONTENTS ; i++) {
			datatime = pad(data[i]['year'] +1900, 4) + "/" + pad(data[i]['month'] +1, 2) + "/" + pad(data[i]['day'], 2) + " " + pad(data[i]['hour'], 2) + ":" + pad(data[i]['min'], 2) + ":" + pad(data[i]['sec'], 2);
			content += "<tr class='list_items'>";
			content += "<td width='30%'>" + getTimeStamp(new Date(datatime)) + "</td>";
			if(data[i]['logtype'] == 'legacy'){
				content += "<td width='45%' align='left'>" + makeEvetCode(data[i]['type'], data[i]['code'], data[i]['value'], data[i]['id']) + "</td>";
			
				content += "<td width='15%'>" + makeObjectToIP(data[i]['object']) + "</td>";
			}else if(data[i]['logtype'] == 'plain'){
				content += "<td width='45%' align='left'>" + data[i]['log'] + "</td>";
				
				content += "<td width='15%'></td>";

			}
			content += "</tr>";
		}
		$("#log_table").append(content);
		$(".result_filed").scrollTop(0);
	});
}	
function initEventForList() {
	setEventForPageItem();
	$(".result_filed").scrollTop(0);

	var disable;
	if( AMOUNT_OF_PAGE <= 10 ){
		disable = true;
	} else {
		disable = false;
	}
	$("#prev_page,#next_page").attr("disabled", true);

	$("#prev_page,#next_page").attr("disabled", AMOUNT_OF_PAGE < MAX_NUM_PAGE);
};
function initEvent() {
	initEventForList();

	function changePage(){
		setPageInfo();
		initEventForList();
		$("#page_" + SELECT_PAGE).trigger("click");
	}
	$("#prev_page").click( function() {
		if( SELECT_PAGE - MAX_NUM_PAGE > 0 ){
			SELECT_PAGE -= MAX_NUM_PAGE;
			SELECT_PAGE = START_PAGE_NUM = Math.floor(SELECT_PAGE/MAX_NUM_PAGE)*10+1 ;
			changePage();
		}
	});
	$("#next_page").click( function() {
		var next_page = (Math.floor((SELECT_PAGE-1)/MAX_NUM_PAGE))*10 + 1 + MAX_NUM_PAGE;
		if( next_page <= AMOUNT_OF_PAGE ) {
		//if( Number(SELECT_PAGE) + Number(MAX_NUM_PAGE) <= AMOUNT_OF_PAGE ){
		//	SELECT_PAGE += MAX_NUM_PAGE;
			SELECT_PAGE = next_page
			SELECT_PAGE = START_PAGE_NUM = Math.floor(SELECT_PAGE/MAX_NUM_PAGE)*10+1 ;
			changePage();
		}
	});

	$("#first_page").click( function() {
		SELECT_PAGE = 1;
		START_PAGE_NUM = 1;
		changePage();
	});
	function checkFilterOption(){
		if( $("[name=filter]:checked").length != 0 ) {
			$("#filter").attr("disabled", false);
		}
		else
		{
			$("#filter").attr("disabled", true);
		}
	}
	$("#cDate").click( function(e){
		$("#dFromDate").attr("disabled", !e.target.checked);
		$("#dToDate").attr("disabled", !e.target.checked);
		checkFilterOption();
	});
	$("#cTime").click( function(e) {
		$("#sFromHour").attr("disabled", !e.target.checked);
		$("#sFromMin").attr("disabled", !e.target.checked);
		$("#sFromSec").attr("disabled", !e.target.checked);
		$("#sToHour").attr("disabled", !e.target.checked);
		$("#sToMin").attr("disabled", !e.target.checked);
		$("#sToSec").attr("disabled", !e.target.checked);
		checkFilterOption();
	});
	$("#cType").click( function(e){
		$("#sType").attr("disabled", !e.target.checked);
		checkFilterOption();
	});
	$("#cSort").click( function(e){
		$("#sSort").attr("disabled", !e.target.checked);
		checkFilterOption();
	});
	if( capInfo['oem'] != 3){
		$("#last_page").click( function() {
			SELECT_PAGE = AMOUNT_OF_PAGE;
			START_PAGE_NUM = Math.floor((SELECT_PAGE-1)/MAX_NUM_PAGE)*10+1 ;
			changePage();
			$(".page_num:last").trigger('click');
		});		
		$("#filter").click( function(){
			filterData(2);
			if( setPageInfo())
				initEventForList(); 
			$(".page_num:first").trigger('click');
		});
			
		$("#refresh").click(function(){
			filterData(1);
			if( setPageInfo() )
				initEventForList(); 
			$(".page_num:first").trigger('click');
		});
	}
	var data ='';
	$("#backup_log").click(function(e) {
		var log_file='log.txt';
		var file_name;
		var lang;

		if(gLanguage == 0)     lang = "English";
		else if(gLanguage == 1) lang = "Korean";
		else if(gLanguage == 2) lang = "Japanese";
		else if(gLanguage == 3) lang = "Russian";

		var url = '/cgi-bin/admin/system.cgi?msubmenu=log';
		data += '&action=backup&lang='+lang;

		$.ajax({
			type:"get",
			url: url,
			data : data,
			beforeSend: function(){ progressUI(true); },
			success: function(data){
				progressUI(false);
				download(log_file);

			},
			error: function() {
				settingFail(menu, getLanguage("msg_fail_retry"));
				progressUI(false);
			}
		});

	});

	return this;
}
function download(file){
	var data;
	var getFile='/'+file;

	var browserState = 'unknown';
	var agent = navigator.userAgent.toLowerCase();
	if(agent.indexOf("chrome")!=-1) browserState="chrome";
	else if(agent.indexOf("safari")!=-1) browserState="safari";
	else if(agent.indexOf("firefox")!=-1) browserState="firefox";
	else if(agent.indexOf("msie")!=-1 || agent.indexOf('trident')!=-1) browserState="IE";
	
	var rawFile = new XMLHttpRequest();
	rawFile.open("GET", getFile, false);
	rawFile.onreadystatechange = function ()
	{
		if(rawFile.readyState === 4)
		{
			if(rawFile.status === 200 || rawFile.status == 0)
			{
				data = rawFile.responseText;
			}
		}
	}
	rawFile.send();

	var element = document.createElement('a');
	if(browserState == "chrome")
	{
		element.setAttribute('href', 'data:text/plain;charset=utf-8, '+encodeURIComponent(data));
		element.setAttribute('download', file);
		element.style.display = 'none';
		document.body.appendChild(element);
		element.click();
		document.body.removeChild(element);
	}else{
		var blob = new Blob([data], { type: 'text/csv' });
		if (window.navigator.msSaveOrOpenBlob) {
			window.navigator.msSaveBlob(blob, file);
		}
		else {
//			window.location = getFile;
			var url = URL.createObjectURL(blob);
			element.href = url;
			element.download = file;
			document.body.appendChild(element);
			element.click();
			setTimeout(function () {
				document.body.removeChild(element);
				window.URL.revokeObjectURL(url);
			}, 0);
		}
	}
}

function initValue() {
	$("#dFromDate").datepicker("setDate", new Date());
	$("#dToDate").datepicker("setDate", new Date());
}

function onLoadPage() {
	if( data != undefined ){
		AMOUNT_OF_CONTENTS = data.length;
		AMOUNT_OF_PAGE = Math.ceil(AMOUNT_OF_CONTENTS / MAX_NUM_ITEM);
		SELECT_PAGE = 1;
		START_PAGE_NUM = 1;
	}
	initUI();
	initValue();
	initEvent();

	$(".page_num:first").trigger('click');

}
$(document).ready( function() {
if( capInfo['oem'] != 3 ){
	$.extend( true, data ,getInformation("log_list"));
	$.extend( true, initdata, data );
}
	onLoadPage();
});
