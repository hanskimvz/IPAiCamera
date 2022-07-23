var menu = "BIA setting";
var settingList = ["bia" , "bia_enabled", "display_zones", "display_objects", "obj_classifications", "obj_heights", "obj_speeds", 
	"obj_areas", "obj_color", "display_eve_mesg", "display_sys_mesg", "display_line_counters", "display_counters", "obj_id", "obj_dwell_time", "confidence"];
var streamNum = 0;
var streamJson = "";
var curStatus = "";
var enable = 1;
var zone = 0;
var object = 0;
var classification = 0;
var height = 0;
var speed = 0;
var area = 0;
var colorSig = 0;
var ticker = 0;
var sysmsg = 0;
var licount = 0;
var count = 0;
var obj_id = 0;
var dwell_time = 0;
var confidence = 0;
var isCalib = false;
var curEngine = "";

function disabled(val ,cmd)
{
	$("#"+val).find("select, input").each(function(i, e){
		var abc = $(this).prop("id") ;
		$("#"+ abc).prop("disabled", cmd);		
	});
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
	var xmlDoc = "";
	var timestamp = new Date().getTime();
	var file = "/plugin_info_list.xml?timestamp="+timestamp;
	xmlDoc = readTextFile(file);;
	return xmlDoc;
}
function getVcaStatus() {
	var text = getXmlData();
	var parser = new DOMParser();
	var xmlDoc = parser.parseFromString(text,"text/xml");
	var length = xmlDoc.querySelectorAll('plugin_info').length;
	if( xmlDoc ) {
		for(var i = 0 ; i < length ; i++) {
			if(xmlDoc.getElementsByTagName("name")[i].childNodes[0].nodeValue.toLowerCase() == "vcaedge") {
				curStatus = xmlDoc.getElementsByTagName("status")[i].childNodes[0]?xmlDoc.getElementsByTagName("status")[i].childNodes[0].nodeValue.toLowerCase():'none';
				if(curStatus != "running") {
					$("#startVca").css("display", "block");
					$("#startVca").text(getLanguage("msg_start_vca"));
				}
			}
		}
	}
}
function initvalue()
{ // BIA off:100, Main stream:0, Sub Stream:1, 3rd Stream:2
	getVcaStatus();
	getCalibJson();
	$("#bia_caution").text(getLanguage("msg_bia_caution"));
	if(object == 0) { //Display object off
		disabled("objectContent",true);
	}
	else if(object == 1) {
		disabled("objectContent",false);
	}
	if(enable == 0) { //BIA off
		$('input[name=bia]').attr("disabled",true);
		disabled("biaSetup",true);
		disabled("objectContent",true);
	}
	else if(enable == 1) {
		$('input[name=bia]').attr("disabled",false);
		disabled("biaSetup",false);
	}
	if(parseInt(VideoInfo[0]["resolution"].split("x")[1]) > 1080) {
		$("[name=bia][value=0]").attr("disabled", true);
	}
	$("[name=bia_enabled][value=" + enable + "]").trigger("click");
	$("[name=bia][value=" + streamNum + "]").trigger("click");
	$("[name=display_zones][value=" + zone + "]").trigger("click");
	$("[name=display_objects][value=" + object + "]").trigger("click");
	$("[name=obj_classifications][value=" + classification + "]").trigger("click");
	$("[name=obj_heights][value=" + height + "]").trigger("click");
	$("[name=obj_speeds][value=" + speed + "]").trigger("click");
	$("[name=obj_areas][value=" + area + "]").trigger("click");
  $("[name=obj_color][value=" + colorSig + "]").trigger("click");
	$("[name=display_eve_mesg][value=" + ticker + "]").trigger("click");
	$("[name=display_sys_mesg][value=" + sysmsg + "]").trigger("click");
	$("[name=display_line_counters][value=" + licount + "]").trigger("click");
	$("[name=display_counters][value=" + count + "]").trigger("click");
  $("[name=obj_id][value=" + obj_id + "]").trigger("click");
  $("[name=obj_dwell_time][value=" + dwell_time + "]").trigger("click");
  $("[name=confidence][value=" + confidence + "]").trigger("click");
	checkDependency("bia");
}

function checkDependency(index)
{
	if($("[name=bia_enabled]:checked").val() == 0){ //off
		$('input[name=bia]').attr("disabled",true);
		disabled("biaSetup",true);
		disabled("objectContent",true);
	}
	else {
		$('input[name=bia]').attr("disabled",false);
		disabled("biaSetup",false);
		if($("[name=display_objects]:checked").val() == 0){ //off
			disabled("objectContent",true);
		}
		else {
			disabled("objectContent",false);
		}
	}
  if($("[name=bia_enabled]:checked").val() == 1 && !isCalib && $("[name=display_objects]:checked").val() == 1) {
		disabled("objectContent",true);
		$('#start_cali_mes').css("display", "inline");
    if($("[name=bia_enabled]:checked").val() == 1 && $("[name=display_objects]:checked").val() == 1)
      disabled("objectColorContent", false);
      disabled("obj_dwell_time", false);
	}
	else
		$('#start_cali_mes').css("display", "none");

  if(curEngine !== 'object_tracker') {
    $('#obj_OT_only_content').css("display", "none");
    $('#obj_confidence').css("display", "block");
  };

  if((curEngine === 'dl_object_tracker' || curEngine === 'dl_people_tracker') && ($("[name=bia_enabled]:checked").val() == 1 && $("[name=display_objects]:checked").val() == 1)) {
    disabled("objectContent",false);
    $('#start_cali_mes').css("display", "none");
  }

	if(parseInt(VideoInfo[0]["resolution"].split("x")[1]) > 1080) {
		$("[name=bia][value=0]").attr("disabled", true);
	}
}
function initEvent() {
	$("[name=bia_enabled]").click(function ( obj ) {	
		checkDependency("bia");
		$("[name=bia][value=" + streamNum + "]").trigger("click");
		$("[name=display_zones][value=" + zone + "]").trigger("click");
		$("[name=display_objects][value=" + object + "]").trigger("click");
		$("[name=obj_classifications][value=" + classification + "]").trigger("click");
		$("[name=obj_heights][value=" + height + "]").trigger("click");
		$("[name=obj_speeds][value=" + speed + "]").trigger("click");
		$("[name=obj_areas][value=" + area + "]").trigger("click");
    $("[name=obj_color][value=" + colorSig + "]").trigger("click");
		$("[name=display_eve_mesg][value=" + ticker + "]").trigger("click");
		$("[name=display_sys_mesg][value=" + sysmsg + "]").trigger("click");
		$("[name=display_line_counters][value=" + licount + "]").trigger("click");
		$("[name=display_counters][value=" + count + "]").trigger("click");
    $("[name=obj_id][value=" + obj_id + "]").trigger("click");
    $("[name=obj_dwell_time][value=" + dwell_time + "]").trigger("click");
    $("[name=confidence][value=" + confidence + "]").trigger("click");
	});
	$("[name=display_objects]").click(function ( obj ) {	
		checkDependency("bia");
	});
	$("[name=bia]").click(function ( obj ) {				
		checkDependency("bia");	
	});
	$("#btOK").click(function(event) {
		var data = null;
		var newValue;
		var changed = false;
		if($("[name=bia_enabled]:checked").val() == 1 && !$("[name=bia]:checked").val()) {
			settingFail(menu, getLanguage("msg_select_stream"));
			return;
		}
		for( var i = 0 ; i < settingList.length ; i++)	{
			var obj = $("#" + settingList[i]);

			if(($("[name = "+settingList[i]+"]").prop("type")) == "radio") {
				newValue = $("[name="+settingList[i]+"]:checked").val();
			} else {
				newValue = obj.val();				
			}
			var txt = settingList[i];
			if(txt == "bia" && newValue != streamJson.streamid) {streamJson.streamid = newValue; changed = true;}
			else if(txt == "bia_enabled" && newValue != streamJson.BIAenable) {streamJson.BIAenable = newValue; changed = true;}
			else if(txt == "display_zones" && newValue != zone) {streamJson.zones = newValue; changed = true;}
			else if(txt == "display_objects" && newValue != object) {streamJson.objects = newValue; changed = true;}
			else if(txt == "obj_classifications" && newValue != classification) {streamJson.class = newValue; changed = true;}
			else if(txt == "obj_heights" && newValue != height) {streamJson.height = newValue; changed = true;}
			else if(txt == "obj_speeds" && newValue != speed) {streamJson.speed = newValue; changed = true;}
			else if(txt == "obj_areas" && newValue != area) {streamJson.area = newValue; changed = true;}
      else if(txt == "obj_color" && newValue != colorSig) {streamJson.color_signature = newValue; changed = true;}
			else if(txt == "display_eve_mesg" && newValue != ticker) {streamJson.evt_msg = newValue; changed = true;}
			else if(txt == "display_sys_mesg" && newValue != sysmsg) {streamJson.sys_msg = newValue; changed = true;}
			else if(txt == "display_line_counters" && newValue != licount) {streamJson.line_counters = newValue; changed = true;}
			else if(txt == "display_counters" && newValue != count) {streamJson.counters = newValue; changed = true;}
      else if(txt == "obj_id" && newValue != obj_id) {streamJson.obj_id = newValue; changed = true;}
      else if(txt == "obj_dwell_time" && newValue != dwell_time) {streamJson.dwell_time = newValue; changed = true;}
      else if(txt == "confidence" && newValue != confidence) {streamJson.confidence = newValue; changed = true;}
		}

		if(changed) {
      console.log(streamJson);
			setStreamJson(streamJson);
		} else {
			pop_msg = getLanguage("msg_nothing_changed");
			settingFail(menu, pop_msg);
			return ;
		}
	});
}
function getCalibJson() {
	$.ajaxSetup({'async': false});
	$.ajax({
		url: "/cgi-bin/admin/vca-api/api/channels/0/calibration/enabled?_=" + new Date().getTime(),
		method: "GET",
		headers: {'Content-Type': 'application/json'},
		success: function(json) {
			isCalib = json;
		}
	});
	$.ajaxSetup({'async': true});
}
function getTrackingEngine() {
  $.ajaxSetup({'async': false});
	$.ajax({
		url: "/cgi-bin/admin/vca/config/tracking_engine.conf?_=" + new Date().getTime(),
		method: "GET",
		headers: {'Content-Type': 'text/javascript'},
		success: function(json) {
			httpJson = JSON.parse(json);
			curEngine = httpJson.tracking_engine;
		}
	});
	$.ajaxSetup({'async': true});
}
function getStreamJson() {
	$.ajaxSetup({'async': false});
	$.ajax({
		url: "/cgi-bin/admin/vca/config/bia.conf?_=" + new Date().getTime(),
		method: "GET",
		headers: {'Content-Type': 'text/javascript'},
		success: function(json) {
			streamJson = JSON.parse(json);
			streamNum = streamJson.streamid;
			enable = streamJson.BIAenable;
			zone = streamJson.zones;
			object = streamJson.objects;
			classification = streamJson.class;
			height = streamJson.height;
			speed = streamJson.speed;
			area = streamJson.area;
      colorSig = streamJson.color_signature;
			ticker = streamJson.evt_msg;
			sysmsg = streamJson.sys_msg;
			licount = streamJson.line_counters;
			count = streamJson.counters;
      obj_id = streamJson.obj_id;
      dwell_time = streamJson.dwell_time;
      confidence = streamJson.confidence;
		}
	});
	$.ajaxSetup({'async': true});
}
function setStreamJson(data) {
	$.ajaxSetup({'async': false});
	var newData = JSON.stringify(data);
	$.post('/cgi-bin/admin/vca/bia/setup_vca_bia.cgi', {
		newData: newData
	})
	.done(function(msg){ settingSuccess(menu, null);refreshMenuContent(); })
	.fail(function(xhr, status, error) {
		settingFail(menu, getLanguage("msg_fail_retry"));
	});
	//refreshMenuContent();
	$.ajaxSetup({'async': true});
}
function onLoadPage() {
	getStreamJson();
  getTrackingEngine();
	initEvent();
	initvalue();
}

$(document).ready( function() {
	onLoadPage();
});
