var canvas, context, activeRect, drag, xmlHttpData;
var rect = new Array({}, {},{}, {}, {});
var max_privacy = 4 ;

var menu =  getLanguage("privacy_mask_conf");
var sensor = { 'width' :  VideoInfo[0].resolution.split('x')[0],
	'height': VideoInfo[0].resolution.split('x')[1] };
var preview_out= { 'width' : 0, 'height' : 288};
var src = MJ.id;
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

var debug_level=0;
var last_info = {};
$.extend(true, last_info, privInfo);

$(document).ready( function() {
		onLoadPage();
		});


function onLoadPage()
{
	var VLC = false, Motion=false;
	VLCManager.setPlayInfo(userInfo, rtspPort);
	VLC = VLCManager.initPreview("vlc_box", true) 
		init();
}
function debug(msg){ if( debug_level ){ console.log("[DEBUG]"+msg);	} }
function init() {
	if(capInfo["oem"] == 15)
		max_privacy =  10 ;
	else if( capInfo["max_privacy"] == undefined )
		max_privacy =  4 ;
	else if( capInfo["camera_module"] == "esca_isp")
		max_privacy = 12 ;
	else
		max_privacy = capInfo["max_privacy"] ;
	initUI();
	initValue();
	initEvent();
	checkDependecy();
}
function setUpCanvas() {
	canvas = $("#motionOverlay")[0];
	context = canvas.getContext('2d');
	drag = false;
}
function initUI() {	
	commonCreateSourceSelectBox("#vin_source");
	if(corridor_mode)
		var canvas = '<canvas id=motionOverlay width="' + preview_out.height  +'" height="' + preview_out.width + '"></canvas>';
	else
		var canvas = '<canvas id=motionOverlay width="' + preview_out.width  +'" height="' + preview_out.height + '"></canvas>';
	$("#overlay_box").append(canvas);

	var content = '', 
	    msg = getLanguage("setup_privacy_area");

	for(i=0 ; i < max_privacy ; i++) {
		content += "<option value=" + i + ">" + msg + "" + (i+1) + "</option>"
	}
	$("#selAreas").append(content);
	setUpCanvas();

	if( capInfo.ptz_module == "af_licom_2812") {
		if(capInfo["oem"] != 19 && capInfo["oem"] != 20 && capInfo["oem"] != 21 && capInfo["oem"] != 10 && capInfo["oem"] != 11 && capInfo["oem"] != 13 && capInfo["oem"] != 25)
		{
			$("#display_box").after("<div id='roi_caution' ></div>");
			$("#roi_caution").text(getLanguage("msg_privacy_caution"));
			$("#roi_caution").addClass("caution");
		}
	}
}
function initValue() {
	activeRect = 1;
	getRecentValue(); 
	$("[name=enabled][value=" + privInfo[src].enabled + "]").prop("checked", true);
}
function initEvent() {
	$("#vin_source").off("change").change(function(e){
			src = getVinSourceIndex("#" + e.currentTarget.id);
			initValue();
			MJ.id = src;
			checkDependecy();
			});
	$("#btClearSelectedArea").click(function(){
			rect[0] = new Object();
			rect[activeRect].start_x = 0;
			rect[activeRect].start_y = 0;
			rect[activeRect].width = 0;
			rect[activeRect].height = 0;
			draw();
			});
	$("#selAreas").change(function(e){
			setActiveRect(e.target.value);
			});
	$("#btPrivacySave").on("click", function() {
			var bparam = "msubmenu=privacy_mask&action=apply&source=" + (src+1) + "&";
			var vparam ="" ;
			var value;
			value = $("[name=enabled]:checked").val();
			if( last_info[src].enabled != value ) {
			vparam += "enabled="  + value + "&";
			}
			for (var i=0; i< privInfo[src].rectangle.length ; i++) {
			if( last_info[src].rectangle[i].start_x != Math.round(rect[i+1].start_x * 100 / preview_out.width ) ){
			vparam += "start_x" + i + "=" + Math.round(rect[i + 1].start_x * 100 / preview_out.width ) + "&";
			}
			if( last_info[src].rectangle[i].start_y != Math.round(rect[i+1].start_y * 100 / preview_out.height) ) {
			vparam += "start_y" + i + "=" + Math.round(rect[i + 1].start_y * 100 / preview_out.height) + "&";
			}
			if( last_info[src].rectangle[i].width != Math.round(rect[i+1].width * 100 / preview_out.width ) ){
			vparam  += "width"   + i + "=" + Math.round(rect[i + 1].width * 100 / preview_out.width ) + "&";
			}
			if( last_info[src].rectangle[i].height != Math.round(rect[i+1].height * 100 / preview_out.height) ){
			vparam  += "height"  + i + "=" + Math.round(rect[i + 1].height * 100 / preview_out.height)  + "&";
			}
			}
			if( vparam == ""){
				settingFail(menu, getLanguage("msg_nothing_changed"));
				return ;
			}
			bparam = bparam + vparam ;
			debug('----- req'+bparam);
			$.ajax({
type : 'get',
url  : '/cgi-bin/admin/camera.cgi',
data : bparam,
cache	: false,
success : function(args) {
var pattern = /OK/g;
if( pattern.test(args) == true){
settingSuccess(menu);
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
$("#btPrivacyRestore").on("click", function(){
		$.extend(true, privInfo, last_info);
		getRecentValue(); 
		initValue();
		checkDependecy();
		if( capInfo["camera_module"] == "wonwoo_isp" || capInfo["camera_module"] == "ytot_isp" || capInfo["camera_module"] == "ov_isp" 
				|| ((capInfo["ptz_module"]=="af_licom_2812"||capInfo["ptz_module"]=="ricon_hv03610pb"||capInfo["ptz_module"]=="ricon_hd027135pb"||capInfo["ptz_module"]=="ricon_hd027135pb_2mp"||capInfo["ptz_module"]=="ricon_hd027135pb_8mp")
					&& (capInfo["oem"] == 19 || capInfo["oem"] == 20 || capInfo["oem"] == 21 || capInfo["oem"] == 10 || capInfo["oem"] == 11 || capInfo["oem"] == 13 || capInfo["oem"] == 25)) )
		{
		rect[0] = new Object();
		draw();
		}
		});

	if ( isIE_fix() == true ) {
		$("#motionOverlay").on("mousedown", function(e, ui) {
				if( privInfo[src].enabled == 0 ) return;
				if( drag ) {
				$("#motionOverlay").trigger("mouseup");
				} else {
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
				rect[0].width   = 0;
				rect[0].height  = 0;
				}
				});
		$("#motionOverlay").on("mouseup", function(e, ui) {
				if( privInfo[src].enabled == 0 ) return;
				$("#motionOverlay").off("mousemove");
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

				debug(rect[activeRect]);
				if(typeof(rect[activeRect].width) !== 'undefined') {
				rect[activeRect].start_x = rect[0].start_x;
				rect[activeRect].start_y = rect[0].start_y;
				rect[activeRect].width   = rect[0].width;
				rect[activeRect].height  = rect[0].height;
				}
				draw();
		});
		$("[name=enabled]").change(function(e){
				checkDependecy();
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
		$("[name=enabled]").change(function(e){
				checkDependecy();
				});



			}

}

function mouseDown(e) {
	  if( privInfo[src].enabled == 0 ) return;
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
	  if( privInfo[src].enabled == 0 ) return;
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

		    debug(rect[activeRect]);
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



function checkDependecy(){
	privInfo[src].enabled = $("[name=enabled]:checked").val();
	debug("checkdependency(): value = "+ privInfo[src].enabled);
	if( privInfo[src].enabled == 1) {
		$("#selAreas").removeAttr("disabled");
		setActiveRect($("#selAreas").val());
	}
	else {
		$("#selAreas").attr("disabled", "true");
		rect[0] = new Object();
		draw();
	}
}
function getRecentValue() {
	debug("getRecentValue()");
	for(var i=0,len=privInfo[src].rectangle.length; i<len; i++) {
		rect[i+1] = {};
		rect[i+1].start_x = privInfo[src].rectangle[i].start_x == 0 ? 0 : Math.round(privInfo[src].rectangle[i].start_x * preview_out.width  / 100 );
		rect[i+1].start_y = privInfo[src].rectangle[i].start_y == 0 ? 0 : Math.round(privInfo[src].rectangle[i].start_y * preview_out.height / 100 );
		rect[i+1].width   = Math.round(privInfo[src].rectangle[i].width   * preview_out.width  / 100);
		rect[i+1].height  = Math.round(privInfo[src].rectangle[i].height  * preview_out.height/ 100);
	}
	setActiveRect($("#selAreas").val());
}


function draw() { 
	debug('draw()');
	if( typeof(context) == "undefined" ) return;
	context.clearRect(0,0,canvas.width,canvas.height);
	if( capInfo["camera_module"] != "wonwoo_isp" && capInfo["camera_module"] != "ov_isp" /*&& capInfo["camera_module"] != "ytot_isp"  */
            && ((capInfo["ptz_module"]!="af_licom_2812" && capInfo["ptz_module"]!="ricon_hv03610pb" && capInfo["ptz_module"]!="ricon_hd027135pb" && capInfo["ptz_module"]!="ricon_hd027135pb_2mp" && capInfo["ptz_module"]!="ricon_hd027135pb_8mp" )
                || (capInfo["oem"] != 19 && capInfo["oem"] != 20 && capInfo["oem"] != 21 && capInfo["oem"] != 10 && capInfo["oem"] != 11 && capInfo["oem"] != 13 && capInfo["oem"] != 25)))
	{
		console.log("draw");
		for(var i=1,len=rect.length; i<len; i++)
		{
			if( typeof(rect[i].width) === 'undefined' || (rect[i].width ==0 && rect[i].height ==0)) 
				continue;

			context.beginPath();
			if( privInfo[src].enabled == 1) {
				context.fillStyle = "rgba(0,0,256, 0.5)";
			}
			else {
				context.fillStyle = "rgba(0,0,0, 0.5)";
				context.lineWidth = 2;
				context.strokeStyle = 'yellow';
				context.stroke();
			}
			context.fillRect(rect[i].start_x, rect[i].start_y, rect[i].width, rect[i].height);
		}
	}
	if( privInfo[src].enabled == 1 && typeof(rect[0].width) != 'undefined' )
	{
		context.beginPath();
		context.rect(rect[0].start_x, rect[0].start_y, rect[0].width, rect[0].height);
		context.fillRect(rect[0].start_x, rect[0].start_y, rect[0].width, rect[0].height);
		context.fillStyle = "rgba(0,0,256, 0.5)";
		context.lineWidth = 2;
		context.strokeStyle = 'yellow';
		context.stroke();
	}
}

function setActiveRect(index) {
	activeRect = Number(index)+1;
	debug("activeRect=" + activeRect );

	if( typeof(rect[activeRect]) != 'undefined' )
	{
		rect[0].start_x = rect[activeRect].start_x;
		rect[0].start_y = rect[activeRect].start_y;
		rect[0].width   = rect[activeRect].width;
		rect[0].height  = rect[activeRect].height;
	}	
	else
	{		
		rect[0] = {};
	}
	if( capInfo["camera_module"] != "wonwoo_isp" && capInfo["camera_module"] != "ov_isp" /*&& capInfo["camera_module"] != "ytot_isp"  */
			&& ((capInfo["ptz_module"]!="af_licom_2812" && capInfo["ptz_module"]!="ricon_hv03610pb"  && capInfo["ptz_module"]!="ricon_hd027135pb" && capInfo["ptz_module"]!="ricon_hd027135pb_2mp" && capInfo["ptz_module"]!="ricon_hd027135pb_8mp" )
				|| (capInfo["oem"] != 19 && capInfo["oem"] != 20 && capInfo["oem"] != 21 && capInfo["oem"] != 10 && capInfo["oem"] != 11 && capInfo["oem"] != 13 && capInfo["oem"] != 25)))
	{
		draw();
	}
}

