var namePattern = /\D+/g,
	maxExpires = new Date("2038/01/18 23:59:59");
document.menu = getLanguage("cert_configuration");
if(capInfo["oem"] == 12){
	var works= [
		{"id":"View",          "ui":"uiView_IV",     "func":null},
		{"id":"Install",       "ui":"uiInstall",     "func":InstallCert},
		{"id":"CreateSSC",     "ui":"uiCreateSSC_IV",   "func":CreateSSC},
		{"id":"CreateCSR",     "ui":"uiCreateCSR_IV",   "func":CreateCSR},
		{"id":"Properties",    "ui":"uiProperties",  "func":function(){return getProperties("certificate");}},
		{"id":"Delete",        "ui":null,            "func":function(){return deleteCertificate("certificate");}},
		{"id":"Cancel",        "ui":"uiView_IV",     "func":null},
		{"id":"CAInstall",     "ui":"uiCAInstall",   "func":null},
		{"id":"CAProperties",  "ui":"uiProperties",  "func":function(){return getProperties("ca");}},
		{"id":"CADelete",      "ui":null,            "func":function(){return deleteCertificate("ca");}}
	];
}else{
	var works= [
		{"id":"View",          "ui":"uiView",        "func":null},
		{"id":"Install",       "ui":"uiInstall",     "func":InstallCert},
		{"id":"CreateSSC",     "ui":"uiCreateSSC",   "func":CreateSSC},
		{"id":"CreateCSR",     "ui":"uiCreateCSR",   "func":CreateCSR},
		{"id":"Properties",    "ui":"uiProperties",  "func":function(){return getProperties("certificate");}},
		{"id":"Delete",        "ui":null,            "func":function(){return deleteCertificate("certificate");}},
		{"id":"Cancel",        "ui":"uiView",        "func":null},
		{"id":"CAInstall",     "ui":"uiCAInstall",   "func":null},
		{"id":"CAProperties",  "ui":"uiProperties",  "func":function(){return getProperties("ca");}},
		{"id":"CADelete",      "ui":null,            "func":function(){return deleteCertificate("ca");}}
	];
}
function oem_dependency(){
	if(capInfo["oem"] == 2){
		$("#frmCreateSelfSignedCert").find("#rsa_mode").attr("disabled", true);
		$("#frmCreateSelfSignedCert").find("#sha_mode").attr("disabled", true);
		$("input#country").val("US");
		$("#frmCreateCertSigningRequest").find("#sha_mode").attr("disabled", true);
	}
}
function InstallCert() {
	$("#uiInstall").find("input").each(function(){
		var obj = $("#"+this.id);
		var type = obj.attr("type");
		if( type == "file" ){
			obj.val("").trigger("change");
			obj.replaceWith( obj.clone(true)).trigger("change");
		} else if( type == "password" || type == "text" ) {
			this.value = '';
		}
	});
	$("#cert_csr").trigger("click");
	return true;
}
function CreateSSC(){
    var cam_ipaddr = window.location.host.split(':');
	if(capInfo["oem"] == 12){
		$("#uiCreateSSC_IV").find("#common_name").val(cam_ipaddr[0]);
		$("#uiCreateSSC_IV").find("#rsa_mode").val(1);
		$("#uiCreateSSC_IV").find("#sha_mode").val(1);
	}else{
		$("#uiCreateSSC").find("#common_name").val(cam_ipaddr[0]);
		$("#uiCreateSSC").find("#rsa_mode").val(1);
		$("#uiCreateSSC").find("#sha_mode").val(1);
	}
	$("#max_expires").html( "~" + getTimeStamp(maxExpires).split(' ')[0]);
	oem_dependency();
	return true;
}
function CreateCSR() {
	initUI();
	var result = false;
	if(capInfo["oem"] != 12){
		var id = $("#certificate").find(".sel_record_item").attr("id");
		if( typeof(id) == "undefined" ) {
			if(capInfo["oem"] == 12)
				settingFail(document.menu, getLanguage("msg_choose_one_certificate_server_client"));
			else
				settingFail(document.menu, getLanguage("msg_choose_one_certificate"));
		} else {
			$("#cert_req_create").html("").parent().css("display", "none");
			certInfo.some(function(e){
				if( e.id == id ) {
					$("#frmCreateCertSigningRequest").find("input#name").val(e.name);
					result = true;
				}
			});
		}
	}else{
		result = true;
		$("#frmCreateCertSigningRequest").find("#rsa_mode").val(1);
	}
	$("#frmCreateCertSigningRequest").find("#sha_mode").val(1);
	oem_dependency();
	return result;
}

function initUI() {
	if(capInfo["oem"] != 12){
		$("#country").prop('placeholder','US');
		$("#uiView").css('display','block');
		$("#uiView_IV, #uiCreateSSC_IV, #uiCreateCSR_IV").remove();
	}else{
		$("#uiView_IV").css('display','block');
		 $("#uiView, #uiCreateSSC, #uiCreateCSR").remove();
	}

	$("#frmCreateSelfSignedCert").find("input").val("");
	var placeholder =  "yyyy-mm-dd";
	if(timeFormat == 1 ) {
		placeholder = "mm/dd/yyyy";
	}
	else if(timeFormat == 2 ) {
		placeholder = "dd/mm/yyyy";
	}
	$("input#expires").prop("placeholder", placeholder);
	//$obj = $("#frmCreateSelfSignedCert");
	//$obj.find("input#name").val("TEST_CERTIFICATE");
	//$obj.find("input#expires").val("2017-09-09");
	//$obj.find("input#country").val("KR");
	//$obj.find("input#state").val("KYEUNG-KI");
	//$obj.find("input#locality").val("BUN-DANG");
	//$obj.find("input#organization").val("CPRO");
	//$obj.find("input#organization_unit").val("SW");
	//$obj.find("input#common_name").val("192.168.1.116");

	$("#frmCreateCertSigningRequest").find("input").val("");
	//$("#frmInstall").find("input").val("");
	if(gLanguage == 4)
	{
		$("#CreateCSR").addClass("extra_longer");
		$("#Install").addClass("width_180");
	}
}

function initEvent() {
	function changeUI(id) {
		works.forEach(function(e){
			if( e.id == id ){
				var result = true;
				if( e.func != null ){
					result = e.func();
				}
				if( result &&e.ui != null ){
					$("[id^=ui]").css("display", "none");
					$obj = $("div#" + e.ui);
				} else {
					$obj = $("div#" + works[0].ui);
				}
				$obj.css("display", "block");
			}
		});
	}
	$("button[name=works]").click(function(e){
		changeUI(e.target.id);
	});
	$("form").submit(function(f){
		f.preventDefault();
		if(capInfo["oem"] == 12)
		{
			var forms = [ {
					"id"     : "frmCreateSelfSignedCert",
					"type"   : "GET",
					"action" : "create_self_signed_cert",
					"items"  : [ "name", "expires", "country", "state", "locality", "organization", "organization_unit", "common_name","rsa_mode", "sha_mode","dns1","dns2","ip" ],
					"menu"   : "certificate",
					"after"  : null
				}, {
					"id"     : "frmCreateCertSigningRequest",
					"type"   : "GET",
					"action" : "create_cert_sign_req",
					"items"  : [ "name", "country", "state", "locality", "organization", "organization_unit", "common_name","rsa_mode","sha_mode","dns1","dns2","ip" ],
					"menu"   : "certificate",
					"after"  : function(e){ 
						$("#cert_req_create").html(e).parent().css("display", "block"); 
					}
				}, {
					"id"     : "frmInstall",
					"type"   : "POST",
					"action" : "install",
					"items"  : [],
					"menu"   : "certificate",
					"after"  : null
				}, {
					"id"     : "frmCAInstall",
					"type"   : "POST",
					"action" : "install",
					"items"  : [],
					"menu"   : "ca",
					"after"  : null
				}
			];
		}
		else
		{
			var forms = [ {
					"id"     : "frmCreateSelfSignedCert",
					"type"   : "GET",
					"action" : "create_self_signed_cert",
					"items"  : [ "name", "expires", "country", "state", "locality", "organization", "organization_unit", "common_name","rsa_mode", "sha_mode","dns1","dns2","ip" ],
					"menu"   : "certificate",
					"after"  : null
				}, {
					"id"     : "frmCreateCertSigningRequest",
					"type"   : "GET",
					"action" : "create_cert_sign_req",
					"items"  : [ "name", "country", "state", "locality", "organization", "organization_unit", "common_name", "sha_mode","dns1","dns2","ip" ],
					"menu"   : "certificate",
					"after"  : function(e){ 
						$("#cert_req_create").html(e).parent().css("display", "block"); 
					}
				}, {
					"id"     : "frmInstall",
					"type"   : "POST",
					"action" : "install",
					"items"  : [],
					"menu"   : "certificate",
					"after"  : null
				}, {
					"id"     : "frmCAInstall",
					"type"   : "POST",
					"action" : "install",
					"items"  : [],
					"menu"   : "ca",
					"after"  : null
				}
			];
		}
		var target = null;
		for(var i=0; i<forms.length ; ++i) {
			if( forms[i].id == this.id ){
				target = forms[i];
				break;
			}
		}
		if( target == null ){
			console.log("can't find form information");
			return;
		}
		var type = target.type;
		var param;
		var submenu = getLanguage("setup_" + target.action);
		if( type == "GET" ) {
			param = "msubmenu=" + target.menu +"&action=" + target.action;
			var valid = true;
			target.items.some(function(e){
				valid = true;
				obj = $("#" + target.id).find("#" + e);
				var val = obj.val();
				if( val.length > 0 ) {
					if( e == "expires") {
						var datePattern = /^\d{4}-\d{1,2}-\d{1,2}/g;
						if( timeFormat == 1 || timeFormat == 2) {
							datePattern = /^\d{1,2}\/\d{1,2}\/\d{4}/g;
						}
						if( datePattern.test(val) == false ) {
							settingFail(submenu, getLanguage('msg_invalid_certificate_expries_on'));
							valid = false;
						}
						else {
							if (timeFormat == 2) { // dd/mm/yy 포맷 js Date 객체에 맞춰주기
								var ddmmyy = val.split("/");
								val = ddmmyy[1] + "-" + ddmmyy[0] + "-" + ddmmyy[2];
							}
							var setDate = new Date(val), nowDate = new Date();
							if( setDate.constructor == Date && nowDate.constructor == Date ) {
								setDate.setHours(nowDate.getUTCHours());
								setDate.setMinutes(nowDate.getUTCMinutes());
								setDate.setSeconds(nowDate.getUTCSeconds());
								setDate.setMilliseconds(nowDate.getUTCMilliseconds());
								var valid_date = Math.floor((setDate - nowDate) /86400000);
								if( valid_date <= 0  ) {
									settingFail(submenu, getLanguage("msg_invalid_expries_on"));
									valid = false;
								}
								console.log("setDate : " + setDate);
								console.log("maxExpires: " + maxExpires);
								if( setDate > maxExpires) {
									settingFail(submenu, getLanguage("msg_invalid_expries_overflow"));
									valid = false;
								}
							}
						}
					}else if(e == "ip"){
						if(!ipv4_validation(val)){
							settingFail(submenu, getLanguage("msg_certificate_alter_ip_wrong"));
							valid = false;
						}
					}else {
						valid = isValidText(val);
						if( valid == false ) {
							settingFail(submenu, getLanguage("msg_invalid_text"));
						}
					}

					if( valid ) {
						if( typeof(obj) != 'undegined' && obj.val() != "" ){
							param += "&" + e + "=" + obj.val();
						}
					}
					else {
						return true;
					}
				}
			});
			if( valid == false )
				return false;

			var result = true;
			var verify = [ /country=/g, /name=/g];
			if( target.action == 'create_self_signed_cert' ){
				$.merge(verify, [ /expires=/g ]);
			}
			verify.some( function(e){
				if( e.test(param) == false ){
					result = false;
					return true;
				}
			});
			if( !result ) {
				settingFail(submenu, getLanguage("msg_must_fill_required_feild"));
				return false;
			}
		} else if( type == "POST") {
			param = new FormData($(this)[0]);
			param.append("password", $("#password").val());
			param.append("msubmenu",target.menu);
			param.append("action", target.action);
		} else {
			settingFail(submenu, getLanguage("setup_unkown_type"));
		}
		$.ajax({
			type: type,
			url : "/cgi-bin/admin/security.cgi",
			data : param,
			cache: false,
			contentType: false,
			processData: false,
			beforeSend: function(){ progressUI(true); },
			success:function(resp){
				var req = /NG/g;
				var NG = req.test(resp);
				var NG_position = resp.search(req);
				var err_code, msg_type;
				if( NG && (NG_position == 0)){
					try{
						err_code = getErrorCode(resp);
						msg_type = "msg_fail";
						if( err_code == APP_ERR_USED_CERTIFICATE ) {
							msg_type = "msg_fail_used_certificate";
						} else if( err_code == APP_ERR_INVALID_COUNTRY_CODE ){
							msg_type = "msg_fail_invalid_country_code";
						}
					}
					catch(e){
						msg_type = "msg_fail";
					}
					settingFail(submenu, getLanguage(msg_type));
				}
				else {
					settingSuccess(submenu);
				}
				progressUI(false);
				if( (NG == false || NG_position != 0) && target.after != null){
					target.after(resp);
				}
				else {
					refreshMenuContent();
				}
			},
			error : function(resp){
				settingFail(submenu, "msg_fail_retry");
				progressUI(false);
			}
		});
	});

	/* ==================== for INSTALL UI ==================== */
	$("input[type=radio][name=type]").change(function(e){
		var obj = $("ul#seperate_type");
		if( e.target.value == 0 ) {
			obj.css("display", "NONE");
			obj.find("input").attr("disabled", true);
		} else {
			obj.css("display", "BLOCK");
			obj.find("input").attr("disabled", false);
			$("#key_seperate_type").trigger("click");
		}
	});
	$("input[type=radio][name=key_type]").change(function(e){
		if( e.target.value  == 0) {
			$("#key_file").attr("disabled", false);
			$("div#key_seperate").css("display", "block");
			$("div#key_password").css("display", "none");
		} else {
			$("#key_file").attr("disabled", true);
			$("div#key_seperate").css("display", "none");
			$("div#key_password").css("display", "block");
		}
	});
	$("input[id$=_file]").change(function(e){
		var fullPath= e.target.value.split("\\");
		var fileName = fullPath[fullPath.length-1];
		$("#" + e.target.id + "_name").html(fileName);
	});
	/* ======================================================== */
}

function setEventForRecordItem(target){
	$("#" + target).find(".list_items").on("click", function(e) {
		$("#" + target).find("tr").removeClass("sel_record_item");
		$("#" + e.delegateTarget.id).addClass("sel_record_item");
	});
}

function getProperties(type) {
	var id = $("#" + type).find(".sel_record_item").attr("id");
	if( typeof(id) == "undefined" ) {
			settingFail(document.menu, getLanguage("msg_choose_one_certificate"));
		return false;
	} else {
		var param= new Object();
		param['msubmenu'] = type;
		param['action'] = "properties";
		param['id'] = id;
		param['data_type'] = "json";
		$.ajax({
			type: 'GET',
			url : "/cgi-bin/admin/security.cgi",
			data: param,
			async : false,
			dataType : "json",
			success:function(data){
				obj = eval(data);
				var pattern = /:/g;
				obj.Modulus = obj.Modulus.replace(pattern, ' ');
				obj.Signature= obj.Signature.replace(pattern, ' ');
				for(key in obj) {
					if( obj.hasOwnProperty(key) ){
						$("#" + key).html(obj[key]);
					}
				}
			}
		});
	}
	return true;
}
function deleteCertificate(type) {
	var id = $("#" + type).find(".sel_record_item").attr("id");
	if( typeof(id) == "undefined"){
		settingFail(document.menu, getLanguage("msg_choose_one_certificate"));
		return false;
	}
	var data = "msubmenu=" + type + "&action=delete&id="+id;
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
				settingFail(document.menu, getLanguage(msg_type));
			}
		}
	});
	return true;
}
function setList(inputObj, target) {
	ajaxQueue = [];
	function getIssuedAndExpires(id){
		var param= new Object();
		param['msubmenu'] = target;
		param['action'] = "properties";
		param['data_type'] = "json";
		param['id'] = id;
		var len = ajaxQueue.length;
		ajaxQueue[len] = $.ajax({
			type: "GET",
			url : "/cgi-bin/admin/security.cgi",
			data: param,
			async : true,
			dataType : "json",
			success:function(data){
				var obj = eval(data);
				var pattern = /:/g;
				inputObj.forEach(function(e){
					if( obj.Name == e.name ){
						var format = 'yyyy-mm-dd';
						if( timeFormat == 1 ){
							format = 'mm/dd/yyyy';
						}
						else if( timeFormat == 2 ){
							format = 'dd/mm/yyyy';
						}
						$("#" + e.id).find(".th_cert_issued").text(new Date(obj.NotBefore).format(format, false));
						$("#" + e.id).find(".th_cert_expire").text(new Date(obj.NotAfter).format(format, false));
					}
				});
			}
		});
	};
	var content="";
	$("#" + target).find(".list_items").remove();
	for(var idx=0 ; idx < inputObj.length ; ++idx) {
		if( inputObj[idx]['id'] == 0 ) continue;
		content += "<tr class='list_items' id='"+ inputObj[idx]['id'] +"'>";
		content += "<td class='th_cert_id'>" + inputObj[idx]['name'] + "</td>";
		content += "<td class='th_cert_issued'><div class='loading_img'></div></td>";
		content += "<td class='th_cert_expire'><div class='loading_img'></div></td></tr>";
	}
	$("#"+target).ready(function(){
		for(var idx=0 ; idx < inputObj.length ; ++idx) {
			getIssuedAndExpires(inputObj[idx].id);
		}
	});
	$("#" +target ).append(content);
	setEventForRecordItem(target);
}
function initValue() {
	setList(certInfo, "certificate");
	setList(CAInfo, "ca");
}

function onLoadPage() {
	initUI();
	initValue();
	initEvent();
	$("input[type=radio][name=type][value=0]").trigger("click");
}

$(document).ready(function(){
	onLoadPage();
});
