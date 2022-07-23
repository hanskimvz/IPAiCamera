var SettingList=["cert_id","admin_policy","operator_policy","viewer_policy","onvif_policy","rtsp_policy"];
var menu = getLanguage("https_configuration");
function initUI(){
	var content= '';
	content += "<option value=0>HTTP</option>";
	content += "<option value=1>HTTPS</option>";
	$("select[name=protocol_policy]").append(content);
	content += "<option value=2>HTTP and HTTPS</option>";
	$("select[name=connect_policy]").append(content);
}
function initValue() {
	//update certificates list
	var content = '';
	for(var i=0; i<certInfo.length; ++i) {
		content += "<option value='" + certInfo[i].id + "'>"
		content += certInfo[i].name +  "</option>";
	}
	if( content.length > 0 )
		$("#certList").append(content).val(httpsInfo['cert_id']);
	SettingList.forEach(function(t){
		$("#" + t).val(httpsInfo[t]);
	});
}
function initEvent() {
	$("button#btnApply").click(function(){
		var data = new Object();
		data["msubmenu"]="https";
		data["action"]="apply";
		SettingList.forEach(function(e){
			if( httpsInfo[e] != $("#" + e ).val() ) {
				if( e == "cert_id" ){
					var cert_id = $("#certList").val();
					if( cert_id != 0 ) {
						certInfo.forEach(function(c){
							if( c.id == $("#certList").val() ) {
								data['cert_id'] = c.id;
								data['cert_name'] = c.name;
							}
						});
					} else {
						data['cert_id'] = 0;
						data['cert_name'] = '';
					}
				} else {
					data[e]= $("#" + e ).val();
				}
			}
		});
		$.ajax({
			type: 'GET',
			url : "/cgi-bin/admin/security.cgi",
			data: data,
			success:function(req){
				var OK = /OK/g;
				if( OK.test(req) ) {
					settingSuccess();
					refreshMenuContent();
				} else {
					var err_code = getErrorCode(req);
					var msg_type = "msg_fail";
					if( err_code == APP_ERR_USED_CERTIFICATE ) {
						msg_type = "msg_fail_used_certificate";
					}
					else if( err_code == APP_ERR_INCOMPLETE_CONFIGURATION ) {
						msg_type = "msg_failed_not_satisfied_requirement";
					} 
					settingFail(menu, getLanguage(msg_type));
				}
			}
		});
	});
}
function onLoadPage() {
	initUI();
	initValue();
	initEvent();
}
$(document).ready(function(){
	onLoadPage();
});
