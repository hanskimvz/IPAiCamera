//var upnp_enable=0;
//var upnp_friendlyname="";

var menu = "UPNP" +" " + getLanguage("settings");
var settingList = ["upnp_enable", "upnp_friendlyname"];

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
			obj.val( upnpInfo[settingList[i]]);
		}	
	}	
	if( upnpInfo['upnp_enable'] == '0')    $("[name=upnp_enable]:radio[value=0]").prop("checked",true)
	else   $("[name=upnp_enable]:radio[value=1]").prop("checked",true)

	checkDependency();
}
function checkDependency()
{
	if($("[name=upnp_enable]:checked").val()==0){
		$("#upnp_friendlyname").prop("disabled", true);
	}
	else{
		$("#upnp_friendlyname").prop("disabled", false);
	}
}			
function checkblank(val , msg){
	pop_msg = getLanguage(msg);
	if($("#" + val).val() == "" ){
		settingFail(menu, pop_msg);
		initValue();
		return false ; 
	}		
	return true;
}
function check_string(val){	
	var x = $("#" + val).val() ;
	console.log( x.match(/^[A-Za-z0-9]+$/));			
}
function initEvent()
{
	$("[name=upnp_enable]").click(function ( obj ) {
		checkDependency();
	});
	$("#btOK").click(function(event) { 
		
		if($("[name=upnp_enable]:checked").val() == 1){
			if(!checkblank("upnp_friendlyname", "msg_upnp_check_blank")) return ;		
		}
		if( !check_valid_data($("#upnp_friendlyname").val()) ){
			settingFail(menu, getLanguage("msg_fail_retry"));
			refreshMenuContent();
			return ;
		}
		function onSuccessApply(msg)
		{
			var tmp= msg.trim().split('\n');
			if(tmp == "OK")
			{		
				settingSuccess(menu, null);
			}
			else 
			{
				settingFail(menu, getLanguage("msg_fail_retry"));
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
					orgValue = upnpInfo[settingList[i]];
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
				data = "msubmenu=upnp&action=apply&"+ data;
			} else {
				settingFail(menu, getLanguage("msg_nothing_changed"));
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
	initEvent();
	initvalue();
	checkDependency();
}

$(document).ready( function() {
	onLoadPage();
});
