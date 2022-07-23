var menu = getLanguage("rtsp_auth_config");
var settingList = [ 'AuthEnabled' ];

function initUI(){

}
function initValue(){
	settingList.forEach(function(target){
		var obj = $("#" + target);
		if( obj.length == 0 ) obj = $("[name=" + target + "]");
		var tag = obj.prop("tagName");

		if( tag == "INPUT"){
			type = obj.prop("type");	
			if( type == "radio"){
				obj = $("[name="+target+"][value="+CRtspAuthinfo[target]+"]").prop("checked",true);
			} else {
				obj.val(CRtspAuthinfo[target]);
			}
		} else {
			obj.val(CRtspAuthinfo[target]);
		}
	});
}

function initEvent(){
	$("#btOK").click( function(){
		var data="msubmenu=rtsp_authentication&action=apply";
		var changed = 0;
		settingList.forEach(function(target){
			var obj = $("#" + target);
			if( obj.length == 0 ) obj = $("[name=" + target + "]:checked");
			var newVal=obj.val();
			var oldVal=CRtspAuthinfo[target];
			
			console.log(target + "(" + newVal + "/" + oldVal + ")");
			if( newVal != oldVal ){
				data += "&" + target + "=" + newVal;
				changed++;
			}
		});
		if( changed == 0 ){
			settingFail(menu, getLanguage("msg_nothing_changed"));
		} else {
			$.ajax({
				type:"get",
				url: "/cgi-bin/admin/security.cgi",
				data: data,
				success: function(ret){
					var reg=/OK/g;
					if( reg.test(ret) ){
						settingSuccess(menu, getLanguage("msg_success"));
						refreshMenuContent();
					} else {
						settingFail(menu, getLanguage("msg_fail"));
					}
				},
				error: function(ret){
					settingSuccess(menu, getLanguage("msg_fail_retry"));
				}
			});
		}
	});
}

function onLoadPage(){
	initUI();
	initValue();
	initEvent();
}

$(document).ready(function(){
	onLoadPage();
});
