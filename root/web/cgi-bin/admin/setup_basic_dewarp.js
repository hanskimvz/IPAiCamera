var menu = "Dewarp Setting";
var settingList = ["dewarp_enabled"];
var src = 0;
Val = new Value();

function initUI() {   
}
function initValue()
{
	Val.setValue(settingList, dewarp_info);
}
function initEvent()
{
	$("#btOK").click(function(event) {
		var data="msubmenu=dewarp&action=apply";
		var changed = 0;
		settingList.forEach(function(target){
			var obj = $("#" + target);
			if( obj.length == 0 ) obj = $("[name=" + target + "]:checked");
			var newVal=obj.val();
//			var oldVal=CRtspAuthinfo[target];

//			console.log(target + "(" + newVal + "/" + oldVal + ")");
//			if( newVal != oldVal ){
				data += "&" + target + "=" + newVal;
				changed++;
//			}
		});
		if( changed == 0 )
		{
			settingFail(menu, getLanguage("msg_nothing_changed"));
		}
		else
		{
			$.ajax({
			type:"get",
			url: "/cgi-bin/admin/basic.cgi",
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
function onLoadPage() 
{
	initUI();
	initEvent();
	initValue();
}
$(document).ready( function() {
    onLoadPage();
});
