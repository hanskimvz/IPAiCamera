var menu = "PTZ Advanced Setting";
var settingList = ["Wiper_action", "Invertmode"];
// var check_run = 0;
//	Val = new Value();


function initUI() {
}
function initValue()
{
	//wiper
	$("#wiper_speed").val(wiperInfo.Speed);
	$("#wiper_timeout").val(wiperInfo.Timeout);
	//invertmode
	$("[name=invert][value=" + invertInfo.Enable + "]").trigger('click');
}
function initEvent()
{
	//wiper
	$("#btOK").on("click" , function(){
		//nothing changed
		if( wiperInfo.Speed == $("#wiper_speed").val() && wiperInfo.Timeout == $("#wiper_timeout").val() )
		{
			settingFail(menu, getLanguage("msg_nothing_changed"));
			return ;
		}

		if( !($("#wiper_speed").val()).match(/^[0-9]+$/) || !($("#wiper_timeout").val()).match(/^[0-9]+$/))  {
			settingFail(menu, getLanguage("msg_onlynumber"));
			return ;
		}
		if( $("#wiper_speed").val() < 1 || $("#wiper_speed").val() > 30) {
			settingFail(menu, getLanguage("msg_check_wiperspeed"));
			return ;
		}
		if( $("#wiper_timeout").val() < 1 || $("#wiper_timeout").val() > 120) {
			settingFail(menu, getLanguage("msg_check_wipertimeout"));
			return ;
		}

		var data = "msubmenu=wiper&action=apply&enabled=0";
		data += "&speed="+$("#wiper_speed").val();
		data += "&timeout="+$("#wiper_timeout").val();
		console.log("data");
		console.log(data);
		$.ajax({
            type:"get",
            url: "/cgi-bin/ptz.cgi",
            data: data,
            success: function(){
				settingSuccess(menu, null);
				refreshMenuContent("wiper_set");
			},
            error: function(){
				pop_msg = getLanguage("msg_fail_retry");
				settingFail(menu, pop_msg);
				refreshMenuContent();
			}
        });
	});
	// Invert
	$("#btinvert").on("click" , function(){
		//nothing changed
		if( invertInfo.Enable == $("[name=invert]:checked").val()) {
			settingFail(menu, getLanguage("msg_nothing_changed"));
			return ;
		}

		var data = "msubmenu=invert&action=apply";
		data += "&enabled="+$("[name=invert]:checked").val();
		console.log(data);
		$.ajax({
            type:"get",
            url: "/cgi-bin/ptz.cgi",
            data: data,
            success: function(){
				settingSuccess(menu, null);
				refreshMenuContent();
			},
            error: function(){
				pop_msg = getLanguage("msg_fail_retry");
				settingFail(menu, pop_msg);
				refreshMenuContent();
			}
        });
	});
}

function onLoadPage() 
{
	initUI();
	initValue();
	initEvent();
}
$(document).ready( function() {
    onLoadPage();
});
