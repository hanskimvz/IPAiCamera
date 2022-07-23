var MAX_NUM_ITEM = Number(10);
var MAX_NUM_PAGE = Number(10);
var START_PAGE_NUM;
var AMOUNT_OF_PAGE;
var AMOUNT_OF_CONTENTS;
var SELECT_PAGE;

var user_count = usersInfo.length;
var auth  = new Array(5);
var authList = { 1: "Admnistrator", 2: "Operator", 4: "Viewer"};
var ApplyMode;
var settingList = ["id", "pass", "auth"];
//var settingList1 = ["id", "pass", "m_pass_confirm" , "auth"];
var menu = getLanguage("setup_system_user_config") + " " + getLanguage("settings");
var pop_msg;
var no=0;
var no_pw_hint=1;
var pw_ng = 0;
var outFormat = [ { "msg":"setup_password_type", "color":"white",},
    { "msg":"setup_password_weak", "color":"red",},
    { "msg":"setup_password_good", "color":"#FF8000"},
    { "msg":"setup_password_strong", "color":"#00FF40"}];
var pw_ng = 0;
var timeout;

$(document).ready( function() {
	if( userInfo != undefined ){
		AMOUNT_OF_CONTENTS = user_count;
		AMOUNT_OF_PAGE = Math.ceil(AMOUNT_OF_CONTENTS / MAX_NUM_ITEM);
		SELECT_PAGE = 1;
		START_PAGE_NUM = 1;
	}

    onLoadPage();
});
function onLoadPage()
{
if( (systemOption & SYSTEM_OPTION_UI_FIXED_DATE_20160504) == 1){	
	$("#meter_wrapper_ui").remove();
}
	initUI();
	if(capInfo["oem"] != 15)
    	initValue();
    initEvent();
	$(".page_num:first").trigger('click');
}
function setEventForPageItem() {
	$(".page_num").click(function(e) {
		$(".list").remove();
		var range;
		$(".page_num_active").removeClass("page_num_active");
		$("#" + e.delegateTarget.id).addClass("page_num_active");
		SELECT_PAGE = Number($("#" + e.delegateTarget.id).text().trim());
		range = SELECT_PAGE * MAX_NUM_ITEM;
		for(var i=range-MAX_NUM_ITEM ; i < range && i < AMOUNT_OF_CONTENTS ; i++) {
			var tmp, obj, radio;

			radio = "<input type='radio' id='index" + i + "' name='index' value=" +i;
			if( i == 0) radio += " checked";
			radio +=  "><label for='index" + i+"'></label>";

			obj= "<tr id='line" + i + "' class='list'>";
			obj += "<td class='t1'>" + radio + "</td>";
			obj += "<td>" + usersInfo[i]["id"] +"</td>";
			obj += "<td>" + getLanguage(authList[usersInfo[i]['auth']]) + "</td>";
			obj += "</tr>";
			$("#profile").append(obj);
		}
	});
}
function initValue()
{
    for( var i = 0 ; i < user_count ; i++) 
    {
        var tmp, obj, radio;

        radio = "<input type='radio' id='index" + i + "' name='index' value=" +i;
        if( i == 0) radio += " checked";
        radio +=  "><label for='index" + i+"'></label>";

        obj= "<tr id='line" + i + "'>";
        obj += "<td class='t1'>" + radio + "</td>";
        obj += "<td>" + usersInfo[i]["id"] +"</td>";
        obj += "<td>" + getLanguage(authList[usersInfo[i]['auth']]) + "</td>";
       // obj += "<td>TBD</td>";
        obj += "</tr>";
        $("#profile").append(obj);
    }
}
function setPageInfo() {
	$("#page_list").find("*").remove(); 
	$("#page_list").text("");

	var content="";
	for( var i = START_PAGE_NUM ; i < START_PAGE_NUM + MAX_NUM_PAGE && i <= AMOUNT_OF_PAGE ;  i++ ) { 
		content += "<label class='page_num' id='page_" + i + "'> " + i + " </label>";
	}   
	$("#page_list").append(content);

	if( $("#page_list").find(".page_num").length == 0 ) { 
		$("#log_table").find(".list_items").remove();
		return false;
	}   
	return true;
}


function initUI()
{
    if(user_count >= 5) $("#btAdd").css("disabled", "true"); 
	if( capInfo["oem"] == 2){
		$("#pass_hint_div").css("display", "block");
	}else{
		$("#pass_hint_div").css("display", "none");
	}
	    if( capInfo["oem"] == 12){
		    $("#msg_change_pass").append("<span >"+getLanguage("pass_msg_noti_iv")+"</span><br>");
        }
        else if( capInfo["oem"] == 2){
		    $("#msg_change_pass").append("<span >"+getLanguage("pass_msg_dw")+"</span><br>");
        }
        else{
		    $("#msg_change_pass").append("<span >"+getLanguage("pass_msg_noti")+"</span><br>");
        }
	if(capInfo["oem"] == 15){
		$("#pages").css("display","block");
		setPageInfo();
	}else{
		$("#pages").css("display","none");
	}
}
function initEventForList() {
	setEventForPageItem();
	var disable;
	if( AMOUNT_OF_PAGE <= 10 ){
		disable = true;
	} else {
		disable = false;
	}
	$("#prev_page,#next_page").attr("disabled", true);

	$("#prev_page,#next_page").attr("disabled", AMOUNT_OF_PAGE < MAX_NUM_PAGE);
	console.log(AMOUNT_OF_PAGE);
	console.log(MAX_NUM_PAGE);
	console.log(AMOUNT_OF_PAGE < MAX_NUM_PAGE);
}

function initEvent()
{
	if(capInfo["oem"] == 15)
		initEventForList();
    function displayModifyDiv(sel)
    {
        if(sel === true){
            $("#View").css("display", "none");
            $("#Modify").css("display", "");
        } else {
            $("#View").css("display", "");
            $("#Modify").css("display", "none");
        }
    }
    function success(ret)
    {
        var response = ret.trim();
        if(response == "OK")
        {
			pop_msg = getLanguage("msg_save_success");
            settingSuccess(menu, pop_msg);
            refreshMenuContent();
        } 
        else 
        {
			pop_msg = getLanguage("msg_save_fail_special_key_retry")+"\n"+getLanguage("pass_msg_combination")+"\n"+getLanguage("pass_msg_symbol");
            settingFail(menu, pop_msg);
        }

		clearTimeout(timeout);
		timeout = setTimeout(function(){
			refreshMenuContent(); 
		}, 3000); 
    }
    function successByDeleteBtn(ret)
    {
        var response = ret.trim();
        if(response == "OK")
        {
			pop_msg = getLanguage("msg_save_success");
            settingSuccess(menu, pop_msg);
            refreshMenuContent();
        } 
        else 
        {
			pop_msg = getLanguage("msg_save_fail_retry");
            settingFail(menu, pop_msg);
        }

		clearTimeout(timeout);
		timeout = setTimeout(function(){
			refreshMenuContent(); 
		}, 3000); 
    }

    $("#btAdd").bind("click", {view: true}, function(event) { 
    	var usercount ;
    	$("#m_id").prop("disabled",false);
    	$("#m_auth").prop("disabled",false);
    	
    	$.ajax({
             type: 'get',
             async : false,
             url: '/cgi-bin/admin/system.cgi?msubmenu=users&action=count',
             success: function(ret){            	 
            	 usercount = ret.trim().split('=');   
             },
             error: function(val){            			
             }
        });
	if(capInfo["oem"] == 15){
    	if( usercount[1] > 31) alert(getLanguage("msg_exceed_users32")) ;
    	else{
	    	displayModifyDiv(event.data.view); 
//			$("#m_pass").trigger("keyup");
	        $("#m_auth").empty();
	        var option = "<option value='2' tkey='Operator'></option><option value='4' tkey='Viewer'></option>";
	        $("#m_auth").append(option).val(2);      
	        $("#m_pass").val("");
	        $("#m_pass_confirm").val("");
	        $("#m_id").val("");   
	        initLanguage();
	        ApplyMode = "add";
    	}
	}else{
    	if( usercount[1] > 4) alert(getLanguage("msg_exceed_users")) ;
    	else{
	    	displayModifyDiv(event.data.view); 
	        $("#m_auth").empty();
			if (multiAdmin)
				var option = "<option value='1' tkey='Admnistrator'></option><option value='2' tkey='Operator'></option><option value='4' tkey='Viewer'></option>";
			else
				var option = "<option value='2' tkey='Operator'></option><option value='4' tkey='Viewer'></option>";
	        $("#m_auth").append(option).val(2);      
	        $("#m_pass").val("");
	        $("#m_pass_confirm").val("");
	        $("#m_id").val("");   
	        initLanguage();
	        ApplyMode = "add";
    	}
	}
    });

    $("#btModify").bind("click", {view: true}, function(event) {
        var selected = $("input[name='index']:checked").val();
        displayModifyDiv(event.data.view); 

        $("#m_auth").empty();

        $("#m_id").prop("disabled",false);
        $("#m_auth").prop("disabled",false);
        
		if(selected === "0"){
			option = "<option value='1' tkey='Admnistrator'></option>";
			$("#m_id").prop("disabled",true);
			$("#m_auth").prop("disabled",true);
		}
		else
		{
			if ((multiAdmin) && (authList[usersInfo[selected]['auth']] == 'Admnistrator'))
				option = "<option value='1' tkey='Admnistrator'></option><option value='2' tkey='Operator'></option><option value='4' tkey='Viewer'></option>";
			else
				option = "<option value='2' tkey='Operator'></option><option value='4' tkey='Viewer'></option>";
			$("#m_id").prop("disabled",true);
		}

        $("#m_auth").append(option);
    	
        for( var i = 0 ; i < settingList.length; i++)
        {           
        	$("#m_" + settingList[i]).val(usersInfo[selected][settingList[i]]);
        }
        $("#m_pass_confirm").val("");
        initLanguage()
        ApplyMode = "modify";
		$("#m_pass").trigger("keyup");
    });
    
    $("#btOK").bind("click", {view: false}, function(event) { 
		if( capInfo["oem"] == 2){
			if($("#m_pass").val() == $("#m_pass_hint").val()){
				settingFail(menu, "Password hint can not be same as password");
				return false;
			}   
		}

        if( chkForm() )
        {
            if(ApplyMode === 'add') 
            {
                var arg = { action: ApplyMode, 
                    id: $("#m_id").val(), 
                    pass: $("#m_pass").val(), 
					passhint:$("#m_pass_hint").val(),
                    auth: $("#m_auth").val()
                };
            }
            else if( ApplyMode === 'modify') 
            {
                var arg = { action: ApplyMode,
                    index: $("input[name=index]:checked").val(),
                    id: $("#m_id").val(), 
                    pass: $("#m_pass").val(),
					passhint:$("#m_pass_hint").val(),
                    auth: $("#m_auth").val() 
                };
            }
            console.log(arg)
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

    $("#btCancle").bind("click", {view: false}, function(event) { 
        no = 0; 
		$("#meter").css("backgroundColor", outFormat[no].color)
			.css('width',$("#meter_wrapper").width()/3*no+'px');
		$("#pass_type").text(getLanguage(outFormat[no].msg));
        displayModifyDiv(event.data.view);
    
    });

    $("#btDelete").bind("click", function(){ 
        $.ajax({
            type: 'get',
            url: '/cgi-bin/admin/system.cgi?msubmenu=users&action=del&index='+ $("input[name='index']:checked").val(),
			success: successByDeleteBtn,
            error: function(){
				pop_msg = getLanguage("msg_loading_fail");	
                settingFaill(menu, pop_msg);
            }
        });
    });

    $("#Modify").css("display", "none");
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
		var id=$("#m_id").val();

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
		if((passwd.indexOf(id) !== -1) && (capInfo["oem"] == 2))
		{
			no=1;
			pw_ng=1;
		}

		$("#meter").css("backgroundColor", outFormat[no].color)
			.css('width',$("#meter_wrapper").width()/3*no+'px');
		$("#pass_type").text(getLanguage(outFormat[no].msg));

	});
	function changePage(){
		setPageInfo();
		initEventForList();
		$("#page_" + SELECT_PAGE).trigger("click");
	}
	$("#prev_page").click( function() {
		if( SELECT_PAGE - MAX_NUM_PAGE > 0 ){
			SELECT_PAGE -= MAX_NUM_PAGE;
			SELECT_PAGE = START_PAGE_NUM = Math.floor(SELECT_PAGE/MAX_NUM_PAGE)*10+1 ;
			changePage();
		}
	});
	$("#next_page").click( function() {
		var next_page = (Math.floor((SELECT_PAGE-1)/MAX_NUM_PAGE))*10 + 1 + MAX_NUM_PAGE;
		if( next_page <= AMOUNT_OF_PAGE ) {
			SELECT_PAGE = next_page
			SELECT_PAGE = START_PAGE_NUM = Math.floor(SELECT_PAGE/MAX_NUM_PAGE)*10+1 ;
			changePage();
		}
	});

	$("#first_page").click( function() {
		SELECT_PAGE = 1;
		START_PAGE_NUM = 1;
		changePage();
	});
	$("#last_page").click( function() {
		SELECT_PAGE = AMOUNT_OF_PAGE;
		START_PAGE_NUM = Math.floor((SELECT_PAGE-1)/MAX_NUM_PAGE)*10+1 ;
		changePage();
		$(".page_num:last").trigger('click');
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
        var passlen=7;
    }else {
        var passlen=8;
    }

	if( capInfo["oem"] == 2){
		if( $("#m_id").val().length < 5 || $("#m_id").val().length > 30) { 
			pop_msg = getLanguage("msg_id_wrong_dw"); 
			settingFail(menu, pop_msg);            
			return false; 
		}
    }else {
		if( $("#m_id").val().length < 4 || $("#m_id").val().length > 30) { 
			pop_msg = getLanguage("msg_id_wrong"); 
			settingFail(menu, pop_msg);            
			return false; 
		}
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
		//if(mask_letters && mask_numbers && mask_special_characters)
		//	return true;
        if(no>1){
            return true;
        }
		return false;
	}
	if( (systemOption & SYSTEM_OPTION_UI_FIXED_DATE_20160504) == 0){	
		if(no<=1)
		{
			if(capInfo["oem"] == 12){
				pop_msg = getLanguage("msg_passwd_too_weak_ng_iv");
			}else{
				if (capInfo["oem"] == 2)
				{
					if (pw_ng == 1)
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
	}	

    //$("#btOK").removeAttr("disabled");
    return true;
}
