var menu = "VCA setting";
var orgVal = 0;
var curStatus = "";
var startstopURL = "";
var curLicenseId = -1;
var isAILicense = false;
var licenseFeatures = {};
var selectedEngine = "";
var isEngineChanged = false;
var curEngine = "";
var httpJson = "";
var observables = {};
var isCalibrated = false;
var isPossibleChangeEngine = false;
var objectClasses = ['Person', 'Vehicle'];
var changeEngineConfirmMsg = getLanguage('setup_vca_enable_confirm_msg');

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
	var pluginList = [];
	var text = getXmlData();
	var parser = new DOMParser();
	var xmlDoc = parser.parseFromString(text,"text/xml");
	var length = xmlDoc.querySelectorAll('plugin_info').length;
	if( xmlDoc ) {
		for(var i = 0 ; i < length ; i++) {
			var pluginName = xmlDoc.getElementsByTagName("name")[i].childNodes[0].nodeValue;
			pluginList.push(pluginName);
			if(pluginName.toLowerCase() == "vcaedge-ai") {
				curStatus = xmlDoc.getElementsByTagName("status")[i].childNodes[0]?xmlDoc.getElementsByTagName("status")[i].childNodes[0].nodeValue.toLowerCase():'none';
				startstopURL = xmlDoc.getElementsByTagName("start")[i].childNodes[0]?xmlDoc.getElementsByTagName("start")[i].childNodes[0].nodeValue:'none';
				var baseFirmware = xmlDoc.getElementsByTagName("basefirmver")[i].childNodes[0]?xmlDoc.getElementsByTagName("basefirmver")[i].childNodes[0].nodeValue:'none';
				var plugDepen = xmlDoc.getElementsByTagName("plugin")[i].childNodes[0]?xmlDoc.getElementsByTagName("plugin")[i].childNodes[0].nodeValue:'none';
				var disableStFirm = false;
				if(baseFirmware.toLowerCase() !== 'none' && baseFirmware.localeCompare(fwInfo) == 1) { 
					disableStFirm = true;
				}
				var disableStPlug = pluginDepenCheck(plugDepen, pluginList);
				if(disableStFirm || disableStPlug) {
					$("#checkDepen").css("display", "block");
					$("#checkDepen").text(getLanguage("msg_vca_dep"));
					$("#vca_enabled_on").attr("disabled", true);
					$("#vca_enabled_off").attr("disabled", true);
					$("#btOK").attr("disabled", true);
				}else if(curStatus != "running") {
					$("#startVca").css("display", "block");
					$("#startVca").text(getLanguage("msg_start_vca"));
					$("[name=vca_enabled][value=0]").trigger("click");
				}
				else
					$("[name=vca_enabled][value=1]").trigger("click");
			}
		}
	}
}
function pluginDepenCheck(pluginDependency, pluginlist) {
	var disableStPlug = false;
	var dependencyArray = pluginDependency.trim().split(",");
	for(var i = 0 ; i < pluginlist.length ; i++) {
		if(pluginlist[i] && pluginDependency.toLowerCase() !== 'none') {
			if(dependencyArray.filter(function (n) {	return n == pluginlist[i];	})[0]){
				dependencyArray = arrayRemove(dependencyArray, pluginlist[i]);
			}
		}
		if(dependencyArray.length != 0 && pluginDependency.toLowerCase() !== 'none')
			disableStPlug = true;
		else
			disableStPlug = false;
	}
	return disableStPlug;
}
function arrayRemove(arr, value) {
	return arr.filter(function(ele){
			return ele != value;
	});
}

//api
function getCurLicense(curStatus)
{
	if(curStatus == "running") {
		$.ajaxSetup({'async': false});
		$.ajax({
			url: "/cgi-bin/admin/vca-api/api/channels/0/license?_=" + new Date().getTime(),
      method: "GET",
      headers: {'Content-Type': 'application/json'},
			success: function(res){
        curLicenseId = res;
			},
			error: function(error) {
				console.log(error);
				refreshMenuContent();
			}
		});
		$.ajaxSetup({'async': true});
	}
}
function getVCALicense(curStatus)
{
	if(curStatus == "running") {
		$.ajaxSetup({'async': false});
		$.ajax({
			url: "/cgi-bin/admin/vca-api/api/licenses/vca/"+curLicenseId+"?_=" + new Date().getTime(),
      method: "GET",
			headers: {'Content-Type': 'application/json'},
			success: function(res){
        isAILicense = chkIsAILicense(res);
        licenseFeatures = res.features;
			},
			error: function(error) {
				console.log(error);
				refreshMenuContent();
			}
		});
		$.ajaxSetup({'async': true});
	}
}

function chkIsAILicense(license) {
  return (license.features.indexOf('pose') !== -1 || license.features.indexOf('DL_tracker') !== -1)
}
function disabled(val ,cmd)
{
	$("#"+val).find("select, input, textarea").each(function(i, e){
		var control = $(this).prop("id");
		$("#"+ control).prop("disabled", cmd);		
	});
}
function checkDependency() {
  if($("[name=vca_enabled]:checked").val() == 0){ //off
    disabled("select_engine", true);
  } else {
    disabled("select_engine", false);
  }
  
  getCurLicense(curStatus);
  if(curLicenseId !== null) {
    getVCALicense(curStatus);
  }

  if(curEngine === 'dl_object_tracker') {
    $("[name=tracker_engine][value=1]").trigger("click");
    selectedEngine = "dl_object_tracker";
  }
  else if(curEngine === 'dl_people_tracker') {
    $("[name=tracker_engine][value=2]").trigger("click");
    selectedEngine = "dl_people_tracker";
  }
  else {
    $("[name=tracker_engine][value=0]").trigger("click");
    selectedEngine = "object_tracker";
  }
  
  if(isAILicense) {
    if(licenseFeatures.indexOf('object_tracking') === -1) {
      $("#tracker_engine_OT").attr("disabled", true);
      $("#span_tracker_engine_OT").css("opacity", 0.4);
    }
    if(licenseFeatures.indexOf('DL_tracker') === -1) {
      $("#tracker_engine_DL_OT").attr("disabled", true);
      $("#span_tracker_engine_DL_OT").css("opacity", 0.4);
    }
    if(licenseFeatures.indexOf('pose') === -1) {
      $("#tracker_engine_DL_PT").attr("disabled", true);
      $("#span_tracker_engine_DL_PT").css("opacity", 0.4);
    }
  } else {
    $("#tracker_engine_DL_OT").attr("disabled", true);
    $("#span_tracker_engine_DL_OT").css("opacity", 0.4);
    $("#tracker_engine_DL_PT").attr("disabled", true);
    $("#span_tracker_engine_DL_PT").css("opacity", 0.4);
  }
}
function initvalue()
{
	getVcaStatus();
  getStreamJson();
  checkDependency();
  isEngineChanged = false;
}
function initEvent() {
	$("#btOK").click(function(event) {
		var data = null;
		var newValue;
		var orgVal = (curStatus=="running")?1:0;
		if(!$("[name=vca_enabled]:checked").val()) {
			settingFail(menu, getLanguage("msg_select_stream"));
			return;
		}

		if(($("[name=vca_enabled]").prop("type")) == "radio") {
			newValue = $("[name=vca_enabled]:checked").val();
		} else {
			newValue = obj.val();				
		}
		
		if( ((orgVal != newValue) && newValue )) {
			data = startstopURL;
		}
      if(data != null && curStatus == "stopped") {
        $.ajax({
          type:'GET',
          url: "/cgi-bin/admin/plugin_upload",
          processData: false,
          contentType: false,
          data: "action=start&url=" + data,
          beforeSend: function(){
            progressUI(true);
            httpJson.tracking_engine = selectedEngine;
            setStreamJson(httpJson, true);
          },
          success: function(msg){
            if(msg.indexOf("error") != -1){
              settingFail(menu, getLanguage("msg_fail_retry"));
            }
            progressUI(false);
            if(capInfo["oem"] == "2" || capInfo["oem"] == "DW") setTimeout(function() { refreshMenuContent("iva/enable_vca"); }, 500);
            else setTimeout(function() { refreshMenuContent("vca/enable_vca"); }, 500);
          },
          error: function(error) {
            progressUI(false);
            settingFail(menu, getLanguage("msg_fail_retry"));
            refreshMenuContent();
          }
        });
      } else if(data != null && curStatus == "running") {
        $.ajax({
          type:'GET',
          url: "/cgi-bin/admin/plugin_upload",
          processData: false,
          contentType: false,
          data: "action=stop&url=" + data,
          beforeSend: function(){
            progressUI(true);
          },
          success: function(msg){
            if(msg.indexOf("error") != -1){
              settingFail(menu, getLanguage("msg_fail_retry"));
            }
            progressUI(false);
            if(capInfo["oem"] == "2" || capInfo["oem"] == "DW") setTimeout(function() { refreshMenuContent("iva/enable_vca"); }, 500);
            else setTimeout(function() { refreshMenuContent("vca/enable_vca"); }, 500);
          },
          error: function(error) {
            progressUI(false);
            settingFail(menu, getLanguage("msg_fail_retry"));
            refreshMenuContent();
          }
        });
      } else if(data == null && isEngineChanged == true) {
        if(confirm(changeEngineConfirmMsg)) {
          $.ajax({
            type:'GET',
            url: "/cgi-bin/admin/plugin_upload",
            processData: false,
            contentType: false,
            data: "action=start&url=" + startstopURL,
            beforeSend: function(){
              progressUI(true);
              httpJson.tracking_engine = selectedEngine;
              setStreamJson(httpJson, true);
            },
            success: function(msg){
              if(msg.indexOf("error") != -1){
                settingFail(menu, getLanguage("msg_fail_retry"));
              }
              progressUI(false);
              if(capInfo["oem"] == "2" || capInfo["oem"] == "DW") setTimeout(function() { refreshMenuContent("iva/enable_vca"); }, 500);
              else setTimeout(function() { refreshMenuContent("vca/enable_vca"); }, 500);
            },
            error: function(error) {
              progressUI(false);
              settingFail(menu, getLanguage("msg_fail_retry"));
              refreshMenuContent();
            }
          });
        }
      } else {
        pop_msg = getLanguage("msg_nothing_changed");
        settingFail(menu, pop_msg);
        return ;
      }
	});
  $("[name=vca_enabled]").click(function(obj) {
    checkDependency();
  });
  $("[name=tracker_engine]").click(function(obj) {
    isEngineChanged = true;
    if($("[name=tracker_engine]:checked").val() == 0) selectedEngine = "object_tracker";
    else if($("[name=tracker_engine]:checked").val() == 1) selectedEngine = "dl_object_tracker";
    else if($("[name=tracker_engine]:checked").val() == 2) selectedEngine = "dl_people_tracker";   
  });
}

function getStreamJson() {
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

function setStreamJson(data, bool) {
	$.ajaxSetup({'async': false});
	var newData = JSON.stringify(data);
	$.post('/cgi-bin/admin/vca/enable/setup_vca_enable.cgi', {
		newData: newData
	})
	.done(function(msg){
		if(!bool)
			settingSuccess(menu, null);
		})
	.fail(function(xhr, status, error) {
		settingFail(menu, getLanguage("msg_fail_retry"));
	});
	$.ajaxSetup({'async': true});
}

function onLoadPage() {
	initEvent();
	initvalue();
}

$(document).ready( function() {
	onLoadPage();
});
