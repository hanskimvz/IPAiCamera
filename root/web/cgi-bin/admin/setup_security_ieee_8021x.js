var menu = getLanguage("ieee_8021x_configuration");
var settingList = ["cert_id", "ca_id", "enabled", "protocol", "eapol_version", "id", "password"];
function initUI() {
	if(capInfo["oem"] == 12)
	{
		$("#protocol option[value='2']").remove();
	}
}
function chkForm()
{
	console.log("chkForm");
	if( $("#password").val() !== $("#password_confirm").val())
	{   
		pop_msg = getLanguage("msg_passwd_mismatch_wrong");
		settingFail(menu, pop_msg);
		return false;
	}
	if( $("#password").val().length < 8 || $("#password").val().length >30)
	{
		pop_msg = getLanguage("msg_passwd_wrong");
		settingFail(menu, pop_msg);
		return false;
	}
	return true;
}
function updateList(id, data)
{
	var content = '';
	for(var i=0; i<data.length; ++i) {
		content += "<option value='" + data[i].id + "'>"
		content += data[i].name +  "</option>";
	}
	if( content.length > 0 )
		$("#" + id).append(content);
}
function initValue(){
	updateList("cert_id", certInfo);
	updateList("ca_id", caInfo);

	var value = new Value() ; 
	value.setValue(settingList, ieee8021xInfo);

	$("#password_confirm").val(""); 
}

function initEvent() {
	$("#btOK").click(function () {
		var items = ieee8021xInfo;
		var cgiData= new Object();
		var newVal;
		var oldVal;
		var value = new Value(); 
		console.log(value);
		if(chkForm()){
			var fail = settingList.some(function(e){
				newVal = value.getValue(e);
				oldVal = items[e];

				if( e == "password"){
					var confirm = value.getValue("password_confirm");
					/*
					if( (confirm != "")&& (newVal != confirm )){
						settingFail(menu, getLanguage("msg_confirmpasswd_wrong"));
						return true;
					}
					*/
					if( newVal != oldVal ) {
						cgiData[e] = newVal;
					}
				} else {
					if( newVal != oldVal ) {
						cgiData[e] = newVal;
					}
				}
			});
			if( !fail ){
				_ajax(cgiData);
			}
		}
	});
	$("#protocol").change(function(e){
		var value = e.currentTarget.value;
		if( value == 0 ){
			$("#id,#password,#password_confirm").attr("disabled", false);
			$("#cert_id,#ca_id").attr("disabled", true);
		} else if( value == 1 || value == 2 ) {
			$("#id,#password,#password_confirm,#ca_id").attr("disabled", false);
			$("#cert_id").attr("disabled", true);
		} else if( value == 3 ) {
			$("#password,#password_confirm").attr("disabled", true);
			$("#id,#cert_id,#ca_id").attr("disabled", false);
		}
	});
	$("#id").change(function(e){
		if(e.currentTarget.value.length < 4 ){
			settingFail(menu, getLanguage("msg_id_wrong"));
		}
	});
	/*
	$("#password").change(function(e){
		if( e.currentTarget.value.length < 4 ){
			settingFail(menu, getLanguage("msg_passwd_wrong"));
		}
	});
	$("#password_confirm").change(function(e){
		if( e.currentTarget.value.length < 4 ){
			settingFail(menu, getLanguage("msg_confirmpasswd_wrong"));
		}
	});
	*/
}
function _ajax(data) {
	$.ajax({
		type:"get",
		url: "/cgi-bin/admin/security.cgi?msubmenu=ieee8021x&action=apply",
		data: data,
		success: function(ret){
			var reg=/OK/g;
			if( reg.test(ret) ){
				settingSuccess(menu, getLanguage("msg_success"));
				refreshMenuContent();
			} else {
				var err_code = getErrorCode(ret);
				var msg_type = "msg_fail";
				if( err_code == 9){
					msg_type = "msg_ip_filter_conflict";
				}
				settingFail(menu, getLanguage(msg_type));
			}
		}, error: function(ret){
			settingSuccess(menu, getLanguage("msg_fail_retry"));
		}
	});
}

function onLoadPage() {
	initUI();
	initValue();
	initEvent();
	$("#protocol").trigger("change");
}

$(document).ready(function(){
	onLoadPage();
});
