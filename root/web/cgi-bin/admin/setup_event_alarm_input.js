var menu = "alarmin Setting";
//var settingList = ["sun", "mon" , "tue", "wed", "thu", "fri", "sat", "shour", "smin", "ehour", "emin", "output", "duration", "transfer" ];   // 
var settingList = [ "device"];   // 

function initUI()
{
	if( alramInfo['device'] == '0')    $("[name=device][value=0]").trigger("click");
	else if(alramInfo['device'] == '1')    $("[name=device][value=1]").trigger("click");
	else if( alramInfo['device'] == '2')    $("[name=device][value=2]").trigger("click");

}

function checkDependency(index)
{
   
}
function initEvent()
{
	menu = getLanguage("setup_alarm_config");
	$("#btOK").click(function(event) {
		function onSuccessApply(msg) {
			var tmp= msg.trim().split('\n');
			console.log(tmp);
			var response = tmp[0];
			if(response == "OK") {		
				settingSuccess(menu, null);
			} else {
				settingFail(menu, tmp[1]);
			}
			refreshMenuContent();
		}
		function onFailApply() {
			settingFail(menu, getLanguage("msg_fail_retry"));
			refreshMenuContent();
		}	

		var data = null;
		var newValue;
		var orgValue;

		for( var i = 0 ; i < settingList.length ; i++)	{	
			var obj = $("#" + settingList[i]);

			if(($("[name = "+settingList[i]+"]").prop("type")) == "radio") {
				newValue = $("[name="+settingList[i]+"]:checked").val();
			}

			orgValue = alramInfo[settingList[i]];
			if( orgValue != newValue ) {
				if( data == null)
					data = settingList[i] + "=" + newValue;
				else
					data += "&" + settingList[i] + "=" + newValue;
			}
		}
				 
		if(data != null) {
			data = "msubmenu=alarmin1&action=apply&"+ data;
		} else {
			settingFail(menu, getLanguage("msg_nothing_changed"));
			return ;
		}
		$.ajax({
			type:"get",
			url: "/cgi-bin/admin/event.cgi",
			cache   : false,
			data: data,
			success: onSuccessApply, 
			error: onFailApply
		});
	});
}
/*
function SetTextBoxEnabled(optMode)
{
	if( $("[name=alarmactivation]:checked").val() == "0" )
	{
		$("#alarmin_setting").find("*").prop("disabled", false);
	} 
	else 
	{
		$("#alarmin_setting").find("*").prop("disabled", true);
	}
}*/

function onLoadPage()
{
	initEvent();
	initUI();
}

$(document).ready( function() {

	onLoadPage();

});
