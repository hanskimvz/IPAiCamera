var menu = getLanguage("video_configuration");
var settingList = [ "codec", "codec_name", "resolution", "framerate", "bitrate_mode","bitrate", "quality", "gopsize", "h264_profile", "rtsp_timeout"];
//if( (systemOption & SYSTEM_OPTION_UI_FIXED_DATE_20160504) == 0 ){
if (1){
	$.merge(settingList, ["lbr_mode","h264_extension_option","SmartCoreMode"]);
}
var activeChannel;
var lastVideoInfo = [];
var debug_level = 0;
function debug(cmd){if(debug_level > 0 ){ console.log("[VIDEO] " + cmd); } }
// 새로운 인자가 추가되서 해당 변수 복사 방식 변경
	$.extend(true, lastVideoInfo, VideoInfo);
var src = MJ.id;

function initFramerate(min, max) {
	$("#framerate").find("option").remove();
	if( min == undefined){
		min = 0;
	}
	if( max == undefined) {
		max = 30;
	}
	for( var i = max ; i >= min ; i--) {
		$("#framerate").append("<option value=" + i + ">" + i + "</option>" );
	}
}
function initUI() {
	commonCreateSourceSelectBox("#vin_source");
    commonCreateAllSettingButton();
	
	function getCodecName(num) {
		switch( num ) {
			case 0: 
				return "NONE";
			break;
			case 1: 
				return "H.264";
			break;
			case 2:
				return "M-JPEG"
			break;
			case 3:
				return "H.265"				
			break;
		}
	}
	var obj='';
	var codec_name;
	$("#profile_title~tr").remove();
	for( var i = 0 ; i < capInfo.channels ; i++ ) {
		index = VinStreamInfo[src][i];
		target = VideoOption[index];
		if( typeof(target) != undefined ){
			obj += '<tr class="channels"><td class="channel2" colspan="2">';
			obj += '<input id="optProfile' + (index+1) + '" name="optProfile"';
			obj += ' type="radio" value="' + index + '">';
			obj += '<label for="optProfile' + (index+1) + '"></label> ';
			if(capInfo["oem"] == 12){
				obj += '<span>'+getLanguage('setup_stream'+(i+1))+'</span> </td>';
			}else{
				obj += '<span>' + (i+1) +  '</span> </td>';
			}
			obj += '<td id="codec' + index + '">' + getCodecName(VideoInfo[index]['codec'])+ '</td>';
			codec_name = VideoInfo[index]['codec_name'].replace(/ /gi, "&nbsp;")
			obj += '<td id="codec_name' + index + '">' + codec_name +'</td></tr>';
		}
	}
	if( typeof(obj) != 'undefined') {
		$("#profile").append(obj);
	}
	
	activeChannel = 0 ;
	switch (VideoInfo[0]['codec']) {
		case 1 :
			obj = VideoOption[activeChannel].h264; break;
		case 2 : 
			obj = VideoOption[activeChannel].jpeg; break;
		case 3 :
			obj = VideoOption[activeChannel].hevc; break;
		default : 
			obj = undefined;
	}
	if( capInfo["oem"] == 19 || capInfo["oem"] == 20 || capInfo["oem"] == 21 ){
		$("#content_preset").show();
	}
	if( capInfo["oem"] == 19 )
	{
		$("#preset_conf").append("<option value=\"1\" tkey=\"setup_video_default\"></option>");
		$("#preset_conf").append("<option value=\"2\" tkey=\"setup_video_default_vms\"></option>");
	}
	else if(capInfo["oem"] == 20 || capInfo["oem"] == 21)
	{
		$("#preset_conf").append("<option value=\"1\" tkey=\"setup_video_default\"></option>");
		$("#preset_conf").append("<option value=\"2\" tkey=\"setup_video_motion\"></option>");
	}

    if( capInfo["video_out"] == 1 ){
		$("#content_vout").show();
		$("#vout_conf").append("<option value=\"0\">1080P</option>");
		$("#vout_conf").append("<option value=\"1\">720P</option>");

		$("#vout_conf option:eq("+VoutInfo.vout_resolution+")").prop("selected", "selected");
    }
	if( capInfo["oem"] == 19 || capInfo["oem"] == 20 || capInfo["oem"] == 21 ) {
		$("#smart_core_label").attr("tkey","smart_core_udp");
		$("#SmartCoreMode").find("#RC").attr("tkey","setup_coremode_0_udp");
		$("#SmartCoreMode").find("#ACF").attr("tkey","setup_coremode_1_stanley");
	} else if( capInfo["oem"] != 12 ){
		$("#smart_core_label").attr("tkey","smart_core_udp");
		$("#SmartCoreMode").find("#RC").attr("tkey","setup_coremode_0_udp");
		$("#SmartCoreMode").find("#ACF").attr("tkey","setup_coremode_1_udp");
	}
		
	if( typeof(obj) != 'undefined')
		initFramerate(obj.frMin, obj.frMax);
	if( capInfo["oem"]== 6 || capInfo["oem"]== 12){
		$("#h264_extension_option_div").css("display" , "none");
	}
    if(smartcontrol == 0 || capInfo.camera_module == "s2l_internal_isp" || capInfo.image_sensor == "bt1120_1080p" || capInfo.image_sensor == "bt1120_720p" ||capInfo.camera_type == "PROXY_CLIENT" || capInfo.camera_type == "PROXY_SERVER"||capInfo.camera_type == "PREDATOR_CLIENT" || capInfo.camera_type == "PREDATOR_SERVER"||capInfo.camera_type == "PROXY_DUAL_CLIENT" || capInfo.camera_type == "PROXY_DUAL_SERVER"){
        $("#SmartCoreMode").css("display","none");
        $("#smart_core_label").css("display","none");
    }else {
        $("#lbr_mode").css("display","none");
        $("#smart_lbr_label").css("display","none");
    }
	/*
	if( capInfo["board_chipset"]== "amba_s2lm55" )
		$("#h264_extension_option").append("<option value='1' tkey='h264_exention_mode1'>B-Frame On(BP)</option>");
		*/
//	else if( capInfo["board_chipset"]== "amba_s2l66" ) ;
}


function checkDependency() {          //  Change UI by variable
	function disableSetting(cmd) {
		$("#contents").find("select").prop("disabled", cmd);
		$("#contents").find("input").prop("disabled", cmd);
	};
	function checkBitrateMode() {
		if( $("#lbr_mode").val() == 0 ){
			$("#bitrate_mode").prop("disabled",false);
			if( $("#bitrate_mode").val() == 0) {// VBR
				//$("#bitrate").before().prop("disabled", true);
				//$("#bitrate").prop("disabled", true);
				$("#quality").before().prop("disabled", false);
				$("#quality").prop("disabled", false);
			} else if ( $("#bitrate_mode").val() == 1) { // CBR
				//$("#bitrate").before().prop("disabled", false);
				//$("#bitrate").prop("disabled", false);
				$("#quality").before().prop("disabled", true);
				$("#quality").prop("disabled", true);
			}
		} else { 
			$("#bitrate_mode").prop("disabled",true);
			$("#quality").prop("disabled", true);
		}
	};
	function checkSmartCoreMode() {
		if( $("#SmartCoreMode").val() != 1 ){  // normal, ACF
			$("#bitrate_mode").prop("disabled",false);
			if( $("#bitrate_mode").val() == 0) {// VBR
				//$("#bitrate").before().prop("disabled", true);
				//$("#bitrate").prop("disabled", true);
				$("#quality").before().prop("disabled", false);
				$("#quality").prop("disabled", false);
			} else if ( $("#bitrate_mode").val() == 1) { // CBR
				//$("#bitrate").before().prop("disabled", false);
				//$("#bitrate").prop("disabled", false);
				$("#quality").before().prop("disabled", true);
				$("#quality").prop("disabled", true);
			}	  
		} else {  //rc
			$("#bitrate_mode").prop("disabled",false);
			$("#quality").prop("disabled", true);
		}
	};
	function initDependencyUI(){
		$("#profile_div").css("display", "block");
	}
	function checkmode(){
        
        if(smartcontrol == 0 || capInfo.camera_module == "s2l_internal_isp" || capInfo.image_sensor == "bt1120_1080p" || capInfo.image_sensor == "bt1120_720p" ||capInfo.camera_type == "PROXY_CLIENT"|| capInfo.camera_type == "PROXY_SERVER"||capInfo.camera_type == "PREDATOR_CLIENT" || capInfo.camera_type == "PREDATOR_SERVER"||capInfo.camera_type == "PROXY_DUAL_CLIENT" || capInfo.camera_type == "PROXY_DUAL_SERVER" ){
            checkBitrateMode();
        }
        else{
		    checkSmartCoreMode();
        }
    }
	initDependencyUI();
	if( $("#codec").val() == 2 ){ // MJPEG
		disableSetting(false);
        checkmode();
	    $("#DisableUI_MJPEG").css("display", "none");
	    $("#DisableUI_MJPEG_Second").css("display", "none");

		//$("#gop").css("display", "none");
		$("#quality").prop("disabled", false);	
	} else if( $("#codec").val() == 1){ // H264
	  $("#bitrate").val( VideoInfo[activeChannel]['bitrate'] );
		disableSetting(false);
		$("#DisableUI_MJPEG").css("display", "block");
		$("#DisableUI_MJPEG_Second").css("display", "block");
        checkmode();
		$("#gop").css("display", "block");
	} else if( $("#codec").val() == 0){ // none
		disableSetting(true);
	} else if( $("#codec").val() == 3){ // HEVC
	  $("#bitrate").val( VideoInfo[activeChannel]['hevc_bitrate'] );
		disableSetting(false);
		$("#DisableUI_MJPEG").css("display", "block");
		$("#DisableUI_MJPEG_Second").css("display", "block");
        checkmode();
		$("#gop").css("display", "block");
		$("#profile_div").css("display", "none");
	}	
	

	$("#codec").prop("disabled", ($("#codec").find("option").length == 1 ));
	if( capInfo['oem'] == 8)
		$("#h264_profile").prop("disabled",true);
}

function checkDependencyUI() {               //  Change UI by channel select

    $("#codec option").remove();
	$("#resolution option").remove();
	$("#bitrate").next().remove();
	$("#quality").next().remove();
	$("#gopsize").next().remove();
    $("#h264_profile option").remove();

	if( typeof(VideoOption[activeChannel]) != "undefined") {
		var obj;
		var resol;
		//if( capInfo.camera_type != "fisheye" && activeChannel != 0 ) $("#codec").append("<option value=0>NONE</option>");
		var content ='';
		if( VideoOption[activeChannel].h264Support ) content += "<option value=1>H.264</option>";
		if( VideoOption[activeChannel].jpegSupport ) content += "<option value=2>MJPEG</option>";
		if( VideoOption[activeChannel].bHEVCSupport ) content += "<option value=3>H.265</option>";
		
		$("#codec").append(content).val( VideoInfo[activeChannel].codec );
		
		if(VideoInfo[activeChannel].codec == 1){
			obj = VideoOption[activeChannel].h264;
		} else if(  VideoInfo[activeChannel].codec == 2){
			obj = VideoOption[activeChannel].jpeg;
		} else if(  VideoInfo[activeChannel].codec == 3)
			obj = VideoOption[activeChannel].hevc;
		
		if( typeof(obj) == 'undefined') return;
		for( var i = 0 ; i < obj.numValidRes ; i++){
			resol = obj.Resolutions[i].Width + "x" + obj.Resolutions[i].Height;
			$("#resolution").append("<option value=" + resol + ">" + resol + "</option>");
		}
		if(	$("#codec").val() ==  1 || $("#codec").val() == 3 ){
			$("#gopsize").after("<span>[ " + obj.govMin + " ~ " + obj.govMax + " ]</span>");
			$("#bitrate").after("<span>Kbps [ " + obj.brMin/1000 + "Kbps ~ " + obj.brMax/1024000 + "Mbps ]</span>"); 
			if (obj.pfSupport[3]) {
				$("#h264_profile").append("<option value=3>" + getLanguage("h264_high") + "</option>");
			}
			if (obj.pfSupport[1]) {
				$("#h264_profile").append("<option value=1>" + getLanguage("h264_main") + "</option>");
			}
			if (obj.pfSupport[0]) {
				$("#h264_profile").append("<option value=0>" + getLanguage("h264_baseline") + "</option>");
			}
		}
		initFramerate(obj.frMin, obj.frMax);
		$("#quality").after("<span>[ " + VideoOption[activeChannel].qMin+ " ~ " + VideoOption[activeChannel].qMax + " ]</span>");
	}
}
function updateInformation(val) {
	for( var i = 0 ; i < settingList.length ; i++)	{
		var obj = $("#" + settingList[i]);
		var tag = obj.prop("tagName");
		var value ;
		if(val == "org") value = lastVideoInfo[activeChannel][settingList[i]];
		else  value = VideoInfo[activeChannel][settingList[i]];	

		debug(settingList[i]+ "=" + value);
		if( tag == "SELECT" || tag == "INPUT") {
//			if(settingList[i] !="codec") obj.val( value );	
			 obj.val( value );
		} 
		if( settingList[i] == "framerate" && obj.val() == null ){
			$("#" + settingList[i] + " option:eq(0)").prop("selected", "selected");
		}
		if( settingList[i] == "rtsp_timeout") {
			if( value ) {
				$("#rtsp_timeout").prop("disabled", false);
				$("#crtsp_timeout").prop("checked", true);
			} else {
				$("#rtsp_timeout").prop("disabled", true);
				$("#crtsp_timeout").prop("checked", false);
			}
		}
	}
}
function check_range(min, max, name){
	var val = $("#"+ name ).val();
	if( val < min || val > max ) {
		$("#"+name).val(lastVideoInfo[activeChannel][name]);  
		settingFail(menu, getLanguage("msg_outofrange"));
		return false ;
	}
	return true;
}
function check_text_excced( max, name){
	var text_length = $("#"+ name ).val().length;
	if( text_length > max ) {
		var orgval = lastVideoInfo[activeChannel][name] ;
		$("#"+name).val(orgval);  
		settingFail(menu, getLanguage("msg_invalid_text_length") + "(30)");
		return false ;
	}
	return true;
}
function initEvent() {
	if(capInfo["oem"] == 12){
		$("#framerate").off("click").click(function(e){
			$("#gopsize").val($("#framerate").val()*2);
		});
	}
	$("#vin_source").off("change").on("change", function(e){
		src = getVinSourceIndex("#" + e.currentTarget.id);
		MJ.id = src;
    onLoadPage();
		$("[name=optProfile]:first").trigger("click");
	});
/*
	$("#codec").off("change").on("change", function(e){
		VideoInfo[activeChannel][e.target.id]= e.target.value;
		checkDependencyUI();
		checkDependency();
	});
*/
	$("[name=optProfile]").off("click").click(function ( obj ) {
		$.extend(true, VideoInfo[activeChannel], lastVideoInfo[activeChannel]);
		activeChannel = obj.target.value;
		checkDependencyUI();
		updateInformation("org");
		
		checkDependency();
	});
	$("#SmartCoreMode").change(function(obj){
		if( this.value == 0 ) {
			$("#bitrate_mode").removeAttr("disabled");
		}
		else if( this.value == 1 ) {
			$("#bitrate_mode").attr("disabled", "true");
		}		
		else {
			$("#bitrate_mode").removeAttr("disabled");
		}
	});
	$("#lbr_mode").change(function(obj){
		if( this.value == 0 ) {
			$("#bitrate_mode").removeAttr("disabled");
		}
		else { 
			$("#bitrate_mode").attr("disabled", "true");
		}		
	});
	$("#btpreset").off("click").click(function(event) {
		var data = null;
		data = "msubmenu=profile&action=apply";
		data += "&value=" + $("#preset_conf").val();
		$.ajax({
			type:"get",
			url: "/cgi-bin/admin/basic.cgi",
			data: data,
			success: function(args){
				settingSuccess(menu, null);
				refreshMenuContent();
			}, 
			error: function() {
			settingFail(menu);
			}
		});
	});
	$("#btvout").off("click").click(function(event) {
		function onSuccessApply(msg) {
			var tmp= msg.trim().split('\n');
			var response = tmp[0].slice(0, -1);
			var error_code = tmp[1];
			var error_result;
			var pattern = /OK/;
			if(pattern.test(msg) ){
				settingSuccess(menu, null);
				refreshMenuContent();
				return;
			} else{		
				settingFail(menu, "Not Change Resolution!");
				refreshMenuContent(); 
			}
			progressUI(false);
		}
		var data = null;
		data = "msubmenu=vout_resolution&action=apply";
		data += "&value=" + $("#vout_conf").val();
		$.ajax({
			type:"get",
			url: "/cgi-bin/admin/basic.cgi",
			data: data,
			success: function(args){
				onSuccessApply(args);
			}, 
			error: function() {
			settingFail(menu);
			}
		});
	});
	$("#btOK").off("click").click(function(event) {
		$("#"+event.currentTarget.id).prop("disabled", true);

		function onSuccessApply(msg) {
			var tmp= msg.trim().split('\n');
			var response = tmp[0].slice(0, -1);
			var error_code = tmp[1];
			var error_result;
			if(error_code != undefined)
				error_result= parserErroncode(error_code);
			var pattern = /OK/;
			if(pattern.test(msg) ){
				settingSuccess(menu, null);
				refreshMenuContent();
				$("#"+event.currentTarget.id).prop("disabled", false);
				return;
			} else{		
//				settingFail(menu, getLanguage("msg_fail_retry"));
				if(!$("#codec_name,#gopsize, #bitrate, #quality, #rtsp_timeout").off("blur").blur()){
					settingFail(menu, error_result);
					$("[name=optProfile][value="+activeChannel+"]").trigger("click");
				}
				refreshMenuContent(); // multi-vin
			}
/*			} else {			
				settingFail(menu, tmp[1], "1");
				$("[name=optProfile][value="+activeChannel+"]").trigger("click");
			}*/
			$("#"+event.currentTarget.id).prop("disabled", false);
			progressUI(false);
		}
		function onFailApply() {
			settingFail(menu, getLanguage("msg_fail_retry"));
			progressUI(false);
			refreshMenuContent();
		}

		var data = null;
		var newValue;
		var orgValue;
		if($("#codec").val() == 2 ) settingList = [ "codec", "codec_name", "resolution", "framerate", "quality", "rtsp_timeout"];
		
		for( var i = 0 ; i < settingList.length ; i++)	{	
			var obj = $("#" + settingList[i]);
//			newValue = VideoInfo[activeChannel][settingList[i]];
			newValue =  $("#" + settingList[i]).val();
			orgValue = lastVideoInfo[activeChannel][settingList[i]];
            if( $("#codec").val() == 3){ // HEVC
    	        if( settingList[i] == "bitrate"){
                    orgValue = lastVideoInfo[activeChannel]["hevc_bitrate"];
                }
            }

			if( orgValue != newValue ) {
				if( settingList[i] == "gopsize" && $("#codec").val() != 1 && $("#codec").val() !=3){
					;
				} else {
					if( data == null) {
						data = settingList[i] + "=" + newValue;
					} else {
						data += "&" + settingList[i] + "=" + newValue;
					}
				}
			}
		}

		if(!isValidText(VideoInfo[activeChannel]["codec_name"]))
		{
			settingFail(menu, getLanguage("msg_invalid_text"));	 
			$("[name=optProfile][value="+activeChannel+"]").trigger("click");
			$("#"+event.currentTarget.id).prop("disabled", false);
			return ;
		}

		if(!checkCharacters("profile",$("#codec_name").val())){
			pop_msg = getLanguage("msg_onlyalphabet");
			if( gLanguage == 0 ){
				pop_msg = getLanguage("msg_onlyalphabet")+" ( only [-],[_] ).";
			}
			else if( gLanguage == 1 ){
				pop_msg = getLanguage("msg_onlyalphabet")+ " [-],[_] " + getLanguage("msg_onlyalphabet1");
			}
	        	settingFail(menu, pop_msg);
			refreshMenuContent();
		        return 0;
		}
		
		if(data != null) {
			data = "msubmenu=video&action=apply&profile_no="+activeChannel+"&" + data;
		} else {
			settingFail(menu, getLanguage("msg_nothing_changed"));
			$("#"+event.currentTarget.id).prop("disabled", false);
			return ;
		}
        //if(capInfo["oem"] == 12)
		if(!capInfo.is_proxy_camera){
			setCookie('stream_cookie',activeChannel,1);
		}
		progressUI(true);
		$.ajax({
			type:"get",
			url: "/cgi-bin/admin/basic.cgi",
			data: data,
			success: function(args){
				onSuccessApply(args);
			}, 
			error: onFailApply
		});
	});

	$("#btApplyAll").off("click").click(function(event) {
		$("#"+event.currentTarget.id).prop("disabled", true);

		function onSuccessApply(msg) {
			var tmp= msg.trim().split('\n');
			var response = tmp[0].slice(0, -1);
			var error_code = tmp[1];
			var error_result = parserErroncode(error_code);
			var pattern = /OK/;
			if(pattern.test(msg) ){
				settingSuccess(menu, getLanguage("apply_all_success"));
				refreshMenuContent();
				$("#"+event.currentTarget.id).prop("disabled", false);
				return;
			} else{		
//				settingFail(menu, getLanguage("msg_fail_retry"));
				settingFail(menu, error_result);
				$("[name=optProfile][value="+activeChannel+"]").trigger("click");
				//refreshMenuContent() // multi-vin
			}
/*			} else {			
				settingFail(menu, tmp[1], "1");
				$("[name=optProfile][value="+activeChannel+"]").trigger("click");
			}*/
			$("#"+event.currentTarget.id).prop("disabled", false);
			progressUI(false);
		}
		function onFailApply() {
			settingFail(menu, getLanguage("msg_fail_retry"));
			progressUI(false);
			refreshMenuContent();
		}

		var data = null;
		var newValue;
		var orgValue;
		if($("#codec").val() == 2 ) settingList = [ "codec", "codec_name", "resolution", "framerate", "quality", "rtsp_timeout"];
		
		for( var i = 0 ; i < settingList.length ; i++)	{	
			var obj = $("#" + settingList[i]);
//			newValue = VideoInfo[activeChannel][settingList[i]];
			newValue =  $("#" + settingList[i]).val();
			orgValue = lastVideoInfo[activeChannel][settingList[i]];

            //all save시 description 변경하지 못함
			if( orgValue != newValue ) {
                if(settingList[i] == "codec_name"){
			    	//pop_msg = "You can not change \"Description\" in \"All Save\".";
			    	pop_msg = getLanguage("apply_all_description");
	            	settingFail(menu, pop_msg);
		        	refreshMenuContent();
		            return 0;                    
                }
				if( settingList[i] == "gopsize" && $("#codec").val() != 1 && $("#codec").val() !=3){
					;
				} else {
					if( data == null) {
						data = settingList[i] + "=" + newValue;
					} else {
						data += "&" + settingList[i] + "=" + newValue;
					}
				}
			}
		}

		if(!isValidText(VideoInfo[activeChannel]["codec_name"]))
		{
			settingFail(menu, getLanguage("msg_invalid_text"));	 
			$("[name=optProfile][value="+activeChannel+"]").trigger("click");
			$("#"+event.currentTarget.id).prop("disabled", false);
			return ;
		}

		if(!checkCharacters("profile",$("#codec_name").val())){
			pop_msg = getLanguage("msg_onlyalphabet");
			if( gLanguage == 0 ){
				pop_msg = getLanguage("msg_onlyalphabet")+" ( only [-],[_] ).";
			}
			else if( gLanguage == 1 ){
				pop_msg = getLanguage("msg_onlyalphabet")+ " [-],[_] " + getLanguage("msg_onlyalphabet1");
			}
	        	settingFail(menu, pop_msg);
			refreshMenuContent();
		        return 0;
		}
		
		if(data != null) {
			data = "msubmenu=video&action=apply&&profile_no="+activeChannel+"&saveall="+capInfo.video_in+"&" + data;
		} else {
			settingFail(menu, getLanguage("msg_nothing_changed"));
			$("#"+event.currentTarget.id).prop("disabled", false);
			return ;
		}
		progressUI(true);
		$.ajax({
			type:"get",
			url: "/cgi-bin/admin/basic.cgi",
			data: data,
			success: function(args){
				onSuccessApply(args);
			}, 
			error: onFailApply
		});
	});

	settingList.forEach(function(id) {
		if( id == "crtsp_timeout" ) return; //ignore
		$target = $("#" + id);
		var tagName = $target.prop("tagName");
		var EVENT;
		if( tagName == "SELECT"){
			EVENT = "change";
		} else { 
			EVENT = "blur";
		}
		$target.off(EVENT).on(EVENT, function(e){
			if( e.target.id != "codec") {
				debug(e.target.id + "=" + e.target.value);
				VideoInfo[activeChannel][e.target.id]= e.target.value;
				checkDependency();
			}
            else if(e.target.id == "codec"){
	     	    VideoInfo[activeChannel][e.target.id]= e.target.value;
		        checkDependencyUI();
		        checkDependency();
            }

		});
	});
	$("#crtsp_timeout").off("click").click(function(event){
		$("#rtsp_timeout").prop("disabled", !event.currentTarget.checked);
		var value = 0;
		if(( $("#crtsp_timeout").prop("checked") ) == true ) {
			if(	VideoInfo[activeChannel]["rtsp_timeout"] == 0 ) {
				value = 30;
			} else {
				value = VideoInfo[activeChannel]["rtsp_timeout"];
			}
		} else {
			value = 0;
		}
		$("#rtsp_timeout").val(value); 
		VideoInfo[activeChannel]['rtsp_timeout'] = value;
	});
	$("#gopsize, #bitrate, #quality, #rtsp_timeout").off("blur").blur( function(obj){
		var name = obj.target.id;
	    if ( $("#"+ name ).val().isDigit()) {
			var codec = $("#codec").val();
			var obj;
			if( codec == 1 ) { 
				obj = VideoOption[activeChannel].h264;	
			} else if ( codec == 2) {
				obj = VideoOption[activeChannel].jpeg;
			} else if ( codec == 3) {
				obj = VideoOption[activeChannel].hevc;
			}
			
			if( name == "gopsize" ) 
				check_range(obj.govMin ,obj.govMax,  name);
			else if( name == "bitrate" ) 
				check_range(obj.brMin/1000, obj.brMax/1000, name);
			else if( name == "quality" ) 
				check_range(VideoOption[activeChannel].qMin ,VideoOption[activeChannel].qMax, name);
			else if( name == "rtsp_timeout" ) 
				check_range(30 ,120, name);
		} else {
	    	$("#"+name).val(lastVideoInfo[activeChannel][name]);
	    	checkDependency();
	    	settingFail(menu, getLanguage("msg_onlynumber"));
		}
	});
	$("#codec_name").off("blur").blur( function(obj){
		var name = obj.target.id ;
		if( name == "codec_name" ) check_text_excced(30 , name);	
	});
}

function onLoadPage() {
	initUI();
	initEvent();
    var cookies = getCookie('stream_cookie');
    if( cookies ){
	    $("[name=optProfile][value="+cookies+"]").trigger("click");
        setCookie('stream_cookie','',-1);
    }else{
	    $("[name=optProfile]:first").trigger("click");
    }
	if( (systemOption & SYSTEM_OPTION_UI_FIXED_DATE_20160504) == 0 ){	
		$("#rtsptimeout_contents").css("display", "none");
	}
}

$(document).ready( function() {
	onLoadPage();
});
