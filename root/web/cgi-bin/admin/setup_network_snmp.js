//var onvif_discovery_mode=0;
//var onvif_auth_mode=2;

var menu = "SNMP" +" "+ getLanguage("settings");;
var settingList = ["Enabled_V1", "Enabled_V2", "RoComName", "RwComName", "Enabled_Trap", "TrapServer", "TrapComName", "RoEnabled_V3", "RoSecuLevel", "RoUserName", "RoAuthAlg", "RoAuthName", "RoPriAlg", "RoPriName", "RwEnabled_V3", "RwUserName",
                   "RwSecuLevel", "RwAuthAlg", "RwAuthName", "RwPriAlg", "RwPriName"];
var PAGE = 0 ;
function initUI()
{
	if( $("#Snmpv3mode").val() == 0 ){
		$("#ROSNMP3_CONTENTS").css("display", "none");
		$("#RWSNMP3_CONTENTS").css("display", "block");
	}else{ 
		$("#ROSNMP3_CONTENTS").css("display", "block");
		$("#RWSNMP3_CONTENTS").css("display", "none");		
	}		

	if($("[name=RoEnabled_V3]:checked").val() == 1 || $("[name=RwEnabled_V3]:checked").val() == 1 ){
		$("[name=Enabled_V1][value=1],[name=Enabled_V2][value=1]").prop("disabled", true);
	}else{
		$("[name=Enabled_V1][value=1],[name=Enabled_V2][value=1]").prop("disabled", false);
	}
	if(capInfo["oem"] == "JCI")
	{
		$("#RoSecuLevel option[value='0']").remove();
	}
}
function initvalue()
{
	var value = new Value() ; 
	value.setValue(settingList, SnmpInfo);
}
function checkDependencyUI(option, val){			
	if( $("[name=Enabled_V1]:checked").val() == 0 && $("[name=Enabled_V2]:checked").val() == 0 ){
		$("#RoComName, #RwComName").prop("disabled", true);
	}else{				
		$("#RoComName, #RwComName").prop("disabled", false);
	}
	
	if( $("[name=Enabled_Trap]:checked").val() == 0 && $("[name=Enabled_Trap]:checked").val() == 0 ){
		$("#TrapServer, #TrapComName").prop("disabled", true);
	}else{				
		$("#TrapServer, #TrapComName").prop("disabled", false);
	}

	if( $("#Snmpv3mode").val() == 0 ){                    // Read
		$("#ROSNMP3_CONTENTS").css("display", "block");
		$("#RWSNMP3_CONTENTS").css("display", "none");							
		
		if($("[name=RoEnabled_V3]:checked").val() == 0 ){        // RoEnabled_V3_disabled
			$("#RoUserName, #RoSecuLevel ,#RoAuthAlg, #RoAuthName, #RoPriAlg, #RoPriName ").prop("disabled", true);
		}else {													 // RoEnabled_V3_enabled
			$("#RoUserName, #RoSecuLevel ,#RoAuthAlg, #RoAuthName, #RoPriAlg, #RoPriName ").prop("disabled", false);					
			
			if( $( "#RoSecuLevel").val() == 0 ){
				$( "#RoAuthAlg, #RoAuthName, #RoPriAlg, #RoPriName").prop("disabled", true);
			}
			else if( $("#RoSecuLevel").val() == 1 ){
				$("#RoAuthAlg, #RoAuthName ").prop("disabled", false);
				$("#RoPriAlg, #RoPriName ").prop("disabled", true);
			}
			else if( $("#RoSecuLevel").val() == 2 ){			
				$("#RoAuthAlg, #RoAuthName, #RoPriAlg, #RoPriName").prop("disabled", false);
			}
		}	
	}else{ 											    // Write
		$("#ROSNMP3_CONTENTS").css("display", "none");
		$("#RWSNMP3_CONTENTS").css("display", "block");							
		
		if($("[name=RwEnabled_V3]:checked").val() == 0 ){       // RwEnabled_V3_disabled
			$("#RwUserName, #RwSecuLevel ,#RwAuthAlg, #RwAuthName, #RwPriAlg, #RwPriName ").prop("disabled", true);
		}else {                                                 // RwEnabled_V3_enabled
			$("#RwUserName, #RwSecuLevel ,#RwAuthAlg, #RwAuthName, #RwPriAlg, #RwPriName ").prop("disabled", false);
			
			if( $("#RwSecuLevel").val() == 0 ){
				$("#RwAuthAlg, #RwAuthName, #RwPriAlg, #RwPriName").prop("disabled", true);			
			}
			else if( $("#RwSecuLevel").val() == 1 ){
				$("#RwAuthAlg, #RwAuthName ").prop("disabled", false);
				$("#RwPriAlg, #RwPriName ").prop("disabled", true);
			}
			else if( $("#RwSecuLevel").val() == 2 ){
				$("#RwAuthAlg, #RwAuthName, #RwPriAlg, #RwPriName").prop("disabled", false);
			}						
		}
	}		
}
function isvalid(val){
	var Valid = new Validation();	
	if( val == "RoAuthName" || val == "RoPriName" || val == "RwAuthName" || val == "RwPriName" )	{
		if(!(Valid.blank( val ))){
			return false;
		}
		if(!(Valid.textlength( val, 8, 32 ))){
			return false;	
		}
		if(!(Valid.isValidText( val ))){
			return false;
		}
	}
	if( val == "RoComName" || val == "RwComName" || val == "TrapComName" ){
		if(!(Valid.blank( val ))){
			return false;
		}	
	}
	return true;	
}
function valid_pass(){
	var result_valid ;
	if( $("#RoSecuLevel").val() == 1 ){
		if( !isvalid("RoAuthName")) return false;
		
	}
	else if( $("#RoSecuLevel").val() == 2 ){
		if( !isvalid("RoAuthName")) return false;
		if( !isvalid("RoPriName")) return false;
	}
	
	if( $("#RwSecuLevel").val() == 1 ){
		if( !isvalid("RwAuthName")) return false;
		
	}
	else if( $("#RwSecuLevel").val() == 2 ){
		if( !isvalid("RwAuthName")) return false;
		if( !isvalid("RwPriName")) return false;
	}

	return true ;
}
function initEvent()
{
	$("[name=RoEnabled_V3],[name=RwEnabled_V3]").click(function(e) { 
		if($("[name=RoEnabled_V3]:checked").val() == 1 || $("[name=RwEnabled_V3]:checked").val() == 1 ){
			$("[name=Enabled_V1][value=0],[name=Enabled_V2][value=0]").prop("checked", true);
			$("[name=Enabled_V1][value=1],[name=Enabled_V2][value=1]").prop("disabled", true);
		}else{
			$("[name=Enabled_V1][value="+SnmpInfo['Enabled_V1']+"],[name=Enabled_V2][value="+SnmpInfo['Enabled_V2']+"]").prop("checked", true);
			$("[name=Enabled_V1][value=1],[name=Enabled_V2][value=1]").prop("disabled", false);
		}

		if( $("[name=Enabled_V1]:checked").val() == 0 && $("[name=Enabled_V2]:checked").val() == 0 ){
			$("#RoComName, #RwComName").prop("disabled", true);
		}else{				
			$("#RoComName, #RwComName").prop("disabled", false);
		}
	});
	$("#RoSecuLevel, #RwSecuLevel, [name=Enabled_V1], [name=Enabled_V2], [name=Enabled_Trap], [name=RoEnabled_V3],[name=RwEnabled_V3],#Snmpv3mode").change(function(e) { 
		checkDependencyUI( );		
	});
	$("#Snmpv3mode").change(function(e) { 
		channel =  $("#Snmpv3mode").val(); 	
		initvalue();
		checkDependencyUI( );		
	});
	
	$("#btOK").click(function(e) { 
		
		function onSuccessApply(msg)
		{
			var tmp= msg.trim().split('\n');
			var response = tmp[0].slice(0, -1);
			console.log(response);
			var error_code = tmp[1];
			var error_result = parserErroncode(error_code);
			var pattern = /OK/;
			if(pattern.test(msg) )
			{		
				settingSuccess(menu, null);
			}
			else 
			{
				settingFail(menu, error_result);
			}
			refreshMenuContent();
		}
		function onFailApply()
		{
			settingFail(menu, "apply fail. retry again.");
			refreshMenuContent();
		}	
		
		var Valid = new Validation();	
		var valid_flag = 0 ;
		var data = null;
		{
			var newValue;
			var orgValue;

			if(!valid_pass()) return 0;   // validation
			
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
					orgValue = SnmpInfo[settingList[i]];

					if( orgValue != newValue )
					{
						if(!isvalid(settingList[i])) return 0 ;   // validation
							
						if( data == null)
							data = settingList[i] + "=" + newValue;
						else
							data += "&" + settingList[i] + "=" + newValue;
					}
				}
			}
//			if( valid_flag == -1 )	return 0 ;
			if(data != null)
			{
				data = "msubmenu=snmp&action=apply&"+ data;
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
	initUI();
	checkDependencyUI();
}

$(document).ready( function() {
	onLoadPage();
	$("#Snmpv3mode").val(channel).change();	
});
