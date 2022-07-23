//var useddns=0;
//var address=2;
//var uname="cprotest.no-ip.org";
//var uid="khan118@naver.com";
//var pw="asd789";
var menu = "DDNS" + " " + getLanguage("settings");
var settingList = ["ddns_enable", "ddns_type", "ddns_hostname", "ddns_username" , "ddns_password"];

function onClickDdnsType()
{	
	if( $("[name=ddns_enable]:checked").val() == 0)     
    {
			$('#ddns_type').attr("disabled",true);
			$('#ddns_hostname').attr("disabled",true);
			$('#ddns_username').attr("disabled",true);
			$('#ddns_password').attr("disabled",true);
    }else {
			$('#ddns_type').attr("disabled",false);
			$('#ddns_hostname').attr("disabled",false);
			$('#ddns_username').attr("disabled",false);
			$('#ddns_password').attr("disabled",false);
	}
}

function CheckForm()
{
	return true;
}

function initUI()
{
	if( ddnsInfo['ddns_enable'] == '0')    $("[name=ddns_enable]:radio[value=0]").prop("checked",true)
	else   $("[name=ddns_enable]:radio[value=1]").prop("checked",true)

	onClickDdnsType();
}
function initvalue()
{
	for( var i = 0 ; i < settingList.length ; i++)	
	{	
		var obj = $("#" + settingList[i]);
		var tag = obj.prop("tagName");
		if( tag == "SELECT" || tag == "INPUT")
		{
			obj.val( ddnsInfo[settingList[i]]);
		}	
	}	
}
function checkblank(val){
	if($("#" + val).val() == ""){
		var orgval = ddnsInfo[val] ;
    	$("#"+val).val(orgval);         // restore
		settingFail(menu, getLanguage("msg_requried_field"));
		return false;
	}
	return true ;
}
function checkblank(val , msg){
	pop_msg = getLanguage(msg);
	if($("#" + val).val() == "" ){
//		var orgval = ddnsInfo[val] ;
//		$("#"+val).val(orgval);        // restore
		settingFail(menu, pop_msg);
		return false ; 
	}		
	return true;
}
function initEvent()
{

	$("[name=ddns_enable]").click(function ( obj ) {
		onClickDdnsType();		
	});
	
	$("#btOK").click(function(event) { 
		
		if($("[name=ddns_enable]:checked").val() == 1){
			if(!checkblank("ddns_hostname", "msg_ddns_check_hostname")) return;			
			if(!checkblank("ddns_username", "msg_ddns_check_username")) return;
			if(!checkblank("ddns_password", "msg_ddns_check_pass")) return;
//			if(!checkstring("ddns_hostname")) return;
//			if(!checkstring("ddns_username")) return;
//			if(!checkstring("ddns_password")) return;			
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
					orgValue = ddnsInfo[settingList[i]];
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
				data = "msubmenu=ddns&action=apply&"+ data;
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

/*	$("#ddns_hostname, #ddns_username, #ddns_password").blur(function(obj){		
			checkblank(obj.target.id);
			console.log(obj.target.id);
	});*/
}
function onLoadPage()
{
	initEvent();
    initUI();
	initvalue();
}

$(document).ready( function() {
	onLoadPage();
});
