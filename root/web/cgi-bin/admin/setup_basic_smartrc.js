var menu = getLanguage("rate_control_configuration");
var settingList = [ "stream_quality"];
var settingList3 = [ "dyn_roi_enable"];
var settingList2 = [ "dyn_gop_enable","fps_drop_enable"];
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

function initUI() {
	if ( capInfo["oem"] != 12 ) {
		menu = getLanguage("rate_control_configuration_udp");
		$("#rate_control").attr("tkey","rate_control_configuration_udp");
	}
	commonCreateSourceSelectBox("#vin_source");

    updateChannelInfomation();

	if( smartrc3 ){
		$("#stream_quality_div").remove();
	}
	else
	{
		$("#dynamic_roi_div").remove();
	}

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

function initValue(){

	var cmd_quality = '';
    var streamQuality = ["Low","Medium","High","Extreme"]; 
    for(index=0;index<streamQuality.length;){
	    cmd_quality += "<option value="+index+">"+getLanguage(streamQuality[index++])+"</option>";
    }
    if(cmd_quality){
        $("#stream_quality").append(cmd_quality);
    }

    var cookies = getCookie('stream_cookie');
    if( cookies ){
        $("#channel").val(cookies);
        setCookie('stream_cookie','',-1);
    }
    activechannel = $("#channel").val();
    if( !smartrc3 ){
		$("#stream_quality").val(RCInfo[activechannel].stream_quality);
	} else {
	$("[name=dyn_roi_enable][value=" + RCInfo[activechannel].dyn_roi_enable + "]").prop("checked", true);
	}
    $("[name=dyn_gop_enable][value=" + RCInfo[activechannel].dyn_gop_enable + "]").prop("checked", true);
    $("[name=fps_drop_enable][value=" + RCInfo[activechannel].fps_drop_enable + "]").prop("checked", true);

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
/*
	$("[name=enabled]").click(function ( obj ) {				
		checkDependencies();	
	});
*/
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
            msubmenu : 'SmartRC',
            action : 'apply',
            source : (Number(src)+1),
            stream : channel,
        }
		
		if(!smartrc3)
		{
	        settingList.forEach( function(id){
	            var value = $("#" + id ).val();
	            if( value != RCInfo[activechannel][id] ){
	                param[id] = value ;
	                change =1;
	            }
	        });  
		}
		else
		{
	        settingList3.forEach( function(id){
	            if( $('[name='+id+']:checked').val() != RCInfo[activechannel][id]){
	                param[id] = $('[name='+id+']:checked').val();
	                change = 1;
	            }
	        });
		}

        settingList2.forEach( function(id){
            if( $('[name='+id+']:checked').val() != RCInfo[activechannel][id]){
                param[id] = $('[name='+id+']:checked').val();
                change = 1;
            }
        });

		if( change == 0 ) {
			pop_msg = getLanguage("msg_nothing_changed");
			settingFail(menu, pop_msg);
			return ; 		
		}
        //if(capInfo["oem"] == 12)
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
				}else{
					settingFail(menu);
					refreshMenuContent();
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

	if(!smartrc3) {
    $("#stream_quality").val(RCInfo[activechannel].stream_quality);
	} else {
    $("[name=dyn_roi_enable][value=" + RCInfo[activechannel].dyn_roi_enable + "]").prop("checked", true);
	}
    $("[name=dyn_gop_enable][value=" + RCInfo[activechannel].dyn_gop_enable + "]").prop("checked", true);
    $("[name=fps_drop_enable][value=" + RCInfo[activechannel].fps_drop_enable + "]").prop("checked", true);

}

function checkDependencies() {
	$("#stream_quality").next().remove();
	$("#dyn_gop_enable").next().remove();
    channel = $("#channel").val();

	var targetChannel = VinStreamInfo[src][channel],isMJPEG=0;
	//isMJPEG = VideoInfo[targetChannel]['codec'] == 2;
    if(VideoInfo[targetChannel]['SmartCoreMode'] != 1 || VideoInfo[targetChannel]['codec'] == 2){
        isMJPEG = true;
    }else
        isMJPEG = false;

	$("#enabled_on").prop("disabled", isMJPEG);
	$("#enabled_off").prop("disabled", isMJPEG);
	if(!smartrc3) {
	$("#stream_quality").prop("disabled", isMJPEG);
	} else {
	$("#roi_enabled_on").prop("disabled", isMJPEG);
	$("#roi_enabled_off").prop("disabled", isMJPEG);
	}
	$("#gop_enabled_on").prop("disabled", isMJPEG);
	$("#gop_enabled_off").prop("disabled", isMJPEG);
	$("#fps_enabled_on").prop("disabled", isMJPEG);
	$("#fps_enabled_off").prop("disabled", isMJPEG);
    
    if(!isMJPEG){
//        $("#stream_quality").after("<span>[ " + 100 + "Kbps ~ " + 10 + "Mbps ]</span>");
//        $("#dyn_gop_enable").after("<span>[ " + 5 + "sec ~ " + 60 + "sec ]</span>");

/*
        if(($("[name=enabled]:checked").val()) == 0){
            settingList.forEach( function(id){
                $("#" + id ).prop("disabled", true);

            });
        }
        else if(($("[name=enabled]:checked").val()) == 1){
            settingList.forEach( function(id){
                $("#" + id ).prop("disabled", false);

            });
        }
*/
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
