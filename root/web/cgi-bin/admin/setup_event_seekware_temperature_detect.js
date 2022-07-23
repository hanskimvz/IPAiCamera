var motion_setup= {};
var canvas, context, rect, activeRect, drag, xmlHttpData, motionColor;
//var menu = "Motion Detection setting";
var checkMotionFlag = 0;
var sensor = { 'width' :  VideoInfo[0].resolution.split('x')[0],
	'height': VideoInfo[0].resolution.split('x')[1] };
var preview_out= { 'width' : 0, 'height' : 288};
var emissivity_table = [ 
	0.97,	// seekware Default
	0.96, 	// Water, pure
	0.95,	// Glass, smooth(uncoated)
	0.92, 	// Limestone
	0.91, 	// Concrete, rough
	0.9,	// Aluminum, anodized
	0.9,	// Brick
	0.9,	// Paint(including white)
	0.89,	// Marble(polished)
	0.89,	// Plaster, rough
	0.88,	// Asphalt
	0.88,	// Paper, roofing or white
	0.87,	// Copper, oxidized
	0.04,	// Copper, polished
	0.04,	// Silver, oxidized
	0.03,	// Aluminum foil
	0.02,	// Silver, polished
];
var seek_temperature_mode = 0;

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
var src = 0;

$(document).ready( function() {
	onLoadPage();
});

function onLoadPage()
{
	var VLC = false, Motion=false;
	VLCManager.setPlayInfo(userInfo, rtspPort);
	VLC = VLCManager.initPreview("vlc_box", true) 
	initUI();
	initValue();
	initEvent();
	dependencyUI();
	//initDisplayMotionStatus("displayMotionStatusArea", capInfo.video_in);
	//checkMotion("displayMotionStatus", 1);
	checkMotion("displayAreaTemperature", 4);
}

function dependencyUI()
{
	if(seek_temperature_mode == 0) // Celsius
	{
		$("#alarm_temp_label").text( "°C [ -40 ~ 330 ]" );
		$("#slope_gradient_label").text("°C [ -100 ~ 100 ]");
	}
	else // Fahrenheit
	{
		$("#alarm_temp_label").text( "°F [ -40 ~ 626 ]" );
		$("#slope_gradient_label").text("°F [ -148 ~ 212 ]");
	}

}

function getAreaTemperature()
{
	var x;
	var y1,y2,y3;
	var margin = 50;

	var width;
	var height;

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

	var alarm_zone = $("#displayAreaTemperature").val(); // 0

	for(var i = 0; i < 8; i++)
	{
		if( ((alarm_zone >> i) & 1) )
		{
			if( i == (activeRect-1) )
			{
				$("#temperature_detected").removeClass("warning_off");
				$("#temperature_detected").addClass("warning_on");
			}
		}
		else
		{
			if( i == (activeRect-1) )
			{
				$("#temperature_detected").removeClass("warning_on");
				$("#temperature_detected").addClass("warning_off");
			}
		}
	}
/*
	if(drag == false)
	{
		if(TemperatureInfo[src][activeRect-1]['enable'])
		{
			x = rect[activeRect].startX;
			y1 = rect[activeRect].startY - 26;

			if(x + margin > width)
				x = width - margin;

			if(y1 - 30 < 0)
			{
				y1 = rect[activeRect].startY + rect[activeRect].h + 12;
				if(y1 + 30 > height)
				{
					y1 = rect[activeRect].startY + 12;
					x = rect[activeRect].startX+rect[activeRect].w+5;
					if(x + margin > width)
					{
						x = rect[activeRect].startX - margin;
						if(x - margin < 0)
							x = rect[activeRect].startX + 5;
					}
				}
			}

			draw();

			var text_min, text_max, text_avg;
			context.font = "12px Arial";
			context.fillStyle = "rgba(255,255,255,1)"; 

			if(seek_temperature_mode == 1) // Fahrenheit //	
			{
				text_min = "Min : " + CelToFah($("#m" + (activeRect-1) + "_mintemp").val());
				text_max = "Max : " + CelToFah($("#m" + (activeRect-1) + "_maxtemp").val());
				text_avg = "Avg : " + CelToFah($("#m" + (activeRect-1) + "_avgtemp").val());
			}
			else
			{
				text_min = "Min : " + $("#m" + (activeRect-1) + "_mintemp").val();
				text_max = "Max : " + $("#m" + (activeRect-1) + "_maxtemp").val();
				text_avg = "Avg : " + $("#m" + (activeRect-1) + "_avgtemp").val();
			}
			context.fillText(text_min, x, y1);
			y2 = y1 + 12;
			context.fillText(text_max, x, y2);
			y3 = y2 + 12;
			context.fillText(text_avg, x, y3);

			var alarm_zone = $("#displayAreaTemperature").val(); // 0
			
			for(var i = 0; i < 8; i++)
			{
				if( ((alarm_zone >> i) & 1) )
				{
					if( i == (activeRect-1) )
					{
						$("#temperature_detected").removeClass("warning_off");
						$("#temperature_detected").addClass("warning_on");
					}
				}
				else
				{
					if( i == (activeRect-1) )
					{
						$("#temperature_detected").removeClass("warning_on");
						$("#temperature_detected").addClass("warning_off");
					}
				}
			}
		}
		else
		{
			$("#temperature_detected").removeClass("warning_on");
			$("#temperature_detected").addClass("warning_off");
		}
	}
*/
}

function initUI()
{	
	commonCreateSourceSelectBox("#vin_source");
	if(corridor_mode)
		var canvas = '<canvas id=motionOverlay width="' + preview_out.height  +'" height="' + preview_out.width + '"></canvas>';
	else
		var canvas = '<canvas id=motionOverlay width="' + preview_out.width  +'" height="' + preview_out.height + '"></canvas>';
	$("#overlay_box").append(canvas);

	activeRect = 1;

	setUpCanvas();

	if( $("#emissivitysel").val() == 17 )	// custom
	{
		$("#emissivity_custom").attr("disabled", false);
		$("#emissivity_custom").val(rect[activeRect].emissivity);
	}
	else
	{
		$("#emissivity_custom").attr("disabled", true);
		$("#emissivity_custom").val(emissivity_table[$("#emissivitysel").val()]);
	}

	$("#temperature_detected").removeClass("warning_off");
	$("#temperature_detected").addClass("warning_off");

}

function initValue()
{
	if(capInfo.camera_type == "seekware") { // for Celsius, Fahrenheit
		seek_temperature_mode = CameraFunc[src]["thermal_temperature_unit"];
	}
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
	for (var i=0; i<TemperatureInfo[src].length; i++) {
		if(seek_temperature_mode == 1) { // Fahrenheit // 
			$("#m" + (i+1) + "_temperature").val(CelToFah(TemperatureInfo[src][i]['temperature']/100 - 40)); 
			$("#m" + (i+1) + "_slopegradient").val(CelToFah(TemperatureInfo[src][i]['slopegradient']/100));
		}
		else {
			$("#m" + (i+1) + "_temperature").val(Math.floor(TemperatureInfo[src][i]['temperature']/100 - 40));
			$("#m" + (i+1) + "_slopegradient").val(Math.floor(TemperatureInfo[src][i]['slopegradient']/100));
		}
			
//		$("#m" + (i+1) + "_temperature").val(TemperatureInfo[src][i]['temperature'] - 40);
		$("#m" + (i+1) + "_filteringtime").val(TemperatureInfo[src][i]['filteringtime']);
		$("#m" + (i+1) + "_tolerance").val(TemperatureInfo[src][i]['tolerance']);
		$("#m" + (i+1) + "_left").val(TemperatureInfo[src][i]['x']);
		$("#m" + (i+1) + "_right").val(TemperatureInfo[src][i]['w']+TemperatureInfo[src][i]['x']);
		$("#m" + (i+1) + "_top").val(TemperatureInfo[src][i]['y']);
		$("#m" + (i+1) + "_bottom").val(TemperatureInfo[src][i]['h']+TemperatureInfo[src][i]['y']);
		$("#m" + (i+1) + "_type").val(TemperatureInfo[src][i]['enable']);
		$("#m" + (i+1) + "_rule").val(TemperatureInfo[src][i]['rule']);
		$("#m" + (i+1) + "_emissivitytype").val(TemperatureInfo[src][i]['emissivitytype']);
		$("#m" + (i+1) + "_emissivity").val(TemperatureInfo[src][i]['emissivity'] / 100);
		$("#m" + (i+1) + "_measurement").val(TemperatureInfo[src][i]['measurement']);
		//$("#m" + (i+1) + "_slopegradient").val(TemperatureInfo[src][i]['slopegradient']);
		$("#m" + (i+1) + "_osd").val(TemperatureInfo[src][i]['osd']);
	}
	$("#temp_convert_md").prop("checked", ConvertInfo[src]['convert_md']);
	load();
}

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
	var emissivity_tmp;
	var inverval_tmp;
	var alarm_temp_min = -40;
	var alarm_temp_max = 330;

	emissivity_tmp = $("#emissivity_custom").val() * 100;
	if((emissivity_tmp < 2) || (emissivity_tmp > 99))
	{
		$("#emissivity_custom").val(rect[activeRect].emissivity);
		settingFail(menu, null);
		return;
	}

	// Celsius, Fahrenheit temperature min, max change
	if(seek_temperature_mode == 1) // Fahrenheit
	{
		alarm_temp_min = CelToFah(alarm_temp_min); // -40 > -40
		alarm_temp_max = CelToFah(alarm_temp_max); // 330 > 626
	}

	if(($("#alarm_temp").val() < alarm_temp_min) || ($("#alarm_temp").val() > alarm_temp_max))
	{
		$("#alarm_temp").val(rect[activeRect].temperature);
		settingFail(menu, null);
		return;
	}

	inverval_tmp = $("#detection_inverval").val();
	if((inverval_tmp < 10) || (inverval_tmp > 600))
	{
		$("#detection_inverval").val(rect[activeRect].filteringtime);
		settingFail(menu, null);
		return;
	}

	rect[activeRect].emissivity = emissivity_tmp / 100;
	rect[activeRect].temperature = $("#alarm_temp").val();
	rect[activeRect].filteringtime = inverval_tmp;
	rect[activeRect].slopegradient = $("#slope_gradient").val();

	// check changed param
	param += onChangedParam();
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
			if(corridor_mode)
			{
				rect[i].startX = Math.round($("#m" + i + "_left")[0].value * preview_out.height / 100);
				rect[i].startY = Math.round($("#m" + i + "_top")[0].value * preview_out.width / 100);
				rect[i].w = Math.round(($("#m" + i + "_right")[0].value - $("#m" + i + "_left")[0].value) * preview_out.height / 100);
				rect[i].h = Math.round(($("#m" + i + "_bottom")[0].value - $("#m" + i + "_top")[0].value) * preview_out.width / 100);
			}
			else
			{
				rect[i].startX = Math.round($("#m" + i + "_left")[0].value * preview_out.width / 100);
				rect[i].startY = Math.round($("#m" + i + "_top")[0].value * preview_out.height / 100);
				rect[i].w = Math.round(($("#m" + i + "_right")[0].value - $("#m" + i + "_left")[0].value) * preview_out.width / 100);
				rect[i].h = Math.round(($("#m" + i + "_bottom")[0].value - $("#m" + i + "_top")[0].value) * preview_out.height / 100);
			}
			rect[i].type = $("#m" + i + "_type")[0].value;
			rect[i].rule = $("#m" + i + "_rule")[0].value;
			rect[i].filteringtime = $("#m" + i + "_filteringtime")[0].value;
			rect[i].temperature = $("#m" + i + "_temperature")[0].value;
			rect[i].tolerance = $("#m" + i + "_tolerance")[0].value;
			rect[i].emissivitytype = $("#m" + i + "_emissivitytype")[0].value;
			rect[i].emissivity = $("#m" + i + "_emissivity")[0].value;
			rect[i].measurement = $("#m" + i + "_measurement")[0].value;
			rect[i].slopegradient = $("#m" + i + "_slopegradient")[0].value;
			rect[i].osd = $("#m" + i + "_osd")[0].value;
		}
	}
    setActiveRect(Number($("#rectsel").val()));
}

function setUpCanvas()
{
	canvas = $("#motionOverlay")[0];
	context = canvas.getContext('2d');
	rect = new Array({}, {}, {}, {}, {}, {}, {}, {}, {});
	motionColor = "blue";
	drag = false;

//	canvas.width = plugin.width;
//	canvas.height = plugin.height;

    rect[0].type = 0;
}

function mouseDown(e)
{
  if(!window.isIE()) {
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

  if(!window.isIE()) {
    document.exitPointerLock = document.exitPointerLock || document.mozExitPointerLock;
    document.exitPointerLock();
  }
}

function mouseMove(e)
{
	coords = canvas.relMouseCoords(e);
	if (drag) 
	{
		if(!window.isIE()) {
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
function setChangeRule(index)
{
	rect[0].rule = index;
	apply();

	if( index == 2 )	// slope rate
	{
		$("#setup_temperature").hide();
		$("#alarm_temp").hide();
		$("#alarm_temp_label").hide();

		$("#setup_slope_gradient").show();
		$("#slope_gradient").show();
		$("#slope_gradient_label").show();

		$("#setup_autoup_interval").show();
		$("#detection_inverval").show();
		$("#detection_inverval_label").show();

		document.getElementById("measurementsel").selectedIndex = 0;
		rect[activeRect].measurement = 0;
		$("#measurementsel").attr("disabled", true);
	}
	else
	{
		$("#setup_temperature").show();
		$("#alarm_temp").show();
		$("#alarm_temp_label").show();

		$("#setup_slope_gradient").hide();
		$("#slope_gradient").hide();
		$("#slope_gradient_label").hide();
		
		$("#setup_autoup_interval").hide();
		$("#detection_inverval").hide();
		$("#detection_inverval_label").hide();

		$("#measurementsel").attr("disabled", false);

	}
}
function setChangeMeasurement(index)
{
	rect[0].measurement = index;
	apply();
}
function setChangeEmissivitytype(index)
{
	rect[0].emissivitytype = index;
	apply();

	if( index == 17 )	// custom
	{
		$("#emissivity_custom").attr("disabled", false);
		$("#emissivity_custom").val(rect[activeRect].emissivity);
	}
	else
	{
		$("#emissivity_custom").attr("disabled", true);
		$("#emissivity_custom").val(emissivity_table[$("#emissivitysel").val()]);
	}
}

function setActiveRect(index)
{
	activeRect = index+1;

	if(typeof rect[activeRect].w !== 'undefined')
	{
		rect[0].startX = rect[activeRect].startX;
		rect[0].startY = rect[activeRect].startY;
		rect[0].w = rect[activeRect].w;
		rect[0].h = rect[activeRect].h;
		rect[0].rule = rect[activeRect].rule;
		rect[0].filteringtime = rect[activeRect].filteringtime;
		rect[0].temperature = rect[activeRect].temperature;
		rect[0].tolerance = rect[activeRect].tolerance;
		rect[0].emissivitytype = rect[activeRect].emissivitytype;
		rect[0].emissivity = rect[activeRect].emissivity;
		rect[0].measurement = rect[activeRect].measurement;
		rect[0].slopegradient = rect[activeRect].slopegradient;
		rect[0].osd = rect[activeRect].osd;
		setRectType(rect[activeRect].type);
		setFieldsDisabled(rect[activeRect].type == 0);
		document.getElementById("typesel").selectedIndex = rect[activeRect].type;
		document.getElementById("osdsel").selectedIndex = rect[activeRect].osd;
		document.getElementById("rulesel").selectedIndex = rect[activeRect].rule;
		document.getElementById("measurementsel").selectedIndex = rect[activeRect].measurement;
		document.getElementById("emissivitysel").selectedIndex = rect[activeRect].emissivitytype;

		if( $("#rulesel").val() == 2 )	// slope rate
		{
			$("#setup_temperature").hide();
			$("#alarm_temp").hide();
			$("#alarm_temp_label").hide();
	
			$("#setup_slope_gradient").show();
			$("#slope_gradient").show();
			$("#slope_gradient_label").show();
	
			$("#setup_autoup_interval").show();
			$("#detection_inverval").show();
			$("#detection_inverval_label").show();
	
			document.getElementById("measurementsel").selectedIndex = 0;
			rect[activeRect].measurement = 0;
			$("#measurementsel").attr("disabled", true);
		}
		else
		{
			$("#setup_temperature").show();
			$("#alarm_temp").show();
			$("#alarm_temp_label").show();
	
			$("#setup_slope_gradient").hide();
			$("#slope_gradient").hide();
			$("#slope_gradient_label").hide();
			
			$("#setup_autoup_interval").hide();
			$("#detection_inverval").hide();
			$("#detection_inverval_label").hide();

			$("#measurementsel").attr("disabled", false);
		}

		$("#alarm_temp").val(rect[activeRect].temperature);

		if( $("#emissivitysel").val() == 17 )	// custom
		{
			$("#emissivity_custom").attr("disabled", false);
			$("#emissivity_custom").val(rect[activeRect].emissivity);
		}
		else
		{
			$("#emissivity_custom").attr("disabled", true);
			$("#emissivity_custom").val(emissivity_table[rect[activeRect].emissivitytype]);
		}

		$("#slope_gradient").val(rect[activeRect].slopegradient);
		$("#detection_inverval").val(rect[activeRect].filteringtime);

	}	
	else
	{		
		rect[0] = {};
		rect[0].type = 0;
		rect[0].rule = 0;
		rect[0].filteringtime = 10;
		rect[0].temperature = 40;
		rect[0].tolerance = 50;
		rect[0].emissivitytype = 97;
		rect[0].emissivity = 97;
		rect[0].measurement = 0;
		rect[0].slopegradient = 0;
		rect[0].osd = 0;

		setFieldsDisabled(true);
		document.getElementById("typesel").selectedIndex = 0;
		document.getElementById("osdsel").selectedIndex = 0;
		document.getElementById("rulesel").selectedIndex = 0;
		document.getElementById("measurementsel").selectedIndex = 0;
		document.getElementById("emissivitysel").selectedIndex = 0;

		if( $("#rulesel").val() == 2 )	// slope rate
		{
			$("#setup_temperature").hide();
			$("#alarm_temp").hide();
			$("#alarm_temp_label").hide();
	
			$("#setup_slope_gradient").show();
			$("#slope_gradient").show();
			$("#slope_gradient_label").show();
	
			$("#setup_autoup_interval").show();
			$("#detection_inverval").show();
			$("#detection_inverval_label").show();
		}
		else
		{
			$("#setup_temperature").show();
			$("#alarm_temp").show();
			$("#alarm_temp_label").show();
	
			$("#setup_slope_gradient").hide();
			$("#slope_gradient").hide();
			$("#slope_gradient_label").hide();
			
			$("#setup_autoup_interval").hide();
			$("#detection_inverval").hide();
			$("#detection_inverval_label").hide();
		}

		$("#alarm_temp").val(rect[0].temperature);
		
		if( $("#emissivitysel").val() == 17 )	// custom
		{
			$("#emissivity_custom").attr("disabled", false);
			$("#emissivity_custom").val(rect[0].emissivity);
		}
		else
		{
			$("#emissivity_custom").attr("disabled", true);
			$("#emissivity_custom").val(emissivity_table[rect[0].emissivitytype]);
		}

		$("#slope_gradient").val(rect[0].slopegradient);
		$("#detection_inverval").val(rect[0].filteringtime);
	}
	draw();
}

function setFieldsDisabled(value)
{
 //   $("#sizeslider").slider("option", "disabled", value);
 //   $("#sensslider").slider("option", "disabled", value);
 }

function setRectOsd(index)
{
	rect[0].osd = index;
	apply();
}

function apply()
{
	var width;
	var height;

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
		rect[activeRect].rule = rect[0].rule;		
		$("#m" + (activeRect-1) + "_rule")[0].value = rect[0].rule;		

		rect[activeRect].filteringtime = rect[0].filteringtime;
		$("#m" + (activeRect-1) + "_filteringtime")[0].value = rect[0].filteringtime;
		rect[activeRect].temperature = rect[0].temperature;		
		$("#m" + (activeRect-1) + "_temperature")[0].value = rect[0].temperature;		
		rect[activeRect].tolerance = rect[0].tolerance;		
		$("#m" + (activeRect-1) + "_tolerance")[0].value = rect[0].tolerance;	
		rect[activeRect].emissivitytype = rect[0].emissivitytype;		
		$("#m" + (activeRect-1) + "_emissivitytype")[0].value = rect[0].emissivitytype;	
		rect[activeRect].emissivity = rect[0].emissivity;		
		$("#m" + (activeRect-1) + "_emissivity")[0].value = rect[0].emissivity;	
		rect[activeRect].measurement = rect[0].measurement;		
		$("#m" + (activeRect-1) + "_measurement")[0].value = rect[0].measurement;	
		rect[activeRect].slopegradient = rect[0].slopegradient;		
		$("#m" + (activeRect-1) + "_slopegradient")[0].value = rect[0].slopegradient;	
		rect[activeRect].osd = rect[0].osd;
		$("#m" + (activeRect-1) + "_osd")[0].value = rect[0].osd;
	}

	draw();
}

function setRectType(index)
{
	setFillType(index);
	rect[0].type = index;
	setFieldsDisabled(index == 0);
	if( index == 0 ) // disable
		$("#osdsel").attr("disabled", true);
	else
		$("#osdsel").attr("disabled", false);
	apply();
}
function setFillType(index) {
//	context.fillStyle = ((index == 0) ? "rgba(192,192,192, 0.3)" : ((index == 1) ? "rgba(0,0,255, 0.3)" : "rgba(255,0,0, 0.3)"));
	context.fillStyle = ((index == 0) ? "rgba(192,192,192, 0.3)" : ((index == 1) ? "rgba(255,0,0, 0.3)" : "rgba(0,0,255, 0.3)"));
}

function CelToFah(value) {
	return Math.round(value * 9 / 5 + 32);
}

function FahToCel(value) {
	return (Math.floor((value - 32) * 500 / 9)) / 100;
}

function onChangedParam() {
	var changedParam = "";
	var i = Number($("#rectsel").val());

	//corridor mode param
	if(corridor_mode)
		{
			changedParam += "x" + i + "=" + Math.round(rect[i+1].startX * 100 / preview_out.height) + "&";
			changedParam += "y" + i + "=" + Math.round(rect[i+1].startY * 100 / preview_out.width) + "&";
			changedParam += "w" + i + "=" + Math.round(rect[i+1].w * 100 / preview_out.height) + "&";
			changedParam += "h" + i + "=" + Math.round(rect[i+1].h * 100 / preview_out.width) + "&";
		}
		else
		{
			changedParam += "x" + i + "=" + Math.round(rect[i+1].startX * 100 / preview_out.width) + "&";
			changedParam += "y" + i + "=" + Math.round(rect[i+1].startY * 100 / preview_out.height) + "&";
			changedParam += "w" + i + "=" + Math.round(rect[i+1].w * 100 / preview_out.width) + "&";
			changedParam += "h" + i + "=" + Math.round(rect[i+1].h * 100 / preview_out.height) + "&";
		}

	// activation check
	if(TemperatureInfo[src][i]['enable'] != document.getElementById("typesel").selectedIndex)
		changedParam += "enable" + i + "=" + rect[i+1].type + "&";

	// osd check
	if(TemperatureInfo[src][i]['osd'] != document.getElementById("osdsel").selectedIndex)
		changedParam += "osd" + i + "=" + rect[i+1].osd + "&";

	// Alarm rule check
	if(TemperatureInfo[src][i]['rule'] != document.getElementById("rulesel").selectedIndex)
		changedParam += "rule" + i + "=" + rect[i+1].rule + "&";

	// Check interval check
	if(TemperatureInfo[src][i]['filteringtime'] != $("#detection_inverval").val())
		changedParam += "filteringtime" + i + "=" + rect[i+1].filteringtime + "&";

	// Alarm temperature check  + slope gradient check
	if(seek_temperature_mode == 1) { // Fahrenheit
		if(CelToFah(TemperatureInfo[src][i]['temperature']/100 - 40) != $("#alarm_temp").val())
			changedParam += "temperature" + i + "=" + (FahToCel(parseFloat(rect[i+1].temperature)) + 40) + "&";
		if(CelToFah(TemperatureInfo[src][i]['slopegradient']/100) != $("#slope_gradient").val())
			changedParam += "slopegradient" + i + "=" + (FahToCel(parseFloat(rect[i+1].slopegradient))) + "&";
	}
	else {
		if(Math.floor(TemperatureInfo[src][i]['temperature']/100 - 40) != $("#alarm_temp").val())
			changedParam += "temperature" + i + "=" + (parseFloat(rect[i+1].temperature) + 40) + "&";
		if(Math.floor(TemperatureInfo[src][i]['slopegradient']/100) != $("#slope_gradient").val())
			changedParam += "slopegradient" + i + "=" + rect[i+1].slopegradient + "&";
	}
	//tolerance not used
	//if(TemperatureInfo[src][i]['tolerance'] != $("#tolerance").val())
	//	changedParam += "tolerance" + i + "=" + rect[i+1].tolerance + "&";
	
	//emissivitytype
	if(TemperatureInfo[src][i]['emissivitytype'] != document.getElementById("emissivitysel").selectedIndex)
		changedParam += "emissivitytype" + i + "=" + rect[i+1].emissivitytype + "&";
	//emissivity
	if(TemperatureInfo[src][i]['emissivity'] / 100 != $("#emissivity_custom").val())
		changedParam += "emissivity" + i + "=" + (rect[i+1].emissivity * 100) + "&";
	//measurement
	if(TemperatureInfo[src][i]['measurement'] != document.getElementById("measurementsel").selectedIndex)
		changedParam += "measurement" + i + "=" + rect[i+1].measurement + "&";

	//convert_md
	if( $("#temp_convert_md").prop("checked") != ConvertInfo[src]['convert_md'] )
		changedParam += "convert_md=" + Number($("#temp_convert_md").prop("checked")) + "&";

	return changedParam;
}
