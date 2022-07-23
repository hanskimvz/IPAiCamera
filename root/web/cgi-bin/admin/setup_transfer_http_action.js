var menu = getLanguage("setup_http_config");
var settingList = ["enabled", "description", "http_addr", "http_port", "id", "pass", "message" ]; // radio 버튼 제외

function disabled(val ,cmd) {
	$("[name="+val + "]").find("select, input, button, textarea").each(function(i, e){
		var type = $(this).prop("id") ;
		$("#"+ type).prop("disabled", cmd);		
	});
}
function chkNumber(min, max, dft) {
	var objEv = event.srcElement;
	var objVal= objEv.value;
	var numPattern = /([^0-9])/;
	var numPattern = objEv.value.match(numPattern);
	if (numPattern != null) {
		settingFail(menu, "only input the number.");		
		objEv.focus();
		objEv.value = dft;
		return false;
	}
	if(objEv.value > max || objEv.value < min){
		objEv.setfocus=true;
		settingFail(menu, "your input valeu is out of range.");
		objEv.value = dft;
		return false;
	}
}

function initUI()
{
	if(HTTPActionInfo['enabled']== 0){
		disabled("SmtpContent",true);
	}
	else{
		disabled("SmtpContent", false);
	} 
}
function initvalue()
{	
	var i, obj, tag, type, str;
	/*
	if(HTTPActionInfo["ssl_enable"]== 0){
		$("[name=ssl_enable][value=0]").trigger("click");
	} else {
		$("[name=ssl_enable][value=1]").trigger("click");
	}
	*/
	var value = new Value();
	value.setValue(settingList, HTTPActionInfo);
	console.log(value);

	settingList.forEach(function(id){
		obj = $("#" + id);
		if( obj.length == 0 ) {
			obj = $("[name=" + id +"]");
			if( obj.length == 0 ) {
				consoel.log("initValue() error!!");
				return;
			}
		}
		tag = obj.prop("tagName");
		type = obj.prop("type");
		if( type == "radio"){
			$("[name=" + id + "][value=" + HTTPActionInfo[id] + "]").attr("checked", true);
		} else if( tag == "SELECT" || tag == "INPUT" ) {
			obj.val( HTTPActionInfo[id] );
		} else if( tag == "TEXTAREA") {
			str = HTTPActionInfo[id];
			obj.val(restoremsg(str));
		}
	});
	checkDependency("enable");	
}
function checkDependency(index) {

	
}
function checkblank(val , msg){
	pop_msg = getLanguage(msg);
	if($("#" + val).val() == "" ){
		settingFail(menu, pop_msg);
		return false ; 
	}		
	return true;
}
function replacemsg(msg) {
	msg = msg.replace(/(?:\r\n|\r|\n)/g, '<br/>');
	return msg;
}
function restoremsg(msg) {
	msg = msg.split('<br/>').join("\r\n");
	return msg;
}
function initEvent() {
	$("[name=enabled]").click( function(e){
		if( e.delegateTarget.value == 0) {
			disabled("SmtpContent",true);
		} else {
			disabled("SmtpContent", false); 
		}
		$("#http_port").val(HTTPActionInfo["http_port"]);
	});

	$("#btOK").click(function(event) {
		if($("[name=enabled]:checked").val() == 1){
//            if(!checkblank("name", "msg_upnp_check_blank")) return;			
			if(!checkblank("http_addr", "msg_http_check_serveraddr")) return;			
			if(!checkblank("http_port", "msg_http_check_port")) return;
		}
		var items = HTTPActionInfo;
		var cgiData = new Object();
		var data = null; 
		var newValue;
		var orgValue;
		var value = new Value();
		var change=0;

		var fail = settingList.some(function(e){
			newValue = value.getValue(e);
			oldValue = items[e];
			if( newValue != oldValue ) {
				cgiData[e] = newValue;
				if(e == "message") cgiData[e] = replacemsg(cgiData[e]);
				change ++;
			}
		});
		if(change == 0)
		{
			settingFail(menu, getLanguage("msg_nothing_changed"));
		}else
		{
			if( !fail){
				console.log(cgiData);
				_ajax(cgiData);
			}
		}
	});
	
/*	$("#id").blur( function(obj){
		if( $("#id").val().length < 4 )  
		{ 
			pop_msg = getLanguage("msg_id_wrong");
			settingFail(menu, "ID is upper 4 character.");
			return false; 
		}
	});
	$("#pass").blur( function(obj){
		if( $("#pass").val().length < 4 )  		{ 
			pop_msg = getLanguage("msg_passwd_wrong");
			settingFail(menu, "ID is upper 4 character.");
			return false; 
		}
	});*/
	function check_length(val){
		if( val == "id" ){
			if( $("#id").val().length < 4 ){  				
				settingFail(menu, getLanguage("msg_id_wrong"));
				return false; 
			}
		}
		else if( val == "pass"){
			if( $("#pass").val().length < 4 ){  				
				settingFail(menu, getLanguage("msg_passwd_wrong"));
				return false; 
			}			
		}	
	}

}
function _ajax(data) {
	$.ajax({
		type:"get",
		url: "/cgi-bin/admin/transfer.cgi?msubmenu=httpaction&action=apply",
		data: data,
		success: function(ret){
			var reg=/OK/g;
			if( reg.test(ret) ){
				settingSuccess(menu, getLanguage("msg_success"));
				refreshMenuContent();
			}else{
				settingFail(menu,getLanguage("msg_fail_retry"));
			}
		}, error: function(ret){
			settingSuccess(menu, getLanguage("msg_fail_retry"));
		}
	});
}

function onLoadPage() {	
	initEvent();
	initvalue();
	initUI();
}

$(document).ready( function() {
	onLoadPage();
});
