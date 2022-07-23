var menu = "Action Rules Setting";
var data, action_data;
var select_item = -1;
var MODE = "list";

var WeekList = [ "sun" , "mon", "tue", "wed", "thu", "fri", "sat" ];
var TimeList = ["shour", "smin", "ehour", "emin" ];
var SettingList = $.merge(["enabled", "name","always", "action_id"], WeekList);

var text = getXmlData();
var parser = new DOMParser();
var xmlDoc = parser.parseFromString(text,"text/xml");
var length = xmlDoc.querySelectorAll('userevent').length;
if( xmlDoc ) {
	for(var i = 0 ; i < length ; i++) {
		if(xmlDoc.getElementsByTagName("eventname")[i]) {
			EventConditionMax++;
		}
	}
}
var isUsereventFlag = 0;
var EventSettingList = Array();
for( var  i = 0 ; i < EventConditionMax ; i++) {
	EventSettingList[i] = ["event" + i + "_type" , "event" + i + "_index" ];
}
var NONE= getLanguage('setup_none');
var MOTION = getLanguage("setup_motion_detection");
var SCHEDULER = getLanguage("schedule");
var RECURRENCES = getLanguage("recurrences");
var SENSOR_ALARM = getLanguage("setup_sensor_detection");
var TEMPERATURE_ALARM = getLanguage("setup_temperature_critical");
var TEMPERATURE_ALARM_SEEK = getLanguage("setup_temperature_critical_seek");
var NETWORK_DISCONNECTED_ALARM = getLanguage("setup_network_disconnected");
var ILLEGAL_LOGIN_ALARM = getLanguage("setup_illegal_login");
var SD_FULL_ALARM = getLanguage("setup_hdd_full");
var TEMPERATURE_DETECTED = getLanguage("setup_temperature_detected");
var TEMPERATURE_DETECTED_SEEK = getLanguage("setup_temperature_detected_seek");
var CUSTOM_SNAP_DETECTED = getLanguage("setup_custom_event_detected");
var PIR_DETECTED = getLanguage("setup_pir_detection");
var SYS_INIT = getLanguage("setup_system_initialize");

var ActionTypeList = [ {"name": NONE, "value": ON_EVENT_NONE} ,
{"name" : MOTION, "value" : ON_EVENT_MOTION }];
//{"name" : NETWORK_DISCONNECTED_ALARM, "value" : ON_EVENT_NETWORK_DISCONNECTED },
//{"name" : ILLEGAL_LOGIN_ALARM, "value" : ON_EVENT_ILLEGAL_LOGIN }];

if( capInfo.sensor_count > 0 || capInfo.have_sdcard > 0)  {
    $.merge( ActionTypeList, [{"name" : NETWORK_DISCONNECTED_ALARM, "value" : ON_EVENT_NETWORK_DISCONNECTED }]);
}

$.merge( ActionTypeList, [{"name" : ILLEGAL_LOGIN_ALARM, "value" : ON_EVENT_ILLEGAL_LOGIN }]);


	if( xmlDoc ) {
		for(var i = 0 ; i < length ; i++) {
			if(xmlDoc.getElementsByTagName("eventname")[i] && xmlDoc.getElementsByTagName("eventid")[i]) {
				if(xmlDoc.getElementsByTagName("eventname")[i].childNodes[0].nodeValue.split(",").length > 1) // One plugin, several events
					multiEventParse(i);
				else {
          if(capInfo.video_in > 1) {
            for(var j=0; j<capInfo.video_in; j++) {
              $.merge( ActionTypeList, [{"name" : xmlDoc.getElementsByTagName("eventname")[i].childNodes[0].nodeValue + '#' + Number(j+1), "value" : getUserEventIndex(xmlDoc.getElementsByTagName("eventid")[i].childNodes[0].nodeValue, j+1) }]);
            }
          } else {
            $.merge( ActionTypeList, [{"name" : xmlDoc.getElementsByTagName("eventname")[i].childNodes[0].nodeValue, "value" : getUserEventIndex(xmlDoc.getElementsByTagName("eventid")[i].childNodes[0].nodeValue) }]);
          }
        }
			}
		}
	}
if(capInfo["oem"]==11 || capInfo["oem"]==25){
	$.merge( ActionTypeList, [{"name" : RECURRENCES, "value" : ON_EVENT_SCHEDULER }]);
}else if(capInfo["oem"] != 2){
	$.merge( ActionTypeList, [{"name" : SCHEDULER, "value" : ON_EVENT_SCHEDULER }]);
}
if( capInfo.temperature_support ) {
	if( capInfo.camera_type == "seekware")
		$.merge( ActionTypeList, [ {"name" : TEMPERATURE_ALARM_SEEK, "value" : ON_EVENT_TEMPERATURE_CRITICAL }])
	else
		$.merge( ActionTypeList, [ {"name" : TEMPERATURE_ALARM, "value" : ON_EVENT_TEMPERATURE_CRITICAL }])
}
if( capInfo.sensor_count > 0 ) {
	var obj = { "name" : SENSOR_ALARM , "value" : ON_EVENT_SENSOR_ALARM };
	$.merge(ActionTypeList, [obj]);
}
if( capInfo.camera_type == "CUBE" ) {
	var obj = { "name" : PIR_DETECTED , "value" : ON_EVENT_PIR_DETECTED };
	$.merge(ActionTypeList, [obj]);
}
if( capInfo.camera_type == "thermal" ) {
	var obj = { "name" : TEMPERATURE_DETECTED , "value" : ON_EVENT_TEMPERATURE_DETECTED };
	$.merge(ActionTypeList, [obj]);
}
if( capInfo.camera_type == "seekware" ) {
	var obj = { "name" : TEMPERATURE_DETECTED_SEEK , "value" : ON_EVENT_TEMPERATURE_DETECTED };
	$.merge(ActionTypeList, [obj]);
}
if( capInfo["oem"]==19) {
	var obj = { "name" : CUSTOM_SNAP_DETECTED , "value" : ON_EVENT_CUSTOM_SNAP };
	$.merge(ActionTypeList, [obj]);
}
if(capInfo["oem"] == 2){
	$.merge( ActionTypeList, [{"name" : SYS_INIT, "value" : ON_EVENT_SYS_INIT }]);
}


function readTextFile(file)
{
	var allText = '';
	var rawFile = new XMLHttpRequest();
	rawFile.open("GET", file, false);
	rawFile.onreadystatechange = function ()
	{
		if(rawFile.readyState === 4)
		{
			if(rawFile.status === 200 || rawFile.status == 0)
			{
				allText = rawFile.responseText;
			}
		}
	}
	rawFile.send(null);
	return allText;
}
function getXmlData()
{
	var timestamp = new Date().getTime();
	var file = "/plugin_info_list.xml?timestamp="+timestamp;
	var xmlDoc = readTextFile(file);//parser.parseFromString(text,"text/xml");
	return xmlDoc;
}
function multiEventParse(index)
{
	var multiEvent = xmlDoc.getElementsByTagName("eventname")[index].childNodes[0].nodeValue.split(",");
	var multiEventId = xmlDoc.getElementsByTagName("eventid")[index].childNodes[0].nodeValue.split(",");
	var multiEventLength = multiEvent.length;
	for(var j = 0; j < multiEventLength; j++) {
		$.merge( ActionTypeList, [{"name" : multiEvent[j], "value" :  getUserEventIndex(multiEventId[j]) }]);
	}
}
function getUserEventIndex(eventId, vinSourceVal)
{
	var timestamp = new Date().getTime();
	var file = "/plugin_user_event_index.txt?timestamp="+timestamp;
	var doc = readTextFile(file);
	var lines = doc.split('\n');
	var eventIndex = 0;
	for(var i = 0;i < lines.length;i++) {
		if(lines[i].search(eventId) >= 0){
      if(capInfo.video_in > 1) {
        eventIndex = (lines[i].split('V' + vinSourceVal + '_VCA_ALL='))[1];
      } else {
        eventIndex = (lines[i].split('all='))[1];
      }
			if(eventIndex != undefined)
				break;
		}
	}
	return eventIndex;
}
function verifyUserEventIndex(type)
{
	var timestamp = new Date().getTime();
	var file = "/plugin_user_event_index.txt?timestamp="+timestamp;
	var doc = readTextFile(file);
	var lines = doc.split('\n');
	var eventIndex = 0;
	for(var i = 0;i < lines.length;i++) {
		if(lines[i].search('='+type) >= 0 && lines[i].indexOf('all') < 0 && lines[i].indexOf('ALL') < 0){
			eventIndex = (lines[i].split('='))[1];
			if(eventIndex != undefined)
				break;
		}
	}
	return eventIndex.toString();
}
function checkList(target) {
	var obj;
	obj = $("#" + target);
	if( obj.length == 0){
		obj = $("[name=" + target  +"]");
		if( obj.length == 0){
			return null;
		}
	}
	return obj;
}
function getValue(obj) {
	var ret = null;
	if( obj.prop("type") == "radio") {
		ret = $("[name="+obj[0].name+"]:checked").val();
	} else if( obj.prop("type") == "checkbox") {
		if( obj.prop("checked") == true) {
			ret = 1;
		} else {
			ret  = 0;					
		}
	} else { // select, input
		ret  = obj.val();				
	}
	return ret;	
}
/* ------------------------------------- INITIALIZING END --------------------------------------- */
function ChangeUI(view) {
	if( view == "add" || view == "modify") {
		$("#actions_list").css("display", "none");
		$("#action_add_modify").css("display", "block");	
	} else {
		MODE = "LIST";
		$("#actions_list").css("display", "block");
		$("#action_add_modify").css("display", "none");	
	}
}
function initSettingsValue(index){ // initvalue required for add, modify, remove
  var content="";
	try{
		if( typeof(index) == "undefined" )
		{
			$("#enabled_on").trigger("click");
			$("#name").val("NewRule");
			$("#action_id").find("*").remove();
			content = "<option value='0'>"+ getLanguage('setup_none') + "</option>";
			for( var i = 0 ; i < action_data.length ; ++ i){
				content += "<option value='" + action_data[i].id + "'>"  + action_data[i].name + "</option>";
			}
			$("#action_id").append(content).val(0);
			$("[name=event_type]").val(0);
			$("#always_on").trigger("click");
			$("#action_id").val(0);
			$("#shour").val(0);
			$("#ehour").val(0);
			$("#smin").val(0);
			$("#emin").val(0);
		}
		else
		{
			if( data[index].enabled == 1) {
				$("#enabled_on").trigger("click");
			} else {
				$("#enabled_off").trigger("click");
			}
			$("#name").val(data[index].name);

			$("#action_id").find("*").remove();
			for( var i = 0 ; i < action_data.length ; ++ i){
				content += "<option value='" + action_data[i].id + "'>"  + action_data[i].name + "</option>";
			}
			$("#action_id").append(content).val(data[index]['action_id']);
			
			for(var i = 0 ; i < data[index].event_type.length ; i++)
			{
				if( data[index].event_type[i].enabled == 1 ){
					$("#event" + i + "_type").val(data[index].event_type[i].type)
				}
				else
					$("#event" + i + "_type").val("0");
			}
			if( data[index].always == 1) {
				$("#always_on").trigger("click"); 
			} else {
				$("#always_off").trigger("click"); 
			}
			for(var i = 0 ; i < WeekList.length ; i++){
				$("#" + WeekList[i]).prop("checked",
					data[index][WeekList[i]] == 0 ? false : true);
			}
			for( var i=0 ; i < TimeList.length ; i++) {
				$("#" + TimeList[i]).val(data[index][TimeList[i]]);
			}
		}
	} catch(e)	{
		ERROR("EROR: initSettingsValue [" + e + "]");
	}
}

function initUI() {
	function addHourMin(obj, max) {
		var content=""; 
		for(var i=0 ; i < max ; i++ ){
			content += "<option value='" + i + "''>";
			if( i < 10 )	content += "0" + i.toString();
			else			content += i.toString();
			content += "</option>";
		}
		$("#" + obj).append(content);
	}
	addHourMin("shour", 24);
	addHourMin("ehour", 24);
	addHourMin("smin", 60);
	addHourMin("emin", 60);
	if( !capInfo.sesnsor_count )
		$("[name=event_type]").find("option[value=512]").remove();
	if( !capInfo.relay_count )
		$("[name=event_type]").find("option[value=1024]").remove();
	if( data.length == MaxNumTrigger ) $("#add").attr("disabled", true);

	for( var i = 0 ; i < ActionTypeList.length; i++) {
		$("[name=event_type]").append("<option value=" + ActionTypeList[i].value + ">" + ActionTypeList[i].name + "</option>");
	}
}
function setEventForListItem(){
	$("tr[name=list_items]").on("click", function(e) {
		if(isUsereventFlag != 0) {
			$("#event0_type").attr("disabled", false);
			$("[name=event_type]").find("option[value="+ isUsereventFlag +"]").remove();
			$("#action_id").attr("disabled", false);
			isUsereventFlag = 0;
		}
		$("tr[name=list_items]").removeClass("sel_list_item");
		$("#" + e.delegateTarget.id).addClass("sel_list_item");
        select_item = Number($(".sel_list_item").attr("val"));
        if(capInfo["oem"]==19 && select_item == 0 && data[select_item]["name"]=="iNode Event")
        {
            $("#modify").attr("disabled", true);
        }
        else
            $("#modify").attr("disabled", false);
            
		$("#event0_type").attr("disabled", false);
		$("#action_id").attr("disabled", false);
		$("#delete").attr("disabled", false);
		for(var i = 0; i < data[select_item].event_type.length; i++) { 
			var eve = data[select_item].event_type[i];
			res = verifyUserEventIndex(eve.type);
			if(res == eve.type) {
				if(e.currentTarget.innerHTML.split("</td>")[1].split(">")[1].toLowerCase() == "user event"
					|| e.currentTarget.innerHTML.split("</td>")[1].split(">")[1].toLowerCase() == "vca_user_event") {
					$("#event0_type").attr("disabled", true);
					if(isContain(res)) 
						$("[name=event_type]").append("<option value=" + res + ">User event</option>");
					$("#event0_type").val(res);
					$("#action_id").attr("disabled", true);
					$("#delete").attr("disabled", true);
				}
				else {
					$("#event0_type").attr("disabled", false);
					if(res != 0)
						$("[name=event_type]").find("option[value="+ res +"]").remove();
					$("#action_id").attr("disabled", false);
					$("#delete").attr("disabled", false);
				}
			}
		}
	});
}
function isContain(res) {
	var added_options = [];
	var evttype = $("[name=event_type]")[0].options;
	var eventlist = Object.keys(evttype).map(function(i) { return evttype[i]; });
	for(var i=0; i < eventlist.length; i++){
		added_options.push(eventlist[i].value);
	}
	if(added_options.indexOf(res)>-1){
		return false;
	} else {
		added_options.push(res);
		isUsereventFlag = res;
		return true;
	}
}
function disabledButton(cmd)
{
	if( cmd !== true && cmd != false ) return -1;
	$("button").attr("disabled", cmd);
	if( data.length == MaxNumTrigger ) $("#add").attr("disabled", true);
}
function check_name(val){
	for(i=0; i < data.length; i++){
		if(data[i]["name"] == val){
			return false ;
		}
    }
    if(capInfo["oem"]==19 && "iNode Event" == val){//iNode
        //console.log("name:" + data[i]["name"]);
        return false ;
    }
	return true ;
}
function initEvent() {
	menu = getLanguage("setup_event_rules_config");

	setEventForListItem();
	$("#add").click(function(e){
		if(isUsereventFlag != 0) {
			$("#event0_type").attr("disabled", false);
			$("[name=event_type]").find("option[value="+ isUsereventFlag +"]").remove();
			$("#action_id").attr("disabled", false);
		}
		if( action_data.length == 0)
		{
			
			settingFail(menu, getLanguage("msg_please_actionrule"));
			return 0;
		}
		MODE = "add";
		ChangeUI(e.currentTarget.id);
		initSettingsValue();
	});
	$("#modify").click(function(e){
		if(isUsereventFlag != 0) {
			$("#event0_type").attr("disabled", true);
			$("[name=event_type]").append("<option value=" + isUsereventFlag + ">User event</option>");
			$("#event0_type").val(isUsereventFlag);
			$("#action_id").attr("disabled", true);
		}
		if( select_item < 0 )
		{
			settingFail(menu, getLanguage("msg_select_item")); 
			return ;
		}
		MODE = "modify";
		ChangeUI(e.currentTarget.id);
		initSettingsValue(select_item);
	});
	$("#delete").click(function(e){
		var datas;
		if( select_item < 0 )
		{
			settingFail(menu, getLanguage("msg_select_item"));
			return ;
		}
		disabledButton(true);
		datas = "msubmenu=event&action=remove&id="+ data[select_item].id;
		$.ajax({
			type:"get",
			url: "/cgi-bin/admin/trigger.cgi",
			async : false,
			data: datas,
			success: function(msg){
				var tmp= msg.trim().split('\n');
				var response = tmp[0];
				var error_code = tmp[1];
				var pattern = /OK/;
				if(pattern.test(msg) == true) {
					settingSuccess(menu, null);
					refreshMenuContent();
				} else {
					settingFail(menu, getLanguage("msg_fail"));
				}
			},
			error: function() {
				settingFail(menu, getLanguage("msg_fail_retry"));
				refreshMenuContent();
			}
		});
		disabledButton(false);
	});	
	$("#save").click(function(e){
		disabledButton(true);
		var datas;
		var newValue;
		var orgValue;
		var schedule_always;
		var obj;
		var type = /event\d_type/;
		var changed = 0 ;
		var activeitem = 0 ;
		try {
			schedule_always = $("[name=always]:checked").val();
			if( schedule_always ){
				SettingLlist = $.merge(SettingList, TimeList);
			}		

			for( var i = 0 ; i < SettingList.length ; i++) {                     	//CHECK General&EventCondition
				obj = checkList( SettingList[i] );
				
				if( obj === null ) continue;
				newValue = getValue(obj);
				if( newValue === null) {
					continue;
				}
				
				if( MODE == "modify" ) {	
					orgValue = data[select_item][SettingList[i]];
					if( orgValue == newValue ) continue;
				}
				if( SettingList[i] == "name" ){
					if( !isValidText(newValue) ) {
						settingFail(menu, getLanguage("msg_invalid_text"));
						disabledButton(false);
						$("tr[name=list_items]").removeClass("sel_list_item");
						select_item = -1;
						return;
					}
					if( newValue.length < 3 || newValue.length > 15 ){
						settingFail(menu, getLanguage("msg_invalid_text_length") + "(3~15)");
						disabledButton(false);
						$("tr[name=list_items]").removeClass("sel_list_item");
						select_item = -1;
						return;
					}
					if( check_name(newValue) == false ){
						settingFail(menu, getLanguage("msg_check_event_name"));
						disabledButton(false);
						$("tr[name=list_items]").removeClass("sel_list_item");
						select_item = -1;
						return;
					}					
				}
				if( typeof(datas)  == 'undefined') {
					datas = SettingList[i] + "=" + newValue;
				} else {
					datas += "&" + SettingList[i] + "=" + newValue;
				}
				if( newValue != orgValue ) changed = 1 ;
				
			}
			 
			for( var i = 0 ; i < EventSettingList.length ; i++ )                   	// check event 5_item   
			{
				for( var j = 0 ; j < 2; j++) 
				{
					obj = checkList( EventSettingList[i][j] );           // check error
					
					if( obj === null ) continue;						
					newValue = getValue(obj);					
					
					if( newValue === null) {
						continue;
					}
					
					if( MODE == "modify" ){						
//						if( orgValue === null ) continue;	
//						if( newValue == orgValue ) continue;
					}
					if( type.test(EventSettingList[i][j])){
						if( newValue != 0 )// NONE
						{
							datas += "&" + EventSettingList[i][j] + "=" + newValue + "&event" + i + "_enabled=1";
						}
						else
						{
							datas += "&event" + i + "_enabled=0";
						}
					} else {
						datas += "&" + EventSettingList[i][j] + "=" + newValue;
					}
					if( MODE == "modify" ) {	
						if(i <  data[select_item]['event_type'].length ){
							orgValue = data[select_item]['event_type'][i]["type"];							
						}
						else orgValue = 0; 
					}			
					if( newValue != orgValue ) changed = 1 ;		
					if( newValue != 0)  activeitem = 1 ;					
				}
			}
			if( MODE == "add" ){
				if($("#action_id").val() == 0){
					settingFail(menu, getLanguage("msg_setting_event_rule"));
					disabledButton(false);
					return ;
				}
			}
			if( activeitem == 0 ){
				settingFail(menu, getLanguage("msg_setting_event_needed"));
				disabledButton(false);
				return ;
			}
			// nothing changed check
			if( typeof(datas) != 'undefined' ) {
				if( MODE == "modify"){
					datas = datas + "&id=" + data[select_item].id ;
				}
				datas = "msubmenu=event&action=" + MODE + "&"+ datas;
			}
			if(!changed){
				settingFail(menu, getLanguage("msg_nothing_changed"));
				disabledButton(false);
				$("tr[name=list_items]").removeClass("sel_list_item");
				select_item = -1;
				return ;
			}
			$.ajax({
				type:"get",
				url: "/cgi-bin/admin/trigger.cgi",
				async: false,
				data: datas,
				success: function(msg){
					var pattern = /OK/;
					if(pattern.test(msg) == true) {
						settingSuccess(menu, null);
						refreshMenuContent();
					} else {
						settingFail(menu, getLanguage("msg_fail"));
					}
				},
				error: function() {
					settingFail(menu, getLanguage("msg_fail_retry"));
					refreshMenuContent();
				}
			});
		} catch (e){
			ERROR("Save error! [ " + e + "]");
		}
		disabledButton(false);
	});
	$("#cancel").click(function(e){ ChangeUI(e.target.id); });
	$("[name=always]").click(function(e){ 
		$("[name=schedule]").attr('disabled', e.target.value == 0 ? false : true);
	});
	$("#shour").change(function(e){
		$("#ehour").find("option").remove();
		for(var i= e.target.value; i < 24 ; i++ ){
			$("#ehour").append("<option val=" + i + ">"+i +"</option>")
		}
	});
}

function initValue() {    // main initValue
	try {
		$("tr[name=list_items]").remove();
		var content,schedule, name, cnt;
		content = "";
		var $record = $("#result_table");
		var idx = 0;
		var i,j,k;
		for( i=0 ; i < data.length ; i++) {
			schedule = data[i]['always'] == 1 ? getLanguage("setup_always") : getLanguage("setup_manual") ;

			name = getLanguage("setup_delete");

			for( j=0 ; j < action_data.length ; j++) {
				if( data[i]['action_id'] == action_data[j]['id'] ) {
					name = action_data[j]['name'];
				}
			}

			if( data[i].id != 0 ) {
				content += "<tr class='list_items' name='list_items' id='list_item"+ i 
				content += "' val='" + i + "'>";
				content += "<td class='qt'>" + data[i]['name'] + "</td>";
				//cnt = 0 ; 
				//data[i].event_type.forEach(function(z){
				//	if( z.enabled == 1 ){
				//		cnt++;
				//	}
				//});
				//content += "<td class='qt'>" + cnt + " / " + EventConditionMax + "</td>";
				for( k = 0 ; k < ActionTypeList.length; k++) {
					if( ActionTypeList[k].value == data[i].event_type[0].type){
						break;
					}
				}
				if(k == ActionTypeList.length)
					k = 0;	
				if(ActionTypeList[k].name.toLowerCase() == "none") {
					for(var j = 0; j < data[i].event_type.length; j++) { 
						var eve = data[i].event_type[j];
						res = verifyUserEventIndex(eve.type);
						if(res == eve.type) {
							ActionTypeList[k].name = getLanguage('vca_user_event');
						}
					}
				}
				content += "<td class='qt'>" + ActionTypeList[k].name + "</td>";
				content += "<td class='qt'>" + schedule + "</td>";
				content += "<td class='qt'>" + name + "</td>";	
				content += "</tr>";
			}
		}
		if( content.length == 0) {
			content += "<tr></tr>";
		}
		$record.append(content);
	} catch (e){
		ERROR("ERROR! :InitValue"+ e);
	}

}
function onLoadPage() {
	initUI();
	initValue();
	initEvent();
}
$(document).ready( function() {
	$.ajaxSetup({async: false});
	data = getInformation( "event_rules" );
	action_data = getInformation("action_rules");
	$.ajaxSetup({async: true});
	onLoadPage();
});
