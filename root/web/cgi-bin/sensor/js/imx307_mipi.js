var settingList = new Array;
settingList = [ "ae_en", "exp_level", "a_flicker", "ae_meter", "awb_en", "awb_mode", "awb_method", "r_gain", "g_gain", "b_gain", "hue", "saturation", "brightness", "contrast", "sharpness", "mctf3dnr", "local_exp", "blc", "hdr", "hdr_level", "dnmode", "shutter","shutter_limit", "sshutter", "mirror", "flip", "cam_gain","tdn_bw_level","tdn_color_level","tdn_resp","ir_enabled"];
var items = {
	//menuTitle 		: [ items in menutitle ]
	"Image_Adjustment"	: [ "sharpness", "brightness", "contrast", "saturation", "hue"], 
	"Exposure_Settings"	: [ "ae_en", "exp_level", "local_exp", "ae_meter", "shutter","shutter_limit", "sshutter" , "cam_gain" ],
	"Day_Night_Settings": [ "dnmode", "tdn_bw_level", "tdn_color_level", "tdn_resp", "color_hour", "color_min", "bw_hour", "bw_min","ir_enabled"],
	"Backlight_Switch"	: ["blc", "hdr", "hdr_level" ],
	"White_Balance"		: [ "awb_en", "awb_method", "awb_mode", "r_gain", "g_gain", "b_gain" ],
	"Image_Enhancement"	: [ "mctf3dnr", "mirror", "flip"],
	"Video_Enhancement" : ["a_flicker"],
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
var hdr_not_supported=0;
if( capInfo.image_sensor == 'imx178' || capInfo.image_sensor =="imx322" || capInfo.image_sensor =="imx226") {
	hdr_not_supported=1;
}
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
	if(capInfo['oem'] == 5 || capInfo['oem'] == 12 || capInfo['oem'] == 11 || capInfo['oem'] == 13 || capInfo['oem'] == 25 ){
		$("#ir_mode").css("display","block");
	}
	debug("initUI");
	if(capInfo['oem'] != 9) 	$("#shutter_limit_tr").css("display" , "none");
	if ( videoType== 0 ){	//NTSC
		$("[name=shutter_limit]").empty();
		$("[name=shutter_limit]").append('<option value=30> 1/30 </option>');
		$("[name=shutter_limit]").append('<option value=60> 1/60 </option>');
		$("[name=shutter_limit]").append('<option value=120> 1/120 </option>');
		$("[name=shutter_limit]").append('<option value=240> 1/240</option>');
		$("[name=shutter_limit]").append('<option value=380> 1/480 </option>');
		$("[name=shutter_limit]").append('<option value=960> 1/960 </option>');
		$("[name=shutter_limit]").append('<option value=1024> 1/1024 </option>');
		$("[name=shutter_limit]").append('<option value=2000> 1/2000 </option>');
		$("[name=shutter_limit]").append('<option value=4000> 1/4000 </option>');
		$("[name=shutter_limit]").append('<option value=8000> 1/8000 </option>');
		$("[name=shutter_limit]").append('<option value=16000> 1/16000 </option>');
		$("[name=shutter_limit]").append('<option value=32000> 1/32000 </option>');
	}else if(videoType == 1){	//PAL
		$("[name=shutter_limit]").empty();
		$("[name=shutter_limit]").append('<option value=25> 1/25 </option>');
		$("[name=shutter_limit]").append('<option value=50> 1/50 </option>');
		$("[name=shutter_limit]").append('<option value=100> 1/100 </option>');
		$("[name=shutter_limit]").append('<option value=200> 1/200</option>');
		$("[name=shutter_limit]").append('<option value=480> 1/480 </option>');
		$("[name=shutter_limit]").append('<option value=960> 1/960 </option>');
		$("[name=shutter_limit]").append('<option value=1024> 1/1024 </option>');
		$("[name=shutter_limit]").append('<option value=2000> 1/2000 </option>');
		$("[name=shutter_limit]").append('<option value=4000> 1/4000 </option>');
		$("[name=shutter_limit]").append('<option value=8000> 1/8000 </option>');
		$("[name=shutter_limit]").append('<option value=16000> 1/16000 </option>');
		$("[name=shutter_limit]").append('<option value=32000> 1/32000 </option>');
	}

   if(capInfo['oem'] == 3 && devInfo['model_num'] == "NDLP-SLAH8" )
		$("#slow_shutter_limit_tr").css("display" , "none");
	else
    {
        $("#max_shutter_limit_tr").css("display" , "none");
    }

	if( capInfo.camera_type == "ANPR" && menu == "Image_Adjustment") {
		$("#ANPR").remove();
	}
	if( capInfo.camera_type == "PREDATOR_CLIENT" && menu == "Day_Night_Settings") {
        $("#iColor_level").css("display","none");
        $("#iBw_level").css("display","none");
        $("#iResp").css("display","none");
	}
	if( hdr_not_supported === 1 ) {
		$("[name=support_hdr]").remove();
		$("[name=support_hdr_level]").remove();
	} else {
		$("[name=support_blc]").remove();
	}

	if(capInfo.image_sensor =="imx226"){
		$("[name=set_mirror]").remove();
		$("[name=set_flip]").remove();
	}

	// 			  name     , min  , max
   setSlider("exp_level"  , 25   , 400);
	
	//setSlider("sharpness"  , 0    , 11);
	//setSlider("brightness" , -255 , 255);
	//setSlider("contrast"   , 0    , 128);
	//setSlider("hue"        , -15  , 15);
	//setSlider("saturation" , 0    , 255);
	setSlider("sharpness"  , 0    , 100);
	setSlider("brightness" , 0 , 100);
	setSlider("contrast"   , 0    , 100);
	setSlider("hue"        , 0  , 100);
	setSlider("saturation" , 0    , 100);
	
	
	setSlider("r_gain"     , 1000 , 2000);
	setSlider("g_gain"     , 1000 , 2000);
	setSlider("b_gain"     , 1000 , 2000);
	setSlider("mctf3dnr"   , 0    , 11);
	var cmd;
	if( $(".select_minor").attr("id") == "Day_Night_Settings"){
		cmd="";
		for(var i = 0 ; i < 11 ; i++) {
			cmd += "<option value=" +  i + ">"+ i +"</option>"
		}
		getElement('tdn_color_level').empty().append(cmd);
		getElement('tdn_bw_level').empty().append(cmd);
        if(capInfo["oem"] != 5 && capInfo["oem"] != 12 && capInfo["oem"] != 11 && capInfo["oem"] != 13 && capInfo["oem"] != 25 ){
		    $("[name=ir_mode]").css("display","none");        
        }
	}

	menu = $(".select_minor").attr("id");
	if( menu == "Exposure_Settings")
	{
		if( CameraFunc['hdr'] == 1 && $("#wdr_caution").length == 0 ) {
			$("#display_box").after("<div id='wdr_caution' class='wdr_caution' tkey='setup_wdr_caution'></div>");
//			$("#camTitle").css( "margin-bottom" , "10px");
//			$("#wdr_caution").css({"font-size":"12px","font-weight" :"600", "margin": "0px 0px 5px 20px"});
//			if(capInfo['oem'] == 2 ) 	$("#wdr_caution").css("color" , "#ee7421");
//			else $("#wdr_caution").css("color" , "#b900000");
			initLanguage();
		}
	}
	else{
		$("#wdr_caution").remove();
	}

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
	getElement("bw_min").empty().append(content);

	//if(capInfo['oem'] == 2 && (systemOption & SYSTEM_OPTION_UI_FIXED_DATE_20160504) ){
	//	$("[name=iSchedule]").find("*").hide();
	//	$(":radio[id=tdn_sched]").nextAll().remove();
	//	$(":radio[id=tdn_sched]").remove();
	//}
	
	if( menu == "Backlight_Switch" && capInfo.board_chipset == "amba_s2l66") {
        if( $("#hdr option[value=1]").length == 0){
            $("#hdr").append("<option value='1'>"+getLanguage('setup_wdr_2x_on')+"</option>");
        }
		if( $("#hdr option[value=2]").length == 0 ){
			$("#hdr").append("<option value='2'>"+getLanguage('setup_wdr_3x_on')+"</option>");
		}
	}
    else if( menu == "Backlight_Switch" ){
        if( $("#hdr option[value=1]").length == 0){
            $("#hdr").append("<option value='1'>"+getLanguage('setup_wdr_on')+"</option>");
        }
        

        //if(capInfo.board_chipset == "amba_s3lm33"||capInfo.board_chipset == "amba_s3l63"){
        if(capInfo.image_sensor == 'imx307'||capInfo.image_sensor == 'imx307_mipi'||capInfo.image_sensor == 'ov4689'||capInfo.image_sensor == 'imx385_mipi'||capInfo.image_sensor == 'imx335_mipi'||capInfo.image_sensor == 'imx334_mipi'||capInfo.image_sensor == 'imx274_mipi'){
		    $("[name=support_hdr_level]").css("display","none");        
        }
    }

	content="";
	if( capInfo.image_sensor == 'ar0230' ) {
		content += "<option value=0> 0 dB </option>";
		content += "<option value=1> 3 dB </option>";
		content += "<option value=2> 6 dB </option>";
		content += "<option value=3> 9 dB </option>";
		content += "<option value=4> 12 dB </option>";
		content += "<option value=5> 15 dB </option>";
		content += "<option value=6> 18 dB </option>";
		content += "<option value=7> 24 dB </option>";
		content += "<option value=8> 30 dB </option>";
		content += "<option value=9> 36 dB </option>";
		content += "<option value=10> 42 dB </option>";
		content += "<option value=11> 44 dB </option>";
        getElement("cam_gain").empty().append(content);
	} else if( capInfo.image_sensor == 'ov4689' ) { 
		content += "<option value=0> 0 dB </option>";
		content += "<option value=1> 3 dB </option>";
		content += "<option value=2> 6 dB </option>";
		content += "<option value=3> 9 dB </option>";
		content += "<option value=4> 12 dB </option>";
		content += "<option value=5> 15 dB </option>";
		content += "<option value=6> 18 dB </option>";
		content += "<option value=7> 24 dB </option>";
		content += "<option value=8> 30 dB </option>";
		content += "<option value=9> 36 dB </option>";
		getElement("cam_gain").empty().append(content);
	} else if( capInfo.image_sensor == 'imx178' ) {
		content += "<option value=0> 0 dB </option>";
		content += "<option value=1> 3 dB </option>";
		content += "<option value=2> 6 dB </option>";
		content += "<option value=3> 9 dB </option>";
		content += "<option value=4> 12 dB </option>";
		content += "<option value=5> 15 dB </option>";
		content += "<option value=6> 18 dB </option>";
		content += "<option value=7> 24 dB </option>";
		content += "<option value=8> 30 dB </option>";
		content += "<option value=9> 36 dB </option>";
		content += "<option value=10> 42 dB </option>";
		content += "<option value=11> 48 dB </option>";
		getElement("cam_gain").empty().append(content);
	} else if( capInfo.image_sensor =="imx322" ) {
		content += "<option value=0> 0 dB </option>";
		content += "<option value=1> 3 dB </option>";
		content += "<option value=2> 6 dB </option>";
		content += "<option value=3> 9 dB </option>";
		content += "<option value=4> 12 dB </option>";
		content += "<option value=5> 15 dB </option>";
		content += "<option value=6> 18 dB </option>";
		content += "<option value=7> 24 dB </option>";
		content += "<option value=8> 30 dB </option>";
		content += "<option value=9> 36 dB </option>";
		content += "<option value=10> 42 dB </option>";
		getElement("cam_gain").empty().append(content);
	} else if( capInfo.image_sensor =="imx307" ) {
		content += "<option value=0> 0 dB </option>";
		content += "<option value=1> 3 dB </option>";
		content += "<option value=2> 6 dB </option>";
		content += "<option value=3> 9 dB </option>";
		content += "<option value=4> 12 dB </option>";
		content += "<option value=5> 15 dB </option>";
		content += "<option value=6> 18 dB </option>";
		content += "<option value=7> 24 dB </option>";
		content += "<option value=8> 30 dB </option>";
		content += "<option value=9> 36 dB </option>";
		content += "<option value=10> 42 dB </option>";
		content += "<option value=11> 48 dB </option>";
		content += "<option value=12> 54 dB </option>";
		content += "<option value=13> 60 dB </option>";
		content += "<option value=14> 66 dB </option>";
		content += "<option value=15> 69 dB </option>";
		getElement("cam_gain").empty().append(content);
	} else if( capInfo.image_sensor =="imx385_mipi" ) {
		content += "<option value=0> 0 dB </option>";
		content += "<option value=1> 3 dB </option>";
		content += "<option value=2> 6 dB </option>";
		content += "<option value=3> 9 dB </option>";
		content += "<option value=4> 12 dB </option>";
		content += "<option value=5> 15 dB </option>";
		content += "<option value=6> 18 dB </option>";
		content += "<option value=7> 24 dB </option>";
		content += "<option value=8> 30 dB </option>";
		content += "<option value=9> 36 dB </option>";
		content += "<option value=10> 42 dB </option>";
		content += "<option value=11> 48 dB </option>";
		content += "<option value=12> 54 dB </option>";
		content += "<option value=13> 60 dB </option>";
		content += "<option value=14> 66 dB </option>";
		content += "<option value=15> 72 dB </option>";
		getElement("cam_gain").empty().append(content);
	} else if( capInfo.image_sensor =="imx335_mipi" ) {
		content += "<option value=0> 0 dB </option>";
		content += "<option value=1> 3 dB </option>";
		content += "<option value=2> 6 dB </option>";
		content += "<option value=3> 9 dB </option>";
		content += "<option value=4> 12 dB </option>";
		content += "<option value=5> 15 dB </option>";
		content += "<option value=6> 18 dB </option>";
		content += "<option value=7> 24 dB </option>";
		content += "<option value=8> 30 dB </option>";
		content += "<option value=9> 36 dB </option>";
		content += "<option value=10> 42 dB </option>";
		content += "<option value=11> 48 dB </option>";
		content += "<option value=12> 54 dB </option>";
		content += "<option value=13> 60 dB </option>";
		content += "<option value=14> 66 dB </option>";
		content += "<option value=15> 72 dB </option>";
		getElement("cam_gain").empty().append(content);
	} else if( capInfo.image_sensor =="imx334_mipi" ) {
		content += "<option value=0> 0 dB </option>";
		content += "<option value=1> 3 dB </option>";
		content += "<option value=2> 6 dB </option>";
		content += "<option value=3> 9 dB </option>";
		content += "<option value=4> 12 dB </option>";
		content += "<option value=5> 15 dB </option>";
		content += "<option value=6> 18 dB </option>";
		content += "<option value=7> 24 dB </option>";
		content += "<option value=8> 30 dB </option>";
		content += "<option value=9> 36 dB </option>";
		content += "<option value=10> 42 dB </option>";
		content += "<option value=11> 48 dB </option>";
		content += "<option value=12> 54 dB </option>";
		content += "<option value=13> 60 dB </option>";
		content += "<option value=14> 66 dB </option>";
		content += "<option value=15> 72 dB </option>";
		getElement("cam_gain").empty().append(content);
	} else if( capInfo.image_sensor =="imx274_mipi" ) {
		content += "<option value=0> 0 dB </option>";
		content += "<option value=1> 3 dB </option>";
		content += "<option value=2> 6 dB </option>";
		content += "<option value=3> 9 dB </option>";
		content += "<option value=4> 12 dB </option>";
		content += "<option value=5> 15 dB </option>";
		content += "<option value=6> 18 dB </option>";
		content += "<option value=7> 24 dB </option>";
		content += "<option value=8> 30 dB </option>";
		content += "<option value=9> 36 dB </option>";
		content += "<option value=10> 42 dB </option>";
		content += "<option value=11> 48 dB </option>";
		content += "<option value=12> 54 dB </option>";
		content += "<option value=13> 60 dB </option>";
		content += "<option value=14> 66 dB </option>";
		content += "<option value=15> 72 dB </option>";
		getElement("cam_gain").empty().append(content);
	} else if( capInfo.image_sensor =="imx226" ) {
		content += "<option value=0> 0 dB </option>";
		content += "<option value=1> 3 dB </option>";
		content += "<option value=2> 6 dB </option>";
		content += "<option value=3> 9 dB </option>";
		content += "<option value=4> 12 dB </option>";
		content += "<option value=5> 15 dB </option>";
		content += "<option value=6> 18 dB </option>";
		content += "<option value=7> 24 dB </option>";
		content += "<option value=8> 30 dB </option>";
		content += "<option value=9> 36 dB </option>";
		content += "<option value=10> 42 dB </option>";
		content += "<option value=11> 45 dB </option>";
		getElement("cam_gain").empty().append(content);
	}

    getElement("awb_mode").empty();
    content="";
    content += "<option value=0>" + getLanguage('setup_auto') + "</option>";
    content += "<option value=1> 2800K </option>";
    content += "<option value=2> 4000K </option>";
    content += "<option value=3> 5000K </option>";
    content += "<option value=4> 6500K </option>";
    content += "<option value=5> 7500K </option>";
    content += "<option value=6>" + getLanguage('setup_flash') + "</option>";
    content += "<option value=7>" + getLanguage('setup_fluorescent') +"</option>";
    content += "<option value=8>" + getLanguage('setup_fluorescent_h') +"</option>";
    content += "<option value=9>" + getLanguage('setup_underwater') +"</option>";
    content += "<option value=10>" + getLanguage('main_manual') +"</option>";
    getElement("awb_mode").append(content);

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
	if( CameraFunc[source].ae_en ) {
		$("[name=shutter]").prop("disabled", true);
		$("[name=shutter_limit]").prop("disabled",false);
	} else {
		$("[name=shutter]").prop("disabled", false );
		$("[name=shutter_limit]").prop("disabled",true);
	}
	if( !CameraFunc[source].awb_en ) {
		$("[name=awb_mode]").prop("disabled", true);		
		disabledSlider("r_gain", 1) ;
		disabledSlider("g_gain", 1) ;
		disabledSlider("b_gain", 1) ;
	} else {
		$("[name=awb_mode]").prop("disabled", false);		
		if ( CameraFunc[source].awb_mode == 10 ) { // custom
			disabledSlider("r_gain", 0) ;
			disabledSlider("g_gain", 0) ;
			disabledSlider("b_gain", 0) ;
		} else {
			disabledSlider("r_gain", 1) ;
			disabledSlider("g_gain", 1) ;
			disabledSlider("b_gain", 1) ;
		}
	}

	if( typeof(CameraFunc[source].hdr) != "undefined" ){
		var hdr_dependency = CameraFunc[source].hdr > 0 ? true : false;
		if( $(".select_minor").attr("id") == "Backlight_Switch") {
			getElement("blc").prop("disabled", hdr_dependency);
			getElement("hdr_level").prop("disabled", !hdr_dependency);
		}
		if( $(".select_minor").attr("id") == "Exposure_Settings"){
			getElement("ae_en").prop("disabled", hdr_dependency);
			getElement("ae_meter").prop("disabled", hdr_dependency || !CameraFunc[source].ae_en);
			getElement("local_exp").prop("disabled", hdr_dependency);
			disabledSlider("exp_level", hdr_dependency || !CameraFunc[source].ae_en);
		}
	}

	if( menu == "Day_Night_Settings" ){
		$("#vin_source").prop("disabled", true);
		source = 0;
		MJ.id = source;
	}
	checkTDNMode();
}

function checkTDNMode()
{
	if( CameraFunc[source].dnmode == 5 ) {
		$("[name=iSchedule]").find("*").prop("disabled", false );
		getElement("tdn_color_level").prop("disabled", true);
		getElement("tdn_bw_level").prop("disabled", true);
		getElement("tdn_resp").prop("disabled", true);
	}
	else
	{
		$("[name=iSchedule]").find("*").prop("disabled", true);
		getElement("tdn_color_level").prop("disabled", false);
		getElement("tdn_bw_level").prop("disabled", false);
		getElement("tdn_resp").prop("disabled", false);
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
		$("#vin_source option:eq("+MJ.id+")").prop("selected", "selected");
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
		$("#vin_source option:eq("+MJ.id+")").prop("selected", "selected");
		getElement("ae_en").on("click",function(){
			var value = $("[name=ae_en]:checked").val();
			_ajax('ae_en', value);
			dependence();
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
		getElement("shutter_limit").on("change",function(){
			var value = getElement("shutter_limit").val();
			_ajax('shutter_limit', value);
		});
		getElement("sshutter").on("change",function(){
			var value = getElement("sshutter").val();
			_ajax('sshutter', value);
		});
		getElement("cam_gain").on("change",function(){
			var value = getElement("cam_gain").val();
			_ajax('cam_gain', value);
		});		
	} 
	else if( menu =="Day_Night_Settings")
	{
		src = 0;
		MJ.id = src;
		$("#vin_source option:eq(0)").prop("selected", "selected");
		getElement('dnmode').on("click", function(event){
			var value = $('[name=dnmode]:checked').val();
			_ajax("dnmode", value);
			checkTDNMode();
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
		getElement("color_hour").on("change", function(){
			var value = getElement("color_hour").val();
			_ajax("color_hour", value);
		});
		getElement("color_min").on("change", function(){
			var value = getElement("color_min").val();
			_ajax("color_min", value);
		});
		getElement("bw_hour").on("change", function(){
			var value = getElement("bw_hour").val();
			_ajax("bw_hour", value);
		});
		getElement("bw_min").on("change", function(){
			var value = getElement("bw_min").val();
			_ajax("bw_min", value);
		});
		getElement("ir_enabled").on("change", function(){
			var value = $('[name=ir_enabled]:checked').val();
			_ajax("ir_enabled", value);
		});
	}
	else if( menu =="Backlight_Switch")
	{
		$("#vin_source option:eq("+MJ.id+")").prop("selected", "selected");
		getElement('blc').on("click", function(event){
			var value = $('[name=blc]:checked').val();
			_ajax("blc", value);
		});
		getElement("hdr").on("change",function(){
			var value = $("#hdr").val();
			_ajax('hdr', value);
			dependence() ;
		});
		getElement("hdr_level").on("change",function(){
			var value = $("#hdr_level").val();
			_ajax('hdr_level', value);
		});
	}
	else if( menu == "White_Balance" )
	{
		$("#vin_source option:eq("+MJ.id+")").prop("selected", "selected");
		debug('menu = white_balance');
		getElement("awb_en").on("click",function(){
			var value = $("[name=awb_en]:checked").val();
			_ajax('awb_en', value);
			dependence();
		});
		getElement("awb_method").on("change", function(){
			var value = getElement("awb_method").val();
			_ajax('awb_method', value);
		});
		getElement("awb_mode").on("change", function(){
			var value = getElement("awb_mode").val();
			_ajax('awb_mode', value);
			dependence()  ;
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
		$("#vin_source option:eq("+MJ.id+")").prop("selected", "selected");
		getElement("mctf3dnr").on("slidechange", function(){
			var value = getElement("mctf3dnr").slider('value'); 
			_ajax('mctf3dnr', value);
		});
		getElement("mirror").on("click", function(){
			var value = $("[name=mirror]:checked").val();
			_ajax("mirror", value);
		});
		getElement("flip").on("click", function(){
			var value = $("[name=flip]:checked").val();
			_ajax("flip", value);
		});
	}
	else if( menu =="Video_Enhancement")
	{
		$("#vin_source option:eq("+MJ.id+")").prop("selected", "selected");
		getElement("a_flicker").on("click",function(){
			var value = $("[name=a_flicker]:checked").val();
			_ajax('a_flicker', value);
		});
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
		dependence();
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
	debug("init()");
    if(menu != $(".select_minor").attr("id")){
        MJ.id=0;
        source=0;
        $.extend(true,CameraFunc[0], initialValue[0]);
    }
	menu = $(".select_minor").attr('id');

    initUI();
	dependence();
	initValue();
	initEvent();
//	initLanguage();
}
function _ajaxs(action, cmd)
{
	if(cmd != null || cmd != undefined)	{
		pop_menu = getLanguage(menu);
		cmd = "msubmenu=camera&action="+ action + "&source="+ (source+1) + cmd;
		Disabled(true);
		$.ajax({
			type : 'get',
			url  : '/cgi-bin/admin/camera.cgi',
			data : cmd,
			async : false,
			success : function(response){
				var OK = /OK/;
				if(OK.test(response)) {
					settingSuccess(pop_menu, null);
					if( action == 'default'){
						$("#initValue").load("setup_camera_init.cgi");
					}
					refreshMenuContent();
				} 
				else {
					settingFail(pop_menu, null);
				}
			},
			error : function(){
				settingFail(pop_menu, null);
			}
		});
		Disabled(false);
	}
}
function _ajax(param, data, slider, cmd)
{
	if( cmd == "apply")
	{
		CameraFunc[source][param] = data;
	}
	else // preview or null
	{
		cmd = "preview";
		if( CameraFunc[source][param] == data ) {
			return ;
		}
		else {
			CameraFunc[source][param] = Number(data);
			return ;                           // 
		}
	}
	var val = "msubmenu=camera&action=" + cmd + "&"+param + "=" + data;

	if(slider != null)
		getElement(slider).html(data);
	
	Disabled(true);
	//$.ajax(
	//	{
	//		type : 'get',
	//		url  : '/cgi-bin/admin/camera.cgi',
	//		async : false, 
	//		data : val,
	//		success : onSuccess,
	//		error	: onFail
	//	}
	//);
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
			data += "&" + items[menu][i] + "=" +CameraFunc[source][items[menu][i] ];
		}
	}
	_ajaxs("apply", data);
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
		url: "/cgi-bin/admin/camera.cgi?msubmenu=camera&action=default&menu=" + menunum + "&source="+ (source+1),
		success: RestoreValue,
		error: onFail
	});
}
