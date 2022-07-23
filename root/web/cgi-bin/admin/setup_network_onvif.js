//var onvif_discovery_mode=0;
//var onvif_auth_mode=2;

var menu = "ONVIF" + " " + getLanguage("settings");
var settingList = ["onvif_discovery", "onvif_auth"];

function initUI()
{
	
}
function initvalue()
{
	for( var i = 0 ; i < settingList.length ; i++)	
	{	
		var obj = $("#" + settingList[i]);
		var tag = obj.prop("tagName");
		if( tag == "SELECT" || tag == "INPUT")
		{
			obj.val( onvifInfo[settingList[i]]);
		}	
	}	
	if( onvifInfo['onvif_auth'] == '0')    $("[name=onvif_auth]:radio[value=0]").prop("checked",true)
	else if( onvifInfo['onvif_auth'] == '1')    $("[name=onvif_auth]:radio[value=1]").prop("checked",true)
	else   $("[name=onvif_auth]:radio[value=2]").prop("checked",true)

	if( onvifInfo['onvif_discovery'] == '0')    $("[name=onvif_discovery]:radio[value=0]").prop("checked",true)
	else   $("[name=onvif_discovery]:radio[value=1]").prop("checked",true)
}


function initEvent()
{
	$("#btOK").click(function(event) { 
		
		function onSuccessApply(msg)
		{
			var tmp= msg.trim().split('\n');
			if(tmp == "OK")
			{		
				settingSuccess(menu, null);
			}
			else 
			{
				settingFail(menu, tmp[0]);
			}
			refreshMenuContent();
		}
		function onFailApply()
		{
			settingFail(menu, "apply fail. retry again.");
			refreshMenuContent();
		}	

		var data = null;
		{
			var newValue;
			var orgValue;

			for( var i = 0 ; i < settingList.length ; i++)	
			{	
				var obj = $("#" + settingList[i]);

					if(($("[name = "+settingList[i]+"]").prop("type")) == "radio")  // radio 
					{
						newValue = $("[name="+settingList[i]+"]:checked").val();
					}
					else if(($("#" + settingList[i]).prop("type")) == "checkbox")  // checkbox
					{
						if(($("#" + settingList[i]).prop("checked")) == true)
							newValue = 1;
						else				
							newValue = 0;					
					}
					else // select , input 
					{
						newValue = obj.val();				
					}
					orgValue = onvifInfo[settingList[i]];
					if( orgValue != newValue )
					{
						if( data == null)
							data = settingList[i] + "=" + newValue;
						else
							data += "&" + settingList[i] + "=" + newValue;
					}
				}
			}
			if(data != null)
			{
				data = "msubmenu=onvif&action=apply&"+ data;
			} else {
				settingFail(menu, getLanguage("msg_nothing_changed"));
				return ;
			}
			$.ajax({
				type:"get",
				url: "/cgi-bin/admin/system.cgi",
				data: data,
				success: onSuccessApply, 
				error: onFailApply
			});
		});
}
function onLoadPage()
{   
	initEvent();
	initvalue();
}

$(document).ready( function() {
	onLoadPage();
});
