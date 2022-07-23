var menu = getLanguage("setup_ftp_config");
var settingList = ["enabled","ftp_addr","upload_path","port","id","pass"]; 
function disabled(val ,cmd) {
	$("#"+val).find("select, input").each(function(i, e){
		var type = $(this).prop("id") ;
		$("#"+ type).prop("disabled", cmd);		
	});
}
function validateURL(textval) {
	var urlregex = new RegExp("^(ftp.){1}([0-9A-Za-z]+\.)");
	return urlregex.test(textval);
}
function validationAddress(textval) {
	var ipformat = /^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$/;
	return ipformat.test(textval);
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
function disabled(val ,cmd)
{
	$("#"+val).find("select, input").each(function(i, e){
		var abc = $(this).prop("id") ;
		$("#"+ abc).prop("disabled", cmd);		
	});
}
function initUI()
{
	if(FtpInfo['enabled'] == 0){
		disabled("Ftpcontent",true);
	} else {
		disabled("Ftpcontent", false); 
	}
}
function initvalue()
{
	var i, obj, tag, type;
	settingList.forEach(function(id){
		obj = $("#" + id);
		if( obj.length == 0 ) {
			obj = $("[name=" + id + "]");
			if( obj.length == 0 ) {
				console.log("initValue() error!!");
				return;
			}
		}
		tag = obj.prop("tagName");
		type = obj.prop("type");
		if( tag == "INPUT" && type == "radio") {
			$("[name=" + id + "][value=" + FtpInfo[id] + "]").attr("checked", true);
		}else {
			obj.val( FtpInfo[id]);
		}
	});
}
function checkblank(val , msg){
	if($("#" + val).val() == "" ){
		settingFail(menu, getLanguage(msg));
		return false ; 
	}		
	return true;
}
function initEvent()
{
	$("[name=enabled]").click( function(e){
		if( e.delegateTarget.value == 0)
		{
			disabled("Ftpcontent",true);
		} else {
			disabled("Ftpcontent", false); 
		}
	});
	$("#btOK").click(function() {
		
		if($("[name=enabled]:checked").val() == 1){
			if(!checkblank("ftp_addr", "msg_ftp_check_serveraddr")) return;			
			if(!checkblank("upload_path", "msg_ftp_check_uploadpath")) return;
			if(!checkblank("port", "msg_ftp_check_ftpport")) return;
			if(!checkblank("id", "msg_ftp_check_ftpid")) return;
			if(!checkblank("pass", "msg_ftp_check_ftppass")) return;
		}
		
		function onSuccessApply(msg) {
			var tmp= msg.trim().split('\n');
			var response = tmp[0];
			var errcode= response.trim().split('=');
			var error_code = errcode[1];

			if(response == "OK") {		
				settingSuccess(menu, null);
				refreshMenuContent();
			} else {
				if(error_code == 0)
					settingFail(menu, getLanguage("msg_nothing_changed"));
				else if(error_code == 6)
					settingFail(menu, getLanguage("msg_invalid_text"));
				else if(error_code == 7)
					settingFail(menu, getLanguage("msg_outofrange"));	
				else									
					settingFail(menu, getLanguage("msg_fail"));	
			}
		}
		function onFailApply() {
			settingFail(menu, getLanguage("msg_fail_retry"));
			refreshMenuContent();
		}	

		var arg = {};
		var newValue;
		var orgValue;
		for( var i = 0 ; i < settingList.length ; i++){
			var obj = $("#" + settingList[i]);
			if( obj.length == 0 ) {
				obj = $("[name=" + settingList[i] + "]:checked");
				if( obj.length == 0 ) {
					consoel.log("initValue() error!!");
					return;
				}
			}
			newValue = obj.val();
			orgValue = FtpInfo[settingList[i]];
			if( orgValue != newValue ) {
				arg[settingList[i]] = newValue;
			}
		}
		if(arg.length != 0) {
			arg["msubmenu"]="ftp";
			arg["action"] ="apply";
		} else {
			settingFail(menu, getLanguage("msg_nothing_changed"));
			return ;
		}

		$.ajax({
			type:"get",
			url: "/cgi-bin/admin/transfer.cgi",
			data: arg,
			success: onSuccessApply, 
			error: onFailApply
		});
	});

/*	$("#ftp_addr, #upload_path, #port, #id, #pass").blur( function(obj){
		//console.log("asdf");
		checkblank(obj.target.id);
		valAddress	= $("#ftp_addr").val();
		if( valAddress != ftp.address ){
			if( !validateURL(valAddress) && !validationAddress(valAddress) ) {
				alert(getLanguage("msg_ftp_wrong"));
				$("#ftp_addr").val(FtpInfo["ftp_addr"])
				return;
			}
		}
	});*/
/*	
	$("#id").blur( function(obj){
		if( $("#id").val().length < 4 )  { 
			settingFail(menu, "ID is upper 4 character.");
			return false; 
		}
	});
	$("#pass").blur( function(obj){
		if( $("#pass").val().length < 4 )  { 
			settingFail(menu, "Password is upper 4 character.");
			return false; 
		}
	});
*/
}

function onLoadPage() {	
	initvalue();
	initUI();	
	initEvent();
}

$(document).ready( function() {
	onLoadPage();
});
