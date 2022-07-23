$.ajaxSetup({ cache: false });

//getSystime(strtime);// it's defined page.js
var ctrlAdminTool;
var ctrlpopup ;
var pantiltspeed = 5 ;
var zoomspeed = 4 ;
var popupflag ;
var preset_popup ;
var presettour_popup ;
var preset = new Array(256) ;
var presettour_index ;
var jog_flag = 0 ;
var VLCManager = new VLC("vlc_play", capInfo, VideoInputInfo, VideoInfo, "lstProfile");
if(typeof(VLCManager) == undefined ){
	console.log("VLCManager initialize fail");
	VLCManager = null;
}

function logout(logout_value)
{
	$.ajax({
            type: "GET",
            url: "/cgi-bin/video.cgi",
            async: false,
            username: "Unknown",
            password: "1",
            headers: { "WWW-Authorization": "Digest xxx" }
	})
	.done(function(){
	    // If we don't get an error, we actually got an error as we expect an 401!
	})
	.fail(function(){
	    // We expect to get an 401 Unauthorized error! In this case we are successfully 
            // logged out and we redirect the user.
	    //window.location = "/cgi-bin/logout.cgi";
		if(logout_value=="logout_btn"){
			try {
				location.replace("/cgi-bin/logout.cgi?value=logout_btn");
			}catch(e){
				console.log(e);
			}
		}else if(logout_value=="session_time_out"){
			try{
		    	location.replace("/cgi-bin/logout.cgi?value=session_time_out");
			}catch(e){
				console.log(e);
			}
		}
			 
	});
    return false;
}

var timer;
function sessionTimeoutInit()
{
  Timeout();
  
  console.log('inside Session.init()'); 
  
   //capturing all click, touch and keypress events 
  window.addEventListener('touchstart',Timeout,false); 
  window.addEventListener('click',Timeout,false); 
  window.addEventListener('keypress', Timeout, false); 
  
  function _timeout(){ 
   		return function() { 
   			//implement your logic here to make 
         //a server side call (REST maybe?) 
         //that kills the server side sessiom 
         logout("session_time_out");
		 if(ctrlAdminTool != null)
			 ctrlAdminTool.close();
   		}	 
  } 
  function Timeout() { 
  console.log('inside goTimeout()'); 
  	if(typeof(timer) != 'undefined'){ 
  		console.log("clearing timer"); 
  		timer = clearTimeout(timer); //reset as soon as something is clicked 
  	} 
	if(capInfo["oem"] == 12)
	{
  		timer = setTimeout(_timeout(), 900000); //15 min
	}
    
	else if(capInfo["oem"] == 2)
   	{
        	timer = setTimeout(_timeout(), 600000); //10 min
   	}

	else
	{
  		timer = setTimeout(_timeout(), 3600000 /*test tiemout period in millisec*/);
	}
  	//timer = setTimeout(_timeout(), 10000 /*test tiemout period in millisec*/); 
  } 
} 
 


function onLoadPage()
{ 
 sessionTimeoutInit(); 
   
	$("#frame").css("display", "none");
	$("#jpeg,.jpeg_menu").css("display","none");
	if(capInfo.have_pantilt){
		getpreset();
		getpresetTour();
	}
	dependency_css();     //lang.js
	initUI();
	getJson();
	initLanguage();
	$("#frame").css("display", "block");
	VLCManager.setPlayInfo(userInfo, rtspPort, webPort, http_mode);

	var VLC  = VLCManager.init();
	
	if(VLC ){
		VLCManager.doGo();
	}
	
	initEvent();
    if(userInfo.pwchange == 0){
		if(capInfo["oem"] == 12){
			$("#div_left").css("display","none");
			$("#sub_menu").css("display","none");
			$("#iv_logo").css("display","block");
			$("#div_main").addClass("div_admin");
			$("#vlc_play").addClass("vlc_div_admin");
		}else{
			$("#frame").find("*").prop("disabled" , true);
			$("#focusmode").css("display","none");
			$("#focusmodetitle").css("display", "none");
			$("#div_zoom_speed").css("display","none");
			$("#have_pantilt_speed").css("display","none");
			$("#change_pass").prop("disabled",false);
		}
    }

	try{
		VLCManager.updateVolume(0);
	}catch(err){}

	if(capInfo["oem"] != 2){
        $("#cb_mute").css("display","none");
    }
	if(capInfo.camera_type == "PROXY_CLIENT" || capInfo.camera_type == "PROXY_DUAL_CLIENT"){
		$("#iv_surround").css("display","none");
	}
    if(audioEnc.input_volume == 0){
        document.getElementById('cb_mic').checked = true;
    }else{
        document.getElementById('cb_mic').checked = false;
    }
//	$("#cb_mic").prop("disabled", true);
	
	if(capInfo.have_pantilt)
	{
		$("#pan_tilt_value").text(5);
		$("#pt_speed_bar").slider("option", "value", 5)
		_ajax("pantiltspeed", 5);
		
		$("#zoom_value").text(4);
		$("#pt_zoom_bar").slider("option", "value", 4)
		_ajax("zoomspeed", 4);
	}
	else
	{
		$("#zoom_value").text(2);
		$("#pt_zoom_bar").slider("option", "value", 2)
		_ajax("zoom_value", 2);	  
	}
	
	initValue();

	if( ( systemOption & SYSTEM_OPTION_UI_FIXED_DATE_20160504) == 0){
		if(userInfo.auth == 1 )
		{
			setTimeout(function(){
				if( checkRecoveryMode(capInfo) ) {
					var resp = confirm(getLanguage("msg_operation_recovery_mode"));
					if( resp ) {
						$.ajax( {
							type : 'get',
							url  : '/cgi-bin/admin/system.cgi',
							data : {
								msubmenu : "recovery_mode",
								action : "clear",
							}
						});
					}
				}
			}, 1000);
		}
	}
	checkMotion("displayMotionStatus", 1);
	VLCManager.updateVolume(0);
    if ((websocket == 0) || (capInfo["oem"] == 19 && isIE()))
	{
		$("#Streming_Type option[value='1']").remove();
		$("#Streming_Type option[value='2']").remove();
		$("#Streming_Type option[value='3']").remove();

		var select = document.getElementById("Streming_Type");
		//select.options[select.options.length] = new Option('VLC Plugin', '1');
		select.options[select.options.length] = new Option('HTML5[MJPEG]', '2');
		if((userInfo.auth == 1 || userInfo.auth == 2 || userInfo.auth == 4)&& userInfo.pwchange == 1)
			$("#Streming_Type").val("2").trigger("change"); 
    }
}
function getpreset(){

	$.ajax({
			type : 'get',
			url  : '/cgi-bin/ptz.cgi',
			async: false,
			data : 'getpreset=1' ,
			dataType: 'json', 
			success : function(ret){	
				presetInfo = ret.presetInfo ;
			}
    }).done(function(){ console.log("요청 성공시 호출") })
	.fail(function(){ console.log("fail") })
	.always(function(){ console.log("always") });	
}
function getpresetTour(){
	var promise = $.ajax(
		{
			type : 'get',
			url  : '/cgi-bin/ptz.cgi',
			async: true,
			dataType: 'json', 
			data : 'getpresetTour=1', 
			success : function(ret){	
				console.log(ret);					
				presetTourInfo = ret.presetTourInfo ;
				
				for( var i = 0 ; i < 256 ; i++ ){
					if( presetTourInfo[i] != undefined ) 
						$("#presetgroup_2").append("<option value="+ i +">Preset Tour"+ pad(i+1,2) + "</option>");
				}		
				if( $("#presetgroup_2 option").length == 0){
					$("#presetgroup_2").append("<option value= -1 >New Preset Tour</option>");			
				}
			}
		}
	);	
}
function initValue(){
	var index = 0 ;
	if( typeof(presetInfo) != 'undefined' ) {
		for(var i = 0 ; i < 256 ; i++){
			if( presetInfo[i] != undefined ){
				preset[index] = i ;
				index++ ;
			}
		}
	}
//	console.log(preset.());
}
function onClickAdmin()
{
}

function onClickSpeaker(obj)
{
	if(obj.id == "speaker"){
		$("#volume_bar").find("*").attr("disabled", !obj.checked);
	VLCManager.toggleMute();
	}
}

function onClickAlarmReset(){
	$("#alarm").attr("class", "alarm_off");
	$("#motion").attr("class", "motion_off");
	$("#EventClear").removeAttr("disabled");
}
function PopupCenter(url, title, w, h, obj) {
	  // Fixes dual-screen position Most browsers      Firefox
	    var dualScreenLeft = window.screenLeft != undefined ? window.screenLeft : screen.left;
	    var dualScreenTop = window.screenTop != undefined ? window.screenTop : screen.top;

	    width = window.innerWidth ? window.innerWidth : document.documentElement.clientWidth ? document.documentElement.clientWidth : screen.width;
	    height = window.innerHeight ? window.innerHeight : document.documentElement.clientHeight ? document.documentElement.clientHeight : screen.height;

	    var left = ((width / 2) - (w / 2)) + dualScreenLeft;
	    var top = ((height / 2) - (h / 2)) + dualScreenTop;
	    return  window.open(url, title, 'toolbar=no, location=no, directories=no, status=no, menubar=no, scrollbars=no, resizable=no, width=' + w + ', height=' + h + ', top=150, left=' + left);
	} 
function popup(){
	if(capInfo["oem"] == 2){
	    PopupCenter('popup_change_pass.cgi', 'abc', 480 ,290, "ctrlpopup");
	}else{

	  if(gLanguage == 2)    
	    PopupCenter('popup_change_pass.cgi', 'abc', 530 ,300, "ctrlpopup");
	  else
	    PopupCenter('popup_change_pass.cgi', 'abc', 480 ,300, "ctrlpopup");
	}
}

$(document).ready( function(){
/*
    if(userInfo.auth == 1 )
	{
		var pass_flag = $.cookie('chpass');
		if( userInfo['pass'] == "admin" && typeof($.cookie('chpass')) == "undefined" ){
			popup();
			console.log("ctrlpopup:"+ctrlpopup);
		}
    }
*/  
	onLoadPage();

	if(capInfo["oem"] == 12)
	{
		window.onunload = function () {
			logout("session_time_out");
		}
	}

});
$(window).unload(function(){
	if( typeof(VLCManager) != 'undefined') {
		VLCManager.exit();
	}
});
function pad(n, width){
    n = n + '';
    return n.length >= width ? n : new Array(width - n.length + 1).join('0') + n;
}
//init UI
function initUI()
{
	if( IOTInfo.pir_autoclear == 1 )
                $("#pir_autoclear").prop("checked", true);
	else    $("#pir_autoclear").prop("checked", false);

	$("#pir_setclear").css("background-color","#7E7E7E");

	Util.setOEM("logo");
	if( capInfo["oem"] == 10){
		$("#cbca_model_name").text(devInfo.model_name);
	}
	if( capInfo["oem"] == 1){
    	$("#logout_btn").css("display","block");
	}

	if( !isIE() && userInfo.pwchange != 0){
		$("#vlc_play").css("background-color","black");
        if(capInfo.camera_type === "PREDATOR_CLIENT" || capInfo.camera_type === "PROXY_DUAL_CLIENT"){
			$("#vlc_play").css("display","flex");
		}
	}

	updateTime();
	initDisplayMotionStatus("displayMotionStatusArea", capInfo.video_in);

	function CheckUIDependency(){
		//audio
		disabledSlider("volume_bar", 1) ;
		if(capInfo.audio_in === 0)
		{
			$("#sound_box").find("*").prop("disabled", true);
			$("#cb_speaker").prop("checked", false);
            if(capInfo["oem"] == 7){
                 $("input[type='checkbox'] + label").css("background-color", "#B8B8B8");
            }
			$("#cb_mic").prop("checked", false);
		}
		// sensor/relayout
		//if(capInfo.pir == 0 )
		if(1)
		{
			if(audioOutUI == 1) {
				$("#sound_box").remove();
				$("#cb_speaker").hide();
			}else{
				$("#sound_box_audioout").remove();
			}
			if(capInfo.camera_type == "CUBE")
				$("#preset").remove();
			else
				$("#pir_box").remove();
			if(capInfo.sensor_count == 0)
			{
				$("#alarmInput_box").find("*").prop("disabled", true);
				$("#alarminput2").remove();
			}
			else if(capInfo.sensor_count == 1)
			{
			//	$("#alarminput2").prop("disabled", true);
				$("#alarminput2").remove();
			}
			
			if(capInfo.relay_count === 0)
			{
				$("#relayOut_box").find("*").prop("disabled", true);
			}    
			if( capInfo.relay_count < 2 )
				$("#cb_relay_out2").remove();
		}
		else
		{
			$("#c_alarm").remove();
			$("#pir_box").find("*").prop("disabled", true);            
		}
		//ptz
		$("button[class*=ptz]").prop("disabled", capInfo.have_pantilt?false:true);
		$("#have_zoom").find("*").prop("disabled", capInfo.have_zoom?false:true);
		$("#have_focus").find("*").prop("disabled", capInfo.have_focus?false:true);
		
		if(devInfo.model_num === "NBU1-SLAH2") {
			$("#have_iris").find("*").prop("disabled", true);
		} else {
			$("#have_iris").find("*").prop("disabled", capInfo.have_iris?false:true);
		}

		if(( capInfo.have_pantilt == 0 ) &&
		   ( capInfo.have_zoom <= 1) &&
		   ( capInfo.have_focus== 0) &&
		   ( capInfo.have_digitalzoom == 0) )
		   {
				$("#have_pantilt_speed").find("*").prop("disabled", true);  
				$("#pt_speed_bar").slider("disable");
				
				$("#div_zoom_speed").find("*").prop("disabled", true);  
				$("#pt_zoom_bar").slider("disable");		
		   }
		//focusmode
		if( capInfo.focus_mode == 0)
		{
			$("#focusmode").css("display", "none");
			$("#focusmodetitle").css("display", "none");
		}
		//TBD
		$("#backup_box").find("*").prop("disabled", true);
		
		//preset 
		$("#presetgroup_1").append("<option value='-1' >Preset</option>");			
		if( typeof(presetInfo) != 'undefined' ) {
			for( var i = 0 ; i < 256 ; i++ ){
				if( presetInfo[i] != undefined ) 
					$("#presetgroup_1").append("<option value="+ i +">["+pad(i+1,3)+"]"+ presetInfo[i]["name"] + "</option>");
			}
		}
		for( var i = 0 ; i < 256 ; i++ ){
			if( presetTourInfo[i] != undefined ) 
				$("#presetgroup_2").append("<option value="+ i +">Preset Tour"+ pad(i+1,2) + "</option>");
		}		
		if( $("#presetgroup_2 option").length == 0){
			$("#presetgroup_2").append("<option value= -1 >New Preset Tour</option>");			
		}
		if( capInfo.camera_module != "ov_isp" ) // overview mode
		{
			$("#have_wiper").remove();
			$("#have_washer").remove();
			$("#have_wled").remove();
		}
		else // overview mode non-IR model
		{
			if(capInfo.have_cds == 0)
				$("#wled_btn").prop("disabled", true);
		}

		
		/////////////////
				
	}
	function resizeWindow()
	{
		if( (window.outerHeight > 825) && (window.screen.height > 720))
			$("#frame").css("margin-top", (window.outerHeight-820)/2);   
		else
			$("#frame").css("margin-top", 0);   
	}
	function onLoadBuffering()
	{
		$("#selectBox").append("<option value='1'>Apples</option>");
		$("#selectBox").append("<option value='2'>After Apples</option>");
		var obj = $("#bufferingProfile");
        var i, min = 200;
        if( capInfo.video_in >= 4 ) {
            min = 300;
        }
		for(i=min ; i <= 900  ; i+=100)
			obj.append("<option value=" + i + ">" + i + " ms</option>");
		for(i = 1000 ; i <= 5000  ; i+=1000)
			obj.append("<option value=" + i + ">" + i + " ms</option>");
		obj.val(VLCManager.buffering).attr("selected", "selected");
	}
	function CheckUIDependencyOEM(){	

		if( capInfo["camera_module"] == "sony_isp" || capInfo["camera_module"] == "wonwoo_isp" || capInfo["camera_module"] == "ov_isp" )
		{
//			$("#ptz_control_label").remove();
			$(".joystick .circle").remove();
		} 	
		else if( capInfo["camera_module"] == "esca_isp" ){
			if( capInfo["ptz_module"] == "af_licom_2812" ){
				$("#div_zoom_speed").find("*").prop("disabled", 1);
				$("#div_zoom_speed").find(".ui-slider").slider("disable");
			}			
		}
		else{
			$(".joystick .circle").remove();
			$("#preset").find("*").prop("disabled" , true);
			
//			$("#set_home_position").remove();
//            $("#set_home_position").find("*").prop("disabled", true);
			
			if( capInfo["ptz_module"] == "rs485" ){
				$("#div_zoom_speed").css("display","none");	
//				$("#have_zoom_speed").css("margin-top" , "0px")					
			}
			else{
				$("#have_pantilt_speed").css("display","none");	
				$("#have_zoom_speed").css("margin-top" , "0px")			
			}
			
		}
	}
	resizeWindow();
	onLoadBuffering();
	window.onresize = resizeWindow;
	setSlider("volume_bar", 0, 100);
	setSlider("volume_bar_audioout", 1, 15);
	if(capInfo.have_pantilt){
	  setSlider("pt_speed_bar", 1, 10);
	  setSlider("pt_zoom_bar", 1, 8);
	}
	else{
	  setSlider("pt_speed_bar", 1, 3);
	  setSlider("pt_zoom_bar", 1, 3);
	}

	CheckUIDependency();
	
	if( capInfo.focus_mode == 1) {
		if(focus_mode == 1){
				$("#have_focus").find("*").prop("disabled", true);
				$("#have_iris").find("*").prop("disabled", true);
				$('#manual',parent).removeClass('color');
				$("#auto").addClass('color');
		}
		else{
				$("#have_focus").find("*").prop("disabled", false);
				$("#have_iris").find("*").prop("disabled", true);
				$('#auto',parent).removeClass('color');
				$("#manual").addClass('color');		
		}
	}
	
	if( userInfo.auth == 2)
	{
		$("#setup").prop("disabled", true);
		$("#cb_mic").prop("disabled", true);
	}
	else if( userInfo.auth == 4) // viewer
	{
		$("#auto, #manual").addClass('disabled');
		$("#auto, #manual").prop('disabled',true);
		disabledSlider("have_pantilt", 1) ;
		$("#have_zoom, #have_iris, #have_focus" ).find("*").prop("disabled",true);
		$("#sub_menu").find("*").prop("disabled", true);
		$("#setup").prop("disabled", true);		
		$("#auto").removeClass('color');
	}
	$("#lstProfile").find("*").remove();

	for(var i = 0 ; i < VideoInfo.length; i++)
	{
		if( typeof(VideoInfo[i].codec) != 'undefined' && VideoInfo[i].codec > 0 )
			$("#lstProfile").append("<option value='" + (i+1) + "' tkey='channel"+ (i+1)+ "'></option>");
	}
	$(".joystick .circle").remove();
	if(capInfo.have_pantilt && capInfo.have_zoom)
	{
//	    $("#ptz_control_label").remove();
		if( capInfo["ptz_module"] == "rs485" ){
			 if( capInfo["camera_module"] == "esca_isp" || capInfo["camera_module"] == "s2l_internal_isp"  ){   //  ESCA_FPAGE_BOX
//				$("#set_home_position").remove(); 
                $("#home_position").find("*").prop("disabled", true);
				$("#focusmode").css("display", "none");
				$("#focusmodetitle").css("display", "none");
				$("#presetgroup_2_div").find("*").prop("disabled" , true);		 
			 }
			 else{     // PTZ_SONY
				$("#presetgroup_2_div").find("*").prop("disabled" , true);
			 }
		}
		else if(capInfo["camera_module"] == "ytot_isp") { // 3x ptz
			$("#presetgroup_2_div").find("*").prop("disabled" , true);
			$("#div_zoom_speed").remove();
		}
		$("#have_zoom_speed").css("margin-top" , "0px")   
	}
	else if(capInfo.have_pantilt)
	{
      if( capInfo["ptz_module"] != "rs485" )
      {
	  $("#preset").find("*").prop("disabled" , true);
      }
      if( capInfo["ptz_module"] == "rs485" )
      {
        $("#presetgroup_2_div").find("*").prop("disabled" , true);
      }
//	  $("#set_home_position").remove();
//      $("#set_home_position").find("*").prop("disabled", true);
	  $("#div_zoom_speed").css("display","none");	
	}
	else if(capInfo.have_zoom)
	{
      if(capInfo["oem"] == 7){
        var $div = $('<div class="cdus_blink"></div>');
        $('#have_zoom').before($div);
        $("#have_pantilt").css("display","none"); 
      }
	  $("#preset").find("*").prop("disabled" , true);
//	  $("#set_home_position").remove();
//      $("#set_home_position").find("*").prop("disabled", true);
	  $("#have_pantilt_speed").css("display","none");	
	  $("#have_zoom_speed").css("margin-top" , "0px")	
	  if( capInfo["camera_module"] == "esca_isp" ){
		  $("#div_zoom_speed").css("display","none");	
	  }
	}
	else
  {
      if(capInfo["oem"] == 7){
        var $div = $('<div class="cdus_blink"></div>');
        $('#have_zoom').before($div);
        $('.cdus_blink').css('padding','0px 0px');
      }
    $("#preset").find("*").prop("disabled" , true);
//    $("#set_home_position").remove();
//    $("#set_home_position").find("*").prop("disabled", true);
    $("#have_pantilt_speed").css("display","none");	
    $("#div_zoom_speed").css("display","none");	
  }  


}
function updateTime()
{
	if( diffTime == undefined )	  now   = new Date().getTime();
	else now   = new Date().getTime() + diffTime;  

    var sTime  = new Date(now);
    $("#timeInfo").text(getTimeStamp(sTime, false));
    
    setTimeout(updateTime, 1000);
}
//EVENT
function _ajax(cmd , val){
	if( cmd == "pantiltspeed" || cmd == "zoomspeed"  )
		val = val ;
	else
		var val = cmd+ "=" + val + "&" + "source" + "=" + VLCManager.selectedChannel ;	
	$.ajax(
		{
			type : 'get',
			url  : '/cgi-bin/ptz.cgi',
			async: true,
			data : val 
		}
	);
}
function _ajax_io(cmd , val){
	$.ajax({
			type : 'get',
//			cache  : false,
			url  : '/cgi-bin/io.cgi',
			data : val,
			async : true ,
			success : function(ret){
				checkMotion("displayMotionStatus", 1);
			}
	});
}

var timer= 0;
function Pan_Interval(cmd , val){
			 timer = setInterval(function () {
			_ajax(cmd , val);
			 }, 1000);
}
var ptzmove_flag = 0 ;
var cmd_flag ;
function ptz_event(){
	
	function mousedown(cmd , val){		
		var num= 0 ;
		num++;	
		if(num == 1) 
		{
			_ajax(cmd , val);
		//	Pan_Interval(cmd, val);
		}	
	}
	//ptz
	
	$("button[class*=ptz]").mousedown(function(e) 
	{	
	//	var realspeed = [1 ,5000 , 10000] ; 
	//	var val = $(this).val()+"&speed=" +  realspeed[pantiltspeed] ; 		
		mousedown("move",  $(this).val() );
		cmd_flag = "move" ;	
		ptzmove_flag = 1;
	});
	//zoom
	$("#m_zoom,#p_zoom").mousedown(function(e)
	{
		mousedown("zoom", $(this).val());
		cmd_flag = "zoom" ;	
		ptzmove_flag = 1;
	});
/*	$("#m_zoom,#p_zoom").click(function(e)
	{
		mousedown("zoom", $(this).val());
		cmd_flag = "zoom" ;	
		_ajax(cmd_flag, "stop");
	});*/
	//iris
	$("#m_iris,#p_iris").mousedown(function(e)
	{
		mousedown("iris", $(this).val());
		cmd_flag = "iris" ;	
		ptzmove_flag = 1;
	});
	//foucus
	$("#m_focus,#p_focus").mousedown(function(e)
	{
		mousedown("focus", $(this).val());
		cmd_flag = "focus" ;	
		ptzmove_flag = 1;
	});
/*	$("#m_focus,#p_focus".click(function(e)
	{
		mousedown("focus", $(this).val());
		cmd_flag = "focus" ;	
		_ajax(cmd_flag, "stop");
	});*/
	$("#ptz").mouseup(function() {		
	  ptzmove_flag = 0;
		if( cmd_flag != "none") 
		{
			_ajax(cmd_flag, "stop");
		}
		
		cmd_flag = "none";
	});
}
function seltour_index(input){ 
	var input_pad  = Number(input)+1;
	if($("#presetgroup_2 option[value=" + input + "]").val() == undefined ){
		$("#presetgroup_2").append("<option value=" + input +">Preset Tour"+ pad( input_pad, 2) +"</option>");	
	}
}
function initPtz(){
	$("#preset_set").on("click", function(){
		var seleted_index = 1 ;
		var input ;

		function sel_index(){
			for( var i = 0 ; i < 256 ; i++){
				var index = $("#presetgroup_1 option[value=" + i + "]").val() ;
				if( index == null ){
					seleted_index = i+1 ;		
					break ;
				}
			}
		}	
		sel_index() ;
		input = prompt('Please enter preset name.', "preset "+pad(seleted_index,3));
		if( input == "" ) {
			settingFail(menu, getLanguage("msg_check_presetname"));
			return 0;
		}
		if( input.length > 30) {
			settingFail(menu, getLanguage("msg_MAX_presetname"));
			return 0;
		}
		if( !input.match(/^[A-Za-z0-9\s]+$/)) {
			settingFail(menu, getLanguage("msg_onlyalphabet_number"));
			return 0;
		}
/*		if(  input < 1 || input > 256){
			alert("input the value : 1 ~ 256") ;
			return 0 ; 
		}
*/		
		$("#presetgroup_1, #preset_remove, #preset_set, #preset_run").prop("disabled", true );
		$("#preset_tour_div").css("display", "none");

		$.ajax(
			{
				type : 'get',
				url  : '/cgi-bin/ptz.cgi',
				async: true,
				data : "savepreset="+ (seleted_index-1) +"&name=" + encodeURIComponent(input) ,
				success: function(msg){
					var tmp= msg.trim().split('\n');
					console.log(tmp);
					if(tmp[0] == "OK"){
//						$("#presetgroup_1 option[value="+ (input-1) +"]").remove();
//						$("#presetgroup_1").append("<option value=" + (seleted_index-1)+">preset"+ pad(input,3) +"</option>");										
/*						$("#presetgroup_1").find("option").remove();
						$("#presetgroup_1").append("<option value='-1' >Preset</option>");			
						if( typeof(presetInfo) != 'undefined' ) {
							for( var i = 0 ; i < 256 ; i++ ){
								if( presetInfo[i] != undefined ) 
									$("#presetgroup_1").append("<option value="+ i +">["+(i+1)+"]"+ presetInfo[i]["name"] + "</option>");
							}
						}
*/						
						$("#presetgroup_1").append("<option value=" + (seleted_index-1)+">["+pad(seleted_index,3)+"]"+ input +"</option>");
						$("#presetgroup_1").append($("#presetgroup_1 option").remove().sort(function(a, b) {
						    var at = $(a).text(), bt = $(b).text();
						    return (at > bt)?1:((at < bt)?-1:0);
						}));	
						
//						if( preset_popup != undefined ) preset_popup.add_preset(input-1);
					}
					$("#presetgroup_1, #preset_remove, #preset_set, #preset_run").prop("disabled", false);
					$("#presetgroup_1 option[value="+ (input-1) +"]").prop("selected", true );
				}			
			}
		);
//		presetInfo[5]['token'] = "preset_006" ;
	});
	$("#preset_remove").on("click", function(){		
		$("#presetgroup_1, #preset_remove, #preset_set, #preset_run").prop("disabled", true );
		var rmindex = $("#presetgroup_1").val() ;	
		$.ajax(
			{
				type : 'get',
				url  : '/cgi-bin/ptz.cgi',
				async: true,
				data : "removepreset="+ rmindex ,
				success: function(msg){
					var tmp= msg.trim().split('\n');
					console.log(tmp);
					if(tmp[0] == "OK"){
						$("#presetgroup_1 option[value="+ rmindex +"]").remove();	
					//	if( preset_popup != undefined )	preset_popup.del_preset(rmindex);
					}
					$("#presetgroup_1, #preset_remove, #preset_set, #preset_run").prop("disabled", false);
					$("#presetgroup_1 option[value="+ (rmindex-1) +"]").prop("selected", true );
				}
			}
		);
	});	
	$("#preset_run").on("click", function(){
		var runindex = $("#presetgroup_1").val() ;
		$("#presetgroup_1, #preset_remove, #preset_set, #preset_run").prop("disabled", "true");
		$.ajax(
			{
				type : 'get',
				url  : '/cgi-bin/ptz.cgi',
				async: true,
				data : "gotopreset="+ runindex ,
				success: function(msg){
					var tmp= msg.trim().split('\n');
					console.log(tmp);
					if(tmp[0] == "OK"){
						console.log("preset_run_completed");						
					}
					$("#presetgroup_1, #preset_remove, #preset_set, #preset_run").prop("disabled", false);
				}
			}
		);
	});	
	$("#presetour_set").on("click", function(){
		preset_popup = PopupCenter('preset_tour.cgi', 'abc1', 530 ,450 , "preset_popup" );		
		preset_popup.focus();
//		window.open('preset_tour.cgi','abc', 'toolbar=no, location=no, directories=no, status=no, menubar=no, scrollbars=no, resizable=no, width=500, height=400, top=150, left=500');
		
		       
	});	
	$("#presetour_remove").on("click", function(){
		$("#presetgroup_2, #presetour_remove, #presetour_set, #presetour_run").prop("disabled", true );
		var rmindex = $("#presetgroup_2").val() ;	
		$.ajax(
			{
				type : 'get',
				url  : '/cgi-bin/ptz.cgi',
				async: true,
				data : "removepresettour="+ rmindex ,
				success: function(msg){
					var tmp= msg.trim().split('\n');
					console.log(tmp);
					if(tmp[0] == "OK"){
						$("#presetgroup_2 option[value="+ rmindex +"]").remove();							
					}
					$("#presetgroup_2, #presetour_remove, #presetour_set, #presetour_run").prop("disabled", false);
					$("#presetgroup_2 option[value="+ (rmindex-1) +"]").prop("selected", true );
					if( preset_popup != undefined ) preset_popup.del_presettour(rmindex);
					
					if( $("#presetgroup_2 option").length == 0){
						$("#presetgroup_2").append("<option value= -1 >New Preset Tour</option>");			
					}
				}
			}
		);       
	});	
	$("#presetour_run").on("click", function(){
		$("#presetgroup_2, #presetour_remove, #presetour_set, #presetour_run").prop("disabled", true );
		var tourindex = $("#presetgroup_2").val() ;	
		$.ajax(
			{
				type : 'get',
				url  : '/cgi-bin/ptz.cgi',
				async: true,
				data : "runpresettour="+ tourindex ,
				success: function(msg){
					var tmp= msg.trim().split('\n');
					console.log(tmp);
					if(tmp[0] == "OK"){
//						$("#presetgroup_2 option[value="+ tourindex +"]").remove();							
					}
					$("#presetgroup_2, #presetour_remove, #presetour_set, #presetour_run").prop("disabled", false);
					$("#presetgroup_2 option[value="+ tourindex +"]").prop("selected", true );
				}
			}
		);   
	});	

	var mousedown_flag = 0 ;
	
	$(".circle").on("mousedown", function(e){	
		mousedown_flag = 1 ;
	});
	$("html").on("mousemove", function(e){		
		if( mousedown_flag == 1){
			$("body").position().top ;
			$("body").position().left ;			
			
			var cur_X = e.clientX - $("#frame").offset().left -($("#ptz").position().left +106 );
			var cur_Y = e.clientY - $("#frame").offset().top -($("#ptz").position().top + 88) ;

//			console.log("atan:"+ Math.sin( Math.atan2( cur_X , cur_Y ) )*38  ) ;
//			console.log("atan:"+ Math.cos( Math.atan2( cur_X , cur_Y ) )*38  ) ;
	
 			var power = (cur_X*cur_X+cur_Y*cur_Y ) / 1000
			
			if(power > 0.945 ) power = 0.945 ;
			console.log( "power"+ power );
			
			var center_x = $("#ptz").position().left +65 ;
			var center_y = $("#ptz").position().top + 47 ;
			var radian = Math.atan2( cur_X , cur_Y ) ;
			var radius = 15 ;
			var image_offset_X = Math.sin( radian )*radius*power + center_x +"px"; 
			var image_offset_Y = Math.cos( radian )*radius*power + center_y +"px";

			
			$(".joystick").css("left", image_offset_X );
			$(".joystick").css("top", image_offset_Y );
			
			var Remainder ;
			if( cur_X > 100 || cur_X < 100 ){
				Remainder = cur_X % 100  ;
				cur_X = Remainder+1 ;
			}
			if( cur_Y > 100 || cur_Y < 100 ){
				Remainder = cur_Y % 100  ;
				cur_Y = Remainder+1 ;
			}		
 			console.log ( "cur_X:" + Math.round(cur_X)/100 +  "cur_Y:" + Math.round(cur_Y)/1);
 			
 			if( jog_flag == 0){
				var val = "jog&pan_speed=" + Math.round(cur_X)/100 + "&tilt_speed=" +  Math.round(cur_Y)/100;	
				jog_flag = 1 ;
				setTimeout("jog_flag_ctrl()" , 500 ) ;
				_ajax( "move" , val) ;
				
 			}
		}		
	});	
	$("html").on("mouseup", function(e){	
		if( ptzmove_flag == 1) 
		{
		  ptzmove_flag = 0;
			_ajax(cmd_flag, "stop");
		}	  
	  if(mousedown_flag == 1)
	  {
		mousedown_flag = 0 ;
		$(".joystick").css("left", ($("#ptz").position().left +65 )+ "px" );
		$(".joystick").css("top", ($("#ptz").position().top + 47) +"px" );
		
		var val = "jog&pan_speed=0&tilt_speed=0";
		_ajax( "move" , val)
		}
	});	
	$("#set_home_position").on("click", function(e){
		$.ajax(
				{
					type : 'get',
					url  : '/cgi-bin/ptz.cgi',
					async: true,
					data : "sethomeposition=0" ,
					success: function(msg){
						var tmp= msg.trim().split('\n');
						console.log(tmp);
						if(tmp[0] == "OK"){
//							alert("The specified position is set to home position.");
							alert("HOME POSITION SETTING SUCCESS!");
//							$("#presetgroup_2 option[value="+ tourindex +"]").remove();							
						}
//						$("#presetgroup_2, #preset_remove, #preset_set, #preset_run").prop("disabled", false);
//						$("#presetgroup_2 option[value="+ tourindex +"]").prop("selected", true );
					}
			}
		);   
	});	
	$("#run_home_position").on("click", function(e){
		$.ajax(
				{
					type : 'get',
					url  : '/cgi-bin/ptz.cgi',
					async: true,
					data : "gotohomeposition=0" ,
					success: function(msg){
						var tmp= msg.trim().split('\n');
						console.log(tmp);
						if(tmp[0] == "OK"){
						}
					}
			}
		);   
	});	
}
function initEvent(){

	if(userInfo.auth == 1 )
	{
		$("#setup").on("click", function() {			
			if( popupflag == 2 ) popupflag = 1 ;
			else popupflag = 0 ;

			var width, height;
			if(capInfo["oem"] == 2)
			{
				width = 820;
				height = 780;
			} 
			else
			{
				width = 805;
				height = 750;
			}			
			var opener_left = window.top.screenLeft;
			var opener_top = window.top.screenTop;
			if (opener_left<0) opener_left = 0;
			if (opener_top<0) opener_top = 0;
            if (!ctrlAdminTool || (ctrlAdminTool && ctrlAdminTool.closed)){
                ctrlAdminTool = window.open('./admin/setup_main.cgi', 'win_camerasetup', 'resizable=no, scrollbars=no, width=' + width+ 'px, height=' + height +'px left='+ opener_left +', top='+ opener_top +'');
            }
			ctrlAdminTool.focus();		
		});
	}
	$("#logout_btn").on("click", function() {           
		$.ajax({
		   method: 'get',
		   url:'./out.cgi', 
		   data: 'msubmenu=users&action=logout',
		   success: function(req){
		   },
		   error: function(req){
			}
		});
		logout("logout_btn");
	});

	$("#wiper_btn").on("click", function() {  // overview mode wiperaction setting
		$.ajax({
			method: 'get',
			url:'/cgi-bin/ptz.cgi?msubmenu=wiper&action=apply',
			data: '&enabled=1&speed='+ wiperInfo.Speed + '&timeout='+ wiperInfo.Timeout ,
			async: true,
			success: function(req){
			},
			error: function(req){
			}
		});
	});

	$("#washer_btn").on("click", function() {  // overview mode washerroutine setting
		$.ajax({
			method: 'get',
			url:'/cgi-bin/ptz.cgi?msubmenu=washer&action=apply',
			data: '&enabled=1',
			async: true,
			success: function(req){
			},
			error: function(req){
			}
		});
	});

	var wlcal = 1;
	$("#wled_btn").on("click", function() {  // overview mode Whiteled setting
		$.ajax({
			method: 'get',
			url:'/cgi-bin/admin/camera.cgi?msubmenu=camera&action=apply',
			data: '&wlmode=' + wlcal ,
			async: true,
			success: function(req){
				if(wlcal == 1)
					wlcal = 0;
				else wlcal = 1;
			},
			error: function(req){
			}
		});
	});

	$("#change_pass").on("click",function(){
        popup();
    });
	window.onunload = function(){
		if( typeof(ctrlAdminTool) != "undefined")
		ctrlAdminTool.close(); 
		
		if( typeof(ctrlpopup) != "undefined"){	
			try{
				ctrlpopup.close(); 
			}catch(e){
				console.log(e);
			}	
		}
	};
	ptz_event();

	$("#fullScreen").on("click", function(){
		VLCManager.onClickFullScreen();             
	});

	//AUDIOOUT Control.S
         $("#volume_bar_audioout").on("slidechange", function(e, ui){
                 if(audioOutUI == 1)
                 {
                         //Audio out volume control
                         var volume = parseInt(ui.value);
                         var data='';
                         data = "output_volume="+ volume +"&";
                         $.ajax({
                                 method: 'get',
                                 url:'./admin/basic.cgi?msubmenu=audio&action=apply',
                                 data: data,
                                 success: function(req){
                         },
                         error: function(req){
                         }
                         });

                 }else{
                         VLCManager.updateVolume(ui.value);
                 }
         });
         console.log(audioSpeakEnc.output_volume);
     $("#volume_bar_audioout").slider("option", "value", audioSpeakEnc.output_volume);
     $("#volume_bar_audioout").val(audioSpeakEnc.output_volume);
     //AUDIOOUT Control.E

	$("#cb_speaker").click(function(e){
	//	$("#volume_bar").slider(e.target.checked ? "enable":"disable");		
		try{
			if( $("#cb_speaker").prop("checked") == true){
				disabledSlider("volume_bar", 0) ;
				var value = $("#volume_bar").slider("value");
				VLCManager.updateVolume(value);
				//VLCManager.audio.mute = false ;
				VLCManager.toggleMute();
			}
			else {
				disabledSlider("volume_bar", 1) ;
				VLCManager.updateVolume(0);
				//VLCManager.audio.mute = true ;
				VLCManager.toggleMute();
			}		
		}catch(e){
			console.log(e);
		}
	});
	
	$("#volume_bar").on("slidechange", function(e, ui){
		VLCManager.updateVolume(ui.value);             
	});

	$("#volume_bar").slider("option", "value", 50);
		if(capInfo.have_pantilt){
		  $("#pt_speed_bar").slider("option", "value", 5);
		  $("#pt_zoom_bar").slider("option", "value", 4);
		}
		else
		  $("#pt_speed_bar").slider("option", "value", 2);	
	$("#pt_speed_bar").on("slidechange", function(e, ui){
		  if(capInfo.have_pantilt)
		   pantiltspeed = ui.value;
		  else
		  {
		    if(ui.value == 1)
		      pantiltspeed = 1;
		    else if(ui.value == 2)
		      pantiltspeed = 5;
		    else if(ui.value == 3)
		      pantiltspeed = 10;
		  }		
		
		  var val = "pantiltspeed="+pantiltspeed+"&zoomspeed="+zoomspeed ;
		  _ajax("pantiltspeed", val);	
	});
	$("#pt_zoom_bar").on("slidechange", function(e, ui){
		  if(capInfo.have_pantilt)
			  zoomspeed = ui.value;
		  else{
		    if(ui.value == 1)
		    	zoomspeed = 1;
		    else if(ui.value == 2)
		    	zoomspeed = 5;
		    else if(ui.value == 3)
		    	zoomspeed = 10;			  
		  }  
		  var val = "pantiltspeed="+pantiltspeed+"&zoomspeed="+zoomspeed ;
		  _ajax("zoomspeed", val);		
	});	
	$("#cb_relay_out1").click(function(){
		if($("#cb_relay_out1").prop("checked") == 0)
			var val = "msubmenu=output&action=apply&output1=0" ;
		else 
			var val = "msubmenu=output&action=apply&output1=1" ;
		_ajax_io("relay_out",val);
		
	});
	$("#cb_relay_out2").click(function(){
		if($("#cb_relay_out2").prop("checked") == 0)
			var val = "msubmenu=output&action=apply&output2=0" ;
		else 
			var val = "msubmenu=output&action=apply&output2=1" ;
		_ajax_io("relay_out",val);
		
	});	
	if( capInfo.focus_mode == 1) {
		$("#auto").click(function(){
			if( userInfo.auth != 4){ // viewer   
				$("#have_focus").find("*").prop("disabled", true);
				$("#have_iris").find("*").prop("disabled", true);
			    var parent = $(this).parents('.switch');
			    $('#manual',parent).removeClass('color');
			    $("#auto").addClass('color');
			    $('.checkbox',parent).prop('checked', true);
				_ajax("focusmode","auto");
			}
		});
		$("#manual").click(function(){
			if( userInfo.auth != 4){ // viewer   
				$("#have_focus").find("*").prop("disabled", false);
				$("#have_iris").find("*").prop("disabled", true);
			    var parent = $(this).parents('.switch');
			    $('#auto',parent).removeClass('color');
			    $("#manual").addClass('color');
			    $('.checkbox',parent).prop('checked', false);
			    if( userInfo.auth != 4) // viewer  
		    	_ajax("focusmode","manual");
			}
		});	
	}

	$("#lstProfile").change(function(e){
		VLCManager.changeChannel(e.currentTarget.value);
	});
	
	$("#Streming_Type").on("change", function(){
		if($("#Streming_Type").val() == 1){		
//			$("#Buffering ,#Stream_Buffering, #bufferingProfile, #Stream_select, #Stream, #fullScreen" ).css("display","block");	
			$("#vlc_play").css("display","block");	
			$("#jpeg").css("display","none");
			MJ.fi = true ;	
			try{
//				VLCManager.obj.playlist.play(); 
//				VLCManager.doGo(); 
//				VLC  = VLCManager.init("vlc_play", 960, 540, false);
				VLCManager.doGo();
			}
		    catch(err){
				console.log("play");
				$("#vlc_play").css("display","block");	
				$("#jpeg").css("display","none");
				MJ.fi = true ;		
			}	
		}
		else if($("#Streming_Type").val() == 2){
			if ((websocket == 0) || (capInfo["oem"] == 19 && isIE())){
				$("#jpeg,.jpeg_menu").css("display","block");
				$(".vlc_menu").css("display","none");
			}
			else{
				$("#vlc_play").css("display","none");
				//			$("#Buffering ,#Stream_Buffering, #bufferingProfile, #Stream_select, #Stream, #fullScreen" ).css("display","none");
				$("#jpeg").css("display","block");
			}
			try{
					clearInterval(VLCManager.monitorTimerId);
//					VLCManager.doStop();
					VLCManager.obj.playlist.stop();
					VLCManager.obj.playlist.items.clear();
//					VLCManager.obj.playlist.clear();
			}
		    catch(err){
					console.log("error");
			}		
			if( encodeVersion == 1 && VLCManager.user.auth != 1) {
				VLCManager.showEncriptedImage("jpeg", 960, 540);
			} else {
				if(capInfo.camera_type == "fisheye")
				{
					var res_width = VideoInfo[2].resolution.split('x')[0];
					var res_height = VideoInfo[2].resolution.split('x')[1];
					$("#jpeg").css("background-color","#000000");
					MJ.fi = false ;
					MJ.dh = 540 ;
					MJ.dw = MJ.dh * res_width/res_height ;
					MJ.dx = (960/2)-(MJ.dw/2) ;
					MJ.streaming();					
				}
				else if(capInfo.camera_type == "seekware")
				{
					if(corridor_mode)
					{
						var res_width = VideoInfo[2].resolution.split('x')[0];
						var res_height = VideoInfo[2].resolution.split('x')[1];
						//$("#jpeg").css("background-color","#000000");
						MJ.fi = false ;
						MJ.dh = 540 ;
						MJ.dw = MJ.dh * res_height/res_width ;
						MJ.dx = (960/2)-(MJ.dw/2) ;
						MJ.streaming();
					}
					else
					{
						var res_width = VideoInfo[2].resolution.split('x')[0];
						var res_height = VideoInfo[2].resolution.split('x')[1];
						MJ.fi = false;
						MJ.dh = 540;
						MJ.dw = MJ.dh / res_height * res_width;
						MJ.dx = (960-MJ.dw) / 2;
					}
				}
				else if(capInfo.is_proxy_camera){
					;
				}
				else
				{
					if(corridor_mode)
					{
						var res_width = VideoInfo[2].resolution.split('x')[0];
						var res_height = VideoInfo[2].resolution.split('x')[1];
						$("#jpeg").css("background-color","#000000");
						MJ.fi = false ;
						MJ.dh = 540 ;
						MJ.dw = MJ.dh * res_height/res_width ;
						MJ.dx = (960/2)-(MJ.dw/2) ;
						MJ.streaming();
					}
					else
					{
						MJ.fi = false ;
						MJ.dw = 960 ;
						MJ.dh = 540 ;
						MJ.streaming();					
					}
				}
			}
		}
		else if($("#Streming_Type").val() == 3){	
			$("#vlc_play").css("display","none");
			$("#jpeg").css("display","block");	
			MJ.fi = true ;	
			
			try{
				clearInterval(VLCManager.monitorTimerId);
				VLCManager.doStop();				
				//VLCManager.obj.playlist.stop();
				//VLCManager.obj.playlist.items.clear();
			}
		    catch(err){
					console.log("error");
			}	
			var linkAd = location.href;
			var div = linkAd.split(":");
			var addChar= div[1].split("/");
			websocketJpeg = new WebSocket('ws://'+ addChar[2]+ ':7800');
			websocketJpeg.onopen = function (event) {
				websocket_recv();
				send_socket();
			};				
		}
	});
	if(capInfo.have_pantilt){
		initPtz();
	}
	init_event_socket();
	$("#pir_setclear").on("click", function(e){
	        var data= null;
        	data = "msubmenu=wifi_setup&action=pir_clear";
        	$.ajax(
                {
                    type : "get",
                    url  : "/cgi-bin/admin/iot_wifi.cgi",
                    async: true,
                    data : data ,
                    success: function(msg){
                        var tmp= msg.trim().split('\n');
                        console.log(tmp);
                        if(tmp[0] == "OK"){
                        }
                    }
            	}
        	);
	});

	$("#pir_autoclear").on("click", function(e){
	        var data= null;
		if($("#pir_autoclear").prop("checked") == 0)
        		data = "msubmenu=wifi_setup&action=pir_autoclear&autoclear=0";
		else
			data = "msubmenu=wifi_setup&action=pir_autoclear&autoclear=1";
        	$.ajax(
                {
                    type : "get",
                    url  : "/cgi-bin/admin/iot_wifi.cgi",
                    async: true,
                    data : data ,
                    success: function(msg){
                        var tmp= msg.trim().split('\n');
                        console.log(tmp);
                        if(tmp[0] == "OK"){
                        }
                    }
            	}
        	);
	});
	$("#btntestaudio1").on("click", function(e){
                 var data= null;
                 data = "msubmenu=testaudio&action=apply&audio=1";
                 $.ajax(
                 {
                     type : "get",
                     url  : "/cgi-bin/admin/basic.cgi",
                     async: true,
                     data : data ,
                     success: function(msg){
                         var tmp= msg.trim().split('\n');
                         console.log(tmp);
                         if(tmp[0] == "OK"){
                         }
                     }
                 }
                 );
        });
	$("#btntestaudio2").on("click", function(e){
		var data= null;
		data = "msubmenu=testaudio&action=apply&audio=2";
                $.ajax(
                 {
                    type : "get",
                     url  : "/cgi-bin/admin/basic.cgi",
                     async: true,
                     data : data ,
                     success: function(msg){
                         var tmp= msg.trim().split('\n');
                         console.log(tmp);
                         if(tmp[0] == "OK"){
                         }
                     }
                }
                 );
         });
}
function jog_flag_ctrl(){
	jog_flag = 0 ;
}

var ImageBuffer = new ArrayBuffer(100000);
var image_offset = new Uint8Array(ImageBuffer) ;	
var video_timeout ;
var audio_timeout ;

function send_socket(id){
		var tmp_buffer = new ArrayBuffer(1);					
		var tmp_Txbuffer = new Uint8Array(tmp_buffer);	
		
		tmp_Txbuffer[0] =  22 ;

		websocketJpeg.binaryType = 'arraybuffer';
		websocketJpeg.send(tmp_Txbuffer);

		clearTimeout(video_timeout);
//		video_timeout = setTimeout( "send_socket()", 1000/10) ;	
		
}
function websocket_recv(){	
		 websocketJpeg.onmessage = function (event) {	
		 var uInt8Array = new Uint8Array(event.data);	

		 for( var i=0 ; i < uInt8Array.length ; i++){
			  image_offset[i] =  uInt8Array[i] ;
		 }  	
		 MJ.urlCreator = window.URL || window.webkitURL;
		 MJ.imageObj = new Image();
		 var blob = new Blob([image_offset], {type: 'image/jpeg'});	
		 MJ.draw(blob);		
	}
}
function init_audio(){
	buffer = new ArrayBuffer(1);					
	Txbuffer = new Uint8Array(buffer);

	Txbuffer[0] =  23 ;
	websocketMic.binaryType = 'arraybuffer';
	websocketMic.send(Txbuffer);
}
function init_event_socket(){
	var linkAd = location.href;
	var div = linkAd.split(":");
	var addChar= div[1].split("/");
	$("#cb_mic").on("click", function(e){		
		var data='';
        if($("#cb_mic").prop("checked") == 1 ){		
           data = "input_volume=0&";
        }
        else{
           data = "input_volume=5&";
        }

		$.ajax({
			method: 'get',
			url:'./admin/basic.cgi?msubmenu=audio&action=apply', 
			data: data,
			success: function(req){
			},
			error: function(req){
            }
        });
        /*
        if( $("#cb_mic").prop("checked") == 1 ){		
			captureUserMedia(mediaConstraints, onMediaSuccess, onMediaError);
			websocketMic = new WebSocket('ws://'+ addChar[2] +':7800'); //ws://192.168.1.136:7800'
			websocketMic.binaryType = 'arraybuffer';
			
		}else{				
			websocketMic.close();
			onMdieaStop() ;
			audio.remove();
		}
		websocketMic.onopen = function (event) {
			if( $("#cb_mic").prop("checked") == 1 ){
				init_audio();
				clearTimeout(audio_timeout);
				SendMic();
			}		
		};
        */
	});		
}
