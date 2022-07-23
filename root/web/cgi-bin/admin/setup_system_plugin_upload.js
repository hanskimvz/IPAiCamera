//udp_version=1.0.d
var menu = "Plugin update";
var data;
var select_item = -1;
var MODE = "list";
var timer1;
var pop_msg="";
var configurationUrl = "";
var configurationPath = "";
var configurationPort = "";
var webBrowser = "";
var startstopURL = "";
var uninstallURL = "";
var supportLog = "";
var logbackupURL = "";
var logfilePath = "";
var curStatus = "";
var pluginList = [];
var complete = true;
var newPluginName = "";
var conffilePath = "";
var confbackupURL = "";
var factoryreset = "";
var showPopup = true;

function initUI() {
	$("#configuration").attr("disabled", true);
	$("#startstop").attr("disabled", true);
	$("#uninstall").attr("disabled", true);
	$("#logs").attr("disabled", true);
	$("#impProgressbox").hide();
	$("#bia_caution").text(getLanguage("msg_pluginupload_imp_caution"));
	var addStorageDate = "2020.04.20";
	var changeStorageSize = "2020.06.18";
	if(capInfo.board_chipset.indexOf("amba_s3l") > -1 && addStorageDate.localeCompare(fwDate) != 1){
		var usage = _ajax("/cgi-bin/admin/plugin_upload", "get&plugin");
		if(changeStorageSize.localeCompare(fwDate) != 1) {// change storage size 30MB to 40MB after 2020.06.18 Main firmware
			usage = _ajax("/cgi-bin/admin/plugin_upload", "get&plugin&storage=40.0");
		}
		$(".s3l").css("display", "inline-block");
		$("#contentUsage").html(usage.split(":")[1] + "%");
	} else if(capInfo.board_chipset.indexOf("amba_s5l") > -1 && changeStorageSize.localeCompare(fwDate) != 1) {
		var usage = _ajax("/cgi-bin/admin/plugin_upload", "get&s5lplugin");
		$(".s3l").css("display", "inline-block");
		$("#contentUsage").html(usage.split(":")[1]);
	}
}
function setEventForListItem(){
	$("tr[name=list_items]").on("click", function(e) {
		$(".isSelectPL").css("display", "block");
		$("#configuration").attr("disabled", false);
		$("#startstop").attr("disabled", false);
		$("#uninstall").attr("disabled", false);
		$("tr[name=list_items]").removeClass("sel_list_item");
		$("#" + e.delegateTarget.id).addClass("sel_list_item");
		select_item = Number($(".sel_list_item").attr("val"));
		var text = getXmlData();
		var parser = new DOMParser();
		var xmlDoc = parser.parseFromString(text,"text/xml");
		var pinfoList =  xmlDoc.getElementsByTagName("plugin_info")[select_item];
		var xmlString = (new XMLSerializer()).serializeToString(pinfoList);
		webBrowser = xmlString.indexOf("<browser")>=0 && pinfoList.getElementsByTagName("browser")[0].childNodes[0]? pinfoList.getElementsByTagName("browser")[0].childNodes[0].nodeValue.toLowerCase():'none';
		configurationUrl = xmlString.indexOf("<url")>=0 && pinfoList.getElementsByTagName("url")[0].childNodes[0]? pinfoList.getElementsByTagName("url")[0].childNodes[0].nodeValue:'none';
		configurationPath = xmlString.indexOf("<linkpath")>=0 && pinfoList.getElementsByTagName("linkpath")[0].childNodes[0]? pinfoList.getElementsByTagName("linkpath")[0].childNodes[0].nodeValue:'none';
		configurationPort = xmlString.indexOf("<port")>=0 && pinfoList.getElementsByTagName("port")[0].childNodes[0]? pinfoList.getElementsByTagName("port")[0].childNodes[0].nodeValue:'none';
		startstopURL = xmlString.indexOf("<start")>=0 && pinfoList.getElementsByTagName("start")[0].childNodes[0]? pinfoList.getElementsByTagName("start")[0].childNodes[0].nodeValue:'none';
		uninstallURL = xmlString.indexOf("<uninstall")>=0 && pinfoList.getElementsByTagName("uninstall")[0].childNodes[0]? pinfoList.getElementsByTagName("uninstall")[0].childNodes[0].nodeValue:'none';
		supportLog = xmlString.indexOf("<supportlog")>=0 && pinfoList.getElementsByTagName("supportlog")[0].childNodes[0]? pinfoList.getElementsByTagName("supportlog")[0].childNodes[0].nodeValue.toLowerCase():'none';
		logbackupURL = xmlString.indexOf("<logbackup")>=0 && pinfoList.getElementsByTagName("logbackup")[0].childNodes[0]? pinfoList.getElementsByTagName("logbackup")[0].childNodes[0].nodeValue:'none';
		logfilePath = xmlString.indexOf("<logfilepath")>=0 && pinfoList.getElementsByTagName("logfilepath")[0].childNodes[0]? pinfoList.getElementsByTagName("logfilepath")[0].childNodes[0].nodeValue:'none';
		curStatus = xmlString.indexOf("<status")>=0 && pinfoList.getElementsByTagName("status")[0].childNodes[0]? pinfoList.getElementsByTagName("status")[0].childNodes[0].nodeValue.toLowerCase():'none';
		factoryreset = xmlString.indexOf("<factoryreset")>=0 && pinfoList.getElementsByTagName("factoryreset")[0].childNodes[0]? pinfoList.getElementsByTagName("factoryreset")[0].childNodes[0].nodeValue:'none';
		var pDescription = xmlString.indexOf("<description")>=0 && pinfoList.getElementsByTagName("description")[0].childNodes[0]? pinfoList.getElementsByTagName("description")[0].childNodes[0].nodeValue:'none';
		var baseFirmware = xmlString.indexOf("<basefirmver")>=0 && pinfoList.getElementsByTagName("basefirmver")[0].childNodes[0]? pinfoList.getElementsByTagName("basefirmver")[0].childNodes[0].nodeValue:'none';
		var plugDepen = xmlString.indexOf("<plugin")>=0 && pinfoList.getElementsByTagName("plugin")[0].childNodes[0]? pinfoList.getElementsByTagName("plugin")[0].childNodes[0].nodeValue:'none';
		var supportBackup = xmlString.indexOf("<supportconfbackup")>=0 && pinfoList.getElementsByTagName("supportconfbackup")[0]? pinfoList.getElementsByTagName("supportconfbackup")[0].childNodes[0].nodeValue:'no';
		conffilePath = xmlString.indexOf("<conffilepath")>=0 && pinfoList.getElementsByTagName("conffilepath")[0]? pinfoList.getElementsByTagName("conffilepath")[0].childNodes[0].nodeValue:'none';
		confbackupURL = xmlString.indexOf("<confbackup")>=0 && pinfoList.getElementsByTagName("confbackup")[0]? pinfoList.getElementsByTagName("confbackup")[0].childNodes[0].nodeValue:'none';
		$("#description").html(pDescription);
		$("#baseFirm").html(baseFirmware);
		$("#pluginDepen").html(plugDepen);
		if(webBrowser === 'none') {
			$("#configuration").attr("disabled", true);
		}
		var disableStFirm = false;
		if(baseFirmware.toLowerCase() !== 'none' && baseFirmware.localeCompare(fwInfo) == 1) { 
			disableStFirm = true;
		}
		var disableStPlug = pluginDepenCheck(plugDepen, pluginList);
		$("#startstop").attr("disabled", disableStFirm || disableStPlug);
		if(curStatus == "stopped")
			$("#startstop").html(getLanguage("setup_start"));
		else if(curStatus == "running")
			$("#startstop").html(getLanguage("setup_stop"));
		$("#logs").attr("disabled", (supportLog == "yes")? false : true);
		//$("#import-btn").attr("disabled", (supportBackup != "no")? false : true);
		$("#impFileInput").attr("disabled", (supportBackup != "no")? false : true);
		$("#export").attr("disabled", (supportBackup != "no")? false : true);
		$("#fd").attr("disabled", (factoryreset != "none")? false : true);
	});
}
function arrayRemove(arr, value) {
	return arr.filter(function(ele){
			return ele != value;
	});
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
function initEvent() {
	menu = getLanguage("setup_system_plugin_config");
	setEventForListItem();
	$("#configuration").click(function(e){
		var protocol = window.location.protocol;
		var domain = window.location.host;
		var port = (configurationPort=='none')?window.location.port:(configurationPort.charAt(0)==':'?configurationPort:':'+configurationPort);
		var path = (configurationPath=='none')?'':(configurationPath.charAt(0)=='/'?configurationPath:'/'+configurationPath);
		var URL =  domain + port + path;
		if(configurationUrl !== 'none') URL = configurationUrl;
		if(webBrowser.indexOf("chrome") != -1) {
			var runUrl = "Chrome " + URL;
			try {
				var shell = new ActiveXObject("WScript.Shell");
				shell.run(runUrl);
			} catch (e){
				var pop = window.open( 
					"",
					"_blank", 
					"toolbar=yes, scrollbars=yes,resizable=yes," +
					"top=0,width=600,height=900,left=200,top=5");
					pop.document.write("<p>If you want to open an URL in the right way, please follow the instructions below. </p>\
					<img src='/images/settings_for_ActiveX.png'>\
					<br>1. Go to Tools > Internet Options\
					<br>2. Select security tab\
					<br>3. Click on Trusted Sites (or Local Intranet depending on whether your site is trusted or not)\
					<br>4. Ensure that 'Initialize and script active x controls is not marked safe for scripting' is enabled or prompt. \
					<br>(this comes under Activex controls and plug-ins section towards 1/4th of the scroll bar.)\
					<br>5. Click OK > OK.\
					<br>6. Once this is completed, clear the browser cookies and cache. Close all your browser sessions. Reopen the IE to launch your site.<br><br>\
					Or paste link URL to your Chrome browser.\
					<input type='text' value="+ URL +" id='myInput'>\
					<button onclick='copyText()'>Copy text</button>\
					<script>function copyText() {\
						var copyText = document.getElementById('myInput');\
						copyText.select();\
						document.execCommand('copy');\
						alert('Copied the text: ' + copyText.value);\
					}</script>\
					");
			}
		}
		else if(webBrowser.indexOf("all") != -1) {
			var pop = window.open(protocol + "//" + URL);
		}
		else { //you have to write pull path(https://www.abcd.com)
			var pop = window.open(URL);
		}
	});
	$("#startstop").click(function(e){
		$("#configuration").attr("disabled", true);
		$("#startstop").attr("disabled", true);
		$("#uninstall").attr("disabled", true);
		$("#logs").attr("disabled", true);
		$('.result_table tr').attr("disabled", true);
		if(curStatus == "stopped") {
			$.ajax({
				type:'GET',
				url: "/cgi-bin/admin/plugin_upload",
				processData: false,
				contentType: false,
				data: "action=start&url=" + startstopURL,
				beforeSend: function(){ progressUI(true); },
				success: function(msg){
					progressUI(false);
					if(msg.indexOf("error") != -1){
						settingFail(menu, getLanguage("msg_fail_retry"));
					}
					//settingSuccess(menu, null);
					refreshMenuContent("system/Plug_in");
				},
				error: function(error) {
					progressUI(false);
					settingFail(menu, getLanguage("msg_fail_retry"));
					refreshMenuContent();
				}
			});
		} else if(curStatus == "running") {
			$.ajax({
				type:'GET',
				url: "/cgi-bin/admin/plugin_upload",
				processData: false,
				contentType: false,
				data: "action=stop&url=" + startstopURL,
				beforeSend: function(){ progressUI(true); },
				success: function(msg){
					progressUI(false);
					if(msg.indexOf("error") != -1){
						settingFail(menu, getLanguage("msg_fail_retry"));
					}
					//settingSuccess(menu, null);
					refreshMenuContent("system/Plug_in");
				},
				error: function(error) {
					progressUI(false);
					settingFail(menu, getLanguage("msg_fail_retry"));
					refreshMenuContent();
				}
			});
		} else {
			progressUI(false);
			settingFail(menu, getLanguage("msg_fail_retry"));
		}
	});
	$("#uninstall").click(function(e){
		var uninstallConfirm = confirm(getLanguage("msg_plugin_uninstall")!="msg_plugin_uninstall"?getLanguage("msg_plugin_uninstall"):"When the plugin is uninstalled, the setting contents are also deleted.\nAre you sure to uninstall this plug-in?");
		if(!uninstallConfirm) {return;}
		$.ajax({
			type:'GET',
			url: "/cgi-bin/admin/plugin_upload",
			processData: false,
			contentType: false,
			data: "action=uninstall&url=" + uninstallURL,
			beforeSend: function(){ progressUI(true); },
			success: function(msg){
				progressUI(false);
				refreshMenuContent("system/Plug_in");
				//document.location.reload();
			},
			error: function(error) {
				progressUI(false);
				settingFail(menu, getLanguage("msg_fail_retry"));
				refreshMenuContent();
			}
		});
	});
	$("#logs").click(function(e){
		$.ajax({
			type:'GET',
			url: "/cgi-bin/admin/plugin_upload",
			processData: false,
			contentType: false,
			data: "action=logbackup&url=" + logbackupURL,
			success: function(msg){
				window.location.assign(logfilePath);
				refreshMenuContent();
			},
			error: function(error) {
				settingFail(menu, getLanguage("msg_fail_retry"));
				refreshMenuContent();
			}
		});
	});
	$("#export").click(function(e){
		$.ajax({
			type:'GET',
			url: "/cgi-bin/admin/plugin_upload",
			processData: false,
			contentType: false,
			data: "action=logbackup&url=" + confbackupURL + " export",
			success: function(msg){
				window.location.assign(conffilePath);
				refreshMenuContent();
			},
			error: function(error) {
				settingFail(menu, getLanguage("msg_fail_retry"));
				refreshMenuContent();
			}
		});
	});
	$("#import-btn").click(function(e){
		$("#import-btn").attr("disabled", true);
		var fd = new FormData();
		var input = document.getElementById("impFileInput");
		fd.append( 'file', input.files[0] );
		$.ajax({
			url: '/cgi-bin/admin/plugin_upload?action=import&url=' + conffilePath,
			data: fd,
			//async: false,
			cache	: false,
			processData: false,
			contentType: false,
			type: 'POST',
			beforeSend: function(){ progressUI(true); },
			success: function(msg){
				if(msg.indexOf("Fail") != -1 || msg.indexOf("error") != -1) {
					document.getElementById("impdemo").innerHTML = "Fail";
					setTimeout( function(){ refreshMenuContent() }, 2000 );
				}
				if(msg.indexOf("Success!") != -1) {
					$.ajax({
						type:'GET',
						url: "/cgi-bin/admin/plugin_upload",
						processData: false,
						contentType: false,
						data: "action=logbackup&url=" + confbackupURL + " import",
						success: function(msg){
							progressUI(false);
							alert("Import Success.")
							document.getElementById("impdemo").innerHTML = "Success!";
							refreshMenuContent();
						},
						error: function(error) {
							progressUI(false);
							settingFail(menu, getLanguage("msg_fail_retry"));
							refreshMenuContent();
						}
					});
				}
			},
			error: function(error) {
				progressUI(false);
				alert(error.statusText);
				refreshMenuContent();
			}
		});
	});
	$("#fd").click(function(e){
        if(confirm(getLanguage("msg_vca_fd")!="msg_vca_fd"?getLanguage("msg_vca_fd"):"Do you want to change plugin settings to default?")) {
			$.ajax({
				type:'GET',
				url: "/cgi-bin/admin/plugin_upload",
				processData: false,
				contentType: false,
				data: "action=logbackup&url=" + factoryreset,
				beforeSend: function(){ progressUI(true); },
				success: function(msg){
					progressUI(false);
					if(msg.toLowerCase().indexOf("complete") != -1){
						refreshMenuContent("system/Plug_in");
					} else {
						settingFail(menu, getLanguage("msg_fail_retry"));
						refreshMenuContent();
					}
				},
				error: function(error) {
					settingFail(menu, getLanguage("msg_fail_retry"));
					refreshMenuContent();
				}
			});
		}
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
				//alert(allText);
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
	xmlDoc = readTextFile(file);;//parser.parseFromString(text,"text/xml");
	return xmlDoc;
}

function initValue() {
	var text, parser, xmlDoc;
	var content;
	$("tr[name=list_items]").remove();
	$record = $("#result_table");
	$record.empty();
	content = "";
	text = getXmlData();
	parser = new DOMParser();
	xmlDoc = parser.parseFromString(text,"text/xml");
	var length = xmlDoc.querySelectorAll('plugin_info').length;
	for(var i = 0 ; i < length ; i++) {
		if( xmlDoc ) {
			var tmpName = xmlDoc.getElementsByTagName("name")[i].childNodes[0].nodeValue;
			var changeName = ((capInfo["oem"] == 2 || capInfo["oem"] == "DW") && tmpName == "VCAedge") ? "IVA" : xmlDoc.getElementsByTagName("name")[i].childNodes[0].nodeValue;
			content += "<tr class='list_items' name='list_items' id='list_item"+ i;
			content += "' val='" + i + "'>" 
			content += "<td class='athird'>" + changeName + "</td>";
			content += "<td class='athird'>" + xmlDoc.getElementsByTagName("version")[i].childNodes[0].nodeValue + "</td>";
			content += "<td class='athird'>" + xmlDoc.getElementsByTagName("status")[i].childNodes[0].nodeValue + "</td>";	
			content += "</tr>";
			pluginList.push(xmlDoc.getElementsByTagName("name")[i].childNodes[0].nodeValue);
		}
	}
	if( !xmlDoc ) { 
		content += "<tr></tr>";
	}
	$record.append(content); 
}
function getnewXmlValuebyPlugin(plugin, tagname) {
	var text, parser, xmlDoc, tmpValue;
	text = getXmlData();
	parser = new DOMParser();
	xmlDoc = parser.parseFromString(text,"text/xml");
	if(xmlDoc) {
		var length = xmlDoc.querySelectorAll('plugin_info').length;
		for(var i=0; i < length ; i++) {
			if(plugin && (xmlDoc.getElementsByTagName("name")[i].childNodes[0].nodeValue == plugin))
				tmpValue = xmlDoc.getElementsByTagName(tagname)[i].childNodes[0]?xmlDoc.getElementsByTagName(tagname)[i].childNodes[0].nodeValue:'none';
		}
	}
	return tmpValue;
}
function getnewXmlValue(tagname) {
	var text, parser, xmlDoc, tmpValue;
	var cmppluginList=[];
	text = getXmlData();
	parser = new DOMParser();
	xmlDoc = parser.parseFromString(text,"text/xml");
	if(xmlDoc) {
		var length = xmlDoc.querySelectorAll('plugin_info').length;
		for(var i=0; i < length ; i++) {
			cmppluginList.push(xmlDoc.getElementsByTagName("name")[i].childNodes[0].nodeValue);
		}
		var newPlugin = compare(pluginList,cmppluginList);
		for(var i=0; i < length ; i++) {
			if(newPlugin && (xmlDoc.getElementsByTagName("name")[i].childNodes[0].nodeValue == newPlugin))
				tmpValue = xmlDoc.getElementsByTagName(tagname)[i].childNodes[0]?xmlDoc.getElementsByTagName(tagname)[i].childNodes[0].nodeValue:'none';
		}
	}
	return tmpValue;
}
function compare(arr1,arr2){
  var objMap=arr2;
	for(var i=0; i<arr1.length; i++) {
		for(var j=0; j<arr2.length; j++) {
			if(arr1[i] == arr2[j])
				objMap.splice( objMap.indexOf(arr1[i]), 1 );
		}
	}
	return objMap;
}
function onLoadPage() {
	$('#tabs').css('overflow','auto');
	initUI();
	initUpload();
	initValue();
	initEvent();
}
$(document).ready( function() {
	data = getInformation( $(".select_minor").attr("id") );
	onLoadPage();
});
function Elapsed_time() {
	pop_msg = getLanguage("msg_update_progress_message");
	$("#FileInput").prop( "disabled" , true );
	timer1 = setTimeout( function(){onUploading(); } , 1000); 
		//timer1 = setInterval(setTimeout( function(){onUploading(); } , 1000), 1000);
}

function fileUpload() {
	var fd = new FormData();
	var input = document.getElementById("FileInput");
	fd.append( 'file', input.files[0] );
	return $.ajax({
		url: '/cgi-bin/admin/plugin_upload?upload',
		data: fd,
		async: false,
		cache	: false,
		processData: false,
		contentType: false,
		type: 'POST',
		success: function(msg){
			if(msg.indexOf("Fail") != -1 || msg.indexOf("error") != -1) {
				document.getElementById("demo").innerHTML = "Fail";
				setTimeout( function(){ refreshMenuContent() }, 2000 );
			}
			if(msg.indexOf("Success!") != -1) {
			}
		},
		error: function(error) {
			alert(error.statusText);
			refreshMenuContent();
		}
	});
}

function runCommand(cmd, text) {
	var tmpComplete = false;
	$("#progressbox").show();
	return $.ajax({
		type:'GET',
		url: "/cgi-bin/admin/plugin_upload",
		async: false,
		data: cmd,
		timeout: 30000,
		success: function(msg){
			if(msg.toLowerCase().indexOf("fail") != -1 || msg.toLowerCase().indexOf("error") != -1 || msg.indexOf(text) == -1) {
				tmpComplete = false;
				if(msg.indexOf("Failed to install plugin.") != -1) { alert(msg.split("Failed to install plugin.")[1]); }
				complete &= tmpComplete;
				return -1;
			}
			if(msg.indexOf("Reboot") != -1){ //only script return "reboot"
				tmpComplete = false;
				alert("Please wait. Reboot is in progress to complete the plugin update.");
				complete &= tmpComplete;
				return -1;
			}
			if(msg.indexOf(text) != -1){
				if(cmd == "extract"){
					if(msg.toLowerCase().indexOf('no popup') != -1) showPopup = false;
					else {
						var strGetPlugname = msg.split("\n");
						for(var i = 0; i < strGetPlugname.length; i++)
							if(strGetPlugname[i].indexOf("Plugin-") != -1)
								break;
						var strArr = strGetPlugname[i].split(" ");
						var resultStr = "";
						for(var j = 1; j < strArr.length - 1; j++)
						{
							resultStr += strArr[j] + " ";
						}
						newPluginName = resultStr.trim();
					}
				}
				tmpComplete = true;
			}
			else
				tmpComplete = false;
			complete &= tmpComplete;
		},
		error: function(error) {
			console.log(error.statusText + "-" + cmd);
			refreshMenuContent();
		}
	});
}
function onUploading() {
	var success_tmp = 0;
	var percentComplete = 0;
	//var stageCount = 4;
	$("#progressbox").show();
	var pGress = setInterval(function() {
		if(success_tmp == 0)
		{
			fileUpload();
			success_tmp += 1;
			percentComplete = 25;
		} 
		else if(success_tmp == 1) {
			setTimeout( function(){runCommand("decode", "Success to Decode plugin firmware");}, 1000 );
			success_tmp += 1;
			percentComplete = 50;
			$('#statustxt').css('color','#fff');
		}
		else if(success_tmp == 2) {
			setTimeout( function(){runCommand("extract", "Success to extract");}, 1000 );
			success_tmp += 1;
			percentComplete = 75;
			$('#statustxt').css('color','#fff');
		}
		else if(success_tmp == 3) {
			setTimeout( function(){runCommand("complete", "Complete!");
			success_tmp += 1;
			percentComplete = 100;
			}, 1000 );
			$('#statustxt').css('color','#fff');
		}
		else if(success_tmp == 4 && complete) {
			document.getElementById("demo").innerHTML = "Success";
			clearInterval(pGress);
			clearInterval(timer1);
			var startUrl = getnewXmlValuebyPlugin(newPluginName, "start");
			var depFirmware = getnewXmlValuebyPlugin(newPluginName, "basefirmver");
			var depPlugin = getnewXmlValuebyPlugin(newPluginName, "plugin");
			depFirmware = depFirmware?depFirmware:'none';
			depPlugin = depPlugin?depPlugin:'none';
			console.log(depFirmware, depPlugin);
			if (showPopup && !(depFirmware.toLowerCase() !== 'none' && depFirmware.localeCompare(fwInfo) == 1) && !pluginDepenCheck(depPlugin, pluginList) && confirm(getLanguage("msg_vca_start"))) {
				$.ajax({
					type:'GET',
					url: "/cgi-bin/admin/plugin_upload",
					processData: false,
					contentType: false,
					data: "action=start&url=" + startUrl,
					beforeSend: function(){ progressUI(true); },
					success: function(msg){
						progressUI(false);
						if(msg.indexOf("error") != -1){
							settingFail(menu, getLanguage("msg_fail_retry"));
						}
						//settingSuccess(menu, null);
						refreshMenuContent("system/Plug_in");
					},
					error: function(error) {
						progressUI(false);
						settingFail(menu, getLanguage("msg_fail_retry"));
						refreshMenuContent("system/Plug_in");
					}
				});
			} else {
				refreshMenuContent("system/Plug_in");
			}
		}
		else {
			document.getElementById("demo").innerHTML = "Fail";
			clearInterval(pGress);
			clearInterval(timer1);
			settingFail(menu, getLanguage("msg_fail_retry"));
			setTimeout( function(){ refreshMenuContent() }, 2000 );
		}
		$("#progressbar").width(percentComplete + '%');
		$("#statustxt").html(percentComplete + '%');
	}, 1000);
}

function _ajax(url, data){
	var timestamp = new Date().getTime();
	var ret = '';
	$.ajax({
		type:'GET',
		url: url,
		processData: false,
		contentType: false,
		async: false,
		data: data +"&_=" + timestamp,
		beforeSend: function(){ progressUI(true); },
		success: function(msg){
			progressUI(false);
			ret = msg;
		},
		error: function(error) {
			progressUI(false);
		}
	});
	return ret;
}

function beforeSubmit() {$("#submit-btn").attr("disabled", true);$('#progressbar').width("0%") ;$('#statustxt').html("0%");}
function success() {Elapsed_time();}
function initUpload()
{
	//progress bar function
	function OnProgress(event, position, total, uploadPercentComplete)
	{
		pop_msg = getLanguage("msg_update_progress_message");
		$('#progressbox').show();
		$('#progressbar').width(0 + '%') ;
		$('#statustxt').html(0 + '%');
	  $('#statustxt').css('color','#000'); //change status text to white after 50%
	}

	$('#MyPluginUploadForm').submit(function(e) {
		e.preventDefault();
		beforeSubmit();
		success();
		OnProgress();
		//$("#MyPluginUploadForm").ajaxSubmit(options);
		return false; // always return false to prevent standard browser submit and page navigation
	});
}
//end_of_file
