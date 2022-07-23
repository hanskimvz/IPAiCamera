var menu = getLanguage("setup_inode_config");
var settingList = ["enabled","ftp_addr","upload_path","port","id","pass","type","image_num", "pre_duration", "post_duration", "duration", "autodelete", "target_stream", "rec_pre_duration" ,"rec_post_duration"];


function getvalue(val)
{
	switch(val)
	{	
		case "settingList" :
			for( var i = 0 ; i < settingList.length ; i++)	
			{	
			var obj = $("#" + settingList[i]);
			var tag = obj.prop("tagName");
				if( tag == "SELECT" || tag == "INPUT")
				{
					obj.val(iNodeInfo[settingList[i]]);
				}	
			}
		break ;
	}
}


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
function initUI()
{
	if(iNodeInfo['enabled'] == 0){
		disabled("Ftpcontent",true);
		disabled("Imagescontent",true);
		disabled("Videocontent",true);
		disabled("operation_layer",true);
		disabled("type_select",true);
	} else {
		disabled("Ftpcontent", false);
		disabled("Imagescontent",false); 
		disabled("Videocontent",false); 
		disabled("operation_layer",false);
		disabled("type_select",false);
	}
	if(iNodeInfo['type'] == 0){
		$("#Imagescontent").css("display", "block");
		$("#Videocontent").css("display", "none");
	}
	else
	{
		$("#Imagescontent").css("display", "none");
		$("#Videocontent").css("display", "block");
	}
}
function checkDependency(val)
{
    if(val == 0){
	    $("#pre_duration").val(iNodeInfo["pre_duration"]);
        $("#post_duration").val(iNodeInfo["post_duration"]);
    }
    else{
	    $("#pre_duration").val(iNodeInfo["rec_pre_duration"]);
        $("#post_duration").val(iNodeInfo["rec_post_duration"]);
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
			$("[name=" + id + "][value=" + iNodeInfo[id] + "]").attr("checked", true);
		}else {
			obj.val( iNodeInfo[id]);
		}
	});
	console.log("test");
	//$("#duration").val(iNodeInfo[11]);
	getvalue("settingList");
	
	//var selindex = $("#image_num option").index($("#image_num option:selected"));

	checkDependency(iNodeInfo['type']);	

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
			disabled("Imagescontent",true);
			disabled("Videocontent",true);
			disabled("operation_layer",true);
			disabled("type_select",true);
		} else {
			disabled("Ftpcontent", false);
			disabled("Imagescontent",false); 
			disabled("Videocontent",false); 
			disabled("operation_layer",false);
			disabled("type_select",false);
		}
	});
	$("[name=type]").click( function(e){
		if( e.delegateTarget.value == 0)
		{
			$("#Imagescontent").css("display", "block");
			$("#Videocontent").css("display", "none");

		} else {
			$("#Imagescontent").css("display", "none");
			$("#Videocontent").css("display", "block");
        }
        checkDependency(e.delegateTarget.value);	
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

		for( var i = 0 ; i < settingList.length ; i++)	
			{	
				var obj = $("#" + settingList[i]);
				
				if(($("[name = "+settingList[i]+"]").prop("type")) == "radio")  // radio 
				{
					newValue = $("[name="+settingList[i]+"]:checked").val();
				}
				else if(($("[name = "+settingList[i]+"]").prop("type")) == "checkbox")  // checkbox 
				{
					newValue = $("[name = "+settingList[i]+"]").is(":checked")?1:0;
				}
				else // select , input 
				{
					newValue = obj.val();				
				}
					orgValue = iNodeInfo[settingList[i]];
					if( orgValue != newValue )
					{
						arg[settingList[i]] = newValue;
					}
			}
		
		//if(arg.length != 0) {
			arg["msubmenu"]="inode";
			arg["action"] ="apply";
		//} else {
		//	settingFail(menu, getLanguage("msg_nothing_changed"));
		//	return ;
		//}

		$.ajax({
			type:"get",
			url: "/cgi-bin/admin/transfer.cgi",
			data: arg,
			success: onSuccessApply, 
			error: onFailApply
		});
	});
}

function onLoadPage() {	
	initvalue();
	initUI();	
	initEvent();
}

$(document).ready( function() {
	onLoadPage();
});
