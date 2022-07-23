if(capInfo["oem"] == 12){
    var menu = getLanguage("cyber_vigilant_configuration");
} else {
    var menu = getLanguage("ip_address_filter_configuration");
}
var settingList = [ "enabled", "type" ];
function initUI(){
    if(capInfo["oem"] == 12){
        $('#ip_filter_title').append('<span tkey="cyber_vigilant_configuration"></span>');
        $('#ip_filter_title').css('text-transform','none');
        $('#ip_address_filter_div').remove();
        $('#cyber_vigilant_div').css('display','block');
        $('#ip_filter_type').css('display','none');
        $('#filtered_ip_addresss').append('<span tkey="setup_authorized_device">');
        $('#address').val(ip);

        if(filterInfo["enabled"]==1)  $('#enabled').prop("checked", true);
        else if(filterInfo["enabled"]==0)  $('#enabled').prop("checked", false);

    }else{
        $("#btRemoveAll").css("display" , "none");
        $('#ip_filter_title').append('<span tkey="ip_address_filter_configuration"></span>');
        $('#ip_address_filter_div').css('display','block');
        $('#cyber_vigilant_div').remove();
        $('#filtered_ip_addresss').append('<span tkey="setup_filtered_ip_addresss">');
    }
}
function setAddressList() {
	var content = "";
	var index=0;
	filterInfo.address.forEach(function(a){
		if( a.length != 0 ) {
			content += "<tr class='list_items' id=address" + ++index + "><td>" + a + "</td></tr>";
		}
	});
	$("#result_table_1").append(content);
}
function initValue(){
	var value = new Value() ; 
	value.setValue(settingList, filterInfo);

	setAddressList();
}

function initEvent(){
	$(".list_items").on("click", function(e) {
		if( e.target.classList.contains("sel_record_item") == false) {
			$("#result_table_1").find("tr").removeClass("sel_record_item");
			$("#" + e.delegateTarget.id).addClass("sel_record_item");
		} else {
			$("#result_table_1").find("tr").removeClass("sel_record_item");
		}
	});
	$("#btOK").click( function(){
		var data="msubmenu=ip_filter&action=apply";
		var changed = 0;
		var checklistip = 0;    //list ip check
        if(capInfo["oem"] == 12){
            if($('#enabled').prop('checked')){
                $('#enabled').val('1');
            }else{
                $('#enabled').val('0');
            }
        }
		settingList.forEach(function(target){
			var obj = $("#" + target);
			if( obj.length == 0 ) obj = $("[name=" + target + "]:checked");
			var newVal=obj.val();
			var oldVal=filterInfo[target];
			
			if( newVal != oldVal ){
				data += "&" + target + "=" + newVal;
				changed++;
			}
		});
		if( capInfo["oem"] == 12 ){
			filterInfo.address.forEach(function(a){
					if(a == ip)
					checklistip++;
					});
			if( changed == 0 ){
				settingFail(menu, getLanguage("msg_nothing_changed"));  //nothing changed
			} else {
				if( $('#enabled') == 1){
					_ajax(data);
				} else {
					if(checklistip == 1){                               //on listip
						_ajax(data);
					} else {
						if(confirm("You have not allowed access from this PCs address("+ip+")\nIf you apply this change you will no longer be able to access the device from this PC.") == 1){
							_ajax(data);
						} else {
							refreshMenuContent();
						}
					}
				}
			}
		} else {
			if( changed == 0 ){
				settingFail(menu, getLanguage("msg_nothing_changed"));
			} else {
				_ajax(data);
			}
		}
	});
	$("#address").keyup( function(){
		var str='';
		if( ipv4_validation(this.value) ){
			str=getLanguage("msg_valid");	
		} else {
			str=getLanguage("msg_invalid");	
		}
		$("#address_status").text(str);
	}).trigger("keyup");
	$("#btAdd").click(function(){
		var addr = $("#address").val(); // valdiation check
		if(!ipv4_validation(addr)){
			settingFail(menu,"Invalid IP Address");
		}
		else
		{
			var data ="msubmenu=ip_filter&action=add&address=" + addr;
			_ajax(data);
		}
	});
	$("#btRemove").click(function(){
		var obj = $(".sel_record_item");
		if( obj.length )
		{
			var addr = obj.text();
			var data ="msubmenu=ip_filter&action=remove&address=" + addr;
			_ajax(data);
		} else {
			settingFail(menu, getLanguage("msg_nothing_changed"));
		}
	});
    $("#btRemoveAll").click(function(){
		var data ="msubmenu=ip_filter&action=remove_all";
		_ajax(data);
	});
}
function _ajax(data)
{
	$.ajax({
		type:"get",
		url: "/cgi-bin/admin/security.cgi",
		data: data,
		success: function(ret){
			var reg=/OK/g;
			if( reg.test(ret) ){
				settingSuccess(menu, getLanguage("msg_success"));
				refreshMenuContent();
			} else {
				var value = ret.split('\n')[1].split(':')[1].trim();
				var msg_type = "msg_fail";
				if( value == 9){
				if( capInfo["oem"] == 12){
					msg_type = "msg_ip_filter_conflict_iv";
					refreshMenuContent();
					} else {
					msg_type = "msg_ip_filter_conflict";
					}
				}
				settingFail(menu, getLanguage(msg_type),2);
			}
		},
		error: function(ret){
			settingSuccess(menu, getLanguage("msg_fail_retry"));
		}
	});
}

function onLoadPage(){
	initUI();
	initValue();
	initEvent();
}

$(document).ready(function(){
	onLoadPage();
});
