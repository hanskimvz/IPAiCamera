//var settingList = new Array;
//settingList = [ "ae_en", "exp_level", "a_flicker", "ae_meter", "awb_en", "awb_mode", "awb_method", "r_gain", "g_gain", "b_gain", "hue", "saturation", "brightness", "contrast", "sharpness", "dnr", "local_exp", "blc", "hdr", "hdr_level", "dnmode", "shutter", "sshutter", "mirror", "flip", "cam_gain","tdn_bw_level","tdn_color_level","tdn_resp"];
var items = {
	//menuTitle 		: [ items in menutitle ]
	"Image_Adjustment"	: [ "sharpness", "brightness", "saturation"], 
	"Exposure_Settings"	: [ "ae_en", "ae_shutter", "ae_gain_limit", "sshutter"],
	"Day_Night_Settings": [ "dnmode", "tdn_bw_level", "tdn_color_level", "color_hour", "color_min", "bw_hour", "bw_min", "led_mode", "led_satu"  ],
	"Backlight_Switch"	: [ "hdr", "hdr_level" ],
	"White_Balance"		: [ "awb_mode", "wb_preset", "kelvin", "r_gain", "b_gain" ],
	"Image_Enhancement"	: [ "dnr", "defog", "defog_level", "deblur", "mirror", "flip" ],
	"Video_Enhancement" : [ "a_flicker"],
	"LV_Filter_Operation" : [ "filter_operation", "filter_mode",  "filter_enhance" ],
	"LV_Filter_Settings" : [ "filter_area", "enhance_level_a", "enhance_level_m", "night_detect", "color_enhance", "3dnr" , "cb_gain", "cr_gain"],	//"cb_offset", , "cr_offset",
	"LV_Filter_Mode" : [  "filter_dn_mode", "filter_hw_dn_mode",  "filter_enable_threshold", "filter_disable_threshold" , "filter_non_time_setting_mode", "filter_disable_str_setting_hour", "filter_disable_str_setting_min"
	                      ,"filter_disable_end_setting_hour", "filter_disable_end_setting_min"],	//"cb_offset", , "cr_offset",
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
function setSlider1(name, min, max)
{
	var obj = $("#" + name );
	if( obj.length == 0)
	{
		obj = $("[name=" + name + "]");   
		if (obj .length == 0)
		{
			return false;   
		}
	} 
	if( obj.next().prop("tagname") != "BUTTON" && obj.next().text() != "+")
		obj.before("<button>-</button>").after("<button>+</button>");
	obj.slider({
		min: min,
		max: max,
		slide : function (event, ui){			   
			if( obj.selector == "#filter_enable_threshold" ){ 
				if( ui.value < $("#filter_disable_threshold").slider("value") )
				{			
					return false;
				}
			}
			else if( obj.selector == "#filter_disable_threshold" ){ 
				if( ui.value > $("#filter_enable_threshold").slider("value") )
				{			
					return false;
				}
			}
			obj.next().next().text( ui.value );
		}
	});
	obj.next().on("click", function(){
		if(  obj.selector == "#filter_disable_threshold"){
			if( obj.slider("value") >= $("#filter_enable_threshold").slider("value")){
					return 0; 
			}
		}
		var value = obj.slider("value");
		obj.slider("value", ++value);
		obj.next().next().text( obj.slider("value") );
	});
	obj.prev().on("click", function(){
		if(  obj.selector == "#filter_enable_threshold"){
			if( obj.slider("value") <= $("#filter_disable_threshold").slider("value")){
					return 0; 
			}
		}

		var value = obj.slider("value");
		obj.slider("value", --value);    
		obj.next().next().text( obj.slider("value") );
	});
	return true;
}
function checkHwfilter(obj, option)
{
	function judgeHwfilter(val){
		$("[name=hwdnmode][value="+ val +"]").prop("checked", true)	
	}
	
	function check()
	{
			try{
				$.ajax({
				url  : '/cgi-bin/result',
				data : "msubmenu=event&action=view",
				cache   : false,
				async: true,
				success : function(ret){
					var tmp = ret.trim().split('\n');
					for( var i=0 ; i<20 ; i++){
						if(tmp[i] == undefined) continue ;
						if( tmp[i].split('=')[0].trim() == "HwFilterStatus" ){	
							var tmp2 = tmp[i].split('=')[1];  
							judgeHwfilter(tmp2);
						}
					}
					clearTimeout(timeout);
					timeout = setTimeout(check, 1000);	
		
					},
				}); 
			}
			catch(exception)
			{
				console.log(exception);
			}			
	}
	clearTimeout(timeout);
	if( camera_init_flag == true )	timeout = setTimeout(check, 4000);		
	else check();

}

/*  name       : initUI
	opertation : initialize sensor UI */
function initUI() {
	debug("initUI");

	setSlider("sharpness"  , 0    , 100);	
	setSlider("brightness" , 0 , 100);
	setSlider("saturation" , 0    , 100);	

	setSlider("tdn_bw_level"   , 0    , 20);
	setSlider("tdn_color_level"   , 0    , 20);
	
	setSlider("led_satu"  , 0   , 20);	
		
	setSlider("r_gain"     , 0 , 20);
	setSlider("b_gain"     , 0 , 20);
		

	setSlider("enhance_level_a"   , 1    , 10);
	setSlider("enhance_level_m"   , 1    , 10);
	
	setSlider("night_detect"   , 1    , 10);
	setSlider("color_enhance"   , 1    , 10);
	setSlider("3dnr"   , 1    , 10);
	setSlider("cb_gain"   , 1    ,100);
	setSlider("cr_gain"   , 1    , 100);	

	setSlider1("filter_enable_threshold"   , 0    ,255);
	setSlider1("filter_disable_threshold"   , 0    , 255);	
	
	if( CameraFunc[source]['awb_mode'] == 3 )
		$("[class=div_wb_preset]").show();
	else 
		$("[class=div_wb_preset]").hide();	
	
	if( CameraFunc[source]['filter_mode'] == 1){
		$("[class=div_enhance_level_m]").show();
		$("[class=div_enhance_level_a]").hide();
	}	
	else {
		$("[class=div_enhance_level_a]").show();
		$("[class=div_enhance_level_m]").hide();
	}
	menu = $(".select_minor").attr("id");
	if( menu == "Exposure_Settings")
	{
		if( CameraFunc[source]['hdr'] == 1 && $("#wdr_caution").length == 0 ) {
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
	getElement("filter_disable_str_setting_hour").empty().append(content);
	getElement("filter_disable_end_setting_hour").empty().append(content);
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
	getElement("bw_min").empty().append(content);
	getElement("filter_disable_str_setting_min").empty().append(content);
	getElement("filter_disable_end_setting_min").empty().append(content);
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
	checkHdr();
	checkExposureMode();
	checkTDNMode();
	checkFilterMode();
	checkHWFilterSettingMode();
	checkHWFilterMode();
	checkDefog();
	console.log("Dependence");
}
function checkWhiteBalance(){
	if( $("[name=awb_mode]").val() == 4 ) {   
		disabledSlider("r_gain", 0) ;
		disabledSlider("b_gain", 0) ;
		$("[name=kelvin]").attr("disabled", false );	
	}
	else{
		disabledSlider("r_gain", 1) ;
		disabledSlider("b_gain", 1) ;
		$("[name=kelvin]").attr("disabled", true );	
	}
	
	if( CameraFunc[source]['wb_preset'] == 1 )
		$("[name=wb_preset]").css("background", "#23203F")
	else
		$("[name=wb_preset]").css("background", "#3d377a")
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
	if( $("[name=hdr]").val() == 3 ) {   
		$("[name=hdr_level]").attr("disabled", false);		
	}else
		$("[name=hdr_level]").attr("disabled", true);
		
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
function checkFilterMode(){
	console.log("checkFilterMode");
	if( $("[name=filter_operation]:checked").val() == 0 ) {   
		$("[name=filter_enhance]").attr("disabled", true );
		$("[name=filter_mode]").attr("disabled", true );
	}
	else
	{
		$("[name=filter_enhance]").attr("disabled", false );
		$("[name=filter_mode]").attr("disabled", false );
	}		
//	$("#hwdnmode").find("*").prop("disabled", true );
}
function checkHWFilterSettingMode(){
	console.log("checkHWFilterMode:"+ CameraFunc[source]["filter_operation"]);
	if( CameraFunc[source]["filter_operation"] == 0){
		$("[name=filter_area]").attr("disabled", true );
		disabledSlider("enhance_level_a", 1) ;
		disabledSlider("enhance_level_m", 1) ;
//		disabledSlider("night_detect", 1) ;
		disabledSlider("color_enhance", 1) ;
		disabledSlider("3dnr", 1) ;
		disabledSlider("cb_gain", 1) ;
		disabledSlider("cr_gain", 1) ;
	}	
	else{
		$("[name=filter_area]").attr("disabled", false );
		disabledSlider("enhance_level_a", 0) ;		
		disabledSlider("enhance_level_m", 0) ;
		disabledSlider("color_enhance", 0) ;
		disabledSlider("3dnr", 0) ;		
		disabledSlider("cb_gain", 0) ;
		disabledSlider("cr_gain", 0) ;
	}		
	if( CameraFunc[source]['filter_enhance'] == 0 )   disabledSlider("night_detect", 0) ;
	else disabledSlider("night_detect", 1) ;		
}
function checkHWFilterMode(){
	if(  $("[name=filter_hw_dn_mode]:checked").val() == 0){
		$("[name=filter_dn_mode]").attr("disabled", true );
		disabledSlider("filter_enable_threshold", 1) ;
		disabledSlider("filter_disable_threshold", 1) ;
		$("[name=filter_non_time_setting_mode]").attr("disabled", true );
		$("[class=tr_nonsettingtime]").find("*").attr("disabled", true );	
	}	
	else{
		$("[name=filter_dn_mode]").attr("disabled", false );
		
		if( $("[name=filter_dn_mode]:checked").val() == 2){		
			disabledSlider("filter_enable_threshold", 0) ;		
			disabledSlider("filter_disable_threshold", 0) ;
			$("[name=filter_non_time_setting_mode]").attr("disabled", false );
			$("[class=tr_nonsettingtime]").find("*").attr("disabled", false );				
		}
		else{
			disabledSlider("filter_enable_threshold", 1) ;		
			disabledSlider("filter_disable_threshold", 1) ;	
			$("[name=filter_non_time_setting_mode]").attr("disabled", true );
			$("[class=tr_nonsettingtime]").find("*").attr("disabled", true );	
		}
	}		
	
	if( $("[name=filter_non_time_setting_mode]:checked").val() == 0)
		$("[class=tr_nonsettingtime]").find("*").attr("disabled", true );	
	else 
		$("[class=tr_nonsettingtime]").find("*").attr("disabled", false );	
}
function checkDefog(){
	if(  $("[name=defog]:checked").val() == 2){
		$("[class=defog_level]").show();
	}
	else {
		$("[class=defog_level]").hide();
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
		if( func == "wb_preset" ){
			getElement(func).on(ui, function(){				
				var value = 1 ;
				if( CameraFunc[source]['wb_preset'] == 0) value = 1 ;
				else value = 0 ;
				_ajaxs(func, value);
			});			
		}		
/*		else if( func == "hwdnmode" ){
			getElement(func).on(ui, function(){				
				var value = $("[name=hwdnmode]:checked").val() ;
				_ajaxs(func, value);
			});			
		}	*/	
		else{
			getElement(func).on(ui, function(){				
				var value = $("[name="+ func +"]:checked").val();
				_ajax(func, value);
			});
		}
	}
	else if( ui == "change"){
		getElement(func).on(ui, function(){
			var value = getElement(func).val();
			_ajax(func, value);
		});
	}
	else{
		
		
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
		console.log("Image_Adjustment12");
		setEvent( "sharpness" , "slidechange" );
		setEvent( "brightness" , "slidechange" );
		setEvent( "saturation" , "slidechange" );

	}
	else if( menu == "Exposure_Settings")
	{
		getElement("ae_en").on("change", function(){
			var value = getElement("ae_en").val();
			_ajax("ae_en", value);
			checkExposureMode();
		});
		setEvent( "ae_shutter" , "change" );
		setEvent( "ae_gain_limit" , "change" );
		setEvent( "sshutter" , "change" );		
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
		setEvent( "led_mode" , "click" );	
		setEvent( "led_satu" , "slidechange" );
	}
	else if( menu =="Backlight_Switch")
	{

		getElement("hdr").on("change", function(){
			var value = getElement("hdr").val();
			_ajax("hdr", value);
			checkHdr();
		});
		setEvent( "hdr_level" , "change" );	
	}
	else if( menu == "White_Balance" )
	{	
		getElement("awb_mode").on("change", function(){
			var value = getElement("awb_mode").val();
			_ajax("awb_mode", value);
			checkWhiteBalance();
		});
		setEvent( "kelvin" , "change" );
		setEvent( "r_gain" , "slidechange" );
		setEvent( "b_gain" , "slidechange" );		
		setEvent( "wb_preset" , "click" );
	}
	else if( menu =="Image_Enhancement" )
	{
		setEvent( "dnr" , "change" );
		getElement("defog").on("click", function(){
			var value = $("[name=defog]:checked").val();
			_ajax("defog", value);
			checkDefog();
		});
		setEvent( "defog_level" , "change" );
		setEvent( "deblur" , "click" );	
		setEvent( "mirror" , "click" );
		setEvent( "flip" , "click" );
	}
	else if( menu =="Video_Enhancement" )
	{
		setEvent( "a_flicker" , "click" );
	}	
	else if( menu =="LV_Filter_Operation" )
	{
		getElement("filter_operation").on("click", function(){
			var value = $("[name=filter_operation]:checked").val();
			_ajax("filter_operation", value);
			checkFilterMode();
		});		
		setEvent( "filter_mode" , "click" );		
		setEvent( "filter_enhance" , "click" );
		
/*		setEvent( "cb_offset" , "slidechange" );
		setEvent( "cb_gain" , "slidechange" );
		setEvent( "cr_offset" , "slidechange" );
		setEvent( "cr_gain" , "slidechange" );
*/		
	}
	else if( menu =="LV_Filter_Settings" )
	{
		setEvent( "filter_area" , "click" );
		setEvent( "enhance_level_a" , "slidechange" );
		setEvent( "enhance_level_m" , "slidechange" );
		setEvent( "night_detect" , "slidechange" );
		setEvent( "color_enhance" , "slidechange" );
		setEvent( "3dnr" , "slidechange" );
		setEvent( "cb_gain" , "slidechange" );		
		setEvent( "cr_gain" , "slidechange" );
	}
	else if( menu =="LV_Filter_Mode" )
	{
		getElement("filter_hw_dn_mode").on("click", function(){
			var value = $("[name=filter_hw_dn_mode]:checked").val();
			_ajax("filter_hw_dn_mode", value);
			checkHWFilterMode();
		});	
		getElement("filter_dn_mode").on("click", function(){
			var value = $("[name=filter_dn_mode]:checked").val();
			_ajax("filter_dn_mode", value);
			checkHWFilterMode();
		});			
		setEvent( "filter_enable_threshold" , "slidechange" );
		setEvent( "filter_disable_threshold" , "slidechange" );
		getElement("filter_non_time_setting_mode").on("click", function(){
			var value = $("[name=filter_non_time_setting_mode]:checked").val();
			_ajax("filter_non_time_setting_mode", value);
			checkHWFilterMode();
		});	
		setEvent( "filter_disable_str_setting_hour" , "change" );
		setEvent( "filter_disable_str_setting_min" , "change" );
		setEvent( "filter_disable_end_setting_hour" , "change" );
		setEvent( "filter_disable_end_setting_min" , "change" );		
	}	
	$("#vin_source").off("change").change(function(e){
		source = getVinSourceIndex("#" + e.currentTarget.id);
		MJ.id = source;
		// restore changed value to call dependence() on init()
		$.extend(true,CameraFunc[source], initialValue[source]); 
		init();
	});
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
	commonCreateSourceSelectBox("#vin_source", "align_right");
	$.extend(true, initialValue , CameraFunc);
}

function init()
{
	$("#vin_source").removeProp("disabled");
	if( firstInit ) return ;
	console.log("camera_init_flag:" + camera_init_flag ) ;

	debug("init()");
	menu = $(".select_minor").attr('id');

	initUI();	
	initValue();
	initEvent();
	dependence();	
	
//	clearTimeout(timeout);
//	checkHwfilter();

	console.log("init");
//	$("#hwdnmode").find("*").prop("disabled", true );
}
function _ajaxs(param, data)
{	
	console.log("_ajax"+data+"param" + param);
	CameraFunc[source][param] = data;
	
	if( param == "wb_preset" ){	
		cmd = "setwbpreset"; 
		cmd += "&value=" + data;
	}
	else if( param == "hwdnmode" ){ 
		cmd = "sethwfilter"; 
		cmd += "&value=" + data;	

		camera_init_flag = true ;
	}
	else cmd = "apply" + param;
	
	if(cmd != null || cmd != undefined)	
	{
		pop_menu = getLanguage(menu);
		cmd = "msubmenu=camera&action="+ cmd ;
		
		
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
					if( CameraFunc[source]['awb_mode'])	checkWhiteBalance();
					if( param != "wb_preset" )
					{	
						settingSuccess(pop_menu, null);	
						Disabled(false);
						refreshMenuContent();						
					}
					else{
						Disabled(false);
						dependence();
					}
			
				} else {
					settingFail(pop_menu, null);
					refreshMenuContent();
				}
			},
			error	: function(){
				Disabled(false);
				settingFail(pop_menu, null);
				refreshMenuContent();
			}
		});
	}
}
function _ajax(param, data, slider, cmd)
{
	console.log(param);
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
		
			
		if( CameraFunc[source][ items[menu][i] ] != initialValue[source][items[menu][i]]){
			if( items[menu][i] == "wb_preset") continue;
			change++;
		}
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
			if( items[menu][i] == "wb_preset") continue;
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
	checkHwfilter();
//	init();
	firstInit = false;
});

function onClickCameraDefault()
{
	Disabled(true);
	var menunum;
	console.log(menu);
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
	case "LV_Filter_Operation":
			menunum = 7 ;
			break;
	case "LV_Filter_Settings":
			menunum = 8 ;
			break;
	case "LV_Filter_Mode":
			menunum = 9 ;
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
