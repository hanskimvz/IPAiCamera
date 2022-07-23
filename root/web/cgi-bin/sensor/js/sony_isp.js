//var settingList = new Array;
//settingList = [ "ae_en", "exp_level", "a_flicker", "ae_meter", "awb_en", "awb_mode", "awb_method", "r_gain", "g_gain", "b_gain", "hue", "saturation", "brightness", "contrast", "sharpness", "dnr", "local_exp", "blc", "hdr", "hdr_level", "dnmode", "shutter", "sshutter", "mirror", "flip", "cam_gain","tdn_bw_level","tdn_color_level","tdn_resp"];
var items = {
	//menuTitle 		: [ items in menutitle ]
	"Image_Adjustment"	: [ "sharpness", "brightness", "contrast", "saturation", "hue"], 
	"Exposure_Settings"	: [ "ae_en", "exp_level", "ae_spot", "ae_shutter", "ae_iris", "ae_gain", "ae_bright", "sshutter", "gain_limit"],
	"Day_Night_Settings": [ "dnmode","dn_threshold", "tdn_bw_level", "tdn_color_level",  "color_hour", "color_min", "bw_hour", "bw_min", "hr_sens", "ir_c"  ],
	"Backlight_Switch"	: [ "blc", "hdr", "hdr_level" ],
	"White_Balance"		: [ "awb_mode", "awb_one_push", "r_gain", "b_gain" ],
	"Image_Enhancement"	: [ "dnr", "defog", "stabilizer", "hr_mode", "mirror", "flip" ],
//	"Video_Enhancement" : [ "a_flicker"],
};
var initialValue={};
var menu;
var source;
try {
	source = getVinSourceIndex("#vin_source");
}
catch (e){
	source = 0;
}
var pop_menu;
var pop_msg;
var firstInit = true;
/*  name 		: getElement
    operate		: check the DOM and set the value
    parameter	: 
    	- name	: DOM name or ID.
        - val	: setting value for DOM.  */
var debug_level=1;
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

	setSlider("brightness" , 0 , 100);
	setSlider("contrast"   , 0    , 100);
	setSlider("hue"        , 0  , 100);
	setSlider("saturation" , 0    , 100);	

	setSlider("exp_level"  , -7   , 7);
	setSlider("sharpness"  , 0    , 100);	
	
	setSlider("r_gain"     , 0 , 255);
	setSlider("b_gain"     , 0 , 255);
	
	setSlider("tdn_color_level"   , 60    , 120);
	setSlider("tdn_bw_level"   , 40    , 100);
	
	setSlider("dnr"   , 0    , 5);	
	
	if( CameraFunc['awb_mode'] == 4 )
		$("[class=div_awb_one_push]").show();
	else 
		$("[class=div_awb_one_push]").hide();
	
	
/*	if( capInfo['have_cds'] == 0 ) {
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
	}*/

	menu = $(".select_minor").attr("id");
	if( menu == "Exposure_Settings")
	{
		if( CameraFunc['hdr'] == 1 && $("#wdr_caution").length == 0 ) {
			$("#display_box").after("<div id='wdr_caution' class='wdr_caution' tkey='setup_wdr_caution'></div>");
			initLanguage();
		}
	}
	else{
		$("#wdr_caution").remove();
	}
/*------------------------------------------------------------*/
	var content="";
	for(var i=0; i < 24 ; i++)
	{
		content += "<option value="	+ i + ">" + i + "</option>";
	}
	getElement("color_hour").empty().append(content);
	getElement("bw_hour").empty().append(content);
	content="";
	for(var i=0; i < 60 ; i++)
	{
		content += "<option value="	+ i + ">";
		if( i < 10 ) 
			content += "0" + i;
		else
			content += i;
		content += "</option>";
	}
	getElement("color_min").empty().append(content);
	getElement("bw_min").empty().append(content)
/*------------------------------------------------------------*/	
/*	if( menu == "Backlight_Switch" && capInfo.board_chipset == "amba_s2l66") {
		if( $("#hdr option[value=2]").length == 0 ){
			$("#hdr").append("<option value='2'>"+getLanguage('setup_wdr_3x_on')+"</option>");
		}
	}
*/ 	
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
			obj.parent().find("label").text( initialValue[source][ID]);
			obj.slider("value", initialValue[source][ID]);
		}
		else if ( tag =="INPUT" ){
			type = obj.prop("type");
			if( type == "radio"){
				var obj_msg="[name=" + ID + "][value="+ initialValue[source][ID] + "]";
				$(obj_msg).prop("checked", true);
			}	
		}
		else if( tag == "SELECT"){
			obj.val(initialValue[source][ID]);
		}
	}
}
/*	define the dependence from the some function */
function dependence()    
{
	checkWhiteBalance();
	checkExposureMode();
	checkTDNMode();
}
function checkWhiteBalance(){
	if( $("[name=awb_mode]").val()  == 5 ) {  
		disabledSlider("r_gain", 0) ;
		disabledSlider("b_gain", 0) ;
	}
	else{
		disabledSlider("r_gain", 1) ;
		disabledSlider("b_gain", 1) ;
	}
}
function checkExposureMode(){
	$("#shutter_tr").hide();
	$("#ae_iris_tr").hide();
	$("#ae_gain_tr").hide();	
	$("#ae_bright_tr").hide();
	
	if( $("[name=ae_en]").val() == 1 ){
		$("#shutter_tr").show();
		$("#ae_iris_tr").show();
		$("#ae_gain_tr").show();
	}
	else if( $("[name=ae_en]").val() == 2){
		$("#shutter_tr").show();
	}
	else if( $("[name=ae_en]").val() == 3){
		$("#ae_iris_tr").show();
	}
	else if( $("[name=ae_en]").val() == 4 ){
		$("#ae_bright_tr").show();
	}	
}
function checkHdr(){
	if( $("[name=hdr]:checked").val() == 0 ) {   //Schedule
		
	}
}
function checkTDNMode()
{
	$("[class=iSchedule]").hide();
	$("[class=dn_threshold]").hide();
	if( $("[name=dnmode]:checked").val() == 3 ) {   //Schedule
		$("[class=iSchedule]").show();
		$("[class=dn_threshold_tr]").hide();
	}
	else
	{
		$("[class=iSchedule]").hide();
		$("[class=dn_threshold_tr]").show();
	}
}
function setEvent( func, ui ){	
	if( ui == "slidechange"){
		getElement(func).on( ui, function(){
			var value = getElement(func).slider("value")
			_ajax( func , value);
		}); 
	}
	else if( ui == "click"){	
		getElement(func).on(ui, function(){
			if( func == "awb_one_push" ){
				var value ;
				
				if( CameraFunc[source]['awb_one_push'] == 0) value = 1 ;
				else value = 0 ;
				
				console.log("CameraFunc[source]['awb_one_push']" + value);
				_ajaxs(func, value);
			}else {
				var value = $("[name="+ func +"]:checked").val();
				_ajax(func, value);				
			}			
		});	
	}
	else if( ui == "change"){
		getElement(func).on(ui, function(){
			var value = getElement(func).val();
			_ajax(func, value);
		});
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
		setEvent( "sharpness" , "slidechange" );
		setEvent( "brightness" , "slidechange" );
		setEvent( "contrast" , "slidechange" );
		setEvent( "saturation" , "slidechange" );
		setEvent( "hue" , "slidechange" );		
	}
	else if( menu == "Exposure_Settings")
	{
		getElement("ae_en").on("change", function(){
			var value = getElement("ae_en").val();
			_ajax("ae_en", value);
			checkExposureMode();
		});
		setEvent( "ae_en" , "change" );
		setEvent( "exp_level" , "slidechange" );
		setEvent( "ae_shutter" , "change" );
		setEvent( "ae_iris" , "change" );
		setEvent( "ae_gain" , "change" );
		setEvent( "ae_bright" , "change" );
		setEvent( "sshutter" , "change" );	
		setEvent( "gain_limit" , "change" );		
	} 
	else if( menu =="Day_Night_Settings")
	{
		getElement("dnmode").on("click", function(){
			var value = $("[name=dnmode]:checked").val();
			_ajax("dnmode", value);
			checkTDNMode();
		});
		setEvent( "tdn_bw_level" , "slidechange" );
		setEvent( "tdn_color_level" , "slidechange" );
		setEvent( "color_hour" , "change" );
		setEvent( "color_min" , "change" );
		setEvent( "bw_hour" , "change" );
		setEvent( "bw_min" , "change" );
		setEvent( "hr_sens" , "click" );	
		setEvent( "ir_c" , "click" );
	}
	else if( menu =="Backlight_Switch")
	{
		getElement("hdr").on("change", function(){
			var value = getElement("hdr").val();
			_ajax("hdr", value);
//			checkWhiteBalance();
		});
		setEvent( "hdr_level" , "change" );	
		setEvent( "blc" , "click" );		
	}
	else if( menu == "White_Balance" )
	{	
		getElement("awb_mode").on("change", function(){
			var value = getElement("awb_mode").val();
			_ajax("awb_mode", value);
			checkWhiteBalance();
		});
		setEvent( "r_gain" , "slidechange" );
		setEvent( "b_gain" , "slidechange" );
		setEvent( "awb_one_push" , "click" );
		
	}
	else if( menu =="Image_Enhancement" )
	{
		setEvent( "dnr" , "slidechange" );
		setEvent( "defog" , "change" );
		setEvent( "stabilizer" , "click" );
		setEvent( "hr_mode" , "click" );	
		setEvent( "mirror" , "click" );
		setEvent( "flip" , "click" );

	}

	$("#btRestore").off("click").click(function(){
		onClickCameraRestore();
		dependence();
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
	commonCreateSourceSelectBox("#vin_source");
	$.extend(true, initialValue , CameraFunc);
}

function init()
{
	if( firstInit ) return ;

	debug("init()");
	console.log("ASD");
	menu = $(".select_minor").attr('id');

	initUI();	
	initValue();
	initEvent();
	dependence();
}
function _ajaxs(param, data)
{	
	var cmd = "";
	
	if( param == "awb_one_push" ){
		cmd = "setwbpreset"; 
		cmd += "&value=" + data;
	}
	else cmd = "apply" +"&source="+source+ param;
	
	if(cmd != null || cmd != undefined)	
	{
		pop_menu = getLanguage(menu);
		cmd = "msubmenu=camera&action="+ cmd 
		
		Disabled(true);

		$.ajax(
		{
			type : 'get',
			url  : '/cgi-bin/admin/camera.cgi',
			data : cmd,
			async : false,
			success : function(response){
				var OK = /OK/;
				if(OK.test(response)) {
					settingSuccess(pop_menu, null);
					if( CameraFunc['awb_mode'])	checkWhiteBalance();
					if( param == "awb_one_push" )	CameraFunc['awb_one_push']  = data;
					Disabled(false);
					refreshMenuContent();
				} else {
					settingFail(pop_menu, null);
					Disabled(false);
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
	CameraFunc[source][param] = Number(data);	
	return ;  
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


	if( menu == "Day_Night_Settings") {
		if( CameraFunc[source].dnmode == 5 && (CameraFunc[source].bw_hour  * 100 + CameraFunc[source].bw_min == CameraFunc[source].color_hour  * 100 + CameraFunc[source].color_min)) {
			pop_msg = getLanguage("setup_dn_sched_dup");
			settingFail(pop_menu, pop_msg);
			return ;
		}
	}
	
	//console.log(cmdCounter);
	// ===========  nothing change check ===========
	for( var i = 0 ; i < cmdCounter ; i++)
	{
		if( CameraFunc[source][ items[menu][i] ] != initialValue[source][items[menu][i]])
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
		if( CameraFunc[source][ items[menu][i] ] != initialValue[source][items[menu][i]])
		{
			data += "&" + items[menu][i] + "=" +CameraFunc[source][ items[menu][i] ];
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
			obj.parent().find("label").text( initialValue[source][ID]);
			obj.slider("value", initialValue[source][ID]);
		}
		else if ( tag =="INPUT" ){
			type = obj.prop("type");
			if( type == "radio"){
				obj = $("[name=" + ID + "][value=" + initialValue[source][ID] + "]")
				obj.prop("checked", true);
				obj.trigger("click");
			}	
		}
		else if( tag == "SELECT"){
			obj.val(initialValue[source][ID]).trigger('change');
		}
	}
	$.extend(true, CameraFunc, initialValue);
	Disabled(false);
}
$(document).ready( function(){
	debug("ducmuent.read");
	onLoadPage();
//	init();
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
