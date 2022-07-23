var menu = getLanguage("Network_Settings");
//var settingList = ["ip", "sm", "gw", "dns", "web_port" , "https_port", "control_port", "video_port", "at_port", "ar_port", "rtsp_port"];
var ipSettings =  ["hostname", "ip_type", "ip", "sm", "gw", "dns_pre", "dns_alt"];
var settingList = ["web_port" , "rtsp_port", "https_port", "mtu" ];//, "https_enabled"];
$.merge(settingList, ipSettings);
function getElement(name, val)
{
	//$("input:text[name='n_t_ip']").val(ip);
	//$("input:radio[name='ip_type']:radio[value='0']").attr("checked", true);
	
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

function CheckIP()
{
    var ipPattern = /^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$/;

    var ipArray     = $("#ip").val().match(ipPattern);
    var smArray     = $("#sm").val().match(ipPattern);
    var gwArray     = $("#gw").val().match(ipPattern);
    var ip_num, gw_num, sm_num, not_sm_num;
    var i, thisSegment;
    if(ipArray == null) {
        settingFail(menu, getLanguage("msg_check_ip"));
        
        $("#ip").focus();
        return false;
    }

    if(smArray == null) {
        settingFail(menu, getLanguage("msg_check_subnet"));
        $("#sm").focus();
        return false;
    }

//    if(gwArray == null) {
 //       settingFail(menu, getLanguage("msg_check_gateway"));
//        $("#gw").focus();
//       return false;
//    }

    var ip_num      = ((ipArray[1]&0xFF)<<24) + ((ipArray[2]&0xFF)<<16) + ((ipArray[3]&0xFF)<<8) + ((ipArray[4]&0xFF)<<0);
    var sm_num      = ((smArray[1]&0xFF)<<24) + ((smArray[2]&0xFF)<<16) + ((smArray[3]&0xFF)<<8) + ((smArray[4]&0xFF)<<0);
    var not_sm_num  = (((~smArray[1])&0xFF)<<24) + (((~smArray[2])&0xFF)<<16) + (((~smArray[3])&0xFF)<<8) + (((~smArray[4])&0xFF)<<0);

    thisSegment = ipArray[1];

    if(thisSegment<1 || thisSegment>223) {
        settingFail(menu, getLanguage("msg_check_ip"));
        $("#ip").focus();
        return false;
    }

    for(i=2; i<5; i++) {
        thisSegment = ipArray[i];
        if(thisSegment>255) {
            settingFail(menu, getLanguage("msg_check_ip"));
            $("#ip").focus();
            return false;
        }
    }

    for(i=1; i<5; i++) {
        thisSegment = smArray[i];
        if(thisSegment>255) {
            settingFail(menu, getLanguage("msg_check_subnet"));
            $("#sm").focus();
            return false;
        }
    }

    for(i=0; i<32; i++) {
        var token = 1<<i;
        if((sm_num&token)>0) break;
    }

    for(i++; i<32; i++) {
        var token = 1<<i;
        if((sm_num&token)==0) {
            settingFail(menu, getLanguage("msg_check_subnet"));
            $("#gw").focus();
            return false;
        }
    }
    if(((ip_num&not_sm_num)==not_sm_num) || ((ip_num&not_sm_num)==0) || ((ip_num&sm_num)==0)) {
        settingFail(menu, getLanguage("msg_check_ip"));
        $("#ip").focus();
        return false;
    }

    if(gwArray != null) {
      
      var gw_num      = ((gwArray[1]&0xFF)<<24) + ((gwArray[2]&0xFF)<<16) + ((gwArray[3]&0xFF)<<8) + ((gwArray[4]&0xFF)<<0);
      if(gw_num != 0)
      {
        thisSegment = gwArray[1];
        if(thisSegment<1 || thisSegment>223) {
            settingFail(menu, getLanguage("msg_check_gateway"));
            $("#gw").focus();
            return false;
        }
    
    
        for(i=2; i<5; i++) {
            thisSegment = gwArray[i];
            if(thisSegment>255) {
                settingFail(menu, getLanguage("msg_check_gateway"));
                $("#gw").focus();
                return false;
            }
        }
    
        if(ip_num==gw_num) {
          settingFail(menu, getLanguage("msg_check_ip"));
          $("#ip").focus();
          return false;
        }
    
        if(((gw_num&not_sm_num)==not_sm_num) || ((gw_num&not_sm_num)==0) || ((gw_num&sm_num)==0)) {
            settingFail(menu, getLanguage("msg_check_gateway"));
            $("#gw").focus();
            return false;
        }
    
        if((ip_num&sm_num) != (gw_num&sm_num)) {
            settingFail(menu, getLanguage("msg_same_ip_gateway"));
            $("#ip").focus();
            return false;
        }
      }
    }

    return true;
}    
    
function CheckDNS()
{
    var ipPattern   = /^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$/;
    var dnsArray;
    var dns2Array;
    var thisSegment;
    var dns_name;
    
     
    dnsArray   = $("#dns_pre").val().match(ipPattern);

    if(dnsArray != null) {
      var dns_num      = ((dnsArray[1]&0xFF)<<24) + ((dnsArray[2]&0xFF)<<16) + ((dnsArray[3]&0xFF)<<8) + ((dnsArray[4]&0xFF)<<0);
      if(dns_num != 0)
      {
      thisSegment=dnsArray;
      if(thisSegment<1 || thisSegment>223) {
          settingFail(menu, getLanguage("msg_check_main_dns"));
          getElement(dns_pre).focus();
          return false;
      }
  
      for(var i=2; i<5; i++) {
          thisSegment = dnsArray[i];
          if(thisSegment>255) {
              settingFail(menu, getLanguage("msg_check_main_dns"));
              getElement(dns_pre).focus();
              return false;
          }
      }
      }
    }

    dns2Array   = $("#dns_alt").val().match(ipPattern);	

    if(dns2Array != null) {
      var dns2_num      = ((dns2Array[1]&0xFF)<<24) + ((dns2Array[2]&0xFF)<<16) + ((dns2Array[3]&0xFF)<<8) + ((dns2Array[4]&0xFF)<<0);
      if(dns2_num != 0)
      {
      thisSegment=dns2Array;
      if(thisSegment<1 || thisSegment>223) {
          settingFail(menu, getLanguage("msg_check_sub_dns"));
          getElement(dns_alt).focus();
          return false;
      }
  
      for(var i=2; i<5; i++) {
          thisSegment = dns2Array[i];
          if(thisSegment>255) {
              settingFail(menu, getLanguage("msg_check_sub_dns"));
              getElement(dns_alt).focus();
              return false;
          }
      }	
      }
    }



    return true;
}
 /*   
function CheckRtspPort()
{	
	 var n_port= $("#web_port").val();
    
    if ( (n_port != 80) && (n_port < 1025 || n_port > 60000) )
    {
        settingFail(menu, getLanguage("msg_http_check_portnumber"));
        return false;
    }
    
    return true;
}
function CheckPORT()
{	
	 var n_port= $("#rtsp_port").val();
    
    if ( (n_port != 554) && (n_port < 1025 || n_port > 60000) )
    {
        settingFail(menu, getLanguage("msg_rtsp_check_portnumber"));
        return false;
    }
    
    return true;
}
*/    
function CheckForm()
{
    if(!CheckDNS()) return false;
    if(!CheckIP()) return false;
//  if(!CheckPORT()) return false;
//  if(!CheckRtspPort()) return false;
    return true;
}
function initUI()
{
	/*$("#control_port").before().prop("disabled", true);
	$("#control_port").prop("disabled", true);
	$("#video_port").before().prop("disabled", true);
	$("#video_port").prop("disabled", true);
	$("#at_port").before().prop("disabled", true);
	$("#at_port").prop("disabled", true);
	$("#ar_port").before().prop("disabled", true);
	$("#ar_port").prop("disabled", true);*/
	if(capInfo["oem"] != 12)
		$("#mtu_setting").css("display", "none");
}
function isvalid(val){
	var Valid = new Validation();	
	var port_flag = true ;
	var vcaport_flag = true ;
	var used_port = [6000, 8080, 8081, 8082, 8088, 8089, 7088, 7089, 7188, 8188, 30001, 30007, 40000, 40001];

	for(var i = 0 ; i < used_port.length ; i++)
	{
		if($("#web_port").val() == used_port[i] || $("#https_port").val() == used_port[i] || $("#rtsp_port").val() == used_port[i] )
			vcaport_flag = false;
	}
	
	if( vcaport_flag == false ){
		settingFail(menu, getLanguage("used_vcaport"));
		return false;	
	}

	if( $("#web_port").val()  == $("#rtsp_port").val() ) port_flag = false ;
	if( $("#https_port").val() == $("#web_port").val() ) port_flag = false ;
	if( $("#rtsp_port").val() == $("#https_port").val() ) port_flag = false	;
	if( port_flag == false ){
		settingFail(menu, getLanguage("msg_duplicate_port"));
		return false;	
	}
	
	if( val == "web_port"  )
	{
		 if(!(Valid.check_range(1025 ,60000, val,80)) || !(Valid.isonlynumber(val))){
			return false;	
		}
	}
	if( val == "https_port"  )
	{
		if(!(Valid.check_range(1025 ,60000, val,443)) || !(Valid.isonlynumber(val))){
			return false;	
		}
	}
	if( val == "rtsp_port"  )
	{
		if(!(Valid.check_range(1025 ,60000, val,554)) || !(Valid.isonlynumber(val))){
			return false;	
		}
	}

	return true;	
	
}
function initEvent()
{
	var  pop_msg ="";
	$("[name=ip_type]").click(function ( obj ) {
		SetTextBoxEnabled();
		for( var i = 0 ; i < ipSettings.length ; i++)	
		{	
			var obj = $("#" + ipSettings[i]);
			var tag = obj.prop("tagName");
			if( tag == "SELECT" || tag == "INPUT")
			{
				if( ipSettings[i] != "ip"){
					obj.val( NetworkInfo[ipSettings[i]]);
				}			
			}
		}
	});
	
	function clearIntervalAll() 
	{
		// setup_main.js var dnsIntervals
		dnsIntervals.forEach( function (interval) { clearInterval(interval) });
		dnsIntervals = [];
	}

	function setDNSUI () {
		$.ajax({
			type:"get",
			url: "/cgi-bin/admin/network.cgi",
			data: "msubmenu=ip&action=get_dns"
		})
		.done( function ( response ) {
			response = JSON.parse(response);
			$("#dns_pre").val(response.dns_pre);
			$("#dns_alt").val(response.dns_alt);
		})
		.fail( function () {
			console.log("get DHCP DNS Fail");
			clearInterval(dnsInterval);
		})
	}
	
	function syncDNSWithInterval() {
		var count = 1;
		
		setDNSUI();

		var dnsInterval = setInterval(function () {
			if(count >= 8) clearInterval(dnsInterval);
			setDNSUI();
			count++
		}, 3000);
		dnsIntervals.push(dnsInterval);
	}

	var clearToclickList = ["#static", "#network_port", "#hostname"];
	clearToclickList.forEach(function ( UIname )  {
		$(UIname).click( function () {
			clearIntervalAll();
		})
	})

	$("#left_frame").click( function(e) {
		if(e.target.id != "Network_Settings")
			clearIntervalAll();
	})

	$("#dhcp").click(function () {
		syncDNSWithInterval();
	})
	
	$("#btOK").click(function(event) {
		clearIntervalAll();
		if( !CheckForm() )
		        return;	    
		
		function onSuccessApply(msg)
		{
			var response = msg.trim();
			if(response == "OK")
			{
				settingSuccess(menu, null);

				if($("#dhcp").is(":checked")) 
				{
					syncDNSWithInterval();
				}
			}
			else 
			{
				settingFail(menu);
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
		var newValue;
		var orgValue;
		for( var i = 0 ; i < settingList.length ; i++){	
			var obj = $("#" + settingList[i]);
			if(obj.length == 0 ) obj = $("[name=" + settingList[i] + "]:checked");
			newValue = obj.val();
			orgValue = NetworkInfo[settingList[i]];

			if(!isvalid(settingList[i]))  return 0 ;    // validation
			if( settingList[i] == "hostname"){
				if( !isValidText(newValue) ) {
					settingFail(menu, getLanguage("msg_invalid_text"));
					return;
				}
				if( newValue.length < 1 || newValue.length > 30 ){
					settingFail(menu, getLanguage("msg_invalid_text_length") + "(1~30)");
					return;
				}	
			}			
			if( ( orgValue != newValue && typeof(newValue) != "undefined" )||
				( settingList[i] == "ip" && orgValue == newValue && $("[name=ip_type]:checked").val() == 0 && NetworkInfo["ip_type"] ==1 ) ){
				if( data == null){
					data = settingList[i] + "=" + newValue;
				} else {
					
					data += "&" + settingList[i] + "=" + newValue;
				}
			}		
		}
			
		if(data != null)
		{
			data = "msubmenu=ip&action=apply&"+data ;
		} else {
			pop_msg = getLanguage("msg_nothing_changed");
			settingFail(menu, pop_msg);
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
function initValue()
{
	for( var i = 0 ; i < settingList.length ; i++)	
	{	
		var obj = $("#" + settingList[i]);
		if( obj.length == 0) obj = $("[name=" + settingList[i] + "]");
		var tag = obj.prop("tagName");
		if(tag=="INPUT"){
			var input_type = obj.attr("type");
			if( input_type == "radio"){
				$("[name="+settingList[i]+"][value="+NetworkInfo[settingList[i]]+"]").prop("checked", true);
			} else {
				obj.val( NetworkInfo[settingList[i]]);
			}
		}  
	}
}
function SetTextBoxEnabled(optMode)
{
	if( getElement('ip_type', '0').is(":checked") )
	{
		$("#static_ip_setting").find("*").prop("disabled", false);
		$("#ip").val(NetworkInfo["ip_static"]);
	} 
	else 
	{
		$("#static_ip_setting").find("*").prop("disabled", true);
		if(NetworkInfo["ip_type"] == 1 )
			$("#ip").val(NetworkInfo["ip_dynamic"]);
		else
			$("#ip").val(NetworkInfo["ip_static"]);
	}
}
function onLoadPage()
{
	initUI();
	initValue();
	initEvent();

	SetTextBoxEnabled();	
}

$(document).ready( function() {

	onLoadPage();

});
