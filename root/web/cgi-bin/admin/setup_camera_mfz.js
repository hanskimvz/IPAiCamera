var VLCManager = new VLC("image_box", capInfo, VideoInputInfo, VideoInfo,"lstProfile");
if(typeof(VLCManager) == undefined ){
	console.log("VLCManager initialize fail");
	VLCManager = null;
}
function onLoadPage() {
	if(typeof(VLCManager) == undefined ){
		console.log("VLCManager initialize fail");
		VLCManager = null;
	}
	getJson();
	initLanguage();
	VLCManager.setPlayInfo(userInfo, rtspPort);
	var VLC  = VLCManager.init(1);
	if(VLC && isIE()){
		VLCManager.doGo();
	}
	else {
        VLCManager.setPlayInfo(userInfo, rtspPort);
        VLC = VLCManager.initPreview("image_box", true);

	}
  

	initUI();
	initEvent();

	$("#zoom_value1").text(2);
	$("#zoom_value2").text(2);
	$("#zoom_value3").text(2);
	$("#zoom_value4").text(2);
	$("#pt_zoom_bar1").slider("option", "value", 2)
	$("#pt_zoom_bar2").slider("option", "value", 2)
	$("#pt_zoom_bar3").slider("option", "value", 2)
	$("#pt_zoom_bar4").slider("option", "value", 2)
	_ajax("zoom_value1", 2);	  
	_ajax("zoom_value2", 2);	  
	_ajax("zoom_value3", 2);	  
	_ajax("zoom_value4", 2);	

	initValue();
}
function initUI(){
	var obj = '',
	i = 0;
	if(capInfo.camera_type == "PROXY_DUAL_CLIENT"){
		$("#mfz_body").css("width","800px");
		$(".multi-view-oneline").css("width","100%");
//		$(".multi-view-oneline").css("height","100%");
		for(var i = 0 ;i<capInfo.video_in;i++){
			$("#mfz_body #jpeg"+i).css("margin-left","2%");
			$("#mfz_body #jpeg"+i).css("margin-right","2%");
			$("#mfz_body #jpeg"+i).css("width","45%");
			$("#mfz_body #jpeg"+i).css("height","100%");
			$("#mfz_body #video"+i).css("margin-left","2%");
			$("#mfz_body #video"+i).css("margin-right","2%");
			$("#mfz_body #video"+i).css("width","45%");
			$("#mfz_body #video"+i).css("height","100%");
		}
	}
	else{
		$("#mfz_body").css("width","1330px");
		
	}
	obj += '<div id="ptz">';
	for( i=0 ; i < capInfo.video_in ; i++) {
		
	if(capInfo.camera_type == "PROXY_DUAL_CLIENT"){
		obj += '<div style="width:50%; display:inline-block;text-align:center; margin-top:18px">';
	}else{
		obj += '<div style="width:25%; display:inline-block;text-align:center; margin-top:18px">';
	}
		obj += '<table style="width:100%;text-align:center;" id="have_mfz';
		obj += Number(i+1) + '">';
		obj += '<tr>';
		obj += '<td class="td_zoom">';
			obj += '<div style="display:inline-block;text-align:center;" class="ptz_small2" id="have_zoom';
			obj += Number(i+1) + '">';
			obj += '<button id="m_zoom' + Number(i+1);
			obj += '"class="button extrasmall3" value="out">-';
			obj += '</button>';
			obj += '<button id="p_zoom' + Number(i+1);
			obj += '"class="button extrasmall3" value="in">+';
			obj += '</button>';
			obj += '</div>';
		obj += '</td>';
		obj += '<td class="td_iris">';
			obj += '<div style="display:inline-block;text-align:center;" class="ptz_small2" id="have_iris';
			obj += Number(i+1) + '">';
			obj += '<button id="m_iris' + Number(i+1);
			obj += '"class="button extrasmall3" value="close">-';
			obj += '</button>';
			obj += '<button id="p_iris' + Number(i+1);
			obj += '"class="button extrasmall3" value="open">+';
			obj += '</button>';
			obj += '</div>';
		obj += '</td>';
		obj += '<td class="td_focus">';
			obj += '<div style="display:inline-block;text-align:center;" class="ptz_small2" id="have_focus';
			obj += Number(i+1) + '">';
			obj += '<button id="m_focus' + Number(i+1);
			obj += '"class="button extrasmall3" value="far">-';
			obj += '</button>';
			obj += '<button id="p_focus' + Number(i+1);
			obj += '"class="button extrasmall3" value="near">+';
			obj += '</button>';
			obj += '</div>';
		obj += '</td>';
		obj += '</tr>';


		obj += '<tr>';
		obj += '<td class="td_zoom">';
			obj += '<label class="title subtitle">'
			obj += getLanguage("main_zoom")+'</label>';
		obj += '</td>';
		obj += '<td class="td_iris">';
			obj += '<label class="title subtitle">'
			obj += getLanguage("main_iris")+'</label>';
		obj += '</td>';
		obj += '<td class="td_focus">';
			obj += '<label class="title subtitle">'
			obj += getLanguage("main_focus")+'</label>';
		obj += '</td>';
		obj += '</tr>';


		obj += '<tr>';
		obj += '<td colspan="3">';
			obj += '<div id="have_zoom_speed';
			obj += Number(i+1) + '" class="slider_box" >';
			obj += '<label class="title subtitle"><span tkey=""></span></label>';
			obj += '<div id="pt_zoom_bar';
			obj += Number(i+1) + '"></div>';
			obj += '<label id="zoom_value';
			obj += Number(i+1) + '">1</label></div>';
		obj += '</td>';
		obj += '</tr>';


		obj += '<tr>';
			obj += '<td colspan="3">';
			obj += '<div><label class="title subtitle" style="margin-top:0px;"><span tkey="Zoom_Speed">zoom speed</span></label></div>';
		obj += '</td>';
		obj += '</tr>';


		obj += '<tr>';
		obj += '<td colspan="3">';
			obj += '<div style="display:inline-block;text-align:center;" id="focusmode';
			obj += Number(i+1) + '" class="field switch button long_180">';
			obj += '<label class="cb-enable"><span id="auto';
			obj += Number(i+1) + '" tkey="setup_auto">Auto</span></label>';
			obj += '<label class="cb-disable" ><span id="manual';
			obj += Number(i+1) + '" tkey="main_manual">Manual</span></label>';
			obj += '<input type="checkbox" id="checkbox';
			obj += Number(i+1) + '" class="checkbox" name="field2" autocomplete="off" hidden></input>';
			obj += '</div>';
		obj += '</td>';
		obj += '</tr>';


		obj += '</table>';
		obj += '</div>';
	}
	obj += '</div>';
	$("#image_box").after(obj);
	


	setSlider("pt_speed_bar1", 1, 3);
	setSlider("pt_speed_bar2", 1, 3);
	setSlider("pt_speed_bar3", 1, 3);
	setSlider("pt_speed_bar4", 1, 3);
	setSlider("pt_zoom_bar1", 1, 3);
	setSlider("pt_zoom_bar2", 1, 3);
	setSlider("pt_zoom_bar3", 1, 3);
	setSlider("pt_zoom_bar4", 1, 3);
	
    $(".td_iris").css("display",capInfo.have_iris?"block":"none");
	$("#image_box").css("text-align","center");
    var i =0;
	for(i=0;i<4;i++){ 
			if( focus_mode & (1<<i)){
				$("#have_focus"+(i+1)).find("*").prop("disabled", true);
				$('#manual'+(i+1),parent).removeClass('color');
				$("#auto"+(i+1)).addClass('color');
			}
			else{
				$("#have_focus"+(i+1)).find("*").prop("disabled", false);
				$('#auto'+(i+1),parent).removeClass('color');
				$("#manual"+(i+1)).addClass('color');
			}
	}

}

var cmd_flag ;
function initEvent(){

	//zoom
	$("#m_zoom1,#p_zoom1").mousedown(function(e)
	{
		mousedown("zoom1", $(this).val());
		cmd_flag = "zoom1";	
		ptzmove_flag = 1;
	});
	$("#m_zoom2,#p_zoom2").mousedown(function(e)
	{
		mousedown("zoom2", $(this).val());
		cmd_flag = "zoom2";	
		ptzmove_flag = 1;
	});
	$("#m_zoom3,#p_zoom3").mousedown(function(e)
	{
		mousedown("zoom3", $(this).val());
		cmd_flag = "zoom3";	
		ptzmove_flag = 1;
	});
	$("#m_zoom4,#p_zoom4").mousedown(function(e)
	{
		mousedown("zoom4", $(this).val());
		cmd_flag = "zoom4";	
		ptzmove_flag = 1;
	});			
	//iris
	$("#m_iris1,#p_iris1").mousedown(function(e)
	{
		mousedown("iris1", $(this).val());
		cmd_flag = "iris1";	
		ptzmove_flag = 1;
	});
	$("#m_iris2,#p_iris2").mousedown(function(e)
	{
		mousedown("iris2", $(this).val());
		cmd_flag = "iris2";	
		ptzmove_flag = 1;
	});
	$("#m_iris3,#p_iris3").mousedown(function(e)
	{
		mousedown("iris3", $(this).val());
		cmd_flag = "iris3";	
		ptzmove_flag = 1;
	});
	$("#m_iris4,#p_iris4").mousedown(function(e)
	{
		mousedown("iris4", $(this).val());
		cmd_flag = "iris4";	
		ptzmove_flag = 1;
	});
	//foucus
	$("#m_focus1,#p_focus1").mousedown(function(e)
	{
		mousedown("focus1", $(this).val());
		cmd_flag = "focus1";	
		ptzmove_flag = 1;
	});
	$("#m_focus2,#p_focus2").mousedown(function(e)
	{
		mousedown("focus2", $(this).val());
		cmd_flag = "focus2";	
		ptzmove_flag = 1;
	});
	$("#m_focus3,#p_focus3").mousedown(function(e)
	{
		mousedown("focus3", $(this).val());
		cmd_flag = "focus3";	
		ptzmove_flag = 1;
	});
	$("#m_focus4,#p_focus4").mousedown(function(e)
	{
		mousedown("focus4", $(this).val());
		cmd_flag = "focus4";	
		ptzmove_flag = 1;
	});


	$("html").on("mouseup", function(e){	
		if( ptzmove_flag == 1) 
		{
		  ptzmove_flag = 0;
			_ajax(cmd_flag, "stop");
		}	  
	});	

	$("#pt_zoom_bar1").on("slidechange", function(e, ui){
		if(ui.value == 1)
			zoomspeed = 1;
		else if(ui.value == 2)
			zoomspeed = 5;
		else if(ui.value == 3)
			zoomspeed = 10;			  
	var val = "pantiltspeed=0"+"&zoomspeed="+zoomspeed ;
	_ajax("zoomspeed1", val);		
	});	
	$("#pt_zoom_bar2").on("slidechange", function(e, ui){
		if(ui.value == 1)
			zoomspeed = 1;
		else if(ui.value == 2)
			zoomspeed = 5;
		else if(ui.value == 3)
			zoomspeed = 10;			  
		var val = "pantiltspeed=0"+"&zoomspeed="+zoomspeed ;
		_ajax("zoomspeed2", val);		
	});
	$("#pt_zoom_bar3").on("slidechange", function(e, ui){
		if(ui.value == 1)
			zoomspeed = 1;
		else if(ui.value == 2)
			zoomspeed = 5;
		else if(ui.value == 3)
			zoomspeed = 10;			  
		var val = "pantiltspeed=0"+"&zoomspeed="+zoomspeed ;
		_ajax("zoomspeed3", val);		
	});
	$("#pt_zoom_bar4").on("slidechange", function(e, ui){
		if(ui.value == 1)
			zoomspeed = 1;
		else if(ui.value == 2)
			zoomspeed = 5;
		else if(ui.value == 3)
			zoomspeed = 10;			  
		var val = "pantiltspeed=0"+"&zoomspeed="+zoomspeed ;
		_ajax("zoomspeed4", val);		
	});


	$("#ptz").mouseup(function() {		
		ptzmove_flag = 0;
		  if( cmd_flag != "none") 
		  {
			  _ajax(cmd_flag, "stop");
		  }
		  
		  cmd_flag = "none";
	  });


	if( capInfo.focus_mode == 1) {
		$("#auto1").click(function(){
			if( userInfo.auth != 4){ // viewer   
				$("#have_focus1").find("*").prop("disabled", true);
				$("#have_iris1").find("*").prop("disabled", true);
				var parent = $(this).parents('.switch');
				$('#manual1',parent).removeClass('color');
				$("#auto1").addClass('color');
				$('.checkbox1',parent).prop('checked', true);
				_ajax("focusmode1","auto");
			}
		});
		$("#auto2").click(function(){
			if( userInfo.auth != 4){ // viewer   
				$("#have_focus2").find("*").prop("disabled", true);
				$("#have_iris2").find("*").prop("disabled", true);
				var parent = $(this).parents('.switch');
				$('#manual2',parent).removeClass('color');
				$("#auto2").addClass('color');
				$('.checkbox2',parent).prop('checked', true);
				_ajax("focusmode2","auto");
			}
		});
		$("#auto3").click(function(){
			if( userInfo.auth != 4){ // viewer   
				$("#have_focus3").find("*").prop("disabled", true);
				$("#have_iris3").find("*").prop("disabled", true);
				var parent = $(this).parents('.switch');
				$('#manual3',parent).removeClass('color');
				$("#auto3").addClass('color');
				$('.checkbox3',parent).prop('checked', true);
				_ajax("focusmode3","auto");
			}
		});
		$("#auto4").click(function(){
			if( userInfo.auth != 4){ // viewer   
				$("#have_focus4").find("*").prop("disabled", true);
				$("#have_iris4").find("*").prop("disabled", true);
				var parent = $(this).parents('.switch');
				$('#manual4',parent).removeClass('color');
				$("#auto4").addClass('color');
				$('.checkbox4',parent).prop('checked', true);
				_ajax("focusmode4","auto");
			}
		});
		


		$("#manual1").click(function(){
			if( userInfo.auth != 4){ // viewer   
				$("#have_zoom1").find("*").prop("disabled", false);
				$("#have_focus1").find("*").prop("disabled", false);
				$("#have_iris1").find("*").prop("disabled", true);
				var parent = $(this).parents('.switch');
				$('#auto1',parent).removeClass('color');
				$("#manual1").addClass('color');
				$('.checkbox1',parent).prop('checked', false);
				if( userInfo.auth != 4) // viewer  
				_ajax("focusmode1","manual");
			}
		});	
		$("#manual2").click(function(){
			if( userInfo.auth != 4){ // viewer   
				$("#have_zoom2").find("*").prop("disabled", false);
				$("#have_focus2").find("*").prop("disabled", false);
				$("#have_iris2").find("*").prop("disabled", true);
				var parent = $(this).parents('.switch');
				$('#auto2',parent).removeClass('color');
				$("#manual2").addClass('color');
				$('.checkbox2',parent).prop('checked', false);
				if( userInfo.auth != 4) // viewer  
				_ajax("focusmode2","manual");
			}
		});	
		$("#manual3").click(function(){
			if( userInfo.auth != 4){ // viewer   
				$("#have_zoom3").find("*").prop("disabled", false);
				$("#have_focus3").find("*").prop("disabled", false);
				$("#have_iris3").find("*").prop("disabled", true);
				var parent = $(this).parents('.switch');
				$('#auto3',parent).removeClass('color');
				$("#manual3").addClass('color');
				$('.checkbox3',parent).prop('checked', false);
				if( userInfo.auth != 4) // viewer  
				_ajax("focusmode3","manual");
			}
		});	
		$("#manual4").click(function(){
			if( userInfo.auth != 4){ // viewer   
				$("#have_zoom4").find("*").prop("disabled", false);
				$("#have_focus4").find("*").prop("disabled", false);
				$("#have_iris4").find("*").prop("disabled", true);
				var parent = $(this).parents('.switch');
				$('#auto4',parent).removeClass('color');
				$("#manual4").addClass('color');
				$('.checkbox4',parent).prop('checked', false);
				if( userInfo.auth != 4) // viewer  
				_ajax("focusmode4","manual");
			}
		});	
	}

}

var ptzmove_flag = 0 ;
function mousedown(cmd , val){		
	var num= 0 ;
	num++;	
	if(num == 1) 
	{
		_ajax(cmd , val);
	//	Pan_Interval(cmd, val);
	}	
}
function _ajax(src, types, dir) {
	var params = {
		msubmenu: "alignment",
		source : src,
		direction : dir,
		type : types,
	};
	$.ajax({
		type:"get",
		url: "/cgi-bin/admin/camera.cgi",
		data: params,
		success: function(resp){
			console.log(resp);
		}, 
		error: function(resp){
			console.log(resp);
		}
	});
}
//EVENT
function _ajax(cmd , val){
    var length = cmd.length;
    var srcidx = cmd.substr(length-1,1);
    cmd = cmd.slice(0,length-1);
	var parameter;
	if( cmd == "zoomspeed"  )
		parameter = val + "&" + "source" + "="+ srcidx;	
	else
		parameter = cmd+ "=" + val + "&" + "source" + "="+ srcidx;	
	$.ajax(
		{
			type : 'get',
			url  : '/cgi-bin/ptz.cgi',
			async: true,
			data : parameter 
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

function initValue(){

}

$(document).ready( function(){
	onLoadPage();
});
