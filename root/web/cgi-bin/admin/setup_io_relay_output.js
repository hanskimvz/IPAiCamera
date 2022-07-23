var menu = "relayout Setting";
var settingList = ["mode", "idlestate", "duration"];   // 
var index = 0 ;

function initValue(){
	var value = new Value() ; 
	value.setValue(settingList, relayInfo[relayout_index]);
    
    if(document.querySelector('input[name="mode"]:checked').value==1){
        $('#duration').prop("disabled", true);
    }
    else{
        $('#duration').prop("disabled", false);
    }

}

function checkDependency()
{
    if( $("[name=mode]:checked").val() == 1){
        $('#duration').prop("disabled", true);
    }
    else if( $("[name=mode]:checked").val() == 0){
        $('#duration').prop("disabled", false);
    }
}

function initEvent()
{
	menu = getLanguage("setup_relay_out_config");
	var  pop_msg ="";
	$("#RelayoutIndex").click(function(event) {
		relayout_index =  $("#RelayoutIndex").val(); 	
		initValue();
		
	});	
	$("[name=mode]").click(function(event) {
		 checkDependency();
		
	});
	$("#btOK").click(function(event) {

	function onSuccessApply(msg)
	{

		var tmp= msg.trim().split('\n');
		console.log(tmp);
		var response = tmp[0];
		if(response == "OK")
		{		
			settingSuccess(menu, null);
		}
		else 
		{
			settingFail(menu, tmp[1]);
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
				else // select , input 
				{
					newValue = obj.val();				
				}
				orgValue = relayInfo[relayout_index][settingList[i]];
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
			data = "msubmenu=relay&action=apply&id="+ relayout_index +"&"+ data;
		} else {
			settingFail(menu, getLanguage("msg_nothing_changed"));
			return ;
		}
		$.ajax({
			type:"get",
			url: "/cgi-bin/admin/io.cgi",
			cache   : false,
			data: data,
			success: onSuccessApply, 
			error: onFailApply
		});
		
	});
}
function initUI(){
	for( var i = 0 ; i < relayInfo.size ; i++ ){
		$("#RelayoutIndex").append("<option value=" + i + ">" +"0"+ Number(i+1) + "</option>" );
	} 	
}

function setActiveRect(index)
{

}

function onLoadPage()
{
	initUI();
	initValue();
	initEvent();
}

$(document).ready( function() {
	onLoadPage();
	$("#RelayoutIndex").val(relayout_index).change();	
	
});
