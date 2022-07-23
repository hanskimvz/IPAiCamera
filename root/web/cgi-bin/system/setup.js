$.ajaxSetup({ cache: false });
var fishInfo_ ;
var completed_flag ;

function onLogClear(){
	var data = {msubmenu: "log",action: "clear" };
	$.ajax({
		url: './setup.cgi',
		method: 'get',
		msubmenu: 'log',
		action: 'clear',
		data: data,
		success: function(ret){
			console.log(data);
			var req = ret.trim();
			if( req == "OK")
			{
				var msg = "System log was deleted!";
				alert(msg);
			}
		},
		error: onReloadInitConfig
	});	
}
function onSetCDSoffset()
{
	var cdsAdj = 0 ;
	var data = {msubmenu: "cdsAdj",
			action: "apply",
			cdsAdj : null
	}
			
//	if ($("input[name=chkCDSAdj]").is(":checked")) {
		data.cdsAdj = $("input[name=txtCDSAdj]").val();

		var isnum = /^[-]{0,1}\d+$/.test(data.cdsAdj);
	    if ( !isnum ) {
	    	alert(getLanguage("msg_onlynumber"));
			return;
		}
//	}
	
	$.ajax({
		url: './setup.cgi?',
		method: 'get',
		msubmenu: 'cdsAdj',
		action: 'apply',
		data: data,
		success: alert("CDS Setting Succes!!"),
		error: onReloadInitConfig
	});
}
function onClickApplyAll()
{

	//var msg = "Do you want to change the system configuration?\r\n\r\n";
	var msg = getLanguage("msg_system_changeconf") +  "\r\n\r\n";

	var data = {msubmenu: "system",
				action: "apply",
				color_system: null, 
				tdn : null, 
				cdsAdj : null, 
				model_num: null,
				model_name: null,
				model_manufacturer: null,
                thermal_offset: null,
				delete_log: null };

	if ($("input[name=chkColorSys]").is(":checked")) {
		var textColorSys = ["NTSC", "PAL"];
		data.color_system = $("input[name=optColorSys]:checked").val();
		/*
		msg += "    * Color System : " + textColorSys[data.color_system] + "\r\n";
		*/
		msg += "    * Color System : " + textColorSys[data.color_system] + " (reset to factory default except network)" + "\r\n";
	}
	if ($("input[name=chkTdn]").is(":checked")) {
		var textTdn= ["Disable", "Enable"];
		data.tdn = $("input[name=optTdn]:checked").val();
		msg += "    * TDN : " + textTdn[data.tdn] + "\r\n";
	}

	if ($("input[name=chkModel]").is(":checked")) {
		data.model_num = $("select[name=selModelNum] option:selected").val();
		msg += "    * Model : " + data.model_num + "\r\n";
	}
	if ($("input[name=chkModelName]").is(":checked")) {
		data.model_name = $("input[name=txtModelName]").val();
		msg += "    * Model Name : " + data.model_name + "\r\n";
	}
	if ($("input[name=chkModelManufacturer]").is(":checked")) {
		data.model_manufacturer = $("input[name=txtModelManufacturer]").val();
		msg += "    * Model Manufacturer : "+ data.model_manufacturer + "\r\n";
	}
    if ($("input[name=chkThermaloffset]").is(":checked")) {
        data.thermal_offset = $("input[name=txtThermaloffset]").val();
        msg += "    * Thermal Offset : "+ data.thermal_offset + "\r\n";
    }

	/*
    if ($("input[name=chkDeleteLog]").is(":checked")) {
		delete_log = 1;
		msg += "    * Delete log file \r\n";
	}
    */

	if ( data.color_system == null 
		&& data.tdn == null 
		&& data.cdsAdj == null 
		&& data.model_num == null 
		&& data.model_name == null 
		&& data.model_manufacturer == null 
        && data.thermal_offset == null
		&& data.delete_log == null) return;

	for( var tmp in data)
	{
		if(data[tmp] == null){
			delete data[tmp];
		}
	}

	if ( !confirm(msg) ) return;
// 'cgi-bin/system/setup.cgi?msubmenu=system&action=apply&
	console.log(data);
	$.ajax({
		url: './setup.cgi',
		method: 'get',
		msubmenu: 'system',
		action: 'apply',
		data: data,
		success: onSuccessRequestAll,
		error: onReloadInitConfig
	});
}
function onClickdevicename() //OEM 13 11 10
{
	var msg = getLanguage("msg_system_changeconf") +  "\r\n\r\n";
	var oldValue = devInfo['model_devicename'];
	var newValue;

	var data = {msubmenu: "device_info",
				action: "apply",
				device_name : null };
	if ($("input[name=chkdevname]").is(":checked")) {
		data.device_name = $("input[name=txtdevicename]").val();
		msg += "    * Device Name : "+ data.device_name + "\r\n";
		newValue = data.device_name;
	}
	if (oldValue == newValue){
		settingFail(menu, getLanguage("msg_nothing_changed"));
		return;
	}
	if ( !isValidText(newValue) ) {
		settingFail(menu, getLanguage("msg_invalid_text"));
		return;
	}
	if ( data.device_name == null ) return;
	if ( !confirm(msg) ) return;
	$.ajax({
		url: "/cgi-bin/admin/system.cgi",
		method: 'get',
		msubmenu: 'device_info',
		action: 'apply',
		data: data,
		success : alert("device_name changed!"),
		error : onReloadInitConfig
	});
}
function onFocusCast(){
	var data = {
		msubmenu: "hwtest",
		action: "focuscast",
		portNo: null
	};
		data.portNo = $("input[name=txtPortNo]").val();
	$.ajax({
		url: './setup.cgi',
		method: 'get',
		msubmenu: 'hwtest',
		action: 'focuscast',
		data: data,
//		success: alert("Start focus caster!"),
		success: function(ret){
			console.log(data);
			var req = ret.trim();
			if( req == "0")
			{
				var msg = "Start focus caster!";
				alert(msg);
			}
			else
			{

				var msg = "Stop focus caster!";
				alert(msg);
			}
		},
		
		error: onReloadInitConfig
	});
}

function initValue()
{
	$("[name=selModelNum]").val(devInfo['model_num']);
	$("input:radio[name='optColorSys']:radio[value=" + devInfo['color_system'] +"]").attr("checked",true);
	$("input:radio[name='optTdn']:radio[value=" + devInfo['tdn'] +"]").attr("checked",true);
	$("input[name=txtCDSAdj").val(devInfo['cdsAdj']);
	$("input[name=txtPortNo").val(9988);
	$("#CDSCor").text(", CDSCor = "+devInfo['cdsAdjCor']);
	$("input[name=txtModelName").val(devInfo['model_name']);
	$("input[name=txtModelManufacturer").val(devInfo['model_manufacturer']);
    $("input[name=txtThermaloffset").val(devInfo['thermal_offset']);
	//  $("input[name=cmdDeleteLog").attr("disabled", !(obj.checked));

	if(capInfo['board_chipset'] == "amba_s5l66"){
		var x = def_start_x;
		var y= def_start_y;

		if(def_start_x==628)
			x=0;
		if(def_start_y == 40)
			y=0;

		$("input[name=numberOffsetX]").val(x);
		$("input[name=numberOffsetY]").val(y);
	}else{
		$("input[name=numberOffsetX]").val(devInfo.fisheye_offset.x);
		$("input[name=numberOffsetY]").val(devInfo.fisheye_offset.y);
	}

	$("input[name=txtdevicename").val(devInfo['model_devicename']);
	
	completed_flag = true ;
}
function onReloadInitConfig()
{
	initValue();
}
function onSuccessRequestAll(ret)
{
	var req = ret.trim();
	if( req == "OK")
	{
		var msg = "System configuration is changed!";
		msg += " The system will be rebooted!";
		alert(msg);
	}
	else
	{
		alert("NG");
	}	
}

function onSuccessDeleteLog()
{
	alert("Apply! The system will be rebooted!");
}

/*function onClickDeleteLog()
{
	if ( !confirm("Do you want to delete all log?") ) return;

	new Ajax.Request('./setup.cgi', {
		method: 'get',
		parameters: {
			msubmenu: 'log',
			action: 'delete',
			trycount: (new Date()).getTime()
		},
		onSuccess: onSuccessDeleteLog,
		onFailure: null
	});
}*/

function onClickSelection(obj) 
{
	switch (obj.name) {
		case "chkColorSys":
			$("input[name=optColorSys]").prop("disabled", !(obj.checked));
			break;
		case "chkTdn":
			$("input[name=optTdn]").prop("disabled", !(obj.checked));
			break;
		case "chkCDSAdj":
			$("input[name=txtCDSAdj]").prop("disabled", !(obj.checked));
			break;
		case "chkModel":
			$("select[name=selModelNum]").prop("disabled", !(obj.checked));
			break;
		case "chkModelName":
			$("input[name=txtModelName]").prop("disabled", !(obj.checked));
			break;
		case "chkModelManufacturer":
			$("input[name=txtModelManufacturer]").prop("disabled", !(obj.checked));
			break;
        case "chkThermaloffset":
            $("input[name=txtThermaloffset]").prop("disabled", !(obj.checked));
            break;          
		case "chkDeleteLog":
			$("input[name=cmdDeleteLog]").prop("disabled", !(obj.checked));
			break;
		case "chkOffsetX":
			$("input[name=numberOffsetX]").prop("disabled", !(obj.checked));
			break;
		case "chkOffsetY":
			$("input[name=numberOffsetY]").prop("disabled", !(obj.checked));
			break;
		case "chkdevname":
			$("input[name=txtdevicename]").prop("disabled", !(obj.checked));
			break;
	}
}
function initUI()
{
	var content = '', model;
    var x_command = '',y_command='';
	for( var id in model_list )
	{
		if( !model_list.hasOwnProperty(id) ) continue;
		model = model_list[id];

		if( capInfo.board_chipset == model['board_chipset'] ){
		  if(capInfo.image_sensor == 'yuv1080p' && (model['image_sensor'] =='yuv1080p' || capInfo.image_sensor == 'bt1120_1080p' || capInfo.image_sensor == 'bt1120_720p' || capInfo.image_sensor == 'bt1120_480p')) {
			  content += "<option value='" + id + "'>";
			  content += id +" (" +  model.description.replace(/[_]/g,' ') + ")" + "</option>";
		  }
		  else if(capInfo.image_sensor != 'yuv1080p' && model['image_sensor'] !='yuv1080p' ) {
			  content += "<option value='" + id + "'>";
			  content += id +" (" +  model.description.replace(/[_]/g,' ') + ")" + "</option>";			  
		  }
		}
	}

    if( capInfo['board_chipset'] == "amba_s5l66"){
        x_command = "<input type=\"number\" min=200 max=1000 class=\"inputText short\" style=\"height:20px; ime-mode:disabled;\" name=\"numberOffsetX\" value=\"\" numberonly=\"true\"> valid range 200~1000";
        y_command = "<input type=\"number\" min=30 max=50 class=\"inputText short\" style=\"height:20px; ime-mode:disabled;\" name=\"numberOffsetY\" numberonly=\"true\"> valid range 30~50";

    }else{
        x_command = "<input type=\"number\" min=-120 max=120 class=\"inputText short\" style=\"height:20px; ime-mode:disabled;\" name=\"numberOffsetX\" value=\"\" numberonly=\"true\"> valid range -120~120";
        y_command = "<input type=\"number\" min=-26 max=26 class=\"inputText short\" style=\"height:20px; ime-mode:disabled;\" name=\"numberOffsetY\" numberonly=\"true\"> valid range -26~26";
    }

    $("#cal_x").append(x_command);
    $("#cal_y").append(y_command);

	$("[name=selModelNum]").append(content);
	$("select").prop("disabled", true);
	$("input[type!=checkbox]").prop("disabled", true);
	$("input[name=txtPortNo]").prop("disabled", false);

	if( capInfo['camera_type'] == "fisheye" ){
			$("[class=fisheye_table],[class=fisheye_div]").css("display", "inline-grid");			
            if( capInfo['board_chipset'] == "amba_s5l66")
		{
//                $("#cmdApplyFisheyeCali").css("display","none");
			$("#cal_y_tr").css("display","none");
		}
	}else
		$("[class=fisheye_table],[class=fisheye_div]").css("display", "none");

	if( capInfo['oem'] == 13 || capInfo['oem'] == 11 || capInfo['oem'] == 10 || capInfo['oem'] == 25 ){
		$("[class=Device_management]").css("display", "inline-grid");
	}else
		$("[class=Device_management]").css("display", "none");

	$.when(get_cali_center_pos()).done(function(){	
		$.when(MJ.ajax()).done(function(){
			$.when(MJ.draw(MJ.blob, "cali_center")).done(function(){
				MJ.drawLine(fishInfo_['cali_center']['pos_x'], fishInfo_['cali_center']['pos_y']);	
			});
		});	
	});	

    $("#button_text").text(testgpioInfo["button"]==2? "Success": testgpioInfo["button"]==3? "Fail":" ");
    $("#wl_text").text(testgpioInfo["wl"]==2? "Success": testgpioInfo["wl"]==3? "Fail":" ");
    $("#d1_text").text(testgpioInfo["d1"]==2? "Success": testgpioInfo["d1"]==3? "Fail":" ");
    $("#d2_text").text(testgpioInfo["d2"]==2? "Success": testgpioInfo["d2"]==3? "Fail":" ");
    $("#audioout_text").text(testgpioInfo["audioout"]==3? "Fail":" ");

    if(capInfo.oem != 22){
        $("#auto_id").css("display", "none");
        $("#bt_id").css("display", "none");
        $("#wl_id").css("display", "none");
        $("#d1_id").css("display", "none");
        $("#d2_id").css("display", "none");
    }
    if(focusOsd == 0)
    {
	    $("[class=FOCUS_osd]").css("display","none");
	    console.log("focusOSD off");
    }
}
function get_cali_center_pos(){	
	var deferred = $.Deferred();
	$.ajax({
		url: '/cgi-bin/admin/fisheye.cgi',
		method: 'get',		
		data: 'msubmenu=cali_center&action=get',
		async: false,
		success: function(json_data){
			    fishInfo_ = $.parseJSON(json_data) ;
			    fishInfo['cali_center']['pos_x'] = fishInfo_['cali_center']['pos_x'] ;
			    fishInfo['cali_center']['pos_y'] = fishInfo_['cali_center']['pos_y'] ;
			    console.log("get_cali_center():"+fishInfo_['cali_center']['pos_x']+":"+ fishInfo_['cali_center']['pos_y']);
			    deferred.resolve();	
		},
		error: function(){
//			alert("NG");
		}
	});		
	return deferred.promise();
}
function cal_cali_center(){
	var deferred = $.Deferred();
	$.ajax({
		url: '/cgi-bin/admin/fisheye.cgi',
		method: 'get',		
		data: 'msubmenu=cali_center&action=set',
//		async: false,
		success: function(json_data){
			    console.log("cal_cali_center");
			    deferred.resolve();	
		},
		error: function(){
			alert("NG");
		}
	});		
	return deferred.promise();	
}
function check_range(min, max, val){
	if( val < min || val > max ) { 
		return false ;
		}
	return true ;
}

function set_cali_offset(mode){
	var data = {};
	data.msubmenu = 'fisheye';
	data.action   = 'apply';
	completed_flag = true ;
	if( mode =="manual" ){
		data.offset_x = $("input[name = numberOffsetX]").val();
		data.offset_y = $("input[name = numberOffsetY]").val();
		// 모델에 따라 120, 26 range 값 조정해야 함. imx178 센서 일 경우 120,26
        if( capInfo['board_chipset'] != "amba_s5l66"){
            if(!check_range( -120 , 120, data.offset_x ) || !check_range( -26 , 26, data.offset_y )){
                alert(" Fail!! check the offset range. ");
                completed_flag = false ;
                return 0 ;		
            }
        }
	}else if(mode == "auto"){
		//if( VideoInfo[2]["resolution"] == "320x240" ){
		//	data.offset_x = -(fishInfo['cali_center']['pos_x'] - 160)*4 ;
		//	data.offset_y = -(fishInfo['cali_center']['pos_y'] - 120)*4 ;      
		//	
		//}
		if(capInfo['board_chipset'] == "amba_s5l66"){
			data.offset_x = fishInfo['cali_center']['pos_x'];
			data.offset_y = $("input[name = numberOffsetY]").val();
		}else{
			data.offset_x = -(fishInfo['cali_center']['pos_x'] - capInfo['max_resolution_width']/2)/2;

			data.offset_y = -(fishInfo['cali_center']['pos_y'] - capInfo['max_resolution_height']/2)/2;
		}
			
		  
	}else if(mode == "origin"){
		data.offset_x = 0 ;
		data.offset_y = 0 ;
//		console.log("origin");
	}	
//	console.log( data.offset_x +":"+ data.offset_y)
			
	var deferred = $.Deferred();	
	$.ajax({
		url: '/cgi-bin/system/setup.cgi',
		method: 'get',
		data: data,
//		async: false,
		beforeSend : function(){ 
			progressUI(true, 1);
		},
		success: function(json_data){				
			  try {
				fishInfo_ = $.parseJSON(json_data) ;
				devInfo["fisheye_offset"]["x"] = fishInfo_['cali_center']['offset_x'] ;
				devInfo["fisheye_offset"]["y"] = fishInfo_['cali_center']['offset_y'] ;
//			    console.log("set_cali_offset():"+devInfo["fisheye_offset"]["x"] +":"+ devInfo["fisheye_offset"]["y"]);
			  } catch (e) {
				var NG = /NG/gi;
				if( NG.test(json_data) ){
					  alert("you need a right test environment.");
					  progressUI(false);
					  document.location.reload();
				} 
			    return 0;
			  }
			  var msg = "restart video encoding please wait moment";
			  console.log("set_cali_offset");
    		  deferred.resolve();				
		},
		error: function(){
			alert("NG2");
		}
	});	
	return deferred.promise();
}

function test_ajax(name){

    console.log(name);
		$.ajax({
			url: '/cgi-bin/system/setup.cgi',
			method: 'get',
			data: 'msubmenu=hwtest&action='+name,
			success: function(){
				alert("SUCCESS");
                document.location.reload();
			},
			error: function(){
				alert("NG");
			}
		});

}

function initEvent()
{
	$("#test_auto").on("click", function(e){
	    
        test_ajax("auto");
        alert("Press apply and then press the button for 2 seconds");
	});	

	$("#test_button").on("click", function(e){
        
        test_ajax("button");
        alert("Press apply and then press the button for 2 seconds");
	});	

	$("#test_wl").on("click", function(e){
        
        test_ajax("wl");
	});	

	$("#test_d1").on("click", function(e){
        
        test_ajax("d1");
	});	

	$("#test_d2").on("click", function(e){
        
        test_ajax("d2");
	});	

	$("#test_audioout").on("click", function(e){
        
        test_ajax("audioout");
	});	

	$("#cmdApplyFisheyeOffset").on("click", function(e){	
		$.when(set_cali_offset("manual")).done(function(){
 			if(capInfo['board_chipset'] != "amba_s5l66"){
				cal_cali_center();
			}	
			progressUI(false);
			if(completed_flag) alert("Success");
			else return 0;
			document.location.reload();
		});		
	});	
	$("#cmdApplyFisheyeCali").on("click", function(e){      // auto 				
		if(capInfo['board_chipset'] == "amba_s5l66"){
			console.log("s5l");
//			$.when(set_cali_offset("origin")).done(function(){ // Change the defalut origin as 0,0 if not origin 0,0 		
				$.when(cal_cali_center()).done(function(){
					$.when(get_cali_center_pos()).done(function(){	
						$.when(set_cali_offset("auto")).done(function(){	
//							cal_cali_center();
							progressUI(false);
							if(completed_flag) alert("Success");
							else return 0;
							document.location.reload();
						});											
				});				
			});
//			});
		}else{
			$.when(set_cali_offset("origin")).done(function(){ // Change the defalut origin as 0,0 if not origin 0,0 		
				$.when(cal_cali_center()).done(function(){
					$.when(get_cali_center_pos()).done(function(){	
						$.when(set_cali_offset("auto")).done(function(){	
							cal_cali_center();
							progressUI(false);
							if(completed_flag) alert("Success");
							else return 0;
							document.location.reload();
						});											
					});
				});				
			});
		}
	});	
}

function onLoadPage()
{
	Util.setOEM("logo");
	getJson();
	initLanguage();
	initUI();
	initValue();
	initEvent();
	checkMotion("displayCDSStatus", 2);
}
$(document).ready(function(){
	Util.setOEM("logo");
	onLoadPage();
});
//-->
