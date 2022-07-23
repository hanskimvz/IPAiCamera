var items = {
	//menuTitle 		: [ items in menutitle ]
	"Image_Enhancement"	: [ "thermal_color", "thermal_flip", "thermal_mirror", "thermal_denoise", "thermal_meta_data_enable", "thermal_temperature_unit" ],
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
	if( menu == "Image_Enhancement" )
	{
		getElement("thermal_color").empty();
		content="";
		content += "<option value=0>" + "WHITE" + "</option>";
		content += "<option value=1>" + "BLACK" + "</option>";
		content += "<option value=2>" + "IRON" + "</option>";
		content += "<option value=3>" + "COOL" + "</option>";
		content += "<option value=4>" + "AMBER" + "</option>";
		content += "<option value=5>" + "INDIGO" + "</option>";
		content += "<option value=6>" + "TYRIAN" + "</option>";
		content += "<option value=7>" + "GLORY" + "</option>";
		content += "<option value=8>" + "ENVY" + "</option>";
		getElement("thermal_color").append(content);
	}
}

function initValue()
{
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

}

/* define the event from the DOM */
function initEvent(){
	//FOR EXPOSURE
	menu = $(".select_minor").attr("id");
	pop_menu = getLanguage(menu);
	debug(menu);
	if( menu =="Image_Enhancement" )
	{
		$("#vin_source option:eq("+MJ.id+")").prop("selected", "selected");

		getElement("thermal_color").on("change",function(){
			var value = $("#thermal_color").val();
			_ajax('thermal_color', value);
		});

		getElement("thermal_flip").on("change",function(){
			var value = $("#thermal_flip").val();
			_ajax('thermal_flip', value);
		});

		getElement("thermal_mirror").on("change",function(){
			var value = $("#thermal_mirror").val();
			_ajax('thermal_mirror', value);
		});

		getElement("thermal_denoise").on("change",function(){
			var value = $("#thermal_denoise").val();
			_ajax('thermal_denoise', value);
		});
/*
		getElement("thermal_meta_data_enable").on("change",function(){
			var value = $("#thermal_meta_data_enable").val();
			_ajax('thermal_meta_data_enable', value);
		});
*/
		getElement("thermal_temperature_unit").on("change",function(){
			var value = $("#thermal_temperature_unit").val();
			_ajax('thermal_temperature_unit', value);
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
//			url  : '/cgi-bin/sensor/ui/seek_thermal.cgi',
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
			return ;
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
	onLoadPage();
	firstInit = false;
});

function onClickCameraDefault()
{
	Disabled(true);
	var menunum;
	switch(menu)
	{
		case "Image_Enhancement":
			menunum = 1 ;
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
