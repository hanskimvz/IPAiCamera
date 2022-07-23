var settingList = new Array;
settingList = [ "ae_en", "exp_level", "a_flicker", "ae_meter", "awb_en", "awb_mode", "awb_method", "r_gain", "g_gain", "b_gain", "hue", "saturation", "brightness", "contrast", "sharpness", "mctf3dnr", "local_exp", "blc", "hdr", "dnmode", "shutter", "sshutter", /* "mirror",*/ "flip", "cam_gain","tdn_bw_level","tdn_color_level","tdn_resp"];
var items = {
	//menuTitle 		: [ items in menutitle ]
	"Image_Adjustment"	: [ "sharpness", "brightness", "contrast", "saturation", "hue"], 
	"Exposure_Settings"	: [ "ae_en", "exp_level", "local_exp", "ae_meter", "shutter", "sshutter" ],
	"Day_Night_Settings": [ "dnmode", "tdn_bw_level", "tdn_color_level", "tdn_resp" ],
	"Backlight_Switch"	: ["blc", "hdr"],
	"White_Balance"		: [ "awb_en", "awb_method", "awb_mode", "r_gain", "g_gain", "b_gain" ],
	"Image_Enhancement"	: [ "mctf3dnr", /*"mirror",*/ "flip"],
	"Video_Enhancement" : ["a_flicker"],
};
var initialValue={};
var menu;
var pop_menu;
var pop_msg;

var firstInit = true;
/*  name 		: getElement
    operate		: check the DOM and set the value
    parameter	: 
    	- name	: DOM name or ID.
        - val	: setting value for DOM.  */
var debug_level=0;
function debug(str){ if( debug_level ){ console.log("[DEBUG] " + str + "\n"); }};
function getElement(name, val)
{
	var type = $("[name=" + name + "]").prop("tagName");

	if(type == "SELECT")
	{
		return $("select[name=" + name + "]");
	}
	else if(type == "INPUT")
	{
		type = $("[name="+ name + "]").attr('type');

		if(type == 'radio')
		{
			if(val == null)
				return $("input:radio[name=" + name + "]");

			return $("input:radio[name=" + name + "][value=" + val +"]");
		}
		else // (type == 'text' || type == 'range' )  
		{
			return $("[name=" + name + "]");
		}
	}
	else
		return $("[name=" + name + "]");
}

/*  name       : initUI
	opertation : initialize sensor UI */
function initUI() {
	debug("initUI");
	// 			  name     , min  , max
	setSlider("exp_level"  , 25   , 400);
	setSlider("sharpness"  , 0    , 11);
	setSlider("brightness" , -255 , 255);
	setSlider("contrast"   , 0    , 128);
	setSlider("hue"        , -15  , 15);
	setSlider("saturation" , 0    , 255);
	setSlider("r_gain"     , 1000 , 2000);
	setSlider("g_gain"     , 1000 , 2000);
	setSlider("b_gain"     , 1000 , 2000);
	setSlider("mctf3dnr"   , 0    , 11);
	
	if( capInfo['have_cds'] == 0 ) {
		$("#iColor_level").remove();
		$("#iBw_level").remove();
	} else {
		var cmd;
		if( $(".select_minor").attr("id") == "Day_Night_Settings"){
			cmd="";
			for(var i = 0 ; i < 11 ; i++) {
				cmd += "<option value=" +  i + ">"+ i +"</option>"
			}
			getElement('tdn_color_level').empty().append(cmd);
			getElement('tdn_bw_level').empty().append(cmd);
		}
	}
}

function initValue()
{
	debug('initValue()');
	var ID, tag, obj;
	for( var i=0; i<items[menu].length;i++) {
		ID=items[menu][i];
		obj = $("[name=" + ID +"]");
		tag = obj.prop("tagName");
		type = obj.attr("type");
		if( tag == "DIV" ){ //slider
			obj.parent().find("label").text( CameraFunc[ID]);
			obj.slider("value", CameraFunc[ID]);
		}
		else if ( tag =="INPUT" ){
			type = obj.prop("type");
			if( type == "radio"){
				var obj_msg="[name=" + ID + "][value="+ CameraFunc[ID] + "]";
				$(obj_msg).prop("checked", true);
			}	
		}
		else if( tag == "SELECT"){
			obj.val(CameraFunc[ID]);
		}
	}
}
/*	define the dependence from the some function */
function dependence()    
{
	if( CameraFunc.ae_en ) {
		$("[name=shutter").prop("disabled", true);
	} else {
		$("[name=shutter").prop("disabled", false );
	}
	if( !CameraFunc.awb_en ) {
		$("[name=awb_mode]").prop("disabled", true);		
		disabledSlider("r_gain", 1) ;
		disabledSlider("g_gain", 1) ;
		disabledSlider("b_gain", 1) ;
	} else {
		if ( CameraFunc.awb_mode == 10 ) { // custom
			disabledSlider("r_gain", 0) ;
			disabledSlider("g_gain", 0) ;
			disabledSlider("b_gain", 0) ;
		} else {
			disabledSlider("r_gain", 1) ;
			disabledSlider("g_gain", 1) ;
			disabledSlider("b_gain", 1) ;
		}
	}

	if( typeof(CameraFunc.hdr) != "undefined" ){
		var hdr_dependency = CameraFunc.hdr == 1 ? true : false;
		if( $(".select_minor").attr("id") == "Backlight_Switch"){
			getElement("blc").prop("disabled", hdr_dependency);
		}
		if( $(".select_minor").attr("id") == "Exposure_Settings"){
			getElement("ae_meter").prop("disabled", hdr_dependency || CameraFunc.ae_en);
			getElement("local_exp").prop("disabled", hdr_dependency);
			disabledSlider("exp_level", hdr_dependency);
		}
	}
}
/* define the event from the DOM */
function initEvent(){
	debug('initEvent()');
	//FOR EXPOSURE
	menu = $(".select_minor").attr("id");
	pop_menu = getLanguage(menu);
	debug(menu);

	if( menu == "Image_Adjustment" )
	{	
		getElement("sharpness").on("slidechange", function(){
			var value = getElement("sharpness").slider("value")
			_ajax('sharpness', value);
		});    
		getElement("brightness").on("slidechange", function(){
			var value = getElement("brightness").slider("value");
			_ajax('brightness', value);
		});
		getElement("contrast").on("slidechange", function(){
			var value = getElement("contrast").slider("value");
			_ajax('contrast', value);
		});
		getElement("saturation").on("slidechange", function(){
			var value = getElement("saturation").slider("value");
			_ajax('saturation', value);
		});
		getElement("hue").on("slidechange", function(){
			var value = getElement("hue").slider("value");
			_ajax('hue', value);
		});
	}
	else if( menu == "Exposure_Settings")
	{
		getElement("ae_en").on("click",function(){
			var value = $("[name=ae_en]:checked").val();
			_ajax('ae_en', value);
		});
		getElement("exp_level").on("slidechange", function(){
			var value = getElement("exp_level").slider("value")
			_ajax('exp_level', value);
		});
		getElement("local_exp").on("change", function(){
			var value = getElement("local_exp").val();
			_ajax('local_exp', value);
		});
		getElement("ae_meter").on("change", function(){
			var value = getElement("ae_meter").val();
			_ajax("ae_meter", value);
		});
		getElement("shutter").on("change", function(){
			var value = getElement("shutter").val();
			_ajax("shutter", value);
		});
		getElement("sshutter").on("click",function(){
			var value = $("[name=sshutter]:checked").val();
			_ajax('sshutter', value);
		});
	} 
	else if( menu =="Day_Night_Settings")
	{
		getElement('dnmode').on("click", function(event){
			var value = $('[name=dnmode]:checked').val();
			_ajax("dnmode", value);
		});
		getElement("tdn_bw_level").on("change", function(){
			var value = getElement("tdn_bw_level").val();
			_ajax("tdn_bw_level", value);
		});
		getElement("tdn_color_level").on("change", function(){
			var value = getElement("tdn_color_level").val();
			_ajax("tdn_color_level", value);
		});
		getElement("tdn_resp").on("change", function(){
			var value = getElement("tdn_resp").val();
			_ajax('tdn_resp', value);
		});
	}
	else if( menu =="Backlight_Switch")
	{
		getElement("blc").on("click",function(){
			var value = $("[name=blc]:checked").val();
			_ajax('blc', value);
		});
		getElement("hdr").on("change",function(){
			var value = $("#hdr").val();
			_ajax('hdr', value);
		});
	}
	else if( menu == "White_Balance" )
	{
		debug('menu = white_balance');
		getElement("awb_en").on("click",function(){
			var value = $("[name=awb_en]:checked").val();
			_ajax('awb_en', value);
		});
		getElement("awb_method").on("change", function(){
			var value = getElement("awb_method").val();
			_ajax('awb_method', value);
		});
		getElement("awb_mode").on("change", function(){
			var value = getElement("awb_mode").val();
			_ajax('awb_mode', value);
		});
		getElement("r_gain").on("slidechange", function(){
			var value = getElement("r_gain").slider("value");
			_ajax("r_gain", value);
		});
		getElement("g_gain").on("slidechange", function(){
			var value = getElement("g_gain").slider("value");
			_ajax("g_gain", value);
		});
		getElement("b_gain").on("slidechange", function(){
			var value = getElement("b_gain").slider("value");
			_ajax("b_gain", value);
		});
	}
	else if( menu =="Image_Enhancement" )
	{
		getElement("mctf3dnr").on("slidechange", function(){
			var value = getElement("mctf3dnr").slider('value'); 
			_ajax('mctf3dnr', value);
		});
		/*
		getElement("mirror").on("click", function(){
			var value = $("[name=mirror]:checked").val();
			_ajax("mirror", value);
		});
		*/
		getElement("flip").on("click", function(){
			var value = $("[name=flip]:checked").val();
			_ajax("flip", value);
		});
	}
	else if( menu =="Video_Enhancement")
	{
		getElement("a_flicker").on("click",function(){
			var value = $("[name=a_flicker]:checked").val();
			_ajax('a_flicker', value);
		});
	}
	$("#btRestore").off("click").click(function(){
		onClickCameraRestore();
	});
	$("#btSave").off("click").click(function(){
		saveCurrentSetting();
	});
	$("#btDefault").off("click").click(function() {
		onClickCameraDefault();
	});
}

function onLoadPage()
{
	$.extend(true, initialValue , CameraFunc);
}

function init()
{
	if( firstInit ) return ;

	debug("init()");
	menu = $(".select_minor").attr('id');

	initUI();
	dependence();
	initValue();
	initEvent();
}
function _ajaxs(cmd)
{
	if(cmd != null || cmd != undefined)	
	{
		pop_menu = getLanguage(menu);
		cmd = "msubmenu=camera&action=apply" + cmd;
		Disabled(true);
		$.ajax(
		{
			type : 'get',
			url  : '/cgi-bin/admin/camera.cgi',
			data : cmd,
			async : false,
			success : function(response){
				var OK = /OK/;
				if(OK.test(response)) 
				{
					settingSuccess(pop_menu, null);
					Disabled(false);
					refreshMenuContent();
				}
				else
				{
					settingFail(pop_menu, null);
				}
			},
			error	: function(){
				Disabled(false);
				settingFail(pop_menu, null);
			}
		});
	}
}
function _ajax(param, data, slider, cmd)
{
	if( cmd == "apply")
	{
		CameraFunc[param] = data;
	}
	else // preview or null
	{
		cmd = "preview";
		if( CameraFunc[param] == data ) {
			return ;
		}
		else {
			CameraFunc[param] = Number(data);
		}
	}
	var val = "msubmenu=camera&action=" + cmd + "&"+param + "=" + data;

	if(slider != null)
		getElement(slider).html(data);
	
	Disabled(true);
	$.ajax(
		{
			type : 'get',
			url  : '/cgi-bin/admin/camera.cgi',
			async : false, 
			data : val,
			success : onSuccess,
			error	: onFail
		}
	);
}

function onSuccess(req)
{
	Disabled(false);
	dependence();
}

function onFail(req)
{
	Disabled(false);
	dependence();
}

function saveCurrentSetting()
{
	debug("saveCurrentSetting()");
	var cmd = "apply";
	
	pop_menu = getLanguage(menu);

	var cmdCounter = items[menu].length;
	var change = 0;
	var data = '';
	
	//console.log(cmdCounter);
	// ===========  nothing change check ===========
	for( var i = 0 ; i < cmdCounter ; i++)
	{
		if( CameraFunc[ items[menu][i] ] != initialValue[items[menu][i]])
			change++;
	}
	if( change == 0 ) 
	{
		pop_msg = getLanguage("msg_nothing_changed");
		settingFail(pop_menu, pop_msg);
		return ;
	}
	//============================================

	Disabled(true);
	change = 0;
	for( var i = 0 ; i < cmdCounter ; i++)
	{
		if( CameraFunc[ items[menu][i] ] != initialValue[items[menu][i]])
		{
			data += "&" + items[menu][i] + "=" +CameraFunc[ items[menu][i] ];
		}
	}
	_ajaxs(data);
}

function onClickCameraRestore()
{
	debug("onClickCameraRestore");
	Disabled(true);
	var type, ID, tag;
	for( var i=0; i<items[menu].length;i++) {
		ID=items[menu][i];
		obj = $("[name=" + ID +"]");
		tag = obj.prop("tagName");
		if( tag == "DIV" ){ //slider
			obj.parent().find("label").text( initialValue[ID]);
			obj.slider("value", initialValue[ID]);
		}
		else if ( tag =="INPUT" ){
			type = obj.prop("type");
			if( type == "radio"){
				obj = $("[name=" + ID + "][value=" + initialValue[ID] + "]")
				obj.prop("checked", true);
				obj.trigger("click");
			}	
		}
		else if( tag == "SELECT"){
			obj.val(initialValue[ID]).trigger('change');
		}
	}
	$.extend(true, CameraFunc, initialValue);
	Disabled(false);
}
$(document).ready( function(){
	debug("ducmuent.read");
	onLoadPage();
	init();
	firstInit = false;
});

function onClickCameraDefault()
{
	Disabled(true);
	var menunum;
	switch(menu)
	{
	case "Image_Adjustment":
			menunum = 0 ;
			break;		
	case "Exposure_Settings":
			menunum = 1 ;
			break;
	case "Day_Night_Settings":
			menunum = 2 ;
			break;
	case "Backlight_Switch":
			menunum = 3 ;
			break;
	case "White_Balance":
			menunum = 4 ;
			break;		
	case "Image_Enhancement":
			menunum = 5 ;
			break;
	case "Video_Enhancement":
			menunum = 6 ;
			break;
	}
	function RestoreValue()
	{
		$("#initValue").load("setup_camera_init.cgi");
		Disabled(false);
		refreshMenuContent();
	}
	$.ajax({
		type:'get',
		url: "/cgi-bin/admin/camera.cgi?msubmenu=camera&action=default&menu=" + menunum ,
		success: RestoreValue,
		error: onFail
	});

}
