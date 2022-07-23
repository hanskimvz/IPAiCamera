var menu = "Corridor Setting";
var settingList = ["enabled"];
var src = 0;
Val = new Value();

function initUI() {
}
function initValue()
{
    Val.setValue(settingList, corridor_info);
}

function initEvent()
{
	$("#btOK").click(function(event) {
		var data="msubmenu=Corridor&action=apply";
		var changed = 0;
		settingList.forEach(function(target){
			var obj = $("#" + target);
			if( obj.length == 0 ) obj = $("[name=" + target + "]:checked");
			var newVal=obj.val();
			data += "&" + target + "=" + newVal;
			changed++;
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
						alert(getLanguage("msg_reboot_45sec_message"));
						window.close();
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

