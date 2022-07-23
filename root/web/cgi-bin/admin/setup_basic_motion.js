var motion_setup= {};
var canvas, context, rect, activeRect, drag, xmlHttpData, motionColor;
//var menu = "Motion Detection setting";
var checkMotionFlag = 0;
var sensor = { 'width' :  VideoInfo[0].resolution.split('x')[0],
	'height': VideoInfo[0].resolution.split('x')[1] };
var preview_out= { 'width' : 0, 'height' : 288};
if( sensor.width * 9 == sensor.height * 16 ) { 
	preview_out.width  = preview_out.height * 16 / 9;
} 
else if( sensor.width * 3 == sensor.height * 4 ){
	preview_out.width  = preview_out.height * 4 / 3;
}
else if(sensor.width == sensor.height){ 
	preview_out.width  = preview_out.height;
}
else{
	preview_out.width = preview_out.height * (sensor.width / sensor.height); 
}
if(corridor_mode)
{
	preview_out.width = preview_out.width/4*3;
	preview_out.height = preview_out.height/4*3;
	$("#vlc_box").width(preview_out.height).height(preview_out.width);
	$("#display_box").css("margin-left", ($("#display_box").width() - preview_out.height) /2);
  $("#display_box").css("position", "relative");
  $("#display_box").css("padding-top", "10px");
}
else
{
	$("#vlc_box").width(preview_out.width).height(preview_out.height);
	$("#display_box").css("margin-left", ($("#display_box").width() - preview_out.width) /2);
  $("#display_box").css("position", "relative");
  $("#display_box").css("padding-top", "10px");
}
var src = MJ.id;

$(document).ready( function() {
	for (var i=0; i<MotionInfo[src].length ; i++) {
		$("#m" + (i+1) + "_sens").val(MotionInfo[src][i]['sens']);
		$("#m" + (i+1) + "_size").val(MotionInfo[src][i]['size']);
		$("#m" + (i+1) + "_left").val(MotionInfo[src][i]['x']);
		$("#m" + (i+1) + "_right").val(MotionInfo[src][i]['w']+MotionInfo[src][i]['x']);
		$("#m" + (i+1) + "_top").val(MotionInfo[src][i]['y']);
		$("#m" + (i+1) + "_bottom").val(MotionInfo[src][i]['h']+MotionInfo[src][i]['y']);
		//$("#m" + (i+1) + "_type").val(MotionInfo[src][i]['type']);
		$("#m" + (i+1) + "_type").val(MotionInfo[src][i]['enable']);
	}
	onLoadPage();
});

function onLoadPage()
{
	var VLC = false, Motion=false;
	VLCManager.setPlayInfo(userInfo, rtspPort);
	VLC = VLCManager.initPreview("vlc_box", true) 
	init();

	initDisplayMotionStatus("displayMotionStatusArea", capInfo.video_in);
	checkMotion("displayMotionStatus", 1);
}
function init()
{
	setSlider("sensslider",1, 100);
	setSlider("sizeslider",1, 100);

	initUI();
	initValue();
	initEvent();
	//checkMotionSetup();
}
function initUI()
{	
	commonCreateSourceSelectBox("#vin_source");
	if(corridor_mode)
		var canvas = '<canvas id=motionOverlay width="' + preview_out.height  +'" height="' + preview_out.width + '"></canvas>';
	else
		var canvas = '<canvas id=motionOverlay width="' + preview_out.width  +'" height="' + preview_out.height + '"></canvas>';
	$("#overlay_box").append(canvas);

	setUpCanvas();

	$("#motion_threshold_setup").css("display","none");
/*	
	if( capInfo["oem"] == 9) {
		$("#sensitivity_sub").append('<span tkey="setup_threshold"></span>');
	}else{
		$("#sensitivity_sub").append('<span tkey="setup_sensitivity"></span>');
	}
*/
}
function checkMotionSetup()
{
}
function initValue()
{
	activeRect = 1;
	$("#sizeslider").slider( "option", "value", rect[activeRect].size); 
	$("#sensslider").slider( "option", "value", rect[activeRect].sens);
	getRecentValue(); 
}
function initEvent()
{
	menu = getLanguage("setup_motion_config");
	$("#vin_source").off("change").change(function(e){
		src = getVinSourceIndex("#" + e.currentTarget.id);
		MJ.id = src;
        initValue();
        $("#rectsel").val(0);
       setActiveRect(Number($("#rectsel").val()));  
	});
	/* ("Initialize event");
	$("[name=rMotion]").on("click", function(){
		onClickMotionDetection(); 
	});
	$("#sens").on("slidechange", function(){
		var value = $("#sens").slider("value");
		onClickMotionDetectionSensitivity(value);
	}); */
	$("#btSave").on("click", function(){
		onClickSave();
	});
	$("#btRestore").on("click", function(){
		getRecentValue(); 
	});
	/*$("[name=rAlarm]").on("click", function(){
		onClickOSDAlarmIcon();
	});*/
	
	
	$("#motionOverlay").on("mousedown", function(event, ui) {
		mouseDown(event);
	});
	$("#overlay_box").on("mouseup", function(event, ui) {
		mouseUp(event);
	});
	$("#overlay_box").on("mousemove",function(event, ui) {
		mouseMove(event);
	});
  $("#overlay_box").on("mouseleave", function(event, ui) {
    mouseUp(event);
  });
}

function getRecentValue()
{
	for (var i=0; i<4; i++) {
		$("#m" + (i+1) + "_sens").val(MotionInfo[src][i]['sens']);
		$("#m" + (i+1) + "_size").val(MotionInfo[src][i]['size']);
		$("#m" + (i+1) + "_left").val(MotionInfo[src][i]['x']);
		$("#m" + (i+1) + "_right").val(MotionInfo[src][i]['w']+MotionInfo[src][i]['x']);
		$("#m" + (i+1) + "_top").val(MotionInfo[src][i]['y']);
		$("#m" + (i+1) + "_bottom").val(MotionInfo[src][i]['h']+MotionInfo[src][i]['y']);
		$("#m" + (i+1) + "_type").val(MotionInfo[src][i]['enable']);
	}
	load();
}

/*
function onClickMotionDetection()
{
	var value;
	var param;
	value = $("[name=rMotion]:checked").val();
	param = "msubmenu=motion&action=apply&enable=" + value;

	$.ajax({
		type : 'get',
		url  : '/cgi-bin/admin/event.cgi',
		data : param,
		cache	: false,
		success : function(args) { 
			if(args != "NG" && value == 1)
				checkMotionFlag = checkAlarm();
			else 
			{
				clearTimeout(checkMotionFlag);
				checkMotionFlag = 0;
				$("#displayMotionStatus").removeClass("alarm_on");
				$("#displayMotionStatus").addClass("alarm_off");
				$("#displayMotionStatus").text("off");   
			}

		},
		//error 	: function(args) { alert("error"); },
	});

}
function onClickMotionDetectionSensitivity(val)
{
	$("#sesn_STR").text(val);
	$.ajax({
		type : 'get',
		url  : '/cgi-bin/admin/event.cgi',
		data : "msubmenu=motion&action=apply" + "&sensitivity=" + val,
		cache	: false,
		success : function(args) {
			//console.log(args);
		},
	});

}
*/

function onSuccessApply(msg)
{

    var tmp= msg.trim().split('\n');
    console.log(tmp);
    var response = tmp[0];
    if(response == "OK")
    {		
        settingSuccess(menu, null);
    }
    else 
    {
        settingFail(menu,getLanguage(tmp[1]));
    }
    refreshMenuContent();
}
function onClickSave()
{
	var param = "msubmenu=motion&action=apply&";

	if(corridor_mode)
	{
		for (var i=0; i<4; i++) {
			param += "x" + i + "=" + Math.round(rect[i+1].startX * 100 / preview_out.height) + "&";
			param += "y" + i + "=" + Math.round(rect[i+1].startY * 100 / preview_out.width) + "&";
			param += "w" + i + "=" + Math.round(rect[i+1].w * 100 / preview_out.height) + "&";
			param += "h" + i + "=" + Math.round(rect[i+1].h * 100 / preview_out.width) + "&";
			param += "enable" + i + "=" + rect[i+1].type + "&";
			param += "size" + i + "=" + rect[i+1].size + "&";
			param += "sens" + i + "=" + rect[i+1].sens + "&";
		}
	}
	else
	{
		for (var i=0; i<4; i++) {
			param += "x" + i + "=" + Math.round(rect[i+1].startX * 100 / preview_out.width) + "&";
			param += "y" + i + "=" + Math.round(rect[i+1].startY * 100 / preview_out.height) + "&";
			param += "w" + i + "=" + Math.round(rect[i+1].w * 100 / preview_out.width) + "&";
			param += "h" + i + "=" + Math.round(rect[i+1].h * 100 / preview_out.height) + "&";
			param += "enable" + i + "=" + rect[i+1].type + "&";
			param += "size" + i + "=" + rect[i+1].size + "&";
			param += "sens" + i + "=" + rect[i+1].sens + "&";
		}
	}
	param += "source=" + src + "&";

	$.ajax({
		type : 'get',
		url  : '/cgi-bin/admin/event.cgi',
		data : param,
		cache	: false,
//		success : function(args) {
//			var pop_msg = getLanguage("msg_motion_success");
//			settingSuccess(menu, pop_msg );
//			refreshMenuContent();
//		},
        success:onSuccessApply,
		error 	: function(args) {
			settingFail(menu, null);
		},
	});

	return;
}

function relMouseCoords(event)
{
	var totalOffsetX = 0;
	var totalOffsetY = 0;
	var canvasX = 0;
	var canvasY = 0;
	var currentElement = this;

	do{
		totalOffsetX += currentElement.offsetLeft;
		totalOffsetY += currentElement.offsetTop;
	}
	while(currentElement = currentElement.offsetParent)

		canvasX = event.pageX - totalOffsetX;
	canvasY = event.pageY - totalOffsetY;

	return {x:canvasX, y:canvasY}
} HTMLCanvasElement.prototype.relMouseCoords = relMouseCoords;

function load()
{
// 	plugin.play("rtsp://" + document.domain + "/stream1");

    for(var i=1,len=rect.length; value=rect[i], i<len; i++) {
		if(typeof($("#m" + i + "_right")[0].value) != "undefined")
		{
			var _left = $("#m" + i + "_left")[0].value;
			var _right = $("#m" + i + "_right")[0].value;
			var _bottom = $("#m" + i + "_bottom")[0].value;
			var _top = $("#m" + i + "_top")[0].value;

			if($("#m" + i + "_right")[0].value<0)
				_right = 256 + Number($("#m" + i + "_right")[0].value);
			if($("#m" + i + "_left")[0].value<0)
				_left = 256 + Number($("#m" + i + "_left")[0].value);
			if($("#m" + i + "_bottom")[0].value<0)
				_bottom = 256 + Number($("#m" + i + "_bottom")[0].value);
			if($("#m" + i + "_top")[0].value<0)
				_top =256+ Number($("#m" + i + "_top")[0].value);

			if(corridor_mode)
			{
				rect[i].startX = Math.round(_left * preview_out.height / 100);
				rect[i].startY = Math.round(_top * preview_out.width / 100);
				rect[i].w = Math.round((_right - _left) * preview_out.height / 100);
				rect[i].h = Math.round(( _bottom - _top) * preview_out.width / 100);
			}
			else
			{
				rect[i].startX = Math.round(_left * preview_out.width / 100);
				rect[i].startY = Math.round(_top * preview_out.height / 100);
				rect[i].w = Math.round((_right - _left) * preview_out.width / 100);
				rect[i].h = Math.round(( _bottom - _top) * preview_out.height / 100);
			}
			rect[i].type = $("#m" + i + "_type")[0].value;
			rect[i].size = $("#m" + i + "_size")[0].value;
			rect[i].sens = $("#m" + i + "_sens")[0].value;
		}
	}
    setActiveRect(Number($("#rectsel").val()));
}

function setUpCanvas()
{
	canvas = $("#motionOverlay")[0];
	context = canvas.getContext('2d');
	rect = new Array({}, {},{}, {}, {});
	motionColor = "blue";
	drag = false;
	$(function() {$( "#sizeslider" ).slider({slide: function(event, ui) {document.getElementById('sizelabel').innerHTML = ui.value; rect[0].size = ui.value;}});});
	$(function() {$( "#sizeslider" ).slider({stop: function(event, ui) {apply();}});});
	$(function() {$( "#sensslider" ).slider({slide: function(event, ui) {document.getElementById('senslabel').innerHTML = ui.value; rect[0].sens = ui.value;}});});
	$(function() {$( "#sensslider" ).slider({stop: function(event, ui) {apply();}});});
	
	$( "#sizeslider" ).next().on("click", function(){		
		var value = ($( "#sizeslider" ).slider("value"));		
		$( "#sizeslider" ).next().next().text( value );
	});
	$( "#sizeslider" ).prev().on("click", function(){
		var value = ($( "#sizeslider" ).slider("value"));
		$( "#sizeslider" ).next().next().text( value );
	});
	$( "#sensslider" ).next().on("click", function(){
		var value = ($( "#sensslider" ).slider("value"));
		rect[0].sens = value;
		apply();
		$( "#sensslider" ).next().next().text( value );
	});
	$( "#sensslider" ).prev().on("click", function(){
		var value = ($( "#sensslider" ).slider("value"));
		rect[0].sens = value;
		apply();
		$( "#sensslider" ).next().next().text( value );
	});

//	canvas.width = plugin.width;
//	canvas.height = plugin.height;

    rect[0].type = 0;
}

function mouseDown(e)
{
  if(!window.isIE_fix()) {
    canvas.requestPointerLock = canvas.requestPointerLock || canvas.mozRequestPointerLock;
    canvas.requestPointerLock();
  }

	coords = canvas.relMouseCoords(e);
	rect[0].startX = coords.x;
	rect[0].startY = coords.y;
  rect[0].w = 0;
  rect[0].h = 0;
	drag = true;
}

function mouseUp(e)
{
	drag = false;
  $("#overlay_box").css("border", "");
	if(rect[0].w < 0)
	{
		rect[0].startX += rect[0].w;
		rect[0].w *= -1;
	}
	if(rect[0].h < 0)
	{
		rect[0].startY += rect[0].h
			rect[0].h *= -1;
	}
	apply();

  if(!window.isIE_fix()) {
    document.exitPointerLock = document.exitPointerLock || document.mozExitPointerLock;
    document.exitPointerLock();
  }

}

function mouseMove(e)
{
	coords = canvas.relMouseCoords(e);
	if (drag) 
	{
		if(!window.isIE_fix()) {
      rect[0].w += e.originalEvent.movementX;
      rect[0].h += e.originalEvent.movementY;
      
      if((rect[0].w + rect[0].startX) >= canvas.width) {
        rect[0].w = canvas.width - rect[0].startX;
      }
      if((rect[0].w + rect[0].startX) <= 0) {
        rect[0].w = rect[0].startX * -1;
      }
      if((rect[0].h + rect[0].startY) >= canvas.height) {
        rect[0].h = canvas.height - rect[0].startY;
      }
      if((rect[0].h + rect[0].startY) <= 0) {
        rect[0].h = rect[0].startY * -1;
      }
    } else {
      $("#overlay_box").css("border", "1px solid #B2B2B2");
      if(coords.x >= canvas.width) coords.x = canvas.width;
      if(coords.x <= 0) coords.x = 0;
      if(coords.y >= canvas.height) coords.y = canvas.height;
      if(coords.y <= 0) coords.y = 0;
      rect[0].w = coords.x - rect[0].startX;
		  rect[0].h = coords.y - rect[0].startY;
    }

    draw();
	}
}
function setMotion(index, value)
{
	if (rect) {
		rect[index+1].motion = value;
		draw();
	}
}
function setMotionColor(color) {motionColor = color;}
function draw() 
{ 
	context.clearRect(0,0,canvas.width,canvas.height);
	for(var i=1,len=rect.length; value=rect[i], i<len; i++)
	{
		if(typeof rect[i].w !== 'undefined' && rect[i].type != 0 && (activeRect != i || !drag))
		{
			if(typeof rect[i].motion == 'undefined' || rect[i].motion == 0)
			{
				setFillType(rect[i].type);
				context.fillRect(rect[i].startX, rect[i].startY, rect[i].w, rect[i].h);
			}
			else
			{
				context.beginPath();
				context.rect(rect[i].startX, rect[i].startY, rect[i].w, rect[i].h);
				setFillType(rect[i].type);
				context.lineWidth = 2;
				context.strokeStyle = motionColor;
				context.stroke();
				context.fillRect(rect[i].startX, rect[i].startY, rect[i].w, rect[i].h);
			}
		}
	}
	if(typeof rect[0].w != 'undefined' && (typeof rect[activeRect].motion == 'undefined' || rect[activeRect].motion != 1))
	{
		context.beginPath();
		context.rect(rect[0].startX, rect[0].startY, rect[0].w, rect[0].h);
		setFillType(rect[0].type);
		context.lineWidth = 2;
		context.strokeStyle = 'yellow';
		context.stroke();
	}
}

function setActiveRect(index)
{
	activeRect = index+1;
    sizelabel = document.getElementById('sizelabel');
    senslabel = document.getElementById('senslabel');

	if(typeof rect[activeRect].w !== 'undefined')
	{
		rect[0].startX = rect[activeRect].startX;
		rect[0].startY = rect[activeRect].startY;
		rect[0].w = rect[activeRect].w;
		rect[0].h = rect[activeRect].h;
		rect[0].size = rect[activeRect].size;
		rect[0].sens = rect[activeRect].sens;
		setRectType(rect[activeRect].type);
		setFieldsDisabled(rect[activeRect].type == 0);
		document.getElementById("typesel").selectedIndex = rect[activeRect].type;
		$("#sizeslider").slider( "option", "value", rect[activeRect].size); 
		$("#sensslider").slider( "option", "value", rect[activeRect].sens);
		sizelabel.innerHTML = rect[activeRect].size;
		senslabel.innerHTML = rect[activeRect].sens;
	}	
	else
	{		
		rect[0] = {};
		rect[0].type = 0;
		rect[0].size = 50;
		rect[0].sens = 50;
		setFieldsDisabled(true);
		document.getElementById("typesel").selectedIndex = 0;
		$("#sizeslider").slider( "option", "value", 50);
		$("#sensslider").slider( "option", "value", 50);
		sizelabel.innerHTML = 50;
		senslabel.innerHTML = 50;
	}
	draw();
}

function setFieldsDisabled(value)
{
 //   $("#sizeslider").slider("option", "disabled", value);
 //   $("#sensslider").slider("option", "disabled", value);
	  disabledSlider("sizeslider", value) ;
	  disabledSlider("sensslider", value) ;
 }

function apply()
{
	var width,heigt;
	if(corridor_mode)
	{
		width 	= preview_out.height;
 		height	= preview_out.width;
	}
	else
	{
		width 	= preview_out.width;
 		height	= preview_out.height;
	}
	typeindex = document.getElementById("typesel").selectedIndex;
	if(typeof rect[0].w !== 'undefined')
	{
		rect[activeRect].startX = rect[0].startX;
		$("#m" + (activeRect-1) + "_left")[0].value = Math.round(rect[0].startX / width * 10000);   
		rect[activeRect].startY = rect[0].startY;
		$("#m" + (activeRect-1) + "_top")[0].value =  Math.round(rect[0].startY / height * 10000); 
		rect[activeRect].w = rect[0].w;
		$("#m" + (activeRect-1) + "_right")[0].value =  Math.round((rect[0].startX + rect[0].w) / width * 10000); 
		rect[activeRect].h = rect[0].h;
		$("#m" + (activeRect-1) + "_bottom")[0].value =  Math.round((rect[0].startY + rect[0].h) / height * 10000); 
		rect[activeRect].type = rect[0].type;
		$("#m" + (activeRect-1) + "_type")[0].value = rect[0].type; 
		rect[activeRect].size = rect[0].size;
		$("#m" + (activeRect-1) + "_size")[0].value = rect[0].size;
		rect[activeRect].sens = rect[0].sens;		
		$("#m" + (activeRect-1) + "_sens")[0].value = rect[0].sens;		
	}
	draw();
}

function setRectType(index)
{
	setFillType(index);
	rect[0].type = index;
	setFieldsDisabled(index == 0);
	apply();
}
function setFillType(index) {
//	context.fillStyle = ((index == 0) ? "rgba(192,192,192, 0.3)" : ((index == 1) ? "rgba(0,0,255, 0.3)" : "rgba(255,0,0, 0.3)"));
	context.fillStyle = ((index == 0) ? "rgba(192,192,192, 0.3)" : ((index == 1) ? "rgba(255,0,0, 0.3)" : "rgba(0,0,255, 0.3)"));
}
