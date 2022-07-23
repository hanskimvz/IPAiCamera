

var MAX_NUM_ITEM = Number(130);
var MAX_NUM_PAGE = Number(10);
var START_PAGE_NUM;
var AMOUNT_OF_PAGE;
var AMOUNT_OF_CONTENTS;
var SELECT_PAGE;

function setPageInfo() {
    $("#page_list").find("*").remove();
    $("#page_list").text("");

    var content="";

    var amount_of_page_fix = AMOUNT_OF_PAGE / 2;
    if(amount_of_page_fix < 1 )
        amount_of_page_fix = 1;
    for( var i = 1 ; i < 1 + MAX_NUM_PAGE && i <= amount_of_page_fix ;  i++ ) {
        content += "<label class='page_num' id='page_" + i + "'> " + i + " </label>";
    }
    $("#page_list").append(content);

    if( $("#page_list").find(".page_num").length == 0 ) {
        $("#result_table").find(".list_items").remove();
        return false;
    }
    return true;
}

function initUI()
{
    setPageInfo();
}

function setEventForPageItem() {
    $(".page_num").click(function(e) {
        var range;
        var content;

        $(".page_num_active").removeClass("page_num_active");
        $("#" + e.delegateTarget.id).addClass("page_num_active");
        SELECT_PAGE = Number($("#" + e.delegateTarget.id).text().trim());
        range = SELECT_PAGE * MAX_NUM_ITEM;
        $(".list_items").remove();
        // input the list
        content = "";

        for(var i= 1 ;  i < AMOUNT_OF_CONTENTS ; i++) {

            logid = i ;
            content += "<tr class='list_items' id='"+ logid + "'>";
            content += "<td class='qt'>" + i + "</td>";
            content += "<td class='qt'>" + data_list[i]['ssid']+ "</td>";
            content += "<td class='qt'>" + data_list[i]['sig']+ "</td>";
            content += "<td class='qt'>" + data_list[i]['enc']+ "</td>";
            content += "</tr>";
        }

        $("#result_table").append(content);
        setEventForRecordItem();
        $(".result_filed").scrollTop(0);
    });
}

function setEventForRecordItem(){
    $(".list_items").on("click", function(e) {
        $("#result_table").find("tr").removeClass("sel_record_item");
        $("#" + e.delegateTarget.id).addClass("sel_record_item");

        var info = $(".sel_record_item");
        var id = info.attr("id");
	var ssid =  data_list[id]['ssid'];
        console.log(ssid);
	$("#sel_ssid").attr("disabled", true);
	$("#sel_ssid").val(ssid);

    });
    $(".list_items").on("dblclick", function(e) {
    });
}

function initEventForList() {
    setEventForPageItem();
    setEventForRecordItem();
    $(".result_filed").scrollTop(0);

    var disable;
    if( AMOUNT_OF_PAGE <= 10 ){
        disable = true;
    } else {
        disable = false;
    }
    $("#prev_page,#next_page").attr("disabled", true);

    $("#prev_page,#next_page").attr("disabled", AMOUNT_OF_PAGE < MAX_NUM_PAGE);
}

function initWiFiConfig(){
	console.log("initWiFiConfig");
	
	var obj = JSON.parse(wifi_config_list);
        IOTInfo = obj;
	if( IOTInfo.WIFIEnabled == 1 )
	{
		$("#connected").prop("checked", true);
		$("input:radio[name='ip_connected'][value='0']").prop('checked', true);
	}
	else
	{
		$("input:radio[name='ip_connected'][value='1']").prop('checked', true);
	}

	$("#sel_ssid").val(IOTInfo["ssid"]);
	$("#sel_pw").val(IOTInfo["psk"]);
	
	$("#wifi_ip").val(IOTInfo["DynamicIpAddr"]);
	$("#wifi_sm").val(IOTInfo["SubnetMask"] );
	$("#wifi_gw").val(IOTInfo["Gateway"]);
	
	console.log("ip="+ IOTInfo["DynamicIpAddr"] + "sm=" + IOTInfo["SubnetMask"] + "gw=" + IOTInfo["Gateway"]);
}

function getElement(name, val)
{
    var type = $("[name="+ name + "]").attr('type');

    if(type == 'text')
    {
        return $("[name=" + name + "]");
    }
    else if(type == 'radio')
    {
        return $("input:radio[name=" + name + "]:radio[value=" + val +"]");
    }
}


function getInformation_WiFiConfig()
{
	var data= null;
        data = "msubmenu=wifi_setup&action=view";
        $.ajax({
            type:"get",
            url: "/cgi-bin/admin/iot_wifi.cgi",
            data: data,
            success: function(msg){
                response = msg.trim();
                wifi_config_list = response;
                console.log(wifi_config_list);
                initWiFiConfig();
                if(response == "OK")
                {
                    //settingSuccess(menu, null);
                }
                else
                {
                    //settingSuccess(menu, null);
                    //settingFail(menu);
                }
                //refreshMenuContent();
            },
            error: function() {
                pop_msg = getLanguage("msg_fail_retry");
                settingFail(menu, pop_msg);
                //refreshMenuContent();
            }
        });
}

function getInformation_WiFiScan()
{
        var data= null;
        data = "msubmenu=wifi_setup&action=scan_iot_wifi";
	
	$.ajaxSetup({async: false});
        $.ajax({
            type:"get",
            url: "/cgi-bin/admin/iot_wifi.cgi",
            data: data,
            success: function(msg){
		response= msg.trim();
		data_list = response;
		console.log(data_list);
            },
            error: function(){
		
	    }
        });
	$.ajaxSetup({async: true});
}

function setConnectSSID()
{
	var req_ssid = $("#sel_ssid").val();
        var req_pw = $("#sel_pw").val();
        console.log(req_pw);


        var data = null;
        data = "ssid=" + req_ssid + "&pw=" + req_pw  ;
        console.log(data);

        if(data != null)
        {
            data = "msubmenu=wifi_setup&action=connect&"+data ;
        } else {
            pop_msg = getLanguage("msg_nothing_changed");
            settingFail(menu, pop_msg);
            return ;
        }
        $.ajax({
            type:"get",
            url: "/cgi-bin/admin/iot_wifi.cgi",
            data: data,
            success: function(msg){
                var response = msg.trim();
                console.log(response);
                if(response == "OK")
                {
                    //settingSuccess(menu, null);
                }
                else
                {
                    //settingSuccess(menu, null);
                    //settingFail(menu);
                }
            },
            error: function() {
                pop_msg = getLanguage("msg_fail_retry");
                settingFail(menu, pop_msg);
            }
        });
}

function initEvent() {

    initEventForList();
    $("#btDownValue").click( function(e){
		var info = $(".sel_record_item");
		var id = info.attr("id");
		console.log(id);
	});

    function changePage(){
        setPageInfo();
        initEventForList();
        $("#page_" + SELECT_PAGE).trigger("click");
    }
    $("[name=ip_type]").click(function ( obj ) {
        SetTextBoxEnabled();
	
    });

    $("#refresh").click( function(){
	getInformation_WiFiConfig();
    });

    $("#btOK").click(function(){
	setConnectSSID();
	getInformation_WiFiConfig();
    });

    return this;
}

function onLoadPage() 
{

	if( data_list != undefined ){
		AMOUNT_OF_CONTENTS = data_list.length;
		AMOUNT_OF_PAGE = Math.ceil(AMOUNT_OF_CONTENTS / MAX_NUM_ITEM);
		SELECT_PAGE = 1;
		START_PAGE_NUM = 1;

		console.log(AMOUNT_OF_CONTENTS);
		console.log(AMOUNT_OF_PAGE);
	}

	initUI();
	initEvent();
    //setContentChose();
    $(".page_num:first").trigger('click');
}

$(document).ready( function() {

	//getInformation_WiFiScan();
	getInformation_WiFiConfig();
	//initWiFiConfig();

  	data_list= getInformation("scan_iot_wifi");
   	onLoadPage();
});
