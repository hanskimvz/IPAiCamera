
var menu = getLanguage("AUTO_IP") +" "+ getLanguage("settings");
//var menu = getLanguage("ZEROCONFIG");
var settingList = ["zeroconfig_enable"];

function initUI()
{
	
}
function initvalue()
{
	for( var i = 0 ; i < settingList.length ; i++)	
	{	
		console.log(settingList[i]);
		var obj = $("#" + settingList[i]);		
		var tag = obj.prop("tagName");
		if( tag == "SELECT" || tag == "INPUT")
		{
			obj.val( targetinfo[settingList[i]]);		
		}	
	}	
	if( targetinfo[settingList[0]] == 0 )    $( "[name="+ settingList[0] + "]:radio[value=0]").prop("checked",true);
	else   $("[name="+ settingList[0] + "]:radio[value=1]").prop("checked",true);

	checkDependency();
}
function checkDependency()
{
	if($("[name="+ settingList[0] + "]:checked").val()==0){
		$("#"+ settingList[0] ).prop("disabled", true);
	}
	else{
		$("#"+ settingList[0] ).prop("disabled", false);
	}
}			

function initEvent()
{
	$("[name="+ settingList[0] +"]").click(function ( obj ) {
//		checkDependency();
	});
	$("#btOK").click(function(event) { 
		
		function onSuccessApply(msg)
		{
			var tmp= msg.trim().split('\n');
			console.log(tmp);
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
			settingFail(menu, getLanguage("msg_fail_retry"));
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
					orgValue = targetinfo[settingList[i]];
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
				data = "msubmenu=zeroconfig&action=apply&"+ data;
			} else {
				settingFail(menu, getLanguage("msg_nothing_changed"));
				console.log("asd");
				return ;
			}
			$.ajax({
				type:"get",
				url: "/cgi-bin/admin/network.cgi",
				data: data,
				success: onSuccessApply, 
				error: onFailApply
			});
		});
}
function onLoadPage()
{   
	$("#zeroconfig_id").html(zeroconfigInfo['zeroconfig_id']);
	$("#zeroconfig_addr").html(zeroconfigInfo['zeroconfig_addr']);
	initEvent();
	initvalue();
//	checkDependency();
}

$(document).ready( function() {
	onLoadPage();
});