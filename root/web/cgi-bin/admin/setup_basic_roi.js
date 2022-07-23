var menu = getLanguage("setup_av_roi_config");
var canvas, context, drag,
	activeRect = 1,
	rect = new Array({}, {},{}, {}, {});
var sensor = { 
	'width' : VideoInfo[0].resolution.split('x')[0],
	'height': VideoInfo[0].resolution.split('x')[1]
};
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
var last_info = {};
$.extend(true, last_info, VideoQproiInfo);
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
var channel = 0;
var isMJPEG = false;
$(document).ready( function() {
	onLoadPage();
});

function onLoadPage() {
	var VLC = false, Motion=false;
	VLCManager.setPlayInfo(userInfo, rtspPort);
	VLC = VLCManager.initPreview("vlc_box", true) 
		init();
}
function init() {
	if( capInfo["oem"] == 8) 	
		setSlider("sensslider",-50, 50);
	else
		setSlider("sensslider",0, 100);
	initUI();
	initValue();
	initEvent();
	checkDependencies();
}
function setUpCanvas() {
	canvas = $("#motionOverlay")[0];
	context = canvas.getContext('2d');
	drag = false;
	rect[0].enable = 0;
}

function initUI() {
	commonCreateSourceSelectBox("#vin_source");

	if(corridor_mode)
		var canvas = '<canvas id=motionOverlay width="' + preview_out.height+ '" height="' + preview_out.width + '"></canvas>';
	else
		var canvas = '<canvas id=motionOverlay width="' + preview_out.width+ '" height="' + preview_out.height + '"></canvas>';
	$("#overlay_box").append(canvas);

	setUpCanvas();

	updateChannelInfomation();
}

function updateChannelInfomation() {
	$("#channel").find("option").remove();
	var cmd = '',
	index = 0,
	name = ["setup_main_stream", "setup_sub_stream", "setup_third_stream" ];
	VinStreamInfo[src].forEach(function(ch){
		if( ch >= 0 ) {
			cmd += "<option value="+index+">"+getLanguage(name[index++])+"</option>";
		}
	});
	if( cmd ) {
		$("#channel").append(cmd);
	}
}

function initValue() {

    var cookies = getCookie('stream_cookie');
    if( cookies ){
        $("#channel").val(cookies);
        setCookie('stream_cookie','',-1);
    }
	$("#sensslider").slider("option", "value", rect[activeRect].sens);
	$("#senslabel").html(rect[activeRect].sens);
	$("#enable").val(rect[activeRect].enable);
	getRecentValue(); 
}
function initEvent() {
	var  pop_msg ="";

    $("#sensslider").next().on("click", function(){              
            var value = $("#senslabel").html();                
            $( "#sensslider" ).next().next().text( value );
            rect[activeRect].sens = value;
    });                                             

    $("#sensslider").prev().on("click", function(){              
            var value = $("#senslabel").html();
            $( "#sensslider" ).next().next().text( value );
            rect[activeRect].sens = value;
    });       

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
		setActiveChannel( channel );
		checkDependencies();
	});

	$("#enable").on("change", function(e){
		rect[activeRect].enable = e.currentTarget.value;
		setActiveChannel($("#channel").val());
	});
	$("#btSave").on("click", function(){
		var param = { 
			msubmenu : 'qproi',
			action : 'apply',
			source : (Number(src)+1),
			stream : channel,
		}, change = 0;

		var i = $("#channel option").index($("#channel option:selected"));
		lpRect = rect[i+1];
		if( last_info[src][i].Qproi_x!= Math.round(lpRect.start_x * 100 / preview_out.width ) ){
			param["x0"] = Math.round(lpRect.start_x * 100 / preview_out.width);
			change = 1;
		}
		if( last_info[src][i].Qproi_y != Math.round(lpRect.start_y * 100 / preview_out.height) ) {
			param["y0"] = Math.round(lpRect.start_y * 100 / preview_out.height);
			change = 1;
		}
		if( last_info[src][i].Qproi_w != Math.round(lpRect.width * 100 / preview_out.width)) {
			param["w0"] = Math.round(lpRect.width * 100 / preview_out.width);
			change = 1;
		}
		if( last_info[src][i].Qproi_h != Math.round(lpRect.height * 100 / preview_out.height) ){
			param["h0"] = Math.round(lpRect.height * 100 / preview_out.height);
			change = 1;
		}
		if( last_info[src][i].Qproi_t != lpRect.enable ) {
			param["t0"] = lpRect.enable;
			change = 1;
		}
		if( last_info[src][i].Qproi_s != lpRect.sens ) {
			if( capInfo["oem"] == 8) 				
				param["s0"] = Number( lpRect.sens ) + Number(50);
			else	
				param["s0"] = lpRect.sens ;
			change = 1;
		}

		if( change == 0 ) {
			pop_msg = getLanguage("msg_nothing_changed");
			settingFail(menu, pop_msg);
			return ; 		
		}
        //if(capInfo["oem"] == 12)
            setCookie('stream_cookie',channel,1);

		$.ajax({
			type : 'get',
			url  : '/cgi-bin/admin/basic.cgi',
			data : param,
			cache	: false,
			success : function(args) {
				var pattern = /OK/g;
				if( pattern.test(args) == true){
					pop_msg = getLanguage("msg_roi_success");
					settingSuccess(menu, pop_msg);
					refreshMenuContent();
				}else{
					settingFail(menu);
				}
			},
			error 	: function(args) {
				settingFail(menu, null);
			},
		});
	});

	$("#btRestore").on("click", function(){
		getRecentValue(); 
	});	

	if( isIE_fix() == true ) {

		$("#motionOverlay").on("mousedown", function(e, ui) {
				var targetChannel = VinStreamInfo[src][channel];
				if ( isMJPEG ) {
				return;
				}
				if( drag ) {
				$("#motionOverlay").trigger("mouseup");
				} 
				else {
				$("#motionOverlay").on("mousemove",function(e, ui) {
						coords = canvas.relMouseCoords(e);
						if (drag) {
						rect[0].width = coords.x - rect[0].start_x;
						rect[0].height = coords.y - rect[0].start_y;
						draw();
						}
						});
				drag = true;
				coords = canvas.relMouseCoords(e);
				rect[0].start_x = coords.x;
				rect[0].start_y = coords.y;
				}
		}).on("mouseup", function(e, ui) {
			$("#motionOverlay").off("mousemove");
			drag = false;
			if( rect[0].width < 0) {
			rect[0].start_x += rect[0].width;
			rect[0].width *= -1;
			}
			if( rect[0].height < 0) {
			rect[0].start_y += rect[0].height;
			rect[0].height *= -1;
			}

			if(typeof(rect[activeRect].width) !== 'undefined') {
			rect[activeRect].start_x = rect[0].start_x;
			rect[activeRect].start_y = rect[0].start_y;
			rect[activeRect].width   = rect[0].width;
			rect[activeRect].height  = rect[0].height;
			}
			draw();
			});

		$( "#sensslider" ).off("slide").on("slide", function(event, ui) {
				rect[activeRect].sens = ui.value;
				});
	} else {
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
		$( "#sensslider" ).off("slide").on("slide", function(event, ui) {
				rect[activeRect].sens = ui.value;
				});
	}
}

function mouseDown(e) {
  drag = true;

    if(!window.isIE()) {
      canvas.requestPointerLock = canvas.requestPointerLock || canvas.mozRequestPointerLock;
      canvas.requestPointerLock();
    }

    coords = canvas.relMouseCoords(e);
    rect[0].start_x = coords.x;
    rect[0].start_y = coords.y;
    rect[0].width = 0;
    rect[0].height = 0;
}

function mouseUp(e) {
  drag = false;
  $("#overlay_box").css("border", "");
  if( rect[0].width < 0) {
    rect[0].start_x += rect[0].width;
    rect[0].width *= -1;
  }
  if( rect[0].height < 0) {
    rect[0].start_y += rect[0].height;
    rect[0].height *= -1;
  }

  if(typeof(rect[activeRect].width) !== 'undefined') {
    rect[activeRect].start_x = rect[0].start_x;
    rect[activeRect].start_y = rect[0].start_y;
    rect[activeRect].width   = rect[0].width;
    rect[activeRect].height  = rect[0].height;
  }
  draw();

  if(!window.isIE()) {
    document.exitPointerLock = document.exitPointerLock || document.mozExitPointerLock;
    document.exitPointerLock();
  }
}

function mouseMove(e) {
  coords = canvas.relMouseCoords(e);
  if (drag) {
    if(!window.isIE()) {
      rect[0].width += e.originalEvent.movementX;
      rect[0].height += e.originalEvent.movementY;

      if((rect[0].width + rect[0].start_x) >= canvas.width) {
        rect[0].width = canvas.width - rect[0].start_x;
      }
      if((rect[0].width + rect[0].start_x) <= 0) {
        rect[0].width = rect[0].start_x * -1;
      }
      if((rect[0].height + rect[0].start_y) >= canvas.height) {
        rect[0].height = canvas.height - rect[0].start_y;
      }
      if((rect[0].height + rect[0].start_y) <= 0) {
        rect[0].height = rect[0].start_y * -1;
      }
    } else {
      $("#overlay_box").css("border", "1px solid #B2B2B2");
      if(coords.x >= canvas.width) coords.x = canvas.width;
      if(coords.x <= 0) coords.x = 0;
      if(coords.y >= canvas.height) coords.y = canvas.height;
      if(coords.y <= 0) coords.y = 0;
      rect[0].width = coords.x - rect[0].start_x;
      rect[0].height = coords.y - rect[0].start_y;
    }

    draw();
  }
}

function checkDependencies() {
	$("#roi_caution").remove();
	var targetChannel = VinStreamInfo[src][channel],
	isMJPEG = VideoInfo[targetChannel]['codec'] == 2;
	$("#enable").prop("disabled", isMJPEG);
	$("#btSave").prop("disabled", isMJPEG);
	$("#btRestore").prop("disabled", isMJPEG);
	//setFieldsDisabled(isMJPEG);
	setFieldsDisabled($("#enable").val()==0);
	if(isMJPEG){
		$("#display_box").after("<div id='roi_caution' ></div>");
		$("#roi_caution").text(getLanguage("msg_roi_caution"));
		$("#roi_caution").addClass("caution");
	}
}
function getRecentValue() {
	var i=0;
	VideoQproiInfo[src].forEach(function(stream){
		rect[i+1].start_x = Math.round(stream['Qproi_x'] * preview_out.width / 100);
		rect[i+1].start_y = Math.round(stream['Qproi_y'] * preview_out.height / 100);
		rect[i+1].width   = Math.round(stream['Qproi_w'] * preview_out.width / 100);
		rect[i+1].height  = Math.round(stream['Qproi_h'] * preview_out.height / 100);
		rect[i+1].enable  = stream['Qproi_t'];

		if( capInfo["oem"] == 8) 			
			rect[i+1].sens    = Number(stream['Qproi_s']) - Number(50);
		else 	
			rect[i+1].sens    = stream['Qproi_s'] ;
		i++;
	});
	setActiveChannel($("#channel").val());
}

function draw() { 
	if( typeof(context) == "undefined" ){
		return;
	}

	context.clearRect(0, 0, canvas.width, canvas.height);
	for(var i=1, len=rect.length; i<len; i++) {
		if( typeof(rect[i].width) === 'undefined' || rect[i].width ==0 && rect[i].height ==0 ) {
			continue;
		}
		//context.fillStyle = "rgba(192,192,192, 0.3)";
		context.beginPath();
		setFillType(rect[i].enable);
		context.fillRect(rect[i].start_x, rect[i].start_y, rect[i].width, rect[i].height);
	}
	if( typeof(rect[0]) != 'undefined' ) {
		//context.fillStyle = (rect[0].enable == 1)? "rgba(255,0,0,0.3)" : "rgba(0,0,255,0.3)";
		context.beginPath();
		context.rect(rect[0].start_x, rect[0].start_y, rect[0].width, rect[0].height);
		setFillType(rect[0].enable);
		context.lineWidth = 2;
		context.strokeStyle = 'yellow';
		context.stroke();
		context.fillRect(rect[0].start_x, rect[0].start_y, rect[0].width, rect[0].height);
	}
}

function setActiveChannel(index) {
	activeRect = Number(index)+1;
	if(typeof(rect[activeRect]) !== 'undefined') {
		rect[0].start_x = rect[activeRect].start_x;
		rect[0].start_y = rect[activeRect].start_y;
		rect[0].width   = rect[activeRect].width;
		rect[0].height  = rect[activeRect].height;
		rect[0].sens    = rect[activeRect].sens;
		rect[0].enable  = rect[activeRect].enable;
		setFieldsDisabled(rect[activeRect].enable == 0);
		document.getElementById("enable").selectedIndex = rect[activeRect].enable;
		$("#sensslider").slider( "option", "value", rect[activeRect].sens);
	}	
	else {
		rect[0] = {};
		setFieldsDisabled(true);
		document.getElementById("enable").selectedIndex = 0;
		if( capInfo["oem"] == 8) 			
			$("#sensslider").slider( "option", "value", 0);
		else 
			$("#sensslider").slider( "option", "value", 50);
	}
	draw();
}

function setFieldsDisabled(value) {
	disabledSlider("sensslider", value) ;
}

function setFillType(index) {
	//	context.fillStyle = ((index == 0) ? "rgba(192,192,192, 0.3)" : ((index == 1) ? "rgba(0,0,255, 0.3)" : "rgba(255,0,0, 0.3)"));
	context.fillStyle = ((index == 0) ? "rgba(192,192,192, 0.0)" : ((index == 1) ? "rgba(255,0,0, 0.3)" : "rgba(0,0,255, 0.3)"));
}
