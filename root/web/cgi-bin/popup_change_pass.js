var no=1;
var no_pw_hint=1;
var outFormat = [ { "msg":"setup_password_type", "color":"white",},
    { "msg":"setup_password_weak", "color":"red",},
    { "msg":"setup_password_good", "color":"#FF8000"},
    { "msg":"setup_password_strong", "color":"#00FF40"}];
//$.ajaxSetup({ cache: false });
var pw_ng = 0;
$(document).ready( function(){
		Util.setOEM("logo");
		getJson();
    	initLanguage();
    	init();
    	dependency_css();
	$("#m_pass").trigger("keyup");
}); 		
function logout()
{
	$.ajax({
            type: "GET",
            url: "/cgi-bin/video.cgi",
            async: false,
            username: "Unknown",
            password: "1",
            headers: { "WWW-Authorization": "Digest xxx" }
	})
	.done(function(){
	    // If we don't get an error, we actually got an error as we expect an 401!
	})
	.fail(function(){
	    // We expect to get an 401 Unauthorized error! In this case we are successfully 
            // logged out and we redirect the user.
	    opener.parent.location.replace("/cgi-bin/logout.cgi?value=firstpass");
	});
    return false;
}
function success(ret)
{
    var response = ret.trim();
	// console.log(response);
    if(response == "OK")
    {
        pop_msg = getLanguage("msg_save_success");
        settingSuccess(menu, pop_msg);
        logout();
        window.close();
//	    opener.parent.location.replace("/cgi-bin/logout.cgi");
        
    } 
    else 
    {
		pop_msg = getLanguage("msg_save_fail_special_key_retry")+"\n"+getLanguage("pass_msg_combination")+"\n"+getLanguage("pass_msg_symbol");
        settingFail(menu, pop_msg);
    }
}
$("#change_pass").on("click", function(){
	console.log("changePw");
		if( capInfo["oem"] == 2){
			if($("#m_pass").val() == $("#m_pass_hint").val()){
				settingFail(menu, "Password hint can not be same as password");
				return false;
			}
		}
        var v_id =0;
        if( chkForm() )
        {
            var arg = { action: "modify",
                index: 0,
                id: userInfo.id, 
                pass: $("#m_pass").val(),
				passhint:$("#m_pass_hint").val(),
                auth: 5
            };
			console.log(arg);
            $.ajax({
                type: 'get',
                url: '/cgi-bin/admin/system.cgi?msubmenu=users',
                data: arg,
                success: success,
                error: function(){
					pop_msg = getLanguage("msg_loading_fail");
                    settingFail(menu, pop_msg);
                }
            });
        }  


});  
$("#check_later").on("click", function(){
    window.close();
});
function init(){	
	if( capInfo["oem"] == 2){
		$("#pass_hint_div").css("display", "block");
		$("#msg_change_pass").css("display", "none");
		$("#msg_change_pass_dw").css("display", "block");
		$("#change_pass").append("<span >"+getLanguage("change_pass")+"</span>");
        $("#set_admin_password").css("display","none");
	}else{
		$("#pass_hint_div").css("display", "none");
		$("#msg_change_pass").css("display", "block");
		$("#msg_change_pass_dw").css("display", "none");
	    if( capInfo["oem"] == 12){
            $("#admin_password").css("display","none");
            $("#check_later").css("display","none");
		    $("#change_pass").append("<span >"+getLanguage("set_pass")+"</span>");
		    $("#msg_change_pass").append("<span >"+getLanguage("pass_msg_noti_iv")+"</span><br>");
        }
        else{
        	$("#set_admin_password").css("display","none");
		    $("#change_pass").append("<span >"+getLanguage("change_pass")+"</span>");
		    $("#msg_change_pass").append("<span >"+getLanguage("pass_msg_noti")+"</span><br>");
        }
	}
	if( capInfo["oem"] == 9){
		$("#passchcontent").removeClass("content");
		$("#passchcontent").addClass("rvi_content");
	}else if( capInfo["oem"] == 12){
		$("#passchcontent").removeClass("content");
		$("#passchcontent").addClass("IV_content");
	}

    $("#m_pass").bind("keyup", function () {
        if( capInfo["oem"] == 12){
            var strongRegex = /^(?=.{12,})(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])(?=.*[\W_]).*$/g;
            var goodRegex   = /^(?=.{8,})(((?=.*[A-Z])(?=.*[a-z]))|((?=.*[A-Z])(?=.*[0-9]))|((?=.*[a-z])(?=.*[0-9]))|((?=.*[A-Z])(?=.*[\W_]))|((?=.*[a-z])(?=.*[\W_]))|((?=.*[0-9])(?=.*[\W_]))).*$/g;
            var weakRegex = /^(?=.{7,})((?=.*[A-Z])|(?=.*[a-z])|(?=.*[\W_])|(?=.*[0-9])).*$/g;
        }
		else if( capInfo["oem"] == 2){
            var strongRegex = /^(?=.{12,})(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])(?=.*[\W_]).*$/g;
            var goodRegex = /^(?=.{8,})(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])(?=.*[\W_]).*$/g;
            var weakRegex = /^(?=.{7,})((?=.*[A-Z])|(?=.*[a-z])|(?=.*[\W_])|(?=.*[0-9])).*$/g;
        }
        else {
            var strongRegex = /^(?=.{12,})(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])(?=.*[\W_]).*$/g;
            var goodRegex = /^(?=.{8,})(((?=.*[A-Z])(?=.*[a-z])(?=.*[\W_]))|((?=.*[A-Z])(?=.*[0-9])(?=.*[\W_]))|((?=.*[a-z])(?=.*[0-9])(?=.*[\W_]))|((?=.*[A-Z])(?=.*[a-z])(?=.*[0-9]))).*$/g;
            var weakRegex   = /^(?=.{8,})(((?=.*[A-Z])(?=.*[a-z]))|((?=.*[A-Z])(?=.*[0-9]))|((?=.*[a-z])(?=.*[0-9]))|((?=.*[A-Z])(?=.*[\W_]))|((?=.*[a-z])(?=.*[\W_]))|((?=.*[0-9])(?=.*[\W_]))).*$/g;
        }
        var passwd=$("#m_pass").val();
		var id_dw ="admin";
        
        if(passwd.length == 0){
			no=0;	
		} else {
			if( strongRegex.test(passwd) ){
				no=3;
			} else if( goodRegex.test(passwd) ){
				no=2;
			} else 
				no=1;	
		}

		if (capInfo["oem"] == 2)
		{
			if (passwd.indexOf(id_dw) !== -1) 
			{
				no=1;
				pw_ng=1;
			}
		}

		$("#meter").css("backgroundColor", outFormat[no].color)
			.css('width',$("#meter_wrapper").width()/3*no+'px');
		$("#pass_type").text(getLanguage(outFormat[no].msg));

	});
	$("#m_pass_hint").keyup(function(event){
		var st = event.which;
		if(st == 9 || st == 13||st == 8) //9:tab 13:enter 8:back space
			no_pw_hint=1;
		else if(st >= 48 && st <= 57)
			no_pw_hint=1;
		else if(st >= 65 && st <= 90) 
			no_pw_hint=1;
		else if(st >= 97 && st <= 122)
			no_pw_hint=1;
		else
			no_pw_hint=0;
	});


}
function chkForm()
{
	if( capInfo["oem"] == 2){ 
		if($("#m_pass_hint").val().length > 60){
			pop_msg = "Password hints must be 60 characters or less.";
			settingFail(menu, pop_msg);
			return false;
		}
		if(no_pw_hint==0){
			pop_msg = "Password hints can only be set in English or Number.";
			settingFail(menu, pop_msg);
			return false;
		}
	}  

	if( capInfo["oem"] == 12){
        var passlen= 7;
    }else {
        var passlen= 8;
    }

    if( $("#m_pass").val().length < passlen || $("#m_pass").val().length > 30){
        pop_msg = getLanguage("msg_passwd_wrong");
        settingFail(menu, pop_msg);
		return false; 
	}
    if( $("#m_pass_confirm").val().length < passlen  || $("#m_pass_confirm").val().length > 30)
	{
		pop_msg = getLanguage("msg_confirmpasswd_wrong");
		settingFail(menu, pop_msg);          
		return false; 
	}
    if( $("#m_pass").val() !== $("#m_pass_confirm").val())
	{
		pop_msg = getLanguage("msg_passwd_mismatch_wrong");
		settingFail(menu, pop_msg); 
		return false;
	}
	function checkPassword() {
		var n;
		var i;
		var tmp; 
		var ob = $('#m_pass').val();
		var mask_letters = 0;
		var mask_numbers = 0;
		var mask_special_characters = 1;
		console.log("n");
		for (i=0; i<ob.length; i++)
		{
			n = ob.charCodeAt(i);
			console.log(n);
			// ~ : 126, ` : 96, 
			// ! : 33, @ : 64, $ : 36, ^ : 94, ( : 40, ) : 41, _ : 95, - : 45, | : 124
			// { : 123, } : 125, [ : 91, ] : 93, ; : 59, . : 46, ? : 63, / : 47
			
			if(n >= 97 && n <= 122) // a ~ z
				mask_letters = 4;
			else if(n >= 65 && n <= 90)  // A ~ Z
				mask_letters = 4;
			else if(n >= 48 && n <= 57)  // 0 ~ 9
				mask_numbers = 4;
			else if(n == 126 || n == 96 ||
				n == 33 || n == 36 || n == 94 || n == 40 || n == 41 || n == 95 || n == 45 || n == 124 ||
				n == 123 || n == 125 || n == 91 || n == 93 || n == 59 || n == 46 || n == 63 || n == 47)
				mask_special_characters = 8;
			else
				return false;
		}
        if(no>1){
            return true;
        }
		return false;
	}
//    if( (systemOption & SYSTEM_OPTION_UI_FIXED_DATE_20160504) == 0){	
        if(no<=1)
        {
			if(capInfo["oem"] == 12){
            	pop_msg = getLanguage("msg_passwd_too_weak_ng_iv");
			}else{
				if (capInfo["oem"] == 2)
				{
					if (pw_ng ==1)
						pop_msg = getLanguage("msg_passwd_id_combine_ng");
					else
						pop_msg = getLanguage("msg_passwd_too_weak_ng_dw");
				}
				else
	            	pop_msg = getLanguage("msg_passwd_too_weak_ng");
			}
            settingFail(menu, pop_msg);
            return false;    	
        }
//    }	

    //$("#btOK").removeAttr("disabled");
    return true;
}