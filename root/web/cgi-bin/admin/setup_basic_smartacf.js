var menu = getLanguage("acf_plus_configuration");
var settingList = [ "framerate","target_bitrate","target_gop","bitrateControl","hold_on_time","trigger_event"];
//if( (systemOption & SYSTEM_OPTION_UI_FIXED_DATE_20160504) == 0 ){
var activeChannel;
var lastVideoInfo = [];
var debug_level = 0;
function debug(cmd){if(debug_level > 0 ){ console.log("[VIDEO] " + cmd); } }
for(var i=0; i< VideoInfo.length ; i++) {
	lastVideoInfo[i] = new Object();
	$.extend(true, lastVideoInfo[i], VideoInfo[i]);
}
var src = 0;

function initFramerate(min, max) {
	$("#framerate").find("option").remove();
	if( min == undefined){
		min = 1;
	}
	if( max == undefined) {
		max = 30;
	}
	for( var i = max ; i >= min ; i--) {
		$("#framerate").append("<option value=" + i + ">" + i + "</option>" );
	}
}
function initUI() {
	if (capInfo["oem"] == 19 || capInfo["oem"] == 20 || capInfo["oem"] == 21){
		menu = getLanguage("acf_plus_configuration_stanley");
		$("#acf_control").attr("tkey","acf_plus_configuration_stanley");
	} else if ( capInfo["oem"] != 12){
		menu = getLanguage("acf_plus_configuration_udp");
		$("#acf_control").attr("tkey","acf_plus_configuration_udp");
	}

    activeChannel = 0;
	switch (VideoInfo[activeChannel]['codec']) {
		case 1 :
			obj = VideoOption[activeChannel].h264; break;
		case 2 : 
			obj = VideoOption[activeChannel].jpeg; break;
		case 3 :
			obj = VideoOption[activeChannel].hevc; break;
		default : 
			obj = undefined;
	}
	commonCreateSourceSelectBox("#vin_source");

//    console.log(typeof(obj));
//    console.log(obj);
	if( typeof(obj) != 'undefined')
		initFramerate(obj.frMin, obj.frMax);

    updateChannelInfomation();

//    $("#channel").prop("disabled", true);

}

function updateChannelInfomation() {
	$("#channel").find("option").remove();
	var cmd = '',
	index = 0,
	name = ["setup_main_stream", "setup_sub_stream", "setup_third_stream" ];
	VinStreamInfo[src].forEach(function(ch){
		if( ch >= 0 && ch < 2) {
//            if(VideoInfo[ch]['codec'] != 2){
    			cmd += "<option value="+index+">"+getLanguage(name[index])+"</option>";
//            }
            index++;
		}
	});
	if( cmd ) {
		$("#channel").append(cmd);
	}
}

//[UDP technology] add plugin event-start
function getUserEventList()
{
	var timestamp = new Date().getTime();
	var file = "/plugin_user_event_index.txt?timestamp="+timestamp;
	var doc = readTextFile(file);
	var lines = doc.split('\n');
	var usernameList = [];
	for(var i = 0;i < lines.length;i++) {
		if(lines[i].search(':all=') >= 0){
			usernameList.push(lines[i]);
		}
	}
	return usernameList;
}
function extractXml(ueveid) {
	var text = getXmlData();
	var parser = new DOMParser();
	var xmlDoc = parser.parseFromString(text,"text/xml");
	var length = xmlDoc.querySelectorAll('eventname').length;
	var uevename = '';
	if( xmlDoc ) {
		for(var i = 0 ; i < length ; i++) {
			if(xmlDoc.getElementsByTagName("eventname")[i] && xmlDoc.getElementsByTagName("eventid")[i]) {
				if(xmlDoc.getElementsByTagName("eventid")[i].childNodes[0].nodeValue.toLowerCase() == ueveid.toLowerCase()) { // One plugin, several events
					uevename = xmlDoc.getElementsByTagName("eventname")[i].childNodes[0].nodeValue
					if(uevename != undefined)
						break;
				}
			}
		}
	}
	return uevename;
}
//[UDP technology] add plugin event-end
function initValue(){

	var cmd_trigger = '';
	if( capInfo['sensor_count'] < 1 ) {
		var triggerEvent = ["Motion"];
	} else {
		var triggerEvent = ["Motion","Alarm Input","Motion & Alarm Input"]; 
	}
    for(index=0;index<triggerEvent.length;){
	    cmd_trigger += "<option value="+index+">"+getLanguage(triggerEvent[index++])+"</option>";
    }
	//[UDP technology] add plugin event-start
	var userevent = getUserEventList();
	for(index=0;index<userevent.length;){
	    cmd_trigger += "<option value="+userevent[index].split(':all=')[1]+">"+extractXml(userevent[index++].split(':all=')[0])+"</option>";
	}
	//[UDP technology] add plugin event-end
    if(cmd_trigger){
        $("#trigger_event").append(cmd_trigger);
    }
    var cookies = getCookie('stream_cookie');
    if( cookies ){
        $("#channel").val(cookies);
        setCookie('stream_cookie','',-1);
    }
    activechannel = $("#channel").val();
	$("#framerate").val(ACFInfo[activechannel].framerate);
	$("#target_bitrate").val(ACFInfo[activechannel].target_bitrate);
	$("#target_gop").val(ACFInfo[activechannel].target_gop);
	$("#bitrateControl").val(ACFInfo[activechannel].bitrateControl);
	$("#hold_on_time").val(ACFInfo[activechannel].hold_on_time);
	$("#trigger_event").val(ACFInfo[activechannel].trigger_event  );

}

function initEvent(){

	$("#vin_source").change(function(e){
		src = getVinSourceIndex("#" + e.currentTarget.id);
		updateChannelInfomation();
		initValue();
		MJ.id = src;
		channel = 0;
		checkDependencies();
	});

	$("#channel").off("change").change(function(e){
		channel = $("#channel").val();
		setChannel( channel );
		checkDependencies();
	});


	$("#btOK").click(function () {
		var data='';
        var enabled=0,change=0;
        activechannel = $("#channel").val(); 
/*
        if( $('[name=enabled]:checked').val() == 1)
            enabled=1;

		settingList.forEach( function(id){
			var value = $("#" + id ).val();
			if( value != ACFInfo[activechannel][id] )
				data += id + "=" + value + "&";
		});
		if(data == ""){
			settingFail(menu, getLanguage("msg_nothing_changed"));
			return ;
		}

*/

        var param = {
            msubmenu : 'SmartACF',
            action : 'apply',
            source : (Number(src)+1),
            stream : channel,
        }

            
            settingList.forEach( function(id){
                var value = $("#" + id ).val();
                if( value != ACFInfo[activechannel][id] ){
                    if(id == "framerate"){
                        if(VideoInfo[activechannel][id]> value){ 
                            if(confirm(getLanguage("ACF_confirm"))){
                                console.log("YES");
                                param[id] = value ;
                                change =1;
                            }
                            else{
                                console.log("cancle");
                            }
                        }
                        else{
                            param[id] = value ;
                            change =1;
                        }
                    }
                    else{
                        param[id] = value ;
                        change =1;
                    }
                }
            });  

		if( change == 0 ) {
			pop_msg = getLanguage("msg_nothing_changed");
			settingFail(menu, pop_msg);
			return ; 		
		}
        
       // if(capInfo["oem"] == 12)
            setCookie('stream_cookie',activechannel,1);
		$.ajax({
			method: 'get',
			url:'./basic.cgi?', 
			data: param,
			success: function(req){
				var pattern = /OK/g;
				if( pattern.test(req) == true){
					pop_msg = getLanguage("Success");
					settingSuccess(menu, pop_msg);
					refreshMenuContent();
//                    $("#channel").val(channel);             
				}else{
					settingFail(menu);
					refreshMenuContent();
//					initValue();
				}
			},
			error: function(req){
				settingFail(menu);
				refreshMenuContent();
			}
		});

    });
}

function setChannel(index) {
	activechannel = Number(index);

    if(VideoInfo[activechannel].codec == 1){
        obj = VideoOption[activechannel].h264;
    } else if(  VideoInfo[activechannel].codec == 2){
        obj = VideoOption[activechannel].jpeg;
    } else if(  VideoInfo[activechannel].codec == 3)
        obj = VideoOption[activechannel].hevc;

    initFramerate(obj.frMin, obj.frMax);

	 $("#framerate").val(ACFInfo[activechannel].framerate);
	 $("#target_bitrate").val(ACFInfo[activechannel].target_bitrate);
	 $("#target_gop").val(ACFInfo[activechannel].target_gop);
	 $("#bitrateControl").val(ACFInfo[activechannel].bitrateControl);
	 $("#hold_on_time").val(ACFInfo[activechannel].hold_on_time);
	 $("#trigger_event").val(ACFInfo[activechannel].trigger_event);

}

function checkDependencies() {
	$("#target_gop").next().remove();
	$("#target_bitrate").next().remove();
	$("#hold_on_time").next().remove();
    channel = $("#channel").val();

	var targetChannel = VinStreamInfo[src][channel],isMJPEG=0;
	//isMJPEG = VideoInfo[targetChannel]['codec'] == 2;
    if(VideoInfo[targetChannel]['SmartCoreMode'] != 2 || VideoInfo[targetChannel]['codec'] == 2){
        isMJPEG = true;
    }else
        isMJPEG = false;

	$("#framerate").prop("disabled", isMJPEG);
	$("#target_bitrate").prop("disabled", isMJPEG);
	$("#target_gop").prop("disabled", isMJPEG);
	$("#bitrateControl").prop("disabled", isMJPEG);
	$("#hold_on_time").prop("disabled", isMJPEG);
	$("#trigger_event").prop("disabled", isMJPEG);

	var obj;
	obj = BitrateInfo[channel].hevc;
    
    if(!isMJPEG){
        $("#target_gop").after("<span>[ " + 1 + " ~ " + 120 + " ]</span>");
        $("#target_bitrate").after("<span>[ " + obj.brMin/1000 + "Kbps ~ " + obj.brMax/1024000 + "Mbps ]</span>");
        $("#hold_on_time").after("<span>[ " + 5 + "sec ~ " + 60 + "sec ]</span>");



    }

}

function onLoadPage() {
	initUI();
    initValue();
	initEvent();
    
    checkDependencies();
}

$(document).ready( function() {
	onLoadPage();
});
