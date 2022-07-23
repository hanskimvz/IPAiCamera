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
	$("#display_box").css("padding-left", ($("#display_box").width() - preview_out.height) /2);
}
else
{
	$("#vlc_box").width(preview_out.width).height(preview_out.height);
	$("#display_box").css("padding-left", ($("#display_box").width() - preview_out.width) /2);
}
var src = 0;

$(document).ready( function() {
	for (var i=0; i<TemperatureInfo[src].length ; i++) {
		$("#m" + (i+1) + "_temperature").val(TemperatureInfo[src][i]['temperature'] - 10);
		$("#m" + (i+1) + "_filteringtime").val(TemperatureInfo[src][i]['filteringtime']);
		$("#m" + (i+1) + "_tolerance").val(TemperatureInfo[src][i]['tolerance']);
		$("#m" + (i+1) + "_left").val(TemperatureInfo[src][i]['x']);
		$("#m" + (i+1) + "_right").val(TemperatureInfo[src][i]['w']+TemperatureInfo[src][i]['x']);
		$("#m" + (i+1) + "_top").val(TemperatureInfo[src][i]['y']);
		$("#m" + (i+1) + "_bottom").val(TemperatureInfo[src][i]['h']+TemperatureInfo[src][i]['y']);
		//$("#m" + (i+1) + "_type").val(TemperatureInfo[src][i]['type']);
		$("#m" + (i+1) + "_type").val(TemperatureInfo[src][i]['enable']);
		$("#m" + (i+1) + "_rule").val(TemperatureInfo[src][i]['rule']);
	}
	console.log("ready");
	onLoadPage();
});

function onLoadPage()
{
	var VLC = false, Motion=false;
	VLCManager.setPlayInfo(userInfo, rtspPort);
	VLC = VLCManager.initPreview("vlc_box", true) 
	init();

	//initDisplayMotionStatus("displayMotionStatusArea", capInfo.video_in);
	//checkMotion("displayMotionStatus", 1);
}
function init()
{
	setSlider("sensslider",-10, 150);
	setSlider("sizeslider",0, 10);
	setSlider("toleranceslider",0, 3);

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

	//$("#motion_threshold_setup").css("display","none");
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
	$("#sensslider").slider( "option", "value", rect[activeRect].temperature);
	$("#sizeslider").slider( "option", "value", rect[activeRect].filteringtime); 
	$("#toleranceslider").slider( "option", "value", rect[activeRect].tolerance);
	getRecentValue(); 
}
function initEvent()
{
	menu = getLanguage("setup_temp_config");
	$("#vin_source").off("change").change(function(e){
		src = getVinSourceIndex("#" + e.currentTarget.id);
		MJ.id = src;
		initValue();
		$("#rectsel").val(0);
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
	$("#motionOverlay").on("mouseup", function(event, ui) {
		mouseUp(event);
	});
	$("#motionOverlay").on("mousemove",function(event, ui) {
		mouseMove(event);
	});

}

function getRecentValue()
{
	for (var i=0; i<4; i++) {
		$("#m" + (i+1) + "_temperature").val(TemperatureInfo[src][i]['temperature']-10);
		$("#m" + (i+1) + "_filteringtime").val(TemperatureInfo[src][i]['filteringtime']);
		$("#m" + (i+1) + "_tolerance").val(TemperatureInfo[src][i]['tolerance']);
		$("#m" + (i+1) + "_left").val(TemperatureInfo[src][i]['x']);
		$("#m" + (i+1) + "_right").val(TemperatureInfo[src][i]['w']+TemperatureInfo[src][i]['x']);
		$("#m" + (i+1) + "_top").val(TemperatureInfo[src][i]['y']);
		$("#m" + (i+1) + "_bottom").val(TemperatureInfo[src][i]['h']+TemperatureInfo[src][i]['y']);
		$("#m" + (i+1) + "_type").val(TemperatureInfo[src][i]['enable']);
		$("#m" + (i+1) + "_rule").val(TemperatureInfo[src][i]['rule']);
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
	var param = "msubmenu=temperature_detect&action=apply&";

	for (var i=0; i<4; i++) {
		param += "x" + i + "=" + Math.round(rect[i+1].startX * 100 / preview_out.width) + "&";
		param += "y" + i + "=" + Math.round(rect[i+1].startY * 100 / preview_out.height) + "&";
		param += "w" + i + "=" + Math.round(rect[i+1].w * 100 / preview_out.width) + "&";
		param += "h" + i + "=" + Math.round(rect[i+1].h * 100 / preview_out.height) + "&";
		param += "enable" + i + "=" + rect[i+1].type + "&";
		param += "filteringtime" + i + "=" + rect[i+1].filteringtime + "&";
		param += "rule" + i + "=" + rect[i+1].rule + "&";
		param += "temperature" + i + "=" + (parseInt(rect[i+1].temperature) + 10) + "&";
		param += "tolerance" + i + "=" + rect[i+1].tolerance + "&";
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
			rect[i].startX = Math.round($("#m" + i + "_left")[0].value * preview_out.width / 100);
			rect[i].startY = Math.round($("#m" + i + "_top")[0].value * preview_out.height / 100);
			rect[i].w = Math.round(($("#m" + i + "_right")[0].value - $("#m" + i + "_left")[0].value) * preview_out.width / 100);
			rect[i].h = Math.round(($("#m" + i + "_bottom")[0].value - $("#m" + i + "_top")[0].value) * preview_out.height / 100);
			rect[i].type = $("#m" + i + "_type")[0].value;
			rect[i].filteringtime = $("#m" + i + "_filteringtime")[0].value;
			rect[i].temperature = $("#m" + i + "_temperature")[0].value;
			rect[i].tolerance = $("#m" + i + "_tolerance")[0].value;
			rect[i].rule = $("#m" + i + "_rule")[0].value;
		}
	}
    setActiveRect(Number($("#rectsel").val()));
}

function setUpCanvas()
{
	canvas = $("#motionOverlay")[0];
	context = canvas.getContext('2d');
	rect = new Array({}, {}, {}, {}, {});
	motionColor = "blue";
	drag = false;
	$(function() {$( "#sizeslider" ).slider({slide: function(event, ui) {document.getElementById('sizelabel').innerHTML = ui.value; rect[0].filteringtime = ui.value;}});});
	$(function() {$( "#sizeslider" ).slider({stop: function(event, ui) {apply();}});});
	$(function() {$( "#sensslider" ).slider({slide: function(event, ui) {document.getElementById('senslabel').innerHTML = ui.value; rect[0].temperature = ui.value;}});});
	$(function() {$( "#sensslider" ).slider({stop: function(event, ui) {apply();}});});
	$(function() {$( "#toleranceslider" ).slider({slide: function(event, ui) {document.getElementById('tolerancelabel').innerHTML = ui.value; rect[0].tolerance = ui.value;}});});
	$(function() {$( "#toleranceslider" ).slider({stop: function(event, ui) {apply();}});});
	
	$( "#sizeslider" ).next().on("click", function(){		
		var value = ($( "#sizeslider" ).slider("value"));		
		rect[0].filteringtime = value;
		apply();
		$( "#sizeslider" ).next().next().text( value );
	});
	$( "#sizeslider" ).prev().on("click", function(){
		var value = ($( "#sizeslider" ).slider("value"));
		rect[0].filteringtime = value;
		apply();
		$( "#sizeslider" ).next().next().text( value );
	});
	$( "#sensslider" ).next().on("click", function(){
		var value = ($( "#sensslider" ).slider("value"));
		rect[0].temperature = value;
		apply();
		$( "#sensslider" ).next().next().text( value );
	});
	$( "#sensslider" ).prev().on("click", function(){
		var value = ($( "#sensslider" ).slider("value"));
		rect[0].temperature = value;
		apply();
		$( "#sensslider" ).next().next().text( value );
	});
	$( "#toleranceslider" ).next().on("click", function(){
		var value = ($( "#toleranceslider" ).slider("value"));
		rect[0].tolerance = value;
		apply();
		$( "#toleranceslider" ).next().next().text( value );
	});
	$( "#toleranceslider" ).prev().on("click", function(){
		var value = ($( "#toleranceslider" ).slider("value"));
		rect[0].tolerance = value;
		apply();
		$( "#toleranceslider" ).next().next().text( value );
	});

//	canvas.width = plugin.width;
//	canvas.height = plugin.height;

    rect[0].type = 0;
}

function mouseDown(e)
{
	coords = canvas.relMouseCoords(e);
	rect[0].startX = coords.x;
	rect[0].startY = coords.y;
	drag = true;
}
canvas.onmouseover = function(e) {
	coords = canvas.relMouseCoords(e);
	//alert("in canvas");
	console.log("in canvas");
	if(drag == false)
	{
		if( (rect[0].startX < coords.x) && (coords.x < rect[0].startX + rect[0].w) )
		{
			if( (rect[0].startY < coords.y) && (coords.y < rect[0].startY + rect[0].h) )
			{
				//alert("in rect");
				console.log("in rect");
			}
		}
		//alert("out rect");
		console.log("out rect");
	}
}

function mouseUp(e)
{
	drag = false;
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
}

function mouseMove(e)
{
	coords = canvas.relMouseCoords(e);
	if (drag) 
	{
		rect[0].w = coords.x - rect[0].startX;
		rect[0].h = coords.y - rect[0].startY;
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
function setChangeRule(index)
{
	rect[0].rule = index;
	apply();
}
function setActiveRect(index)
{
	activeRect = index+1;
    sizelabel = document.getElementById('sizelabel');
	senslabel = document.getElementById('senslabel');
	tolerancelabel = document.getElementById('tolerancelabel');

	if(typeof rect[activeRect].w !== 'undefined')
	{
		rect[0].startX = rect[activeRect].startX;
		rect[0].startY = rect[activeRect].startY;
		rect[0].w = rect[activeRect].w;
		rect[0].h = rect[activeRect].h;
		rect[0].filteringtime = rect[activeRect].filteringtime;
		rect[0].temperature = rect[activeRect].temperature;
		rect[0].tolerance = rect[activeRect].tolerance;
		rect[0].rule = rect[activeRect].rule;
		setRectType(rect[activeRect].type);
		setFieldsDisabled(rect[activeRect].type == 0);
		document.getElementById("typesel").selectedIndex = rect[activeRect].type;
		document.getElementById("rulesel").selectedIndex = rect[activeRect].rule;
		$("#sizeslider").slider( "option", "value", rect[activeRect].filteringtime); 
		$("#sensslider").slider( "option", "value", rect[activeRect].temperature);
		$("#toleranceslider").slider( "option", "value", rect[activeRect].tolerance);
		sizelabel.innerHTML = rect[activeRect].filteringtime;
		senslabel.innerHTML = rect[activeRect].temperature;
		tolerancelabel.innerHTML = rect[activeRect].tolerance;
	}	
	else
	{		
		rect[0] = {};
		rect[0].type = 0;
		rect[0].filteringtime = 50;
		rect[0].temperature = 50;
		rect[0].tolerance = 50;
		rect[0].rule = 0;
		setFieldsDisabled(true);
		document.getElementById("typesel").selectedIndex = 0;
		document.getElementById("rulesel").selectedIndex = 0;
		$("#sizeslider").slider( "option", "value", -10);
		$("#sensslider").slider( "option", "value", 0);
		$("#toleranceslider").slider( "option", "value", 0);
		sizelabel.innerHTML = -10;
		senslabel.innerHTML = 0;
		toleranceabel.innerHTML = 0;
	}
	draw();
}

function setFieldsDisabled(value)
{
 //   $("#sizeslider").slider("option", "disabled", value);
 //   $("#sensslider").slider("option", "disabled", value);
	  disabledSlider("sizeslider", value) ;
	  disabledSlider("sensslider", value) ;
	  disabledSlider("toleranceslider", value) ;
 }

function apply()
{
	var width 	= preview_out.width;
	var height	= preview_out.height;
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
		rect[activeRect].filteringtime = rect[0].filteringtime;
		$("#m" + (activeRect-1) + "_filteringtime")[0].value = rect[0].filteringtime;
		rect[activeRect].temperature = rect[0].temperature;		
		$("#m" + (activeRect-1) + "_temperature")[0].value = rect[0].temperature;		
		rect[activeRect].rule = rect[0].rule;		
		$("#m" + (activeRect-1) + "_rule")[0].value = rect[0].rule;		
		rect[activeRect].tolerance = rect[0].tolerance;		
		$("#m" + (activeRect-1) + "_tolerance")[0].value = rect[0].tolerance;		
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
