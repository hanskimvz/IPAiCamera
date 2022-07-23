var MAX_NUM_ITEM = Number(20),
	MAX_NUM_PAGE = Number(10),
	START_PAGE_NUM,
	AMOUNT_OF_PAGE,
	AMOUNT_OF_CONTENTS,
	SELECT_PAGE,
	data,
	format = "yy-mm-dd",
	mStorageIndex=MJ.id,
	initdata = new Object();
if( timeFormat == 1 ){
	format = "mm/dd/yy";
}
else if( timeFormat == 2 ){
	format = "dd/mm/yy";
}
if( capInfo["board_chipset"]== "amba_s2lm55" || capInfo["board_chipset"]== "amba_s2l66" ){
    var file_type_ext= ".ts"
}
else{
    var file_type_ext= ".mp4"
}


function filterData(option) {
	if( option == 1){
		data = [];
		$.extend(true, data ,getInformation("record_list", mStorageIndex));
		$.extend(true, initdata ,data);
	}
	else if( option == 2){
		$.extend(true, data ,initdata);
	}

	function timeToInt(hours, mins, secs){
		return (Number(hours) * 3600 + Number(mins) * 60 + Number(secs));
	}
	var mEvent = $("#sEvent").val();
	var regex;
	var mStorage = $("#sStorage").val();
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
	var checkEvent = $("#cEvent").is(":checked");
	var checkStorage = $("#cStorage").is(":checked");
	var checkSort = $("#cSort").is(":checked");
	if( mEvent == "On Continous"){
		regex = /setup_continous/i;
	} else if( mEvent == "On Motion"){
		regex = /motion/i;
	} else if( mEvent == "On Schedule"){
		regex = /schedule/i;
	} else if( mEvent == "On Relay"){
		regex = /relay/i;
	} else if( mEvent == "On Sensor Alarm"){
		regex = /alarm/i;
	} else if( mEvent == "Network Disconnected"){
		regex = /network/i;
	} else if ( mEvent == "Temperature Critical") {
		regex = /temperature/i;
	} else if ( mEvent == "Illegal Login Detected") {
		regex = /illegal/i;
	} else if ( mEvent == "Temperature Detected") {
		regex = /temperature_detected/i;
	} else if ( mEvent == "Custum Event Detected") {
		regex = /iNode_detected/i;
	} else if ( mEvent == "System Initialize") {
		regex = /event_sys/i;
	} else {
		regex = /unkown/;
	}

	if( $("#dFromDate").val() == 0 && $("#dToDate").val() == 0) {
		checkDate = false;	
	}

	if( checkDate ){
//		mFromDate = new Date($("#dFromDate").val());
//		mToDate = new Date($("#dToDate").val());

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

		//mFromDate.setHours(00);
		//mToDate.setHours(24);
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
			date = new Date((data[i]['start'].split('-')[0]));
			insert = (mFromDate <= date && mToDate >= date);
		}
		if( insert && checkTime ) {
			tmp =  data[i]['start'].split('-')[1].split(":");
			time = timeToInt( tmp[0], tmp[1], tmp[2]);
			insert = ( mFromTime <= time && mToTime >= time);
		}
		if( insert && checkEvent ) {
			if( mEvent == "all") {
				insert = true;
			} else {
				insert = regex.test(data[i]['event']);
			}
		}
		if( insert && checkStorage ) {
			insert = ( data[i]['storage'].trim().toUpperCase() == mStorage.toUpperCase() 
					|| mStorage.toUpperCase() == "ALL");
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
		$("#result_table").find(".list_items").remove();
		return false;
	}
	return true;
}
function getProperty(in_location)
{
	var url;
	var returnValue;
	var tkoen, starttime, endtime, recordingtime, status;
	if( Browser.ie ) {
		url = in_location.replace(/(\/.+@)/, "//");
	} else {
		url = in_location;
	}
	$.ajax({
		type: "GET"
		, url: url 
		, async : false 
		, cache : false
		, username : userInfo.id
		, password : userInfo.pass 
		, context : this
		, success: function(ret){
			var timezone = new Date().getTimezoneOffset()* 60000,
				r_status = ret.substr(17,9).trim(),
				start = new Date(new Date(ret.substr(27,17).replace(/-|_/g, ' ').replace(/(\d\d\d\d)(\d\d)(\d\d)/g, '$1/$2/$3')).getTime() - timezone),
				end = new Date(new Date(ret.substr(45,17).replace(/-|_/g, ' ').replace(/(\d\d\d\d)(\d\d)(\d\d)/g, '$1/$2/$3')).getTime() - timezone),
				difftime = new Date(end-start);

			$("#p_token").text(ret.substr(0,16));
			$("#p_starttime").text( getTimeStamp(start, false));
			$("#p_endtime").text( getTimeStamp(end, false));
			$("#p_recordingtime").text(difftime.format("MM:ss"));
			$("#p_status").text(getLanguage(r_status));

			returnValue = true;
		}
		, statusCode : {
			404: function(){
				alert(getLanguage("html_error_404"));
			}
		}
		, error : function( msg ){
			$("#p_token").text("");
			$("#p_starttime").text("");
			$("#p_endtime").text("");
			$("#p_recordingtime").text("");
			$("#p_status").text("");

			returnValue = false;
		}
	}); 
	return returnValue;
}
function getDateOfList() {
	var info = $(".sel_record_item");

	if(info.length == 0)
		    settingFail(menu, getLanguage("msg_select_item"));

	var date_obj = info.find("td")[0].innerHTML;
	var time_obj = info.find("td")[1].innerHTML.split(':');
	
	if (timeFormat == 2)
	{
		date_obj = date_obj.split('/');
		date_obj = (date_obj[2]+"/"+date_obj[1]+"/"+date_obj[0]);
	}
	else if (timeFormat == 0)
	{
		if (!(Browser.firefox))
			date_obj = date_obj.replace('-','/');
	}

	if (time_obj[2].indexOf("pm") != -1)
		time_obj = ((+time_obj[0]+12)+":"+time_obj[1]+":"+time_obj[2].replace('pm',''));
	else
		time_obj = (time_obj[0]+":"+time_obj[1]+":"+time_obj[2].replace('am',''));

	return new Date(date_obj + " " + time_obj);  
}
function getFile(path) {
	var date = getDateOfList();
	var id = $(".sel_record_item").attr("id");
	var dir;
	var loc = document.location;
	if(path == 0){
		dir = "/sdcard/recording/"
	}else{
	dir = loc.protocol + "//";
	dir += userInfo.id + ":" + userInfo.pass + "@";
	dir += loc.host + "/storage" + mStorageIndex + "/";
	}

    //INODIC recording file name dose adding localtime
    if( capInfo["oem"]== 6 ){
        var ldate = new Date((date/1000-((gmt-12)*3600) )* 1000);
        dir += ldate.format("yyyymmdd/HH/yyyymmdd_HHMMss_", false) + id + ldate.format("/yyyymmdd_HH/yyyymmdd_HHMMss",false) + "_(localtime_" + date.format("yyyymmdd_HHMMss)_",false)+ id;
	}
	else if( capInfo["oem"]== 19 ){// hdseo for iNode
		//sprintf(iNode_name, "clip_%04d%02d%02d%02d%02d%02d", stime.tm_year+1900, stime.tm_mon+1, stime.tm_mday ,stime.tm_hour, stime.tm_min, stime.tm_sec);
		dir += date.format("yyyymmdd/HH/yyyymmdd_HHMMss_", true) + id + date.format("/yyyymmdd_HH/",true) + "clip_" + date.format("yyyymmddHHMMss",true);
	}else{
        dir += date.format("yyyymmdd/HH/yyyymmdd_HHMMss_", true) + id + date.format("/yyyymmdd_HH/yyyymmdd_HHMMss_",true) + id;
    }
    return dir;
}
function getDateOfFile() {
	var date = getDateOfList();
	var timezone = new Date().getTimezoneOffset()* 60000;
    var ldate = new Date(date - timezone);
	var id = $(".sel_record_item").attr("id");
	var dir = "";
	dir += ldate.format("yyyy/mm/dd HH:MM:ss", true);

	return dir;
}
function initUI() {
	function initializeStorageDevice() {
		var content ='',
			index=0;

		mStorageDeviceConf.forEach(function(Device) {
			if( Device.hasOwnProperty("Type")) {
				if( Device.Type != 0 ){
					content += '<option value="' + index + '">' + getLanguage('storage');
					content += ++index + '</option>';
				}
			}
		});
		if( content.length > 0 ) {
			$("#storage_index").append(content);
		}
		else {
			$("#storages").remove();
		}
	}
	if( capInfo.relay_count <= 0 ) $("#sEvent option[value='On Sensor Alarm']").remove();
	if( capInfo.camera_type != "thermal" ) $("#sEvent option[value='Temperature Detected']").remove();
	initializeStorageDevice();
	
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
	var cmd= '';
	for(var i=0 ; i < 24 ; i++ ){
		cmd += "<option value=" + i + ">"+i +"</option>";
	}
	$("#sFromHour").append(cmd);
	$("#sToHour").append(cmd);

	cmd ='';
	for(var i=0 ; i < 60 ; i++ ){
		cmd += "<option value=" + i + ">"+i +"</option>";
	}
	$("#sFromMin").append(cmd);
	$("#sToMin").append(cmd);

	cmd ='';
	for(var i=0 ; i < 60 ; i++ ){
		cmd += "<option value=" + i + ">"+i +"</option>";
	}
	$("#sFromSec").append(cmd);
	$("#sToSec").append(cmd);
	setPageInfo();

	if( true ) {
		$("#remove").prop("disabled", true);
		$("#properties").prop("disabled", true);
	}

	// Handle options tag "selected" according to current MJ.id
	var options = $("#storage_index > option")
	if( options ) {
		options.each(function (index, option) {
			if(option.value == mStorageIndex) 
			option.selected = true;
		})
	}
}

function setEventForRecordItem(){
	$(".list_items").on("click", function(e) {
		$("#result_table").find("tr").removeClass("sel_record_item");
		$("#" + e.delegateTarget.id).addClass("sel_record_item");
	});
	$(".list_items").on("dblclick", function(e) {
		$("#play").trigger("click");
	});
}
function getEvent( val ){	
	var flag = 1; 
	var option = "" ;
	
	switch( val ){
		case "setup_continous":
		case "ON_EVENT_MOTION":
		case "ON_EVENT_SCHEDULER":
		case "ON_EVENT_RELAY":
		case "ON_EVENT_SENSOR_ALARM":
			flag = 1 ;
			break;
		default:
			flag = 0 ;
			break;		
	}		
	if( flag == 0 ) option = "<br>";	
	
	if( 23 <= val && val <= 38) return getUserEvent( val ); //UDP technology - add vca user event
	if( val == "ON_EVENT_SCHEDULER" && ( capInfo["oem"]==11 || capInfo["oem"]==25 )){
		return getLanguage("ON_EVENT_RECURRENCES") + option;
	} else {
		return getLanguage(val) + option ;
	}
}
//UDP technology - add getUserEvent function
function getUserEvent( val ){	
	$.ajaxSetup({async: false});
	var zoneid = '';
	$.get("/plugin_user_event_index_ext.txt", function(data, status){
		var tmp= data.trim().split('\n');
		for(var i=0; i<tmp.length; i++) {
			if(tmp[i].split('=')[1] == val) {
				zoneid = tmp[i+1].split('*|')[3];
				if(zoneid == 'all') zoneid = tmp[i+1].split('*|')[2];
			}
		}
	});
	$.ajaxSetup({async: true});
	return zoneid;
}
function setEventForPageItem() {
	$(".page_num").click(function(e) {
		var range;
		var content;

		$(".page_num_active").removeClass("page_num_active");
		$("#" + e.delegateTarget.id).addClass("page_num_active");
		SELECT_PAGE = Number($("#" + e.delegateTarget.id).text().trim());
		range = SELECT_PAGE * MAX_NUM_ITEM;
		$(".list_items").remove();
		// input the list
		content = "";
		var i, duration, _date;
		for(i=range-MAX_NUM_ITEM ; i < range && i < AMOUNT_OF_CONTENTS ; i++) {
			_date = getTimeStamp(new Date(data[i]['start'].replace('-', ' '))).split(' ');
			content += "<tr class='list_items' id='"+ data[i]['key'] +"'>";
			content += "<td class='qt'>" + _date[0]+ "</td>";
			content += "<td class='qt'>" + _date[1]+ "</td>";
			duration = (data[i].flag & 4) != 4 ?  duration = data[i]['duration'] : "-";
			content += "<td class='qt'>" + duration + "</td>";
			
//			content += "<td class='qt'>" + data[i]['event'].replace(/,/g, "<br>") + "</td>";
			content += "<td class='qt'>" +getEvent( data[i]['event'] ) + "</td>";
			content += "</tr>";
		}
		$("#result_table").append(content);
		setEventForRecordItem();
		$(".result_filed").scrollTop(0);
	});
}	
function initEventForList() {
	setEventForPageItem();
	setEventForRecordItem();
	$(".result_filed").scrollTop(0);

	var disable;
	if( AMOUNT_OF_PAGE <= 10 ){
		disable = true;
	} else {
		disable = false;
	}
	$("#prev_page,#next_page").attr("disabled", true);

	$("#prev_page,#next_page").attr("disabled", AMOUNT_OF_PAGE < MAX_NUM_PAGE);
	$("#first_page,#last_page").attr("disabled", AMOUNT_OF_PAGE <= 1);
	console.log("AMOUNT_OF_PAGE"+AMOUNT_OF_PAGE);
};
function initEvent() {
  menu = getLanguage("setup_reccording");
	initEventForList();
	$("#back").click(function(e) {
		var vlc = document.getElementById("vlc");
        
        if((navigator.userAgent.indexOf("MSIE") != -1 ) || (!!document.documentMode == true )) //IF IE > 10
        {
		    vlc.playlist.stop();
    		vlc.playlist.clear();
        }
        $("#recording").css("display", "block");
		$("#record_video").css("display", "none");
	});
	$("#replay").click(function(e){
        if((navigator.userAgent.indexOf("MSIE") != -1 ) || (!!document.documentMode == true )) //IF IE > 10
        {
	    	document.getElementById("vlc").playlist.stop();
	    	document.getElementById("vlc").playlist.play();
        }
	})
	$("#play").click(function(e) {
		var target = $(".sel_record_item");
		if ( target.length === 0 ) return false;
		var location = getFile();
		if( typeof(location) !== "undefined"){
			if( getProperty(location + ".txt") == true ) {
				$("#record_video").show(1,function(){
					$("#recording").hide();
					var vlc = document.getElementById("vlc");
                    if((navigator.userAgent.indexOf("MSIE") != -1 ) || (!!document.documentMode == true )) //IF IE > 10
                    {
					    vlc.playlist.clear();
				    	item = vlc.playlist.add(location + file_type_ext);
				    	vlc.playlist.play();
                    }else{
                        $("#replay").attr("disabled", true);
                    }
				});
			}
		}
	});
	$("#filter").click( function(){
		filterData(2);
		if( setPageInfo() )
			initEventForList(); 
		$(".page_num:first").trigger('click');
	});
	$("#download").click( function(e){
		if(capInfo["oem"] == 19 )
		{
			$("#download_video").show(1,function(){
				$("#recording").hide();
				$("#download_key").val('');
				$("#download_purpose").val('');
			});
		}
		else
		{
			var dateOffile = getDateOfFile();
			var pop_menu = "Input the purpose of the file download (max : 32 characters)";
			var reason = prompt(pop_menu,'');
			var pop_msg ="";
			if (!checkCharacters("record", reason))
			{
				pop_msg = getLanguage("msg_onlyalphabet");
				if( gLanguage == 0 ){
					pop_msg = getLanguage("msg_onlyalphabet")+" ( only [-],[_] ).";
				}
				else if( gLanguage == 1 ){
					pop_msg = getLanguage("msg_onlyalphabet")+ " [-],[_] " + getLanguage("msg_onlyalphabet1");
				}
				settingFail(menu, pop_msg);
				return 0;
			}
			var datas = "";
			datas += "file=" + dateOffile + "&";
			//????????? ????????????
			datas += "reason=" + encodeURIComponent(reason);
			if(datas.length != 0) {
				datas = "msubmenu=export&" + datas;
			} else {
				return ;
			}
			$.ajax({
				type:"get",
				url: "/cgi-bin/admin/record.cgi",
				data: datas,
				success: function(msg){
					var tmp= msg.trim().split('\n');
					var response = tmp[0];
					var error_code = tmp[1];
					if(response == "OK") {
						var file = getFile();
						url = file.replace(/(\/.+@)/, "//");
						url += file_type_ext;				  
						$("#forDownload").attr('src', url);
					} else {
						var err_msg ="";
						err_msg = getLanguage("msg_onlyalphabet");
						if( gLanguage == 0 ){
							err_msg = getLanguage("msg_onlyalphabet")+" ( only [-],[_] ).";
						}
						else if( gLanguage == 1 ){
							err_msg = getLanguage("msg_onlyalphabet")+ " [-],[_] " + getLanguage("msg_onlyalphabet1");
						}  
						settingFail(menu, err_msg);
					}
				},
				error: function() {
					settingFail(menu, getLanguage("msg_fail_retry"));
				}
			});		

			//$("#forDownload").attr('src', url);
			/*
			   $.get(url, function(ret){
			   var completed = new RegExp(/completed/g);
			   if( completed.test(ret)) $("#forDownload").attr('src', file + ".ts");
			   else settingFail("download", "this file is recording!. please retry download after complete");
			   });
			   */
		}
	});
	$("#cancel").click(function(e) {
		$("#recording").show(1,function(){
			$("#download_video").hide();
		});
	});
	$("#btOK").click(function(e) {
		var dateOffile = getDateOfFile();
		if($("#download_key").val.length>32 || $("#download_purpose").val().length>32){
			settingFail(menu, getLanguage("msg_invalid_text_length")+"(32)");
			return 0;
		}
		var file = getFile(0);
		var path = file.replace(/(\/.+@)/, "//");
		path += file_type_ext;
		var datas = "";
		datas += "file=" + dateOffile + "&";
		datas += "key=" + encodeURIComponent($("#download_key").val())+"&";
		datas += "path="+path+"&";
		datas += "reason=" + encodeURIComponent($("#download_purpose").val());
		if(datas.length != 0) {
			datas = "msubmenu=export&" + datas;
		} else {
			return ;
		}
		$.ajax({
			type:"get",
			url: "/cgi-bin/admin/record.cgi",
			data: datas,
			beforeSend: function(){ progressUI(true); },
			success: function(msg){
				var tmp= msg.trim().split('\n');
				var response = tmp[0];
				var error_code = tmp[1];
				if(response == "OK") {
					document.location = "/cgi-bin/admin/record.cgi?msubmenu=download&path="+path+".enc";
					progressUI(true);
				} else {
					settingFail(menu, getLanguage("msg_fail_retry"));
				}
				progressUI(false);
			},
			error: function() {
				settingFail(menu, getLanguage("msg_fail_retry"));
				progressUI(false);
			}
		});		

	});
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
	$("#last_page").click( function() {
		SELECT_PAGE = AMOUNT_OF_PAGE;
		START_PAGE_NUM = Math.floor((SELECT_PAGE-1)/MAX_NUM_PAGE)*10+1 ;
		changePage();
		$(".page_num:last").trigger('click');
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
	$("#cEvent").click( function(e){
		$("#sEvent").attr("disabled", !e.target.checked);
		checkFilterOption();
	});
	$("#cStorage").click( function(e){
		$("#sStorage").attr("disabled", !e.target.checked);
		checkFilterOption();
	});
	$("#cSort").click( function(e){
		$("#sSort").attr("disabled", !e.target.checked);
		checkFilterOption();
	});
	$("#refresh").click(function(){
		filterData(1);
		if( setPageInfo() )
			initEventForList(); 
		$(".page_num:first").trigger('click');
	});
	$("#storage_index").change(function(obj){
		mStorageIndex = $("#storage_index").val();
    MJ.id = mStorageIndex;
		filterData(1);
		if( setPageInfo() )
			initEventForList(); 
		$(".page_num:first").trigger('click');
	});
	return this;
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
	$.extend(true, data ,getInformation("record_list", mStorageIndex));
	$.extend(true, initdata, data);
	onLoadPage();
});
