// this javascript page for defining common function 
// system time
var DW_EDGE_FIRMWARE = (0x1 << 1 );
function ERROR( cmd ) { alert(cmd); }
var diffTime;
var systime;
var refresh_web = 0;
var Browser = { chk : navigator.userAgent.toLowerCase() };
Browser = {
	ie : Browser.chk.indexOf('msie') !== -1,
	ie6 : Browser.chk.indexOf('msie 6') !== -1,
	ie7 : Browser.chk.indexOf('msie 7') !== -1,
	ie8 : Browser.chk.indexOf('msie 8') !== -1,
	ie9 : Browser.chk.indexOf('msie 9') !== -1,
	ie10 : Browser.chk.indexOf('msie 10') !== -1,
	opera : !!window.opera,
	safari : Browser.chk.indexOf('safari') !== -1,
	safari3 : Browser.chk.indexOf('applewebkir/5') !== -1,
	mac : Browser.chk.indexOf('mac') !== -1,
	chrome : Browser.chk.indexOf('chrome') !== -1,
	firefox : Browser.chk.indexOf('firefox') !== -1
};
var menu ;

var Util = {
	remove_menu : function( oem , menu) {
		for(var i = 0 ; i < Tabs.length ; i++) {
			for(var j = 0 ; j < Tabs[i].menu.length ; j++){ 
				if( capInfo['oem'] == oem && Tabs[i].menu[j][0] == menu )	Tabs[i].menu.splice(j, 1);	
				else if( oem == null && Tabs[i].menu[j][0] == menu )	Tabs[i].menu.splice(j, 1);	
			}
		}		
	}
	,setOEM : function(target){		
		if( capInfo['oem'] == 2)
		{
            $("#"+ target).click( function(){ window.open("http://digital-watchdog.com/"); });
			$("#div_left").append('<div class="copy_right" tkey="copy_right"></div>');
			$("#left_frame").append('<div class="copy_right" tkey="copy_right"></div>');
			
			$("#rtsp_auth").css("font-size","12.5px");		
		}
		else if( capInfo['oem'] == 5)
		{
			$("#logo").css( "cssText", "margin-bottom: 5px !important; margin-top: 10px !important;");			
		}
		else if( capInfo['oem'] == 1 || capInfo['oem'] == 6){
//			$('head').append('<link class="sb_css" rel="stylesheet" href="/css/sb.css" type="text/css" />');				
		}	
		else if( capInfo['oem'] == 8)
		{			
//			$("html").css("background", "rgba(116, 116, 116, 1) !important")
		}
		else if( capInfo['oem'] == 9)
		{			
			if( capInfo['have_pantilt'] == 0 ){
				$("#have_pantilt").remove();
				$("#preset").remove();
				$("#ptz_control_label").remove();
			}
		}
		
		if( capInfo['oem'] != 2 && capInfo['oem'] != 19 && capInfo['oem'] != 20 && capInfo['oem'] != 21)
		{
			$("#rtsp_auth").css( "cssText", "font-size: 11.5px !important");				
		}
	}	
}
function parserErroncode(str)
{
	var tmp= str.trim().split(':');
	var message = tmp[1].trim();

//	console.log(message);
	switch(message)
	{
		case "0" :  // APP_NONE
			message = getLanguage("msg_fail_retry");	
			break ;
		case "7" :  //  APP_ERR_OUT_OF_RANGE
			message = getLanguage("msg_outofrange");	
			break ;
		case "10" :  //  APP_ERR_OUT_OF_RANGE
			message = getLanguage("msg_duplicate_name");	
			break ;			
		case "11" : //  APP_ERR_CAPABILITY_NOT_SUPPORTED
			message = getLanguage("msg_outofcapability");			
			break;
		case "46" :
			message = getLanguage("msg_sd_format_fail_to_mediaserver");
			break ;	
		default : 
			message = getLanguage("msg_fail_retry");
			break;
	}
	return message ;
}
/*
   name 		: getTimeStamp
   operate 	: return time String.
   parameter 	: 
   - d : Time object 
   - f : if Time object is set the UTC, its value is True. 
   in case of the opposite, value is false.
   */
function getTimeStamp(d, f)
{

	function leadingZeros(n, digits)
	{
		var zero = '';
		n = n.toString();

		if (n.length < digits) {
			for (var i = 0; i < digits - n.length; i++)
				zero += '0';
		}
		return zero + n;
	}
	var s, yy, mm, dd, h, m, s, ap;
	if(f == true){
		s =
			yy = leadingZeros(d.getUTCFullYear(), 4);
			mm = leadingZeros(d.getUTCMonth() + 1, 2);
			dd = leadingZeros(d.getUTCDate(), 2);
			h = leadingZeros(d.getUTCHours(), 2);
			m = leadingZeros(d.getUTCMinutes(), 2);
			s = leadingZeros(d.getUTCSeconds(), 2);
	} else {
		s =
			yy = leadingZeros(d.getFullYear(), 4);
			mm = leadingZeros(d.getMonth() + 1, 2);
			dd = leadingZeros(d.getDate(), 2);
			h = leadingZeros(d.getHours(), 2);
			m = leadingZeros(d.getMinutes(), 2);
			s = leadingZeros(d.getSeconds(), 2);
	}
	if(hourFormat == 1){
		if(h > 12) {
			h = leadingZeros(h - 12, 2);
			ap = 'pm';
		}
		else ap = 'am';

		s = s + ap;
	}

	switch ( timeFormat ) {
		case 1 : // mm/dd/yy h:m:s
			s = mm + '/' + dd + '/' + yy + ' ' + h + ':' + m + ':' + s;
			break;
		case 2 : // dd/mm/yy h:m:s
			s = dd + '/' + mm + '/' + yy + ' ' + h + ':' + m + ':' + s;
			break;
		default :// yyyy-mm-dd h:m:s
			s = yy + '-' + mm + '-' + dd + ' ' + h + ':' + m + ':' + s;
			break;
	}
	return s;
}

function settingSuccess(title, str)
{

	var msg = getLanguage("msg_success");
	console.log(title);
//	var pattern = new RegExp("/|&");
//	title = title.substring(0,1).toUpperCase() + title.substring(1);
//	title = title.replace(pattern,"_");

	if( title == null || title == undefined)
	{
		msg = "Setting " + msg;
	}
	else
	{
		msg = title + " " + msg;
        console.log(msg);
	}
	if(str != null || str != undefined)
	{
		msg = msg + "\n[ " + str + " ]";
	}
	alert(msg);   
}
/*
   name 		: settingFail
   operate 	: alert ajax fail message and adding error string.
   parameter	: 
   - str : adding error message.
   */
function settingFail(title, str, mode)
{
	var msg = getLanguage("msg_fail");

	var pattern = new RegExp("/|&");
	
	if(mode == "1")
		str = parserErroncode(str);
	if( title == null || title == undefined)
	{
		msg = "Setting " + msg;
	}
	else
	{
		title = title.replace(pattern,"_"); 
		title = title.substring(0,1).toUpperCase() + title.substring(1);
		msg = title +" " + msg;
	}
	if(str != null || str != undefined)
	{
		if(mode == 2)
			msg = "[ " + str +  " ]\n"+msg;
		else
			msg = msg + "\n[ " + str +  " ]";
		
	}
	
	console.log(msg);
	alert(msg);
}
/*
	name		: checkMotion
	operator	: change the object image active and deactive status.
	parameter 	: obj => obj id
 */
var __motion_value = 0;
var count = 0 ;
var option = 0 ;
var timeout ;
function checkMotion(obj, option)
{
	var color = "#D90000";
	if(  capInfo['oem'] == 2 ) {
		color = "#EE7421";
	}
    else if(  capInfo['oem'] == 10 ) {
        color = "#6ea0be";
	}else if(  capInfo['oem'] == 9 ) {
		color = "#82bde1";
    }
	var _runCheckAlarm = false;
	function on()
	{
		$("#" + obj).removeClass("alarm_off");
		$("#" + obj).addClass("alarm_on");
		__motion_value = 1;
	}
	function off()
	{
		$("#" + obj).removeClass("alarm_on");
		$("#" + obj).addClass("alarm_off");
		__motion_value = 0;
	}
	function isOn()
	{
		if( $("#" + obj).attr("class") == "alarm_on" ) {
			return true;	
		} else {
			return false;
		}
	}
	function judgeMotion(value)
	{
		if( capInfo.video_in == 1 ) {
			if( value >= 1) {
				on();
			} else {
				off()
			}
			var object = $("#" + obj ).length != 0;
	/*		if( _runCheckAlarm && object )
			{
	//			setTimeout(check, 2000);
			}
			else if( object == false)*/
			if( object == false)
			{
				_runCheckAlarm = false;	
				if( isOn() )
					off();
			}
		}
		else {
			var icons = $("[name=" + obj + "]"), i;
			for( i=0; i < icons.length ; i++) {
				if((value & (0x1 << i)) > 0 ) { 
					icons[i].style.backgroundColor = color;
				} else {
					icons[i].style.backgroundColor = "#7E7E7E";
				}
			}
		}
	}
	function judgePIR(value)
	{
		if( value == 1) {
			$("#btnpir_e").css("background-color", color);
		}
		else{   $("#btnpir_e").css("background-color", "#7E7E7E");   }
	}
	function judgePIRCNT(value)
	{
        var elem = document.getElementById("btnpir_s");
        if(elem == null || elem == undefined)
            return;
		elem.innerHTML = value;
		if( value >= 1) {  $("#btnpir_s").css("background-color", color);       }
		else{   $("#btnpir_s").css("background-color", "#7E7E7E");   }
	}

	function judgeAlarmin(num, value)
	{
		if(option == 3)
		{
			if(num == 1){
                var elem1 = document.getElementById("alarminput1_adc");
                if(elem1 == null || elem1 == undefined)
                    return;
				elem1.innerHTML = value;
				if( value == 1) $("#alarminput1_adc").css("background-color", color);
				else            $("#alarminput1_adc").css("background-color", "#7E7E7E");
			}
			if(num == 2){
                var elem2 = document.getElementById("alarminput2_adc");
                if(elem2 == null || elem2 == undefined)
                    return;
				elem2.innerHTML = value;
				if( value == 1) $("#alarminput2_adc").css("background-color", color);
				else            $("#alarminput2_adc").css("background-color", "#7E7E7E");
			}
		}
		else{
			if(num == 1){
                var elem1 = document.getElementById("alarminput1");
                if(elem1 == null || elem1 == undefined)
                    return;
				elem1.innerHTML = value;
				if( value == 1) $("#alarminput1").css("background-color", color);
				else            $("#alarminput1").css("background-color", "#7E7E7E");
			}
			if(num == 2){
                var elem2 = document.getElementById("alarminput2");
                if(elem2 == null || elem2 == undefined)
                    return;                
				elem2.innerHTML = value;
				if( value == 1) $("#alarminput2").css("background-color", color);
				else            $("#alarminput2").css("background-color", "#7E7E7E");
			}
		}
	}
	function judgeAlarmout(num , value)
	{	
		
		if( option == 0 ){
			if( num == 1 ){
				if(  value == 0 ) 	$("#cb_relay_out1").prop("checked",false);
				else $("#cb_relay_out1").prop("checked",true);
			}
			if( num == 2 ){
				if(  value == 0 ) 	$("#cb_relay_out2").prop("checked",false);
				else $("#cb_relay_out2").prop("checked",true);
			}			
		}
	}
	function judgeMaxTemp(value)
	{
		for (i = 0; i < 8; i++)
			$("#m" + i + "_maxtemp").val(value[i]);
	}
	function judgeMinTemp(value)
	{
		for (i = 0; i < 8; i++)
			$("#m" + i + "_mintemp").val(value[i]);
	}
	function judgeAvgTemp(value)
	{
		for (i = 0; i < 8; i++)
			$("#m" + i + "_avgtemp").val(value[i]);
	}
	function judgeAreaTemperature(value)
	{	
		$("#" + obj).val(value);
		$("#" + obj).change();
	}

	function check()
	{

/*		if( window.opener != null && window.opener.location.pathname == "/cgi-bin/index.cgi")  // setup
		{
			judge(window.opener.__motion_value);
		}
		else   // main
		{*/
			try{
				$.ajax({
				url  : '/cgi-bin/result',
				data : "msubmenu=event&action=view",
//				dataType: "html",
				cache   : false,
				async: true,
				success : function(ret){
				    var idx  = 0;
					var tmp = ret.trim().split('\n');		
					
					try {                                     // system_time
						for( var i=0 ; i<tmp.length ; i++){
							if(tmp[i] == undefined) continue ;
							if( tmp[i].split('=')[0].trim() == "motion" ){
								var tmp2 = tmp[i].split('=')[1];  
								if (option < 2) judgeMotion(tmp2);
							}
							if( tmp[i].split('=')[0].trim() == "PIR" ){
								var tmp2 = tmp[i].split('=')[1];
								if (option<=2)  judgePIR(tmp2);
							}
							if( tmp[i].split('=')[0].trim() == "PIRCNT" ){
								var tmp2 = tmp[i].split('=')[1];
								if (option<=2)  judgePIRCNT(tmp2);
							}
							if( tmp[i].split('=')[0].trim() == "in0" ){
								var tmp2 = tmp[i].split('=')[1];  
								judgeAlarmin( 1, tmp2);
							}
							if( tmp[i].split('=')[0].trim() == "in1" ){
								var tmp2 = tmp[i].split('=')[1];  
								judgeAlarmin( 2, tmp2);
							}						
							if( tmp[i].split('=')[0].trim() == "out0" ){	
								var tmp2 = tmp[i].split('=')[1];  
								if (option<=2)	judgeAlarmout( 1, tmp2);
							}	
							if( tmp[i].split('=')[0].trim() == "out1" ){	
								var tmp2 = tmp[i].split('=')[1];  
								if (option<=2) judgeAlarmout( 2, tmp2);
							}
							if( tmp[i].split('=')[0].trim() == "refreshtime" ){
								var tmp2 = tmp[i].split('=')[1];  
								if(refresh_web == 0)
								{
									refresh_web = tmp2;
								}
								else if(refresh_web != tmp2)
								{
									refresh_web = tmp2;
								}	
							}
							if( tmp[i].split('=')[0].trim() == "ptzstatus" ){
								var tmp2 = tmp[i].split('=')[1];  
								if( tmp2 == 0 ) $("#focus_status").text("");
								if( tmp2 == 1) $("#focus_status").text(getLanguage("focus_status_doing"));						
								else if( tmp2 == 2) $("#focus_status").text(getLanguage("focus_status_completed"));
							}	
							if( tmp[i].split('=')[0].trim() == "system_time" ){
								var tmp2 = tmp[i].split('=')[1];  
								if(tmp2.length > 0)
								{
									systime = new Date(tmp2).getTime();
									if(typeof(systime) != 'undefined') 
									{
										diffTime = systime - new Date().getTime();
									}
								}
							}
							if( tmp[i].split('=')[0].trim() == "CDS" ){
								var tmp2 = tmp[i].split('=')[1];
								if (option==2) $("#" + obj).text(tmp2);
							}
							if( tmp[i].split('=')[0].trim() == "HTTPSMode" ){
								if (option <=2)
								{
									var tmp2 = tmp[i].split('=')[1];
									if( tmp2 == 0 ) $("#http_status").text("");						
									else if( tmp2 == 1) $("#http_status").text("The live video viewed in the browser will use RTSP over TCP. This data maybe un-encrypted");
								}
							}
							if( tmp[i].split('=')[0].trim() == "ADC0" ){
                                var tmp2 = tmp[i].split('=')[1];
                                if(tmp2 != 0) tmp2 = tmp2/10;
                                if(tmp2 > 3.5) tmp2 = 3.5;
                                if (option==3) $("#ADC0").text(tmp2);
                           }
                           if( tmp[i].split('=')[0].trim() == "ADC1" ){
                               var tmp2 = tmp[i].split('=')[1];
                               if(tmp2 != 0) tmp2 = tmp2/10;
                               if(tmp2 > 3.5) tmp2 = 3.5;
                               if (option==3)  $("#ADC1").text(tmp2);
                           }
							if( tmp[i].split('=')[0].trim() == "MaxTemp" ){
								var tmp2 = tmp[i].split('=')[1];
								judgeMaxTemp(tmp2.split('/'));
					   		}
						   if( tmp[i].split('=')[0].trim() == "MinTemp" ){
								var tmp2 = tmp[i].split('=')[1];
								judgeMinTemp(tmp2.split('/'));
					   		}
						   if( tmp[i].split('=')[0].trim() == "AvgTemp" ){
								var tmp2 = tmp[i].split('=')[1];
								judgeAvgTemp(tmp2.split('/'));
					   		}
							if( tmp[i].split('=')[0].trim() == "AreaTemperature" ){
								var tmp2 = tmp[i].split('=')[1];
								if (option==4)  judgeAreaTemperature(tmp2);
							}
						}
					} catch (e){
						console.log(e);
					}
					/////////////////////////////////
					if( option == 1){
						clearTimeout(timeout);
						timeout = setTimeout(check, 1000);
						option = 0 ;
					}
					if( option == 2){
						clearTimeout(timeout);
						timeout = setTimeout(check, 500);
					}
					else if( option == 4){
						clearTimeout(timeout);
						timeout = setTimeout(check, 1000);
					}
					else{
						clearTimeout(timeout);
						timeout = setTimeout(check, 2000);
					}
				},
				error: function(){
					// if failed, retry to get information afater 10 seconds
					clearTimeout(timeout);
					timeout = setTimeout(check, 10000); 
				},
				}); 
			}
			catch(exception)
			{
				console.log(exception);
				_runCheckAlarm = false;
			}			
//		}
	}
	_runCheckAlarm = true;
	 check();
	
}
/*
   name 		: setSlider
   operate 	: initialize the Jquery slider.
   parameter	: 
   - name : initialize object name.
   - min : set slider mininumal value.
   - max : set slider maximum value.
   */
function setSlider(name, min, max)
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
	function update(event, ui){
		obj.next().next().text( ui.value );
	}
    if( typeof(obj.slider('instance')) != 'undefined') {
        return true;
    }

	if( obj.next().prop("tagname") != "BUTTON" && obj.next().text() != "+")
		obj.before("<button>-</button>").after("<button>+</button>");
	obj.slider({
		min: min,
		max: max,
		slide :update,
		change : update
	});
	obj.next().on("click", function(){
		var value = obj.slider("value");
		obj.slider("value", ++value);
		obj.next().next().text( obj.slider("value") );
	});
	obj.prev().on("click", function(){
		var value = obj.slider("value");
		obj.slider("value", --value);    
		obj.next().next().text( obj.slider("value") );
	});
	return true;
}
function disabledSlider( name, value )
{
	var parent = $("#" + name).parent();
	parent.find("*").prop("disabled", value);
	if ( value )
		value = "disable";
	else
		value = "enable";
	parent.find(".ui-slider").slider(value);
}
/*
   name		: Disabled
   operate		: Change the DOM object status to "endlabed" or "disabled"
   parameter 	: 
   - val : if value is "true", DOM in body will disable. 
   if value is "false", DOM in body will enable.
   */
function Disabled(val)
{
	$("body").find("*").prop("disabled", val);

	if( val )	val = "disable";
	else		val = "enable";
	$(".ui-slider").slider(val);
}


/**
 * [parseViewCGI description]
 * @param  {[string]}  
 * @return {[Object]} 
 */
function parseViewCGI( input )
{
	var ret = new Object();
	var tmp, tmp2;

	tmp =  input.split("\r\n");

	for ( var i = 0 ; i < tmp.length ; i ++)
	{
		var tmp2 = tmp[i].split("=");
		ret[tmp2[0]] = tmp2[1];
	}
	return ret;
}
function isValidText( input )
{
	var n;
	var i;
	var tmp; 
	for (i=0; i<input.length; i++)
	{
		n = input[i];
		if ((n >= 'a' && n <= 'z') || (n >= 'A' && n <= 'Z') || (n >= '0' && n <= '9') || n == '-' || n == '_' || n == ' ' || n == '.' || n == '@')
			continue;
		else
			return false;
	}
	return true;
}
function getInformation(cmd, iStorageIndex)
{
	if( typeof(iStorageIndex) == 'undefined' ){
		iStorageIndex = 0;
	}
	function fail(){
		settingFail(menu, "apply fail. retry again.");
		refreshMenuContent();
	}
	var obj;
	$.ajaxSetup({async: false});
	switch(cmd)
	{
		case "record_management" :
			{
				$.ajax({
					type:"get",
					url: "/cgi-bin/admin/record.cgi",
					data: "msubmenu=manage&action=get",
					success: function(msg){
						obj = eval(msg);
					},
					error : fail
				});
			}
			break;
		case "record_list":
			{
				var data = {
					msubmenu : "list",
					action : "get",
					storage_index : iStorageIndex
				}
				$.ajax({
					type:"get",
					url: "/cgi-bin/admin/record.cgi",
					data: data,
					success: function(msg){
						var i, date = new Date();
						obj = eval(msg);
						if( typeof(obj) != "undefined" ){
							obj.reverse();
							for( i = 0 ; i < obj.length ; i++) {
			          if(  capInfo['oem'] == 6 )
                               obj[i].start = new Date((obj[i].start+((gmt-12)*3600) )* 1000).format("yyyy/mm/dd-HH:MM:ss", true);	
                else
                {						  
								date.setTime(obj[i].start * 1000);
								obj[i].start = date.format("yyyy/mm/dd-HH:MM:ss", false);
								}
								obj[i].key = makeRecordToken(obj[i].key_h, obj[i].key_l);
								while( obj[i].key.length < 16 ){
									obj[i].key = "0" + obj[i].key; 
								}
								date.setTime(obj[i].duration * 1000);
								obj[i].duration = date.format("MM:ss", false);
							}
						}
					},
					error: fail
				});
			}
			break;
		case "event_rules" :
			{

				$.ajax({
					type:"get",
					url: "/cgi-bin/admin/trigger.cgi",
					data: "msubmenu=event&action=get",
					success: function(msg){
						obj = eval(msg);
					},
					error : fail
				});
			}
			break;
		case "action_rules":
			{
				$.ajax({
					type:"get",
					url: "/cgi-bin/admin/trigger.cgi",
					data: "msubmenu=action&action=get",
					success: function(msg){
						obj = eval(msg);
					},
					error: fail
				});
			}
			break;
		case "log_list":
			{
				$.ajax({
					type:"get",
					url: "/cgi-bin/admin/system.cgi",
					data: "msubmenu=log&action=getlog",
					success: function(msg){
						obj = eval(msg);
					},
					error: fail
				});
			}
			break;	
 	        case "scan_cube_wifi":
            	{
                 $.ajax({
                                      type:"get",
                                      url: "/cgi-bin/admin/cube_wifi.cgi",
                                        data: "msubmenu=wifi_setup&action=scan_cube_wifi",
                                        success: function(msg){
                                                obj = eval(msg);
                                        },
                                        error : fail
                                });
            	}
             	break;
		case "set_cube_wifi":
                        {
                                $.ajax({
                                        type:"get",
                                        url: "/cgi-bin/admin/cube_wifi.cgi",
                                        data: "msubmenu=wifi_setup&action=set_cube_wifi",
                                        success: function(msg){
                                                obj = eval(msg);
                                        },
                                        error: fail
                                });
                        }
                        break;		
 	        case "scan_iot_wifi":
            	{
                 $.ajax({
                                      type:"get",
                                      url: "/cgi-bin/admin/iot_wifi.cgi",
                                        data: "msubmenu=wifi_setup&action=scan_iot_wifi",
                                        success: function(msg){
                                                obj = eval(msg);
                                        },
                                        error : fail
                                });
            	}
             	break;
		case "set_iot_wifi":
                        {
                                $.ajax({
                                        type:"get",
                                        url: "/cgi-bin/admin/iot_wifi.cgi",
                                        data: "msubmenu=wifi_setup&action=set_iot_wifi",
                                        success: function(msg){
                                                obj = eval(msg);
                                        },
                                        error: fail
                                });
                        }
                        break;		
		default :
			obj = new Object();
	}
	$.ajaxSetup({async: true});
	return obj;
}
var dateFormat = function () {
	var	token = /d{1,4}|m{1,4}|yy(?:yy)?|([HhMsTt])\1?|[LloSZ]|"[^"]*"|'[^']*'/g,
		timezone = /\b(?:[PMCEA][SDP]T|(?:Pacific|Mountain|Central|Eastern|Atlantic) (?:Standard|Daylight|Prevailing) Time|(?:GMT|UTC)(?:[-+]\d{4})?)\b/g,
		timezoneClip = /[^-+\dA-Z]/g,
		pad = function (val, len) {
			val = String(val);
			len = len || 2;
			while (val.length < len) val = "0" + val;
			return val;
		};

	// Regexes and supporting functions are cached through closure
	return function (date, mask, utc) {
		var dF = dateFormat;

		// You can't provide utc if you skip other args (use the "UTC:" mask prefix)
		if (arguments.length == 1 && Object.prototype.toString.call(date) == "[object String]" && !/\d/.test(date)) {
			mask = date;
			date = undefined;
		}

		// Passing date through Date applies Date.parse, if necessary
		date = date ? new Date(date) : new Date;
		if (isNaN(date)) throw SyntaxError("invalid date");

		mask = String(dF.masks[mask] || mask || dF.masks["default"]);

		// Allow setting the utc argument via the mask
		if (mask.slice(0, 4) == "UTC:") {
			mask = mask.slice(4);
			utc = true;
		}

		var	_ = utc ? "getUTC" : "get",
			d = date[_ + "Date"](),
			D = date[_ + "Day"](),
			m = date[_ + "Month"](),
			y = date[_ + "FullYear"](),
			H = date[_ + "Hours"](),
			M = date[_ + "Minutes"](),
			s = date[_ + "Seconds"](),
			L = date[_ + "Milliseconds"](),
			o = utc ? 0 : date.getTimezoneOffset(),
			flags = {
				d:    d,
				dd:   pad(d),
				ddd:  dF.i18n.dayNames[D],
				dddd: dF.i18n.dayNames[D + 7],
				m:    m + 1,
				mm:   pad(m + 1),
				mmm:  dF.i18n.monthNames[m],
				mmmm: dF.i18n.monthNames[m + 12],
				yy:   String(y).slice(2),
				yyyy: y,
				h:    H % 12 || 12,
				hh:   pad(H % 12 || 12),
				H:    H,
				HH:   pad(H),
				M:    M,
				MM:   pad(M),
				s:    s,
				ss:   pad(s),
				l:    pad(L, 3),
				L:    pad(L > 99 ? Math.round(L / 10) : L),
				t:    H < 12 ? "a"  : "p",
				tt:   H < 12 ? "am" : "pm",
				T:    H < 12 ? "A"  : "P",
				TT:   H < 12 ? "AM" : "PM",
				Z:    utc ? "UTC" : (String(date).match(timezone) || [""]).pop().replace(timezoneClip, ""),
				o:    (o > 0 ? "-" : "+") + pad(Math.floor(Math.abs(o) / 60) * 100 + Math.abs(o) % 60, 4),
				S:    ["th", "st", "nd", "rd"][d % 10 > 3 ? 0 : (d % 100 - d % 10 != 10) * d % 10]
			};

		return mask.replace(token, function ($0) {
			return $0 in flags ? flags[$0] : $0.slice(1, $0.length - 1);
		});
	};
}();

// Some common format strings
dateFormat.masks = {
	"default":      "ddd mmm dd yyyy HH:MM:ss",
	shortDate:      "m/d/yy",
	mediumDate:     "mmm d, yyyy",
	longDate:       "mmmm d, yyyy",
	fullDate:       "dddd, mmmm d, yyyy",
	shortTime:      "h:MM TT",
	mediumTime:     "h:MM:ss TT",
	longTime:       "h:MM:ss TT Z",
	isoDate:        "yyyy-mm-dd",
	isoTime:        "HH:MM:ss",
	isoDateTime:    "yyyy-mm-dd'T'HH:MM:ss",
	isoUtcDateTime: "UTC:yyyy-mm-dd'T'HH:MM:ss'Z'"
};

// Internationalization strings
dateFormat.i18n = {
	dayNames: [
		"Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat",
	"Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"
		],
	monthNames: [
		"Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec",
	"January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"
		]
};

// For convenience...
Date.prototype.format = function (mask, utc) {
	return dateFormat(this, mask, utc);
};
String.prototype.isDigit = function(){
	return ((/\d+/g.test(this))&&!(/\D+/g.test(this)));
};
function makeRecordToken(key_h, key_l)
{
	// ORIG
	// var ke6y;
	// key = key_h.toString(16) + key_l.toString(16);
	// while( key.length != 16){ key = "0" + key; }
	// return key;

	// PATCH
	var hex_key_h, hex_key_l;

	hex_key_h = key_h.toString(16);
	while( hex_key_h.length < 8){ hex_key_h = "0" + hex_key_h; }

	hex_key_l = key_l.toString(16);

	while( hex_key_l.length < 8){ hex_key_l = "0" + hex_key_l; }
	return hex_key_h + hex_key_l;
}
function ipv4_validation(value) {
	var reg=/[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}/
	if( reg.test(value) ) {
		tmp = value.split('.');
		if( tmp.length != 4 ) return false;
		for(var i=0; i < tmp.length ; i++) {
			if( tmp[i] > 255 || tmp[i] < 0 || tmp[i]== '') return false;
		}
		return true;
	}
	return false;
}
function Value(){
	this.setValue = function($items, $value, $translate){
		try {
			$items.forEach(function(e){
				var value = $value[e];
				if( typeof( value ) == "undefined" ){
					console.log(" can't find " + e + "'s value at list");
				}
				if( typeof($translate) != 'undefined' && $translate.hasOwnProperty(e)){
					if( typeof( $translate[e][value] ) != 'undefined' ){
						value = $translate[e][value];
					}
				}
				var obj = $("#" + e);
				if( obj.length == 0 ){
					obj = $("[name=" + e + "]");
				}
				if( obj.length == 0 ){
					console.log("can't find " + e);
					return;
				}
				var tag = obj.prop("tagName");
				if( typeof(tag) == 'undefined'){
					console.log("tagName is" + tag);
					return;
				} else if( tag == "SELECT" ) {
					obj.val( value );
				} else if( tag == "INPUT") {
					var type = obj.prop("type");
					if( type == "radio") {
						$("input[name=" + e + "]:checked").removeProp("checked");
						$("input[name=" + e + "][value=" + value + "]").prop("checked", true);
					} else if( type =="checkbox") {
						//todo
						console.log("todo checkbox");
					} else {
						obj.val(value);
					}
				}
			});
		}
		catch(e) {
			console.error(e);
		}
	}
	this.getValue = function($str){
		try {
			var obj = $("#" + $str);
			if( obj.length == 0 ){
				obj = $("[name=" + $str + "]");
				if( obj.length == 0 ){
					console.log("can't find " + $str);
					return undefined;
				}
			}
			var tag = obj.prop("tagName");
			if( typeof(tag) == 'undefined'){
				console.log("tagName is" + tag);
				return undefined;
			} else if( tag == "SELECT" ) {
				return obj.val();
			} else if( tag == "INPUT" || tag == "TEXTAREA" ) {
				var type = obj.prop("type");
				if( type == "radio" || type == "checkbox") {
					return $("input[name=" + $str + "]:checked").val();
				} else {
					return obj.val();
				}
			}
			return undefined;
		} catch(e) {
			console.log(e);
		}
	}	
	
}
function getErrorCode(str){
	var regex = new RegExp(/result[\S|\s]:[\S|\s]\d*/g);
	return regex.exec(str)[0].split(":")[1];
}
function progressUI(input, option){
	var enabled = true;
	if( input == false ){
		enabled = false;
	}
	if( enabled == true ) {
		var body = $("body");
		var w = body.width();
		var h = body.height();
		if(option == 1 ) var content="<figure class='loading option1'>";
		else  var content="<figure class='loading'>";
		
		content += "<div><img src='/images/loading.gif' />";
		
		if(option == 1 ) content += "<figcaption>Processing...</figcaption>";
		else content += "<figcaption>"+getLanguage("setup_msg_process")+"</figcaption>";
		content += "</div></figure>";
		body.append(content);
	} else {
		$("figure[class=loading]").remove();
	}
}

function Validation(){
	this.isValidText = function(input){
		var obj = $("#" + input);
		var r = /^[a-zA-Z0-9-_.@]+$/;
		var x = r.test(obj.val());	
		if( x == false ){
			alert(getLanguage("validation_text_network"));
		}
		return x ;
	}
	this.blank = function(input){
		var obj = $("#" + input).val();
		var tkey = $("#" + input).prev().attr("tkey");
		if( obj == ""){
			var message = getLanguage("msg_check_blank") +"( "+ getLanguage(tkey) +" )";
			settingFail(menu, getLanguage(message));
			return false;	
		}
		return true ;
	}
	this.isonlynumber = function(input){
		var obj = $("#" + input).val();
		if (!obj.match(/^[0-9]+$/)) 
		{
			settingFail(menu, getLanguage("msg_onlynumber"));
			return false;	
		}
		return true ;
	}
	this.textlength = function(input , min, max){
		var obj = $("#" + input);
		var tkey = $("#" + input).prev().attr("tkey");
		if( obj.val().length < min || obj.val().length > max ){
			var message = getLanguage("validation_length") + "( "+min + "~" + max +" )"+"( "+ getLanguage(tkey) +" )";
			settingFail(menu, message);
//			alert(message);
			return false ;	
		}
		return true ;
	}
	this.isValiPort = function(input , min, max){
		var obj = $("#" + input);
		if( obj.val()< min || obj.val() > max ){
			var message =  getLanguage("validation_length") + "(" + min + "~" + max + ")" ;
			alert(message);
			return false ;	
		}
		return true ;
	}
	this.isValidMcasIP = function(input){
		 var obj = $("#" + input);
		 if (/^(22[4-9]|23[0-9])\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$/.test(obj.val()) )
		 {  
//			 alert("You have entered an IP ad dress!")  
			 return true ; 
		 }  		
		 alert(getLanguage("multicast_waring"));  
		 return false  ;		
	}
	this.check_range = function(min, max, name, initval){
		var val = $("#"+ name ).val();
		
		if( val == initval ){         // default value
			return true;	
		}	
		if( val < min || val > max ) {   // check range
//			$("#"+name).val(lastVideoInfo[activeChannel][name]);  
			if( menu == undefined ){
				alert("Input the value between " +min+ "~"+max );
			}
			else {
				settingFail(menu, getLanguage("msg_outofrange"));
			}
			return false ;
		}
		return true;
	}
}
function getSelectListItem() {
	var obj = $(".sel_list_item");
	if( obj.length == 0 ){
		return -1;
	} else {
		return obj.attr("val");
	}
}
function checkRecoveryMode(capInfo) {
	try {
		if( typeof(capInfo) == "object" &&
				capInfo.hasOwnProperty('recovery_mode') ) {
			return capInfo['recovery_mode'] == 1 ? true : false;
		}
	} catch(e) {
		console.log(e);
	}
}

function getVinSourceIndex(id)
{
	if( $(id + " option").length > 0 ) {
		return $(id).prop("selectedIndex");
	}
	return 0;
}

function commonCreateSourceSelectBox(id, align)
{
/*	if( capInfo.video_in <= 1 ) {
		$(id).parent().parent().remove();
	}
*/
	if( capInfo.video_in > 1){
		$(id).parent().parent().show();
	}
	if( $(id).find("option").length == 0 ) {
		var cmd = '';
		if( align == 'align_right') {
			$(id).parent().parent().addClass("selSource");
		}
		for(var i=1 ; i <= capInfo.video_in ; i++) {
			if(i-1 == MJ.id) {
        cmd += "<option value=" + i + " selected>" + getLanguage("setup_video");
      } else {
        cmd += "<option value=" + i + ">" + getLanguage("setup_video");
      }
			cmd += i +  "</option>";
		}
		$(id).append(cmd);
		//MJ.change_video_id(0);
	}
	return 0;
}

function commonCreateAllSettingButton()
{
    if( $("#btApplyAll").size()  == 0){
    if( capInfo.video_in>1){
            var cmd = '';
            cmd += " <button class=\"button\" id=\"btApplyAll\">";
            cmd += "<span tkey=\"setup_apply_all\"></span>";
            cmd += "</button>";
            $("#btOK").after(cmd);
        }
    }
}
function getStorageTypeName(type){
	var text ="";
	switch ( type ) {
		case 0:
			text = "setup_none";
			break;
		case 1:
		case 3:
			text = "setup_sdcard";
			break;
		case 2:
			text = "Network Shared";
			break;
	}
	return getLanguage(text);
}
function initDisplayMotionStatus(id, num) {
	var i, cmd = '';
	if( num == 1 ) {
		cmd += "<div id='displayMotionStatus' class='alarm_off'></div>";
	} 
	else {
		for(i=0; i < num; i++){
			cmd += "<button name=displayMotionStatus class='button box'>";
			cmd += Number(i+1) + "</button>";
		}
		$("#" + id).removeClass("right");
	}
	$("#" + id).find("div").remove();
	$("#" + id).append(cmd);
}
function relMouseCoords(event) {
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
function checkCharacters(name,text) {
	var n;
	var i,j;
	var tmp; 
	//var ob = $(text).val();
	for (i=0; i<text.length; i++)
	{
		n = text.charCodeAt(i);
		// # : 35 , \ : 92 , " : 34
		// & : 39 , + : 43 , ' : 39
		if(( n == 34 || n== 35 || n == 38 || n == 43 || n == 92 || n == 39 )&& name!='camera_profile')
			return false;
		if(name == 'record'){
			for(j=33;j<=47;j++)
				if(n == j&& n != 45)
					return false;
			for(j=58;j<=64;j++)
				if(n == j)
					return false;
			for(j=92;j<=96;j++)
				if(n == j && n != 95)
					return false;
			for(j=123;j<=126;j++)
				if(n == j)
					return false;
		}
		// 숫자, 영문(대,소), 특수문자(-, _, 공백) 만 허용
		if (name == 'profile')
		{
			if (!((n == 32) || (n == 45) || (n > 47 && n < 58) || (n > 64 && n < 91) || (n == 95) || (n > 96 && n < 123)))
				return false;
		}
        if(name == 'camera_profile'){
            if(n == 32)
                return false;
        }
	}
	return true;
}

// 쿠키 생성
function setCookie(cName, cValue, cDay){
	var expire = new Date();
	expire.setDate(expire.getDate() + cDay);
	cookies = cName + '=' + escape(cValue) + '; path=/ '; // 한글 깨짐을 막기위해 escape(cValue)를 합니다.
	if(typeof cDay != 'undefined') cookies += ';expires=' + expire.toGMTString() + ';';
	document.cookie = cookies;
}

// 쿠키 가져오기
function getCookie(cName) {
	cName = cName + '=';
	var cookieData = document.cookie;
	var start = cookieData.indexOf(cName);
	var cValue = '';
	if(start != -1){
		start += cName.length;
		var end = cookieData.indexOf(';', start);
		if(end == -1)end = cookieData.length;
		cValue = cookieData.substring(start, end);
	}
	return unescape(cValue);
}
function check_valid_data(data)
{
	var invalid_pattern = /[&+"]/gi; 
	if(invalid_pattern.test(data))
		return false;
	return true;
}

function isIE() {
	return (((navigator.appName == 'Microsoft Internet Explorer') && (capInfo["oem"] != 19 && capInfo["oem"] != 20 && capInfo["oem"] != 21))
		|| ((navigator.appName == 'Netscape')
			&& (new RegExp("Trident/.*rv:([0-9]{1,}[\.0-9]{0,})").exec(navigator.userAgent) != null)));
}

function isIE_fix()
{
	var agent = navigator.userAgent.toLowerCase(); 
	var ret = true;
	if ( (navigator.appName == 'Netscape' && navigator.userAgent.search('Trident') != -1) || (agent.indexOf("msie") != -1) )
		ret = true;
	else
	 	ret = false;

	return ret;
}
