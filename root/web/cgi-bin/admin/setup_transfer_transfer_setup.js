var menu = "transfer setting";
var settingList = [ "image_num", "pre_duration", "post_duration", "max_img_cnt", "max_img_enable"]; // radio 버튼 제외

function getvalue(val)
{
	switch(val)
	{	
		case "settingList" :
			for( var i = 0 ; i < settingList.length ; i++)	
			{	
			var obj = $("#" + settingList[i]);
			var tag = obj.prop("tagName");
				if( tag == "SELECT" || tag == "INPUT")
				{
					obj.val(TransferInfo[settingList[i]]);
				}	
			}
		break ;
	}
}
function initUI()
{

}
function initvalue()
{	
	if(TransferInfo["mode"]== 2) 	$("[name=mode][value=2]").trigger("click");
	else if (TransferInfo["mode"]== 0)	$("[name=mode][value=0]").trigger("click");
	else if (TransferInfo["mode"]== 1)	$("[name=mode][value=1]").trigger("click");
	
	getvalue("settingList");
	
	var selindex = $("#image_num option").index($("#image_num option:selected"));

	checkDependency(selindex);	

}

function checkDependency(val)
{
	$("#pre_duration").val(TransferInfo["pre_duration"]);
	$("#post_duration").val(TransferInfo["post_duration"]);
	$("#max_img_cnt").val(TransferInfo["max_img_cnt"]);
	if(TransferInfo["max_img_enable"]== 1) 	$("[name=max_img_enable]").trigger("click");
	else $("#max_img_cnt").prop("disabled", true);

	$("#max_img_enable").click( function(e){
		$("#max_img_cnt").attr("disabled", !e.target.checked);
	});
}
function initEvent()
{
	menu = getLanguage("setup_transfer_config");
	var  pop_msg ="";
/*	$("#image_num").change(function ( obj ) {				

		var selindex = $("#image_num option").index($("#image_num option:selected"));

		checkDependency(selindex);	
	});
*/
	$("#btOK").click(function(event) {
			
		function onSuccessApply(msg)
		{
			var pattern=/OK/;
			if( pattern.test(msg) )
			{		
				settingSuccess(menu, getLanguage("msg_save_success"));
			}
			else 
			{
				settingFail(menu, getLanguage("msg_save_fail_retry"));
			}
			refreshMenuContent();
		}
		function onFailApply()
		{
			pop_msg = getLanguage("msg_fail_retry");
			settingFail(menu, pop_msg);
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
				else if(($("[name = "+settingList[i]+"]").prop("type")) == "checkbox")  // checkbox 
				{
					newValue = $("[name = "+settingList[i]+"]").is(":checked")?1:0;
				}
				else // select , input 
				{
					newValue = obj.val();				
				}
					orgValue = TransferInfo[settingList[i]];
					if( orgValue != newValue )
					{
						if( data == null)
							data = settingList[i] + "=" + newValue;
						else
							data += "&" + settingList[i] + "=" + newValue;
					}
			}
		}
		console.log(data);	 
		if(data != null)
		{
			data = "msubmenu=transfer&action=apply&"+ data;
		} else {
			pop_msg = getLanguage("msg_nothing_changed");
			settingFail(menu, pop_msg);
			return ;
		}
		$.ajax({
			type:"get",
			url: "/cgi-bin/admin/transfer.cgi",
			data: data,
			success: onSuccessApply, 
			error: onFailApply
		});
	});
}

function onLoadPage()
{
	initUI();
	initEvent();
	initvalue();
}

$(document).ready( function() {

	onLoadPage();

});
